from dataclasses import dataclass
from pathlib import Path
import os

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover
    load_dotenv = lambda: None


@dataclass(frozen=True)
class Settings:
    api_key: str | None
    model: str | None
    db_path: Path
    computer_use_enabled: bool
    allowed_roots: tuple[Path, ...]
    log_level: str

    @classmethod
    def from_env(cls) -> "Settings":
        load_dotenv()
        roots = tuple(Path(x).expanduser().resolve() for x in os.getenv("JARVIS_ALLOWED_ROOTS", ".").split(os.pathsep) if x)
        return cls(
            api_key=os.getenv("OPENAI_API_KEY") or None,
            model=os.getenv("OPENAI_MODEL") or None,
            db_path=Path(os.getenv("JARVIS_DB_PATH", "data/jarvis.sqlite3")).expanduser(),
            computer_use_enabled=os.getenv("JARVIS_COMPUTER_USE_ENABLED", "false").lower() in {"1", "true", "yes"},
            allowed_roots=roots or (Path.cwd().resolve(),),
            log_level=os.getenv("JARVIS_LOG_LEVEL", "INFO"),
        )
