# memory/context_store.py

class ContextStore:
    def __init__(self):
        self.logs = []

    def remember(self, entry: str):
        self.logs.append(entry)

    def recall(self):
        return self.logs[-5:]  # You can change this window later
