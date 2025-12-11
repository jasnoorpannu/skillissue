from typing import List
from core.parser import ParsedEvent
from core.rules import Suggestion


def get_suggestions(event: ParsedEvent) -> List[Suggestion]:
    cmd = event.command.lower()
    out = event.output.lower()
    suggestions: List[Suggestion] = []

    if "git pull" in cmd and "divergent branches" in out:
        suggestions.append(
            Suggestion(
                text=(
                    "Git pull shows divergent branches. Consider:\n"
                    "  • `git pull --rebase` to rebase your local commits\n"
                    "  • or configure: `git config pull.rebase true`"
                ),
                score=0.82,
                source="plugin:git_divergent",
            )
        )

    if "did not match any file(s) known to git" in out:
        suggestions.append(
            Suggestion(
                text=(
                    "Git couldn't find that file.\n"
                    "  • Check for typos in the path\n"
                    "  • Use `git status` or `git ls-files` to see tracked files."
                ),
                score=0.8,
                source="plugin:git_missing_file",
            )
        )

    return suggestions
