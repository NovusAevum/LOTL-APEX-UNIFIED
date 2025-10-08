import os
import sqlite3
from datetime import datetime
from typing import List, Optional, Tuple, Dict, Any

DB_PATH = os.path.expanduser(os.getenv("APEX_DB", "~/SovereignAI-data/apex_memory.db"))


def _connect() -> sqlite3.Connection:
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    return conn


def ensure_schema():
    with _connect() as conn:
        # Content memory (FTS5 for BM25 search)
        conn.execute(
            """
            CREATE VIRTUAL TABLE IF NOT EXISTS memory_fts USING fts5(
              content,
              metadata,
              created_at UNINDEXED,
              tokenize='porter'
            )
            """
        )
        # Tasks table
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              title TEXT NOT NULL,
              description TEXT,
              status TEXT NOT NULL DEFAULT 'queued',
              priority INTEGER NOT NULL DEFAULT 5,
              created_at TEXT NOT NULL,
              updated_at TEXT
            )
            """
        )
        conn.commit()


def upsert_memory(content: str, metadata: Optional[Dict[str, Any]] = None):
    ensure_schema()
    with _connect() as conn:
        conn.execute(
            "INSERT INTO memory_fts (content, metadata, created_at) VALUES (?, ?, ?)",
            (content, (metadata and str(metadata)) or "{}", datetime.utcnow().isoformat()),
        )
        conn.commit()


def search_memory(query: str, limit: int = 5) -> List[Dict[str, str]]:
    ensure_schema()
    with _connect() as conn:
        cur = conn.execute(
            "SELECT content, metadata, created_at FROM memory_fts WHERE memory_fts MATCH ? ORDER BY rank LIMIT ?",
            (query, limit),
        )
        rows = cur.fetchall()
        return [
            {"content": r[0], "metadata": r[1], "created_at": r[2]}
            for r in rows
        ]


def add_task(title: str, description: str, priority: int = 5) -> int:
    ensure_schema()
    with _connect() as conn:
        cur = conn.execute(
            "INSERT INTO tasks (title, description, priority, status, created_at) VALUES (?, ?, ?, 'queued', ?)",
            (title, description, priority, datetime.utcnow().isoformat()),
        )
        conn.commit()
        return int(cur.lastrowid)


def list_tasks(status: Optional[str] = None) -> List[Dict[str, Any]]:
    ensure_schema()
    with _connect() as conn:
        if status:
            cur = conn.execute(
                "SELECT id, title, description, status, priority, created_at, updated_at FROM tasks WHERE status=? ORDER BY priority ASC, id ASC",
                (status,),
            )
        else:
            cur = conn.execute(
                "SELECT id, title, description, status, priority, created_at, updated_at FROM tasks ORDER BY priority ASC, id ASC"
            )
        rows = cur.fetchall()
        return [
            {
                "id": r[0],
                "title": r[1],
                "description": r[2],
                "status": r[3],
                "priority": r[4],
                "created_at": r[5],
                "updated_at": r[6],
            }
            for r in rows
        ]


def update_task_status(task_id: int, status: str):
    ensure_schema()
    with _connect() as conn:
        conn.execute(
            "UPDATE tasks SET status=?, updated_at=? WHERE id=?",
            (status, datetime.utcnow().isoformat(), task_id),
        )
        conn.commit()
