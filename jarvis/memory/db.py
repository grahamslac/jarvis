import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

class Database:
    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row
        self.init_schema()
    def init_schema(self):
        self.conn.executescript("""
        CREATE TABLE IF NOT EXISTS tasks(id INTEGER PRIMARY KEY, title TEXT NOT NULL, due_at TEXT, priority INTEGER DEFAULT 2, completed INTEGER DEFAULT 0, created_at TEXT NOT NULL, updated_at TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY, title TEXT NOT NULL, starts_at TEXT NOT NULL, ends_at TEXT, notes TEXT, created_at TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS memories(id INTEGER PRIMARY KEY, kind TEXT NOT NULL, content TEXT NOT NULL, metadata TEXT, created_at TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS reminders(id INTEGER PRIMARY KEY, title TEXT NOT NULL, run_at TEXT NOT NULL, recurrence TEXT, completed INTEGER DEFAULT 0, created_at TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS action_logs(id INTEGER PRIMARY KEY, request TEXT NOT NULL, tool TEXT, action TEXT, result TEXT, error TEXT, created_at TEXT NOT NULL);
        """); self.conn.commit()
    def add(self, table: str, values: dict[str, Any]) -> int:
        keys = ",".join(values); cur = self.conn.execute(f"INSERT INTO {table} ({keys}) VALUES ({','.join('?' for _ in values)})", tuple(values.values())); self.conn.commit(); return int(cur.lastrowid)
    def rows(self, table: str, where: str = "", params: tuple[Any, ...] = ()) -> list[dict[str, Any]]:
        return [dict(r) for r in self.conn.execute(f"SELECT * FROM {table} {where}", params).fetchall()]
    def execute(self, sql: str, params: tuple[Any, ...] = ()):
        cur = self.conn.execute(sql, params); self.conn.commit(); return cur
    def log(self, request: str, tool: str | None, action: str, result: Any = None, error: str | None = None):
        safe = json.dumps(result, ensure_ascii=False) if result is not None else None
        self.add("action_logs", {"request": request, "tool": tool, "action": action, "result": safe, "error": error, "created_at": now_iso()})
