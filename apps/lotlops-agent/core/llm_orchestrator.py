import os
import subprocess
from typing import Optional

import json
import http.client
from urllib.parse import urlparse


class OllamaModel:
    """Enterprise-ready Ollama client.

    Prefers HTTP API for reliability and containerization, with CLI fallback.
    """

    def __init__(self, model_name: Optional[str] = None, base_url: Optional[str] = None):
        self.model_name = model_name or os.getenv("OLLAMA_MODEL", "llama3")
        # Default to local host. In Docker, consider host.docker.internal
        self.base_url = base_url or os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
        self.temperature = float(os.getenv("LLM_TEMPERATURE", "0.7"))
        self.top_k = int(os.getenv("LLM_TOP_K", "40"))

    def _invoke_http(self, prompt: str) -> Optional[str]:
        try:
            parsed = urlparse(self.base_url)
            if parsed.scheme not in {"http", "https"}:
                return None

            body = json.dumps({
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": self.temperature,
                    "top_k": self.top_k,
                },
            })

            conn_cls = http.client.HTTPSConnection if parsed.scheme == "https" else http.client.HTTPConnection
            port = parsed.port or (443 if parsed.scheme == "https" else 80)
            conn = conn_cls(parsed.hostname, port, timeout=60)
            try:
                conn.request("POST", parsed.path or "/api/generate", body=body, headers={
                    "Content-Type": "application/json"
                })
                resp = conn.getresponse()
                data = resp.read().decode("utf-8")
                if resp.status >= 200 and resp.status < 300:
                    payload = json.loads(data)
                    # Non-streaming returns { response: "..." }
                    return payload.get("response") or data
                return f"❌ Ollama HTTP {resp.status}: {data}"
            finally:
                conn.close()
        except Exception as exc:  # noqa: BLE001
            return f"❌ Ollama HTTP error: {exc}"

    def _invoke_cli(self, prompt: str) -> str:
        try:
            result = subprocess.run(
                ["bash", "-lc", f'printf %s "{prompt}" | ollama run {self.model_name}'],
                capture_output=True,
                text=True,
                check=True,
                timeout=120,
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            return f"❌ Ollama CLI error: {e.stderr.strip()}"
        except Exception as exc:  # noqa: BLE001
            return f"❌ Ollama CLI error: {exc}"

    def invoke(self, prompt: str) -> str:
        # Prefer HTTP API
        result = self._invoke_http(prompt)
        if result is None or (isinstance(result, str) and result.startswith("❌")):
            # Fallback to CLI
            return self._invoke_cli(prompt)
        return result
