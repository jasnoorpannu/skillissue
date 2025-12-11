from typing import List
from core.parser import ParsedEvent
from core.rules import Suggestion


def get_suggestions(event: ParsedEvent) -> List[Suggestion]:
    out = event.output.lower()
    cmd = event.command.lower()
    suggestions: List[Suggestion] = []

    if "cannot connect to the docker daemon" in out or "is the docker daemon running" in out:
        suggestions.append(
            Suggestion(
                text=(
                    "Docker daemon seems down.\n"
                    "Try starting it:\n"
                    "  • `sudo systemctl start docker`\n"
                    "  • Or ensure your user is in the `docker` group."
                ),
                score=0.88,
                source="plugin:docker_daemon",
            )
        )

    if "no space left on device" in out and "docker" in cmd:
        suggestions.append(
            Suggestion(
                text=(
                    "Docker ran out of disk space.\n"
                    "You can clean unused data with:\n"
                    "  • `docker system df`\n"
                    "  • `docker system prune -a` (careful, removes unused images/containers)"
                ),
                score=0.83,
                source="plugin:docker_space",
            )
        )

    return suggestions
