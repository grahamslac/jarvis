import logging
from jarvis.config.settings import Settings
from jarvis.memory.db import Database
from jarvis.security.policy import SecurityPolicy
from jarvis.tasks.tools import TaskTools
from jarvis.calendar.events import CalendarTools
from jarvis.files.operations import FileTools
from jarvis.tools.system import get_system_status
from jarvis.ai.client import OpenAIClient
from jarvis.computer.adapter import ComputerUseAdapter
from jarvis.core.orchestrator import Orchestrator

def build(settings=None):
    settings = settings or Settings.from_env(); logging.basicConfig(level=settings.log_level)
    db = Database(settings.db_path); policy = SecurityPolicy(settings.allowed_roots)
    return Orchestrator(db, TaskTools(db), CalendarTools(db), FileTools(policy), get_system_status, OpenAIClient(settings.api_key, settings.model), ComputerUseAdapter(settings.computer_use_enabled), policy)

def main():
    jarvis = build(); print("JARVIS listo. Escribe 'salir' para terminar.")
    while True:
        try: request = input("Tú: ").strip()
        except (EOFError, KeyboardInterrupt): break
        if request.lower() in {"salir", "exit", "quit"}: break
        if request: print("JARVIS:", jarvis.handle(request, confirm=lambda x: input(f"Voy a realizar '{x}'. ¿Confirmas? [s/N] ").lower() in {"s", "si", "sí"}).text)

if __name__ == "__main__": main()
