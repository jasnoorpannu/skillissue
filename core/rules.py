import re
from dataclasses import dataclass
from typing import Callable, List

from core.parser import ParsedEvent
from core.utils import get_all_commands, find_similar_command, get_git_subcommands


@dataclass
class Suggestion:
    text: str
    score: float
    source: str


RuleFunc = Callable[[ParsedEvent], List[Suggestion]]

AVAILABLE_COMMANDS = get_all_commands()


def rule_command_not_found(event: ParsedEvent) -> List[Suggestion]:
    output = event.output.lower()
    if "command not found" not in output:
        return []

    cmd = event.command.split()[0] if event.command else "<?>"
    similar = find_similar_command(cmd, AVAILABLE_COMMANDS)

    if similar:
        msg = (
            f"Command '{cmd}' not found.\n"
            f"Did you mean: `{similar}` ?"
        )
        return [Suggestion(text=msg, score=0.97, source="rule:typo_command")]

    msg = (
        f"It looks like `{cmd}` is not installed. "
        "Try installing it via your package manager or check for typos."
    )
    return [Suggestion(text=msg, score=0.80, source="rule:command_not_found")]


def rule_git_merge_conflict(event: ParsedEvent) -> List[Suggestion]:
    out = event.output.lower()
    if "merge conflict" not in out and "conflict" not in out:
        return []

    msg = (
        "Git merge conflict detected. You can:\n"
        "  • Inspect conflicts: `git status`\n"
        "  • Abort merge: `git merge --abort`\n"
        "  • Resolve files then: `git add <files> && git commit`"
    )
    return [Suggestion(text=msg, score=0.85, source="rule:git_conflict")]


def rule_npm_error(event: ParsedEvent) -> List[Suggestion]:
    out = event.output.lower()
    if "npm err!" not in out:
        return []

    msg = (
        "npm reported errors. Possible fixes:\n"
        "  • Check logs around `npm ERR!`\n"
        "  • Run: `npm audit fix`\n"
        "  • Or: `npm install --legacy-peer-deps`\n"
        "  • Ensure correct Node version with nvm"
    )
    return [Suggestion(text=msg, score=0.80, source="rule:npm_error")]


def rule_addr_in_use(event: ParsedEvent) -> List[Suggestion]:
    if "eaddrinuse" not in event.output.lower():
        return []

    msg = (
        "Port already in use (EADDRINUSE).\n"
        "Try:\n"
        "  • `lsof -i :<port>` then `kill <pid>`\n"
        "  • Or select a different port"
    )
    return [Suggestion(text=msg, score=0.90, source="rule:addr_in_use")]


def rule_systemctl_failed(event: ParsedEvent) -> List[Suggestion]:
    if "systemctl" not in event.command:
        return []
    if "failed" not in event.output.lower():
        return []

    msg = (
        "systemd unit failed. Try:\n"
        "  • `systemctl status <unit> -l`\n"
        "  • `journalctl -u <unit>` for logs"
    )
    return [Suggestion(text=msg, score=0.75, source="rule:systemctl_failed")]


def rule_git_subcommand_typo(event: ParsedEvent) -> List[Suggestion]:
    if not event.command.startswith("git "):
        return []

    parts = event.command.split()
    if len(parts) < 2:
        return []

    sub = parts[1]
    lower_output = event.output.lower()

    if f"'{sub}' is not a git command" not in lower_output:
        return []

    available = get_git_subcommands()
    similar = find_similar_command(sub, available)

    if similar:
        msg = (
            f"Git subcommand '{sub}' is not valid.\n"
            f"Did you mean: `git {similar}` ?"
        )
        return [Suggestion(text=msg, score=0.98, source="rule:git_subcommand_typo")]

    msg = (
        f"Git subcommand '{sub}' is not valid.\n"
        "Run `git help -a` to see available commands."
    )
    return [Suggestion(text=msg, score=0.70, source="rule:git_subcommand_unknown")]


RULES: List[RuleFunc] = [
    rule_command_not_found,
    rule_git_subcommand_typo,
    rule_git_merge_conflict,
    rule_npm_error,
    rule_addr_in_use,
    rule_systemctl_failed,
]


def apply_rules(event: ParsedEvent) -> List[Suggestion]:
    suggestions: List[Suggestion] = []
    for rule in RULES:
        suggestions.extend(rule(event))
    suggestions.sort(key=lambda s: s.score, reverse=True)
    return suggestions
