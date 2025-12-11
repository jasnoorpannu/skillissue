import json
import sys
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional


HISTORY_PATH = Path(__file__).resolve().parent.parent / "data" / "history.log"


@dataclass
class TerminalEvent:
    timestamp: str
    command: str
    exit_code: int
    output: str


def create_event(command: str, exit_code: int, output: str) -> TerminalEvent:
    """Construct a TerminalEvent from pieces."""
    return TerminalEvent(
        timestamp=datetime.utcnow().isoformat() + "Z",
        command=command.strip(),
        exit_code=int(exit_code),
        output=output.rstrip(),
    )


def log_event(event: TerminalEvent, history_path: Optional[Path] = None) -> None:
    """Append the event as JSONL to history.log."""
    path = history_path or HISTORY_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(asdict(event), ensure_ascii=False) + "\n")


def read_last_event(history_path: Optional[Path] = None) -> Optional[TerminalEvent]:
    """Read the last logged event, if any."""
    path = history_path or HISTORY_PATH
    if not path.exists():
        return None

    *_, last_line = path.read_text(encoding="utf-8").splitlines() or [""]
    if not last_line.strip():
        return None

    try:
        data = json.loads(last_line)
        return TerminalEvent(**data)
    except Exception:
        return None


def main_from_stdin():
    """
    Used by cli.py 'hook' subcommand.

    Expects:
      --cmd <command string>
      --exit <exit code>
    Reads full output from stdin.
    """

    raise SystemExit(
        "shell_hook.main_from_stdin() is not meant to be run directly. "
        "Use `python cli.py hook ...` instead."
    )


if __name__ == "__main__":
    data = sys.stdin.read()
    print(f"Read from stdin:\n{data}")
