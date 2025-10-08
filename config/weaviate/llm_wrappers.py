import os
from anthropic import Anthropic
from openai import OpenAI
from langchain_community.llms.ollama import Ollama
import requests

class Claude:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("CLAUDE_SOONET4.0_API_KEY"))

    def invoke(self, prompt):
        return self.client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        ).content[0].text

class Gemini:
    def invoke(self, prompt):
        # You’ll need Gemini SDK or custom HTTP
        raise NotImplementedError("👹 Gemini not yet tamed. I’ll teach next scroll.")

class GroqLLama:
    def invoke(self, prompt):
        res = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}"},
            json={
                "model": "llama3-70b-8192",
                "messages": [{"role": "user", "content": prompt}]
            }
        )
        return res.json()['choices'][0]['message']['content']

class GPT4:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def invoke(self, prompt):
        return self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        ).choices[0].message.content

class DeepSeekCoder:
    def invoke(self, prompt):
        # Assuming you serve via Ollama
        return Ollama(model="deepseek-coder").invoke(prompt)

class Codestral:
    def invoke(self, prompt):
        return Ollama(model="codestral").invoke(prompt)

class Phi3:
    def invoke(self, prompt):
        return Ollama(model="phi3").invoke(prompt)

class ContinueDev:
    def invoke(self, prompt):
        raise NotImplementedError("🥷 Still sharpening the blades of ContinueDev")

class CohereEmbed:
    def invoke(self, text):
        res = requests.post(
            "https://api.cohere.ai/v1/embed",
            headers={"Authorization": f"Bearer {os.getenv('COHERE_API_KEY')}"},
            json={"texts": [text]}
        )
        return res.json()["embeddings"][0]

class NomicEmbed:
    def invoke(self, text):
        return requests.post("http://localhost:8000/embed", json={"text": text}).json()["embedding"]
