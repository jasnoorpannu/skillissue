from dataclasses import dataclass
from typing import Optional

from .parser import ParsedEvent


@dataclass
class Classification:
    is_error: bool
    category: Optional[str] = None
    confidence: float = 0.0


def classify_event(event: ParsedEvent) -> Classification:
    """
    Super dumb heuristic classifier for v1.
    Later this becomes ML-driven.
    """

    cmd = event.command.lower()
    out = event.output.lower()
    is_error = event.exit_code != 0 or "error" in out or "failed" in out

    if not is_error:
        return Classification(is_error=False, category=None, confidence=0.0)
    if "git" in cmd or "fatal:" in out and "git" in out:
        return Classification(True, "git", 0.8)
    if "docker" in cmd or "docker:" in out:
        return Classification(True, "docker", 0.8)
    if "npm" in cmd or "yarn" in cmd:
        return Classification(True, "node", 0.7)
    if "traceback" in out or "exception" in out:
        return Classification(True, "python", 0.7)
    if "command not found" in out:
        return Classification(True, "missing_command", 0.9)

    return Classification(True, "generic", 0.5)
