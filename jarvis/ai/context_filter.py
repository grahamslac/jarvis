from dataclasses import dataclass
import re

@dataclass(frozen=True)
class FilteredContext:
    text: str
    estimated_tokens: int
    intent_hints: tuple[str, ...]


class ContextFilter:
    def filter(self, text: str) -> FilteredContext:
        clean = re.sub(r"\s+", " ", text).strip()
        hints = tuple(x for x in ("task" if any(w in clean.lower() for w in ("tarea", "recuérdame", "pendiente")) else "", "event" if any(w in clean.lower() for w in ("calendario", "examen", "clase", "reunión")) else "", "file" if any(w in clean.lower() for w in ("archivo", "carpeta", "documento")) else "") if x)
        return FilteredContext(clean, max(1, len(clean) // 4), hints)
