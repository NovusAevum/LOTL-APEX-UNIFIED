from llm_fallback_agent import LLMFallbackAgent

agent = LLMFallbackAgent()
task = "reasoning"
prompt = "Give me a Sun Tzu quote and explain its relevance in business strategy."

try:
    response = agent.call(task, prompt)
    print("🧠 Response:\n", response)
except RuntimeError as e:
    print(str(e))
