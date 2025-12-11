# AI-Assisted Terminal (prototype)

You broke something, this tries to guess **how** and **what to do next**.

## What it does (for now)

- Logs terminal commands + their output into `data/history.log` (JSONL).
- Runs simple rules + plugins on errors:
  - git issues (conflicts, missing files)
  - docker daemon / space issues
  - python tracebacks
  - basic `command not found`, `EADDRINUSE`, etc.
- Prints **inline suggestions** after failed commands.

No ML yet. This is the rules-based scaffolding that will later feed training data.

## Project layout

```text
ai-assisted-terminal/
  core/
    shell_hook.py        # logging + event model
    parser.py            # parse history.log
    classifier.py        # dumb heuristics: error vs success, category
    suggestion_engine.py # call rules/plugins, pick best suggestion
    rules.py             # generic pattern-based rules
  plugins/
    git.py               # git-specific suggestions
    docker.py            # docker-specific suggestions
    python.py            # python-error-specific suggestions
  data/
    history.log          # auto-created JSONL event log
    training.jsonl       # future: labeled data for ML
  cli.py                 # entrypoint: hook, last, history
