import getpass

RESET = "\033[0m"
DIM = "\033[2m"
BOLD = "\033[1m"
CYAN = "\033[36m"
GREEN = "\033[32m"

# move up one line and erase it
CLEAR_LINE = "\033[1A\033[2K"


ART = """
  ██████╗ ██████╗  █████╗ ██╗   ██╗██████╗ ███████╗
  ██╔══██╗██╔══██╗██╔══██╗██║   ██║██╔══██╗██╔════╝
  ██████╔╝██████╔╝███████║██║   ██║██║  ██║█████╗
  ██╔═══╝ ██╔══██╗██╔══██║██║   ██║██║  ██║██╔══╝
  ██║     ██║  ██║██║  ██║╚██████╔╝██████╔╝███████╗
  ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝"""


def banner():
    print(f"{CYAN}{BOLD}{ART}{RESET}")
    print(f"  {DIM}program → claude scope builder · by SpiizN{RESET}\n")


def ask(prompt):
    value = input(f"  {CYAN}?{RESET} {prompt} ")
    print(CLEAR_LINE, end="")
    return value


def ask_secret(prompt):
    value = getpass.getpass(f"  {CYAN}?{RESET} {prompt} ")
    print(CLEAR_LINE, end="")
    return value


def confirm(question):
    answer = input(f"  {CYAN}?{RESET} {question} [y/N] ")
    print(CLEAR_LINE, end="")
    return answer.strip().lower() in ("y", "yes")


def info(message):
    print(f"  {DIM}{message}{RESET}")


def summary(program, files):
    rows = [
        ("program", program.get("title") or "-"),
        ("organization", program.get("organization_name") or "-"),
        ("type", program.get("program_type") or "-"),
        ("in-scope assets", str(len(program.get("in_scope") or []))),
        ("test accounts", str(len(program.get("accounts") or []))),
    ]

    print(f"\n  {GREEN}{BOLD}✓ collected{RESET}")
    for label, value in rows:
        print(f"    {DIM}{label:<16}{RESET} {value}")

    print()
    for path in files:
        print(f"    {GREEN}→{RESET} {path}")
    print()
