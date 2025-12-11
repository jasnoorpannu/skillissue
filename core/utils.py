import os
from pathlib import Path
from difflib import SequenceMatcher
import subprocess

_COMMAND_CACHE = None
_GIT_SUBCOMMANDS = None


def get_git_subcommands():
    global _GIT_SUBCOMMANDS
    if _GIT_SUBCOMMANDS is not None:
        return _GIT_SUBCOMMANDS

    try:
        output = subprocess.check_output(["git", "help", "-a"], stderr=subprocess.STDOUT)
        text = output.decode("utf-8")
    except Exception:
        _GIT_SUBCOMMANDS = set()
        return _GIT_SUBCOMMANDS

    commands = set()

    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue

        # Accept any line containing multiple tokens
        parts = line.split()
        for p in parts:
            if p.isalpha():
                commands.add(p)

    _GIT_SUBCOMMANDS = commands
    return _GIT_SUBCOMMANDS



def get_all_commands():
    global _COMMAND_CACHE
    if _COMMAND_CACHE is not None:
        return _COMMAND_CACHE

    commands = set()
    paths = os.environ.get("PATH", "").split(":")

    for p in paths:
        p = Path(p)
        if not p.exists():
            continue

        for f in p.iterdir():
            if f.is_file() and os.access(f, os.X_OK):
                commands.add(f.name)

    _COMMAND_CACHE = commands
    return commands


def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()


def levenshtein(a, b):
    if len(a) < len(b):
        return levenshtein(b, a)
    if len(b) == 0:
        return len(a)

    prev = range(len(b) + 1)
    for i, c1 in enumerate(a):
        curr = [i + 1]
        for j, c2 in enumerate(b):
            insertions = prev[j + 1] + 1
            deletions = curr[j] + 1
            subs = prev[j] + (c1 != c2)
            curr.append(min(insertions, deletions, subs))
        prev = curr
    return prev[-1]


def find_similar_command(cmd, available_commands):
    cmd = cmd.strip()

    if len(cmd) < 3:
        return None

    best = None
    best_score = 0.0

    for candidate in available_commands:
        if not candidate:
            continue
        if candidate[0] != cmd[0]:
            continue

        sim = similarity(cmd, candidate)
        dist = levenshtein(cmd, candidate)

        if sim < 0.75:
            continue
        if dist > 2:
            continue

        if sim > best_score:
            best_score = sim
            best = candidate

    return best
