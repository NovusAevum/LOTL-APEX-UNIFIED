from llm_wrappers import Claude, Gemini, GroqLLama, GPT4, DeepSeekCoder, Codestral, Phi3, ContinueDev, CohereEmbed, NomicEmbed

class LLMFallbackAgent:
    def __init__(self):
        self.models = {
            "reasoning": [Claude(), Gemini(), GroqLLama(), GPT4()],
            "coding": [DeepSeekCoder(), Codestral(), Phi3(), ContinueDev()],
            "embedding": [CohereEmbed(), NomicEmbed()]
        }

    def call(self, task_type, prompt):
        for model in self.models.get(task_type, []):
            try:
                result = model.invoke(prompt)
                print(f"✅ {model.__class__.__name__} succeeded.")
                return result
            except Exception as e:
                print(f"⚠️ {model.__class__.__name__} failed. Reason: {e}")
        raise RuntimeError(f"🚨 All models failed for task: {task_type}")
