SKILLISSUE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

skillissue_capture() {
    local exit_code=$?
    local cmd="${BASH_COMMAND}"

    [[ -z "$cmd" ]] && return

    case "$cmd" in
        skillissue*|*cli.py*|_* )
            return ;;
    esac

    python3 "$SKILLISSUE_ROOT/cli.py" hook \
        --cmd "$cmd" \
        --exit "$exit_code" </dev/null >/dev/null 2>&1
}

trap skillissue_capture DEBUG

command_not_found_handle() {
    local cmd="$1"
    shift
    local args="$*"
    local msg="bash: $cmd: command not found"

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
        --exit "$rc" < "$tmp" >/dev/null 2>&1

    rm -f "$tmp"
    return $rc
}

if type -P npm >/dev/null 2>&1; then
    npm() { _skillissue_run_and_capture npm "$@"; }
fi

if type -P docker >/dev/null 2>&1; then
    docker() { _skillissue_run_and_capture docker "$@"; }
fi
