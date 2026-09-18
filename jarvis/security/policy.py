from pathlib import Path

SENSITIVE_WORDS = ("elimina", "borrar", "borra", "envía", "envia", "compra", "paga", "ejecuta", "renombra", "mueve")

class SecurityPolicy:
    def __init__(self, allowed_roots: tuple[Path, ...]):
        self.allowed_roots = tuple(p.resolve() for p in allowed_roots)
    def requires_confirmation(self, action: str) -> bool:
        text = action.lower(); return any(word in text for word in SENSITIVE_WORDS)
    def allowed_path(self, path: Path) -> bool:
        resolved = path.expanduser().resolve(); return any(resolved == root or root in resolved.parents for root in self.allowed_roots)
