# praude

Praude (program to claude) is a CLI tool to make an instruction file for claude to bug hunt on a provided target.

## Install

```bash
pipx install git+https://github.com/Phantom-Thieves-Bug-Bounty-Club/praude.git
```

Or from a local clone:

```bash
pipx install .
```

For development without installing:

```bash
pip install -r requirements.txt
python main.py <program-slug>
```

## Usage

```bash
praude <program-slug>
```

This writes three files in the current directory:

- `SCOPE.md` — all the program info (assets, rules, accounts, qualifying vulns...).
- `PROMPT.md` — a ready-to-use prompt for an autonomous bug bounty agent, adapted
  to the program (points the agent at `SCOPE.md`, web/API only, YWH reporting
  skills, Burp/Firefox/Exegol MCP, context in `CLAUDE.md`, findings in `findings/`).
- `targets.txt` — the list of in-scope targets, one per line.

## Options

- `--proxy URL` — route every HTTP request through a proxy (e.g. `--proxy http://127.0.0.1:8080`).
- `--store-token` — after login, asks for confirmation and, if accepted, writes the
  YWH token to `/tmp/.praude-token`.
- `--claude` / `--codex` — tailor `PROMPT.md` to that agent (context file `CLAUDE.md`
  resp. `AGENTS.md`, and agent-specific reporting-skill wording). With neither flag
  the prompt stays generic and prescribes no particular file names.

## Authentication

There is no config file. Each run asks for your YesWeHack email, password and 2FA
code. If `/tmp/.praude-token` exists and is still valid, it is reused instead — this
file is only created when you run with `--store-token`.

## Manual accounts

Optionally, create an `accounts.csv` file in the current directory to add your own test accounts.
See `praude/templates/accounts.example.csv` for the format:

```csv
slug,scope,label,username,password,notes
```

- If the tool finds automatically-assigned credentials on YesWeHack, it merges your accounts with the ones found on the platform.
- If two accounts have the same "scope+username" key, the platform one is overridden by the manually created account.
