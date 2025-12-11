from typing import Optional

from .classifier import classify_event
from .parser import ParsedEvent
from .rules import Suggestion, apply_rules
from plugins import git as git_plugin
from plugins import docker as docker_plugin
from plugins import python as python_plugin


def generate_suggestion(event: ParsedEvent) -> Optional[Suggestion]:
    """
    Central brain: classify event, run relevant rules/plugins, pick best suggestion.
    """
    classification = classify_event(event)

    if not classification.is_error:
        return None

    suggestions = []

    suggestions.extend(apply_rules(event))

    if classification.category == "git":
        suggestions.extend(git_plugin.get_suggestions(event))
    elif classification.category == "docker":
        suggestions.extend(docker_plugin.get_suggestions(event))
    elif classification.category == "python":
        suggestions.extend(python_plugin.get_suggestions(event))

    if not suggestions:
        return None

    suggestions.sort(key=lambda s: s.score, reverse=True)
    best = suggestions[0]
    
    if best.score < 0.6:
        return None

    return best
