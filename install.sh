#!/bin/bash

REPO_PATH="$(cd "$(dirname "$0")" && pwd)"

echo "[skillissue] installing hooks..."


if [[ -n "$ZSH_VERSION" || -f "$HOME/.zshrc" ]]; then
    HOOK="source \"$REPO_PATH/skillissue.zsh\""
    if ! grep -Fxq "$HOOK" "$HOME/.zshrc"; then
        echo "$HOOK" >> "$HOME/.zshrc"
        echo "[skillissue] added zsh hook"
    fi
fi

if [[ -n "$BASH_VERSION" || -f "$HOME/.bashrc" ]]; then
    HOOK="source \"$REPO_PATH/skillissue.bash\""
    if ! grep -Fxq "$HOOK" "$HOME/.bashrc"; then
        echo "$HOOK" >> "$HOME/.bashrc"
        echo "[skillissue] added bash hook"
    fi
fi

echo "[skillissue] installation complete. Restart your terminal."
