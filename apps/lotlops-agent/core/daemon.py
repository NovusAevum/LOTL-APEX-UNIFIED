import os
from apscheduler.schedulers.background import BackgroundScheduler
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from agents.lotl import LotlOpsDaemon
from memory.context_store import ContextStore


class _HistoryHandler(FileSystemEventHandler):
    def __init__(self, memory: ContextStore, path_label: str):
        self.memory = memory
        self.path_label = path_label

    def on_modified(self, event):
        try:
            if event.is_directory:
                return
            with open(event.src_path, "r", errors="ignore") as f:
                tail = f.readlines()[-5:]
            self.memory.remember(f"[HISTORY][{self.path_label}]\n" + "".join(tail))
        except Exception:
            pass


def _nightly(memory: ContextStore):
    memory.remember("[SCHEDULE] nightly consolidation complete")


if __name__ == "__main__":
    agent = LotlOpsDaemon()
    memory = agent.memory

    # Background scheduler for nightly tasks
    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_job(lambda: _nightly(memory), "cron", hour=0, minute=3)
    scheduler.start()

    # Filesystem observation for adaptive learning
    observer = Observer()
    for path, label in [
        (os.path.expanduser("~/.zsh_history"), "zsh"),
        (os.path.expanduser("~/Documents"), "docs"),
        (os.path.expanduser("~/AIProjects"), "ai"),
    ]:
        if os.path.exists(path):
            handler = _HistoryHandler(memory, label)
            observer.schedule(handler, path=path, recursive=True)
    observer.start()

    try:
        while True:
            try:
                raw = input("🧠 LotlOps >> ").strip()
                if raw.startswith("🧠 LotlOps >>"):
                    raw = raw.replace("🧠 LotlOps >>", "").strip()
                if raw.lower() in ["exit", "quit"]:
                    break
                agent.execute(raw)
            except KeyboardInterrupt:
                break
    finally:
        try:
            observer.stop()
            observer.join(timeout=2)
        except Exception:
            pass
        try:
            scheduler.shutdown(wait=False)
        except Exception:
            pass
