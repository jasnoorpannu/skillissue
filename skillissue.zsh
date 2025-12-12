SKILLISSUE_ROOT="$(cd "$(dirname "${(%):-%N}")" && pwd)"

skillissue_preexec() {
    SI_LAST_CMD="$1"
}

skillissue_precmd() {
    local exit_code=$?
    local cmd="$SI_LAST_CMD"

    cmd="${cmd%"${cmd##*[![:space:]]}"}"
    [[ -z "$cmd" ]] && return

    case "$cmd" in
        exec\ zsh|precmd*|preexec*|add-zsh-hook|_* )
            return ;;
    esac

    if [[ "$cmd" == *"skillissue"* ]] || [[ "$cmd" == *"cli.py"* ]]; then
        return
    fi

    python3 "$SKILLISSUE_ROOT/cli.py" hook \
        --cmd "$cmd" \
        --exit "$exit_code"
}

autoload -Uz add-zsh-hook
add-zsh-hook preexec skillissue_preexec
add-zsh-hook precmd skillissue_precmd

command_not_found_handler() {
    local cmd="$1"
    shift
    local args="$*"
    local msg="zsh: $cmd: command not found"

    python3 "$SKILLISSUE_ROOT/cli.py" hook \
        --cmd "$cmd $args" \
        --exit 127 <<< "$msg"

    return 127
}

REAL_GIT="$(command -v git)"

_skillissue_run_and_capture() {
    local bin="$1"; shift
    local args=("$@")
    local tmp="$(mktemp /tmp/skillissue.XXXXXX)"

    command "$bin" "${args[@]}" >"$tmp" 2>&1
    local rc=$?

    if [[ "$bin" = "git" ]]; then
        if grep -qi "not a git repository" "$tmp" || \
           grep -qi "GIT_DISCOVERY_ACROSS_FILESYSTEM" "$tmp"; then
            true
        else
            cat "$tmp"
        fi
    else
        cat "$tmp"
    fi

    python3 "$SKILLISSUE_ROOT/cli.py" hook \
        --cmd "$bin ${args[*]}" \
        --exit "$rc" \
        < "$tmp" >/dev/null 2>&1

    rm -f "$tmp"
    return $rc
}


if type -P npm >/dev/null 2>&1; then
    npm() { _skillissue_run_and_capture npm "$@"; }
fi

if type -P docker >/dev/null 2>&1; then
    docker() { _skillissue_run_and_capture docker "$@"; }
fi

unfunction npm 2>/dev/null
unfunction docker 2>/dev/null

npm()     { _skillissue_run_and_capture npm "$@"; }
docker()  { _skillissue_run_and_capture docker "$@"; }

