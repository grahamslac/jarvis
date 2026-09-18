import re
from dataclasses import dataclass, field
from jarvis.ai.context_filter import ContextFilter

@dataclass
class RunResult:
    text: str
    tool: str | None = None
    stats: dict = field(default_factory=dict)

class Orchestrator:
    def __init__(self, db, tasks, calendar, files, system, ai, computer, policy):
        self.db, self.tasks, self.calendar, self.files, self.system, self.ai, self.computer, self.policy = db, tasks, calendar, files, system, ai, computer, policy
        self.filter = ContextFilter()

    def handle(self, request: str, confirm=lambda _: False) -> RunResult:
        ctx = self.filter.filter(request); low = ctx.text.lower(); tool = None
        try:
            if self.policy.requires_confirmation(request) and not confirm(request):
                return RunResult(f"Necesito confirmación antes de realizar: {request}", stats={"input_tokens_estimated": ctx.estimated_tokens})
            if any(x in low for x in ("recuérdame", "crear tarea", "agrega una tarea", "añade una tarea")):
                title = re.sub(r"^(jarvis,?\s*)?(recuérdame|crear tarea|agrega una tarea|añade una tarea)\s*", "", ctx.text, flags=re.I).strip(" .")
                result = self.tasks.create_task(title); tool = "create_task"; text = f"Tarea creada: {title}."
            elif "pendiente" in low or "mis tareas" in low or "lista de tareas" in low:
                result = self.tasks.list_tasks(); tool = "list_tasks"; text = "\n".join(f"- {x['title']}" for x in result) or "No tienes tareas pendientes."
            elif "marca" in low and "complet" in low:
                query = re.sub(r".*?marca\s+(.+?)\s+como\s+completada?.*", r"\1", ctx.text, flags=re.I); result = self.tasks.complete_task(query); tool = "complete_task"; text = "Tarea completada." if result.get("found") else "No encontré esa tarea."
            elif any(x in low for x in ("calendario", "eventos", "clases", "examen")) and ("qué" in low or "lista" in low or "revisa" in low):
                result = self.calendar.list_events(); tool = "list_events"; text = "\n".join(f"- {x['starts_at']}: {x['title']}" for x in result) or "No hay eventos registrados."
            elif "busca" in low and ("archivo" in low or "carpeta" in low):
                query = re.sub(r".*?(?:archivo|carpeta)\s+(?:de\s+)?", "", ctx.text, flags=re.I).strip(" ."); result = self.files.search_file(query); tool = "search_file"; text = "\n".join(result) or "No encontré coincidencias."
            elif "estado" in low or "sistema" in low:
                result = self.system(); tool = "get_system_status"; text = f"Sistema: {result['platform']} · Python {result['python']}"
            elif self.ai.available():
                answer = self.ai.ask(ctx.text, "Eres JARVIS, un asistente local conciso. No inventes acciones realizadas; si hace falta una herramienta no disponible, dilo."); result = answer; text = answer.text; tool = "openai_responses"
            else:
                result = self.computer.run(ctx.text); tool = "computer_use"; text = result["message"]
            self.db.log(request, tool, "handle", result)
            return RunResult(text, tool, {"input_tokens_estimated": ctx.estimated_tokens, "tool": tool})
        except Exception as exc:
            self.db.log(request, tool, "handle", error=str(exc)); return RunResult(f"No pude completar la acción: {exc}", tool, {"input_tokens_estimated": ctx.estimated_tokens})
