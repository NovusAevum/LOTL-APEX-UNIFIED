import hmac
import json
import logging
import os
import time
from hashlib import sha256
from typing import Deque, Dict, Tuple

from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from starlette.responses import StreamingResponse

from core.llm_orchestrator import OllamaModel
from shell_planner.task_engine import ShellExecutor
from agents.lotl import LotlOpsDaemon
from memory.semantic_store import search_memory, add_task, list_tasks

app = FastAPI(title="LotlOps Agent API", version="1.1.0")
ollama = OllamaModel()
shell = ShellExecutor()


class PromptRequest(BaseModel):
    prompt: str
    model: str | None = None


class ShellRequest(BaseModel):
    command: str


AGENT_SHARED_SECRET = os.getenv("AGENT_SHARED_SECRET", "change-me")
ALLOW_ORIGINS = os.getenv("ALLOW_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


logger = logging.getLogger("apex-agent")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def verify_signature(x_timestamp: str | None, x_signature: str | None, body_bytes: bytes):
    if not x_timestamp or not x_signature:
        raise HTTPException(status_code=401, detail="missing auth headers")
    # Reject too old requests (5 minutes)
    try:
        ts = int(x_timestamp)
    except ValueError:
        raise HTTPException(status_code=401, detail="invalid timestamp")
    if abs(int(time.time()) - ts) > 300:
        raise HTTPException(status_code=401, detail="stale request")
    mac = hmac.new(AGENT_SHARED_SECRET.encode(), x_timestamp.encode() + b"." + body_bytes, sha256).hexdigest()
    if not hmac.compare_digest(mac, x_signature):
        raise HTTPException(status_code=401, detail="bad signature")


# Optional Redis-backed rate limiting for production
RATE_LIMIT_RPS = float(os.getenv("RATE_LIMIT_RPS", "5"))
REDIS_URL = os.getenv("REDIS_URL")
last_seen: Dict[str, Tuple[float, float]] = {}
redis_client = None
if REDIS_URL:
    try:
        import redis

        redis_client = redis.Redis.from_url(REDIS_URL)
    except Exception:
        redis_client = None


async def rate_limit(request: Request):
    if RATE_LIMIT_RPS <= 0:
        return
    ip = request.client.host if request.client else "unknown"
    if redis_client:
        key = f"rl:{ip}"
        try:
            with redis_client.pipeline() as p:
                # token bucket: tokens + rps per second, max rps
                p.hgetall(key)
                data = p.execute()[0] or {}
                now = time.time()
                last_ts = float(data.get(b"ts", b"0").decode() or 0)
                tokens = float(data.get(b"tok", b"0").decode() or 0)
                tokens = min(RATE_LIMIT_RPS, tokens + (now - last_ts) * RATE_LIMIT_RPS)
                if tokens < 1:
                    raise HTTPException(status_code=429, detail="rate limit")
                tokens -= 1
                p.hmset(key, {"ts": now, "tok": tokens})
                p.expire(key, 10)
                p.execute()
        except HTTPException:
            raise
        except Exception:
            pass
    else:
        now = time.time()
        bucket_ts, tokens = last_seen.get(ip, (now, RATE_LIMIT_RPS))
        tokens = min(RATE_LIMIT_RPS, tokens + (now - bucket_ts) * RATE_LIMIT_RPS)
        if tokens < 1:
            raise HTTPException(status_code=429, detail="rate limit")
        last_seen[ip] = (now, tokens - 1)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/ready")
def ready() -> dict:
    import http.client
    from urllib.parse import urlparse

    url = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate").replace("/api/generate", "/api/tags")
    p = urlparse(url)
    conn_cls = http.client.HTTPSConnection if p.scheme == "https" else http.client.HTTPConnection
    try:
        conn = conn_cls(p.hostname, p.port or (443 if p.scheme == "https" else 80), timeout=2)
        conn.request("GET", p.path or "/api/tags")
        resp = conn.getresponse()
        ok = 200 <= resp.status < 300
        return {"ollama": ok}
    except Exception:
        return {"ollama": False}


@app.post("/invoke")
async def invoke(
    request: Request,
    req: PromptRequest,
    x_timestamp: str | None = Header(default=None),
    x_signature: str | None = Header(default=None),
    _rl=Depends(rate_limit),
):
    raw = await request.body()
    verify_signature(x_timestamp, x_signature, raw)
    model = req.model or os.getenv("OLLAMA_MODEL", "llama3")
    local = OllamaModel(model_name=model)
    output = local.invoke(req.prompt)
    logger.info("invoke model=%s bytes=%d", model, len(output.encode()))
    return {"output": output}


@app.post("/shell")
async def run_shell(
    request: Request,
    req: ShellRequest,
    x_timestamp: str | None = Header(default=None),
    x_signature: str | None = Header(default=None),
    _rl=Depends(rate_limit),
):
    raw = await request.body()
    verify_signature(x_timestamp, x_signature, raw)
    output = shell.run(req.command)
    logger.info("shell cmd=%s", req.command.split(" ")[0] if req.command else "")
    return {"output": output}


@app.post("/stream")
async def stream(
    request: Request,
    req: PromptRequest,
    x_timestamp: str | None = Header(default=None),
    x_signature: str | None = Header(default=None),
    _rl=Depends(rate_limit),
):
    raw = await request.body()
    verify_signature(x_timestamp, x_signature, raw)

    import httpx

    model = req.model or os.getenv("OLLAMA_MODEL", "llama3")
    ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")

    async def gen():
        async with httpx.AsyncClient(timeout=60.0) as client:
            async with client.stream(
                "POST",
                ollama_url,
                json={"model": model, "prompt": req.prompt, "stream": True},
            ) as r:
                async for line in r.aiter_lines():
                    if not line:
                        continue
                    yield (line + "\n").encode()

    return StreamingResponse(gen(), media_type="text/event-stream")


class PartnerRequest(BaseModel):
    instruction: str


@app.post("/partner")
async def partner(
    request: Request,
    req: PartnerRequest,
    x_timestamp: str | None = Header(default=None),
    x_signature: str | None = Header(default=None),
    _rl=Depends(rate_limit),
):
    raw = await request.body()
    verify_signature(x_timestamp, x_signature, raw)
    daemon = LotlOpsDaemon()
    result = daemon.partner(req.instruction)
    return result


@app.get("/tasks")
async def tasks():
    return {"tasks": list_tasks()}


class MemoryQuery(BaseModel):
    q: str
    limit: int | None = 5


@app.post("/memory/search")
async def memory_search(req: MemoryQuery):
    return {"results": search_memory(req.q, limit=req.limit or 5)}
