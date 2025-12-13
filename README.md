# skillissue

`skillissue` is a lightweight terminal assistant that watches your commands, detects common mistakes, and tells you what you *meant* to do — loudly, clearly, and without pretending to be smarter than you.

It runs locally, requires no API keys, no cloud, no telemetry, and does **not** execute commands for you.
It only observes failures and suggests fixes.

If you typo `mkkdir`, it will call it out.
If a command fails, it will explain why.
If everything works, it stays quiet.

Minimal. Opinionated. Slightly judgmental.

---

## Features

* Catches **command typos** (e.g. `mkkdir → mkdir`)
* Detects **command-not-found** errors
* Surfaces **useful suggestions** after failed commands
* Works in **zsh and bash**
* Zero dependencies beyond Python 3
* No background daemon, no shell replacement
* Runs entirely on your machine

What it **does not** do:

* It does not auto-run corrected commands
* It does not modify your shell behavior
* It does not phone home
* It does not “AI hallucinate” fixes

---

## Requirements

* Python **3.8+**
* `bash` or `zsh`
* Linux / macOS (Windows not supported)

---

## Installation

Clone the repository:

```bash
git clone https://github.com/<your-username>/skillissue.git
cd skillissue
```

Run the installer:

```bash
chmod +x install.sh
./install.sh
```

Then restart your terminal:

```bash
exec $SHELL
```

That’s it.

`skillissue` now hooks into your shell and activates automatically.

---

## Usage

Use your terminal normally.

When a command fails, `skillissue` may respond like:

```text
✖ skillissue | skill issue confirmed:
Command 'mkkdir' not found.
Did you mean: `mkdir` ?
```

If there’s nothing useful to say, it stays silent.

No commands to remember.
No aliases to use.
No new workflow to learn.

---

## Uninstallation

To completely remove `skillissue` from your system:

```bash
cd path/to/skillissue
chmod +x uninstall.sh
./uninstall.sh
```

Restart your terminal:

```bash
exec $SHELL
```

Optionally delete the repository:

```bash
rm -rf skillissue
```

After this, **no hooks, no files, no residue** remain.

---

## How It Works (Briefly)

* Hooks into shell lifecycle (`preexec`, `precmd`, `command_not_found`)
* Captures:

  * the command you ran
  * exit code
  * output
* Runs a small rules engine in Python
* Prints a suggestion *only if one is actually helpful*

No ML model yet.
No magic.
Just common sense, automated.

---

## Philosophy

Terminals already tell you *that* something failed.
`skillissue` tells you **why** and **what to do next**.

It does not fix mistakes for you.
It simply makes them obvious.

---

## License

MIT

Use it. Fork it. Improve it.
