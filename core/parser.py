from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, List
import json
from core.shell_hook import TerminalEvent


@dataclass
class ParsedEvent:
    timestamp: datetime
    full_command: str
    cmd: str
    subcommand: str
    args: List[str]
    tokens: List[str]
    exit_code: int
    output: str


def parse_event(raw: TerminalEvent) -> ParsedEvent:
    ts = datetime.fromisoformat(raw.timestamp.replace("Z", "+00:00"))

    text = (raw.command or "").strip()
    text = " ".join(text.split())

    parts = text.split() if text else []

    cmd = parts[0] if parts else ""
    sub = parts[1] if len(parts) > 1 else ""

    args = parts[1:] if len(parts) > 1 else []
    tokens = parts

    return ParsedEvent(
        timestamp=ts,
        full_command=text,
        cmd=cmd,
        subcommand=sub,
        args=args,
        tokens=tokens,
        exit_code=raw.exit_code,
        output=raw.output or "",
    )


def read_events(history_path: Path) -> Iterable[ParsedEvent]:
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
    events = list(read_events(history_path))
    return events[-n:]
