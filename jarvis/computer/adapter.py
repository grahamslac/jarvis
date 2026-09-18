from typing import Protocol, Any

class ActionExecutor(Protocol):
    def execute(self, action: dict[str, Any]) -> dict[str, Any]: ...

class ComputerUseAdapter:
    """Adaptador para el Computer Use oficial; el ejecutor de pantalla queda a cargo del entorno autorizado."""
    def __init__(self, enabled: bool, executor: ActionExecutor | None = None):
        self.enabled, self.executor = enabled, executor
    def run(self, task: str) -> dict[str, Any]:
        if not self.enabled: return {"status": "disabled", "message": "Computer Use está desactivado; configura un ejecutor autorizado."}
        if self.executor is None: return {"status": "unconfigured", "message": "Falta configurar el ejecutor gráfico."}
        return self.executor.execute({"task": task})
