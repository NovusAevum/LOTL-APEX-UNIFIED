import os
import requests
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

class GroqLLama:
    def __init__(self):
        self.name = "Groq"
        self.api_key = os.getenv("GROQ_API_KEY")

    def invoke(self, prompt):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "llama3-8b-8192",
            "messages": [{"role": "user", "content": prompt}]
        }
        res = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=data
        )
        return res.json()["choices"][0]["message"]["content"]

class Gemini:
    def __init__(self):
        self.name = "Gemini"
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

    def invoke(self, prompt):
        return self.model.generate_content(prompt).text
