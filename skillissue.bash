skillissue_capture() {
    local exit_code=$?
    local cmd="${BASH_COMMAND}"

    [[ "$cmd" == *"skillissue"* ]] && return

    python3 "$HOME/CSE/Projects/AITerminal/cli.py" hook \
        --cmd "$cmd" \
        --exit "$exit_code"
}

trap skillissue_capture DEBUG
