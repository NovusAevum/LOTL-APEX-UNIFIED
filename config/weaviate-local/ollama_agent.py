from langchain.agents import initialize_agent, Tool
from langchain_community.llms.ollama import Ollama
import requests

# Define the embedding tool
def embedding_tool(text: str):
    res = requests.post("http://localhost:8000/embed", json={"text": text})
    return res.json()["embedding"]

tools = [
    Tool(
        name="OllamaEmbedder",
        func=embedding_tool,
        description="Embeds user text via local Ollama API"
    )
]

# Load Ollama LLM (local)
llm = Ollama(model="llama3")  # Ensure `ollama run llama3` is running

# Initialize agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent="zero-shot-react-description",
    verbose=True
)

# Run agent
response = agent.invoke("Embed the sentence 'Knowledge is power'")
print(response)
