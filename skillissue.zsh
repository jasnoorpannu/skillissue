skillissue_preexec() {
    export SI_LAST_CMD="$1"
}

skillissue_precmd() {
    local exit_code=$?
    local cmd="$SI_LAST_CMD"

    [[ -z "$cmd" ]] && return

    if [[ "$cmd" == *"skillissue"* ]] || [[ "$cmd" == *"cli.py"* ]]; then
        return
    fi

    python3 "$HOME/CSE/Projects/AITerminal/cli.py" hook \
        --cmd "$cmd" \
        --exit "$exit_code" </dev/null >/dev/null 2>&1
}


autoload -Uz add-zsh-hook
add-zsh-hook preexec skillissue_preexec
add-zsh-hook precmd skillissue_precmd
