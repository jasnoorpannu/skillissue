skillissue_capture() {
    local exit_code=$?
    local cmd="${BASH_COMMAND}"

    if [[ "$cmd" == *"skillissue"* ]] || [[ "$cmd" == *"cli.py"* ]]; then
        return
    fi

    python3 "$HOME/CSE/Projects/AITerminal/cli.py" hook \
        --cmd "$cmd" \
        --exit "$exit_code" </dev/null >/dev/null 2>&1
}

trap skillissue_capture DEBUG
