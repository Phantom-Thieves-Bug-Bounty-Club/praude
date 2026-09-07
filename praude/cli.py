import argparse
from importlib.resources import files

from jinja2 import Template

from praude import ui


def render(template_name, output_path, data):
    text = files("praude.templates").joinpath(template_name).read_text(encoding="utf-8")
    template = Template(text, trim_blocks=True, lstrip_blocks=True)
    with open(output_path, "w") as f:
        f.write(template.render(**data))


def main():
    try:
        run()
    except (KeyboardInterrupt, EOFError):
        print(f"\n  {ui.DIM}aborted{ui.RESET}")
        raise SystemExit(130)


def run():
    parser = argparse.ArgumentParser(prog="praude")
    parser.add_argument("slug", help="Program slug")
    parser.add_argument("--proxy", help="Proxy URL for all HTTP requests, e.g. http://127.0.0.1:8080")
    parser.add_argument("--store-token", action="store_true", help="After login, offer to store the YWH token in /tmp/.praude-token for reuse")

    # agent type spec
    agent = parser.add_mutually_exclusive_group()
    agent.add_argument("--claude", dest="agent", action="store_const", const="claude", help="Tailor PROMPT.md for Claude Code (CLAUDE.md, ~/.claude skills)")
    agent.add_argument("--codex", dest="agent", action="store_const", const="codex", help="Tailor PROMPT.md for Codex (AGENTS.md)")

    args = parser.parse_args()

    ui.banner()

    # imported here so the banner shows before the auth prompts
    from praude.yeswehack import YesWeHack

    ywh = YesWeHack(proxy=args.proxy, store_token=args.store_token)
    program_data = ywh.get_instructions_data(args.slug)
    program_data["agent"] = args.agent

    render("instructions.md", "SCOPE.md", program_data)
    render("prompt.md", "PROMPT.md", program_data)

    with open("targets.txt", "w") as f:
        for asset in program_data["in_scope"]:
            f.write(asset["target"] + "\n")

    ui.summary(program_data, ["SCOPE.md", "PROMPT.md", "targets.txt"])


if __name__ == "__main__":
    main()

