#!/bin/bash

REPO_PATH="$(cd "$(dirname "$0")" && pwd)"

echo "[skillissue] installing hooks..."

if [[ -f "$HOME/.zshrc" ]]; then
    HOOK="source \"$REPO_PATH/skillissue.zsh\""
    if ! grep -Fxq "$HOOK" "$HOME/.zshrc"; then
        echo "$HOOK" >> "$HOME/.zshrc"
        echo "[skillissue] added zsh hook"
    else
        echo "[skillissue] zsh hook already installed"
    fi
fi

if [[ -f "$HOME/.bashrc" ]]; then
    HOOK="source \"$REPO_PATH/skillissue.bash\""
    if ! grep -Fxq "$HOOK" "$HOME/.bashrc"; then
        echo "$HOOK" >> "$HOME/.bashrc"
        echo "[skillissue] added bash hook"
    else
        echo "[skillissue] bash hook already installed"
    fi
fi

echo "[skillissue] installation complete. Restart your terminal."
