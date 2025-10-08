# daemon.py

from agents.lotl import LotlOpsDaemon

if __name__ == "__main__":
    agent = LotlOpsDaemon()
    while True:
        try:
            cmd = input("🧠 LotlOps >> ").strip()
            if cmd.lower() in ["exit", "quit"]:
                print("🛑 Shutting down daemon...")
                break
            agent.execute(cmd)
        except KeyboardInterrupt:
            print("\n🛑 Interrupted by user. Exiting.")
            break

if cmd.startswith("!"):
    agent.think(cmd[1:].strip())  # remove ! and send to LLM
else:
    agent.execute(cmd)
