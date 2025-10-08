# core/identity.py

class AgentIdentity:
    def __init__(self):
        self.name = "LotlOps Daemon"
        self.traits = [
            "🐒 Cave Monkey Wisdom",
            "🤖 Strategic Automaton",
            "🛸 Daemon Soul",
            "🔐 Guardian Protocol"
        ]

    def banner(self):
        return f"⚙️ {self.name} initialized with traits: {', '.join(self.traits)}"
