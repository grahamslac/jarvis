import tempfile
import unittest
from datetime import datetime, timezone, timedelta
from pathlib import Path
from jarvis.memory.db import Database
from jarvis.tasks.tools import TaskTools
from jarvis.calendar.events import CalendarTools
from jarvis.scheduler.service import Scheduler
from jarvis.ai.context_filter import ContextFilter
from jarvis.security.policy import SecurityPolicy
from jarvis.computer.adapter import ComputerUseAdapter

class JarvisTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.db = Database(Path(self.tmp.name) / "test.sqlite3")
    def tearDown(self): self.tmp.cleanup()
    def test_tasks_lifecycle(self):
        tasks = TaskTools(self.db); tasks.create_task("Estudiar cálculo", priority=1)
        self.assertEqual(len(tasks.list_tasks()), 1); self.assertTrue(tasks.complete_task("cálculo")["found"]); self.assertEqual(tasks.list_tasks(), [])
    def test_calendar_and_scheduler(self):
        events = CalendarTools(self.db); events.create_event("Examen", "2099-01-02T10:00:00+00:00"); self.assertEqual(events.list_events()[0]["title"], "Examen")
        scheduler = Scheduler(self.db); due = (datetime.now(timezone.utc) - timedelta(minutes=1)).isoformat(); ident = scheduler.add_reminder("Revisar tareas", due); self.assertEqual(scheduler.due()[0]["id"], ident)
    def test_filter_and_security(self):
        result = ContextFilter().filter("  Recuérdame   estudiar cálculo mañana a las 8.  "); self.assertEqual(result.text, "Recuérdame estudiar cálculo mañana a las 8."); self.assertIn("task", result.intent_hints)
        policy = SecurityPolicy((Path(self.tmp.name),)); self.assertTrue(policy.requires_confirmation("elimina el archivo")); self.assertEqual(ComputerUseAdapter(False).run("abre") ["status"], "disabled")

if __name__ == "__main__": unittest.main()
