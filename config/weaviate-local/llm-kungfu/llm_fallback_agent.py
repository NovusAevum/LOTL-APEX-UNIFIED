from llm_wrappers import Gemini, GroqLLama

class LLMFallbackAgent:
    def __init__(self):
        self.models = {
            "reasoning": [GroqLLama(), Gemini()]
        }

    def call(self, task_type, prompt):
        for model in self.models.get(task_type, []):
            try:
                print(f"⚡ Trying {model.name}")
                return model.invoke(prompt)
            except Exception as e:
                print(f"⚠️ {model.name} failed. Reason: {e}")
        raise RuntimeError(f"🚨 All models failed for task: {task_type}")
