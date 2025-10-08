from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import httpx

app = FastAPI(title="Ollama Embedding Middleware Agent")

OLLAMA_URL = "http://localhost:11434/api/embeddings"

class EmbedRequest(BaseModel):
    text: str

class EmbedResponse(BaseModel):
    embedding: List[float]

@app.post("/embed", response_model=EmbedResponse)
async def generate_embedding(req: EmbedRequest):
    payload = {
        "model": "nomic-embed-text",
        "prompt": req.text
    }
    async with httpx.AsyncClient() as client:
        try:
            res = await client.post(OLLAMA_URL, json=payload)
            res.raise_for_status()
            data = res.json()
            return {"embedding": data["embedding"]}
        except Exception as e:
            return {"embedding": []}
