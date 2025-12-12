import re
from dataclasses import dataclass
from typing import Callable, List

from core.parser import ParsedEvent
from core.utils import get_all_commands, find_similar_command

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

    cmd = event.cmd or ""
    similar = find_similar_command(cmd, AVAILABLE_COMMANDS)

    if similar:
        msg = (
            f"Command '{cmd}' not found.\n"
            f"Did you mean: `{similar}` ?"
        )
        return [Suggestion(msg, 0.97, "rule:typo_command")]

    msg = (
        f"'{cmd}' is not installed. "
        "Check spelling or install it."
    )
    return [Suggestion(msg, 0.80, "rule:command_not_found")]

def rule_npm_error(event: ParsedEvent) -> List[Suggestion]:
    out = event.output.lower()
    if "npm err!" not in out:
        return []
    msg = (
        "npm reported errors.\n"
        "Try:\n"
        "  • npm audit fix\n"
        "  • npm install --legacy-peer-deps\n"
        "  • check Node version"
    )
    return [Suggestion(msg, 0.80, "rule:npm_error")]

def rule_addr_in_use(event: ParsedEvent) -> List[Suggestion]:
    if "eaddrinuse" not in event.output.lower():
        return []
    msg = (
        "Port already in use.\n"
        "Try:\n"
        "  • lsof -i :<port>\n"
        "  • kill <pid>\n"
        "  • change port"
    )
    return [Suggestion(msg, 0.90, "rule:addr_in_use")]

def rule_systemctl_failed(event: ParsedEvent) -> List[Suggestion]:
    if "systemctl" not in event.full_command:
        return []
    if "failed" not in event.output.lower():
        return []
    msg = (
        "Systemd unit failed.\n"
        "Try:\n"
        "  • systemctl status <unit> -l\n"
        "  • journalctl -u <unit>"
    )
    return [Suggestion(msg, 0.75, "rule:systemctl_failed")]

RULES = [
    rule_command_not_found,
    rule_npm_error,
    rule_addr_in_use,
    rule_systemctl_failed,
]

def apply_rules(event: ParsedEvent) -> List[Suggestion]:
    suggestions = []
    for rule in RULES:
        suggestions.extend(rule(event))
    suggestions.sort(key=lambda s: s.score, reverse=True)
    return suggestions
