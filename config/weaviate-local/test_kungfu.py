from llm_fallback_agent import LLMFallbackAgent

agent = LLMFallbackAgent()

# Choose your Kungfu task: 'reasoning', 'coding', or 'embedding'
task = "reasoning"
prompt = "Explain the philosophy of stoicism in 3 bullets."

response = agent.call(task, prompt)
print("\n🧘 Response:\n", response)
