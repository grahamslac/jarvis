from jarvis.memory.db import Database, now_iso

class TaskTools:
    def __init__(self, db: Database): self.db = db
    def create_task(self, title: str, due_at: str | None = None, priority: int = 2):
        ident = self.db.add("tasks", {"title": title, "due_at": due_at, "priority": priority, "completed": 0, "created_at": now_iso(), "updated_at": now_iso()})
        return {"id": ident, "title": title, "due_at": due_at, "priority": priority}
    def list_tasks(self, include_completed=False):
        where = "" if include_completed else "WHERE completed=0"
        return self.db.rows("tasks", where + " ORDER BY completed, priority, due_at")
    def complete_task(self, query: str):
        rows = self.db.rows("tasks", "WHERE completed=0 AND lower(title) LIKE ? LIMIT 1", (f"%{query.lower()}%",))
        if not rows: return {"found": False, "query": query}
        self.db.execute("UPDATE tasks SET completed=1, updated_at=? WHERE id=?", (now_iso(), rows[0]["id"]))
        return {"found": True, "task": rows[0]["title"]}
