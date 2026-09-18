from datetime import datetime, timezone
from jarvis.memory.db import Database, now_iso

class Scheduler:
    def __init__(self, db: Database): self.db = db
    def add_reminder(self, title: str, run_at: str, recurrence: str | None = None):
        return self.db.add("reminders", {"title": title, "run_at": run_at, "recurrence": recurrence, "completed": 0, "created_at": now_iso()})
    def due(self, now: datetime | None = None):
        current = (now or datetime.now(timezone.utc)).isoformat()
        return self.db.rows("reminders", "WHERE completed=0 AND run_at<=? ORDER BY run_at", (current,))
    def mark_done(self, reminder_id: int): self.db.execute("UPDATE reminders SET completed=1 WHERE id=?", (reminder_id,))
