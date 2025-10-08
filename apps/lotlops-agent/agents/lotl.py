# agents/lotl.py

from core.identity import AgentIdentity
from core.loader import load_env
from shell_planner.task_engine import ShellExecutor
from memory.context_store import ContextStore
from core.llm_orchestrator import OllamaModel  # Required
import os
from memory.semantic_store import upsert_memory, search_memory, add_task

class LotlOpsDaemon:
    def __init__(self):
        self.id = AgentIdentity()
        self.env = load_env()
        self.executor = ShellExecutor()
        self.memory = ContextStore()
        default_model = os.getenv("OLLAMA_MODEL", "llama3")
        self.llm = OllamaModel(default_model)
        print(self.id.banner())

    def execute(self, cmd: str):
        if cmd.startswith("!"):
            prompt = cmd[1:].strip()
            output = self.llm.invoke(prompt)
        else:
            output = self.executor.run(cmd)

        self.memory.remember(f"$ {cmd}\n{output}")
        # Store into semantic memory for future recall
        upsert_memory(output, {"source": "console", "cmd": cmd})
        print(output)

    def partner(self, instruction: str):
        # Plan: create task entry and immediate suggestion based on memory recall
        task_id = add_task(title=instruction[:80], description=instruction)
        recalls = search_memory(instruction, limit=3)
        context = "\n".join([r["content"] for r in recalls])
        plan = self.llm.invoke(
            f"You are APEX partner. Instruction: {instruction}\nRelevant context:\n{context}\nPlan concise next steps as a numbered list."
        )
        self.memory.remember(f"[PARTNER][task:{task_id}]\n{plan}")
        return {"task_id": task_id, "plan": plan, "context": recalls}
