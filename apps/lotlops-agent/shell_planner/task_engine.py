# shell_planner/task_engine.py

import os
import shlex
import subprocess
from typing import List


class ShellExecutor:
    """Hardened shell execution with allowlist and timeouts."""

    def __init__(self, allowed_commands: List[str] | None = None, timeout_seconds: int | None = None):
        allowed_env = os.getenv("ALLOWED_COMMANDS", "git,ls,cat,echo,python,python3,pip,pip3,uv,rg,rgp,ruff,black")
        self.allowed_commands = [c.strip() for c in (allowed_commands or allowed_env.split(",")) if c.strip()]
        self.timeout_seconds = timeout_seconds or int(os.getenv("COMMAND_TIMEOUT_SECONDS", "30"))

    def _is_allowed(self, command: str) -> bool:
        try:
            parts = shlex.split(command)
        except ValueError:
            return False
        if not parts:
            return False
        base = os.path.basename(parts[0])
        return base in self.allowed_commands

    def run(self, command: str) -> str:
        if not self._is_allowed(command):
            return "❌ Command not allowed by policy"
        try:
            args = shlex.split(command)
            result = subprocess.run(
                args,
                shell=False,
                check=True,
                text=True,
                capture_output=True,
                timeout=self.timeout_seconds,
            )
            return result.stdout.strip()
        except subprocess.TimeoutExpired:
            return "❌ Error: command timeout"
        except subprocess.CalledProcessError as e:
            return f"❌ Error: {e.stderr.strip()}"
