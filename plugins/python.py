from typing import List
from core.parser import ParsedEvent
from core.rules import Suggestion


def get_suggestions(event: ParsedEvent) -> List[Suggestion]:
    out = event.output
    lower = out.lower()
    suggestions: List[Suggestion] = []

    if "traceback" in lower and "module not found error" in lower:
        suggestions.append(
            Suggestion(
                text=(
                    "Python `ModuleNotFoundError` detected.\n"
                    "Check that the package is installed in this environment:\n"
                    "  • `pip list` or `pip show <package>`\n"
                    "  • Install: `pip install <package>` (or correct virtualenv)."
                ),
                score=0.85,
                source="plugin:python_module_not_found",
            )
        )

    if "indexerror: list index out of range" in lower:
        suggestions.append(
            Suggestion(
                text=(
                    "Python `IndexError: list index out of range`.\n"
                    "You probably accessed an index that doesn't exist.\n"
                    "Add bounds checks or print `len(list)` and the index used."
                ),
                score=0.8,
                source="plugin:python_index_error",
            )
        )

    if "keyerror:" in lower:
        suggestions.append(
            Suggestion(
                text=(
                    "Python `KeyError` on a dict.\n"
                    "Use `.get(key)` with a default or check `key in dict` before access."
                ),
                score=0.78,
                source="plugin:python_key_error",
            )
        )

    return suggestions
