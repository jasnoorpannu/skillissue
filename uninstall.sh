#!/bin/bash

REPO_PATH="$(cd "$(dirname "$0")" && pwd)"

echo "[skillissue] removing hooks..."

HOOK_ZSH="source \"$REPO_PATH/skillissue.zsh\""
HOOK_BASH="source \"$REPO_PATH/skillissue.bash\""

sed -i "\|$HOOK_ZSH|d" "$HOME/.zshrc" 2>/dev/null
sed -i "\|$HOOK_BASH|d" "$HOME/.bashrc" 2>/dev/null

echo "[skillissue] uninstalled. Restart your terminal."
