from jarvis.memory.db import Database, now_iso

class CalendarTools:
    def __init__(self, db: Database): self.db = db
    def create_event(self, title: str, starts_at: str, ends_at: str | None = None, notes: str | None = None):
        ident = self.db.add("events", {"title": title, "starts_at": starts_at, "ends_at": ends_at, "notes": notes, "created_at": now_iso()})
        return {"id": ident, "title": title, "starts_at": starts_at, "ends_at": ends_at}
    def list_events(self): return self.db.rows("events", "ORDER BY starts_at")
