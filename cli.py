import argparse
import sys
import select
from pathlib import Path

from core.shell_hook import create_event, log_event, read_last_event, HISTORY_PATH
from core.parser import parse_event
from core.suggestion_engine import generate_suggestion


# Colours
RED = "\033[91m"
RESET = "\033[0m"


def _safe_stdin_read() -> str:
    """
    Prevents blocking forever when run inside a preexec/precmd hook.
    Reads stdin only if data is immediately available.
    """
    if sys.stdin.isatty():
        return ""

    r, _, _ = select.select([sys.stdin], [], [], 0.01)
    if r:
        return sys.stdin.read()

    return ""


def cmd_hook(args: argparse.Namespace) -> int:
    """
    Shell integration entrypoint.
    Reads command output safely (non-blocking), logs event,
    runs suggestion engine, prints colored suggestions.
    """
    output = _safe_stdin_read()

    event = create_event(args.cmd, args.exit, output)
    log_event(event)
    parsed = parse_event(event)
    suggestion = generate_suggestion(parsed)

    if suggestion:
        import random
        prefixes = [
            "huge L detected",
            "skill issue confirmed",
            "bro cooked",
            "terminal says get good",
            "IDE watching your downfall",
            "kernel panics at your code",
            "git just shook its head",
            "this commit will haunt you",
        ]
        banner = random.choice(prefixes)

        sys.stderr.write(f"\n{RED}$ skillissue | {banner}:{RESET}\n")
        sys.stderr.write(suggestion.text + "\n\n")

    return 0


def cmd_last(args: argparse.Namespace) -> int:
    """
    Debug: show the last logged event and suggested fix.
    """
    raw = read_last_event()
    if not raw:
        print("No events logged yet.")
        return 0

    parsed = parse_event(raw)
    print("Last event:")
    print(f"  timestamp: {parsed.timestamp}")
    print(f"  command:   {parsed.command}")
    print(f"  exit_code: {parsed.exit_code}")
    print("  output:")
    print(parsed.output[:800] + ("\n...[truncated]..." if len(parsed.output) > 800 else ""))

    suggestion = generate_suggestion(parsed)
    if suggestion:
        print("\nSuggestion:")
        print(suggestion.text)
    else:
        print("\nNo suggestion for this event.")

    return 0


def cmd_history(args: argparse.Namespace) -> int:
    """
    Show where data/history.log lives.
    """
    print(f"History file: {HISTORY_PATH}")
    if HISTORY_PATH.exists():
        size = HISTORY_PATH.stat().st_size
        print(f"Exists, size: {size} bytes")
    else:
        print("File does not exist yet.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="skillissue",
        description="SkillIssue terminal helper.",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_hook = sub.add_parser("hook", help="Log a command + output and emit suggestions.")
    p_hook.add_argument("--cmd", required=True, help="Command that was executed.")
    p_hook.add_argument("--exit", required=True, type=int, help="Exit code of that command.")
    p_hook.set_defaults(func=cmd_hook)

    p_last = sub.add_parser("last", help="Show last logged event + suggestion.")
    p_last.set_defaults(func=cmd_last)

    p_hist = sub.add_parser("history", help="Show history.log location and size.")
    p_hist.set_defaults(func=cmd_history)

    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
