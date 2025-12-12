from dataclasses import dataclass
from typing import Optional
from .parser import ParsedEvent

@dataclass
class Classification:
    is_error: bool
    category: Optional[str] = None
    confidence: float = 0.0

def classify_event(event: ParsedEvent) -> Classification:
    program = (event.cmd or "").lower()
    out = (event.output or "").lower()

    is_error = (
        event.exit_code != 0
        or "error" in out
        or "failed" in out
        or "command not found" in out
    )

    if not is_error:
        return Classification(False, None, 0.0)

    if program in ("npm", "yarn") or "npm err!" in out:
        return Classification(True, "node", 0.8)

    if "traceback" in out or "exception" in out:
        return Classification(True, "python", 0.75)

    if "command not found" in out:
        return Classification(True, "missing_command", 0.95)

    return Classification(True, "generic", 0.5)
