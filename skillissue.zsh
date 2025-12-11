skillissue_preexec() {
    export SI_LAST_CMD="$1"
}

skillissue_precmd() {
    local exit_code=$?
    local cmd="$SI_LAST_CMD"

    [[ -z "$cmd" ]] && return

    python3 "$HOME/CSE/Projects/AITerminal/cli.py" hook \
        --cmd "$cmd" \
        --exit "$exit_code"
}

autoload -Uz add-zsh-hook
add-zsh-hook preexec skillissue_preexec
add-zsh-hook precmd skillissue_precmd
