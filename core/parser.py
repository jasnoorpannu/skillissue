import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, List

from .shell_hook import TerminalEvent


@dataclass
class ParsedEvent:
    timestamp: datetime
    command: str
    exit_code: int
    output: str


def parse_event(raw: TerminalEvent) -> ParsedEvent:
    """Convert raw TerminalEvent to ParsedEvent with datetime object."""
    ts = datetime.fromisoformat(raw.timestamp.replace("Z", "+00:00"))
    return ParsedEvent(
        timestamp=ts,
        command=raw.command,
        exit_code=raw.exit_code,
        output=raw.output,
    )


def read_events(history_path: Path) -> Iterable[ParsedEvent]:
    """Stream all events from history.log."""
    if not history_path.exists():
        return []

    with history_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                raw = TerminalEvent(**data)
                yield parse_event(raw)
            except Exception:
                continue


def read_last_n_events(history_path: Path, n: int = 50) -> List[ParsedEvent]:
    """Return last N events (inefficient but fine for v1)."""
    events = list(read_events(history_path))
    return events[-n:]
