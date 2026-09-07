import os, csv
from requests import Session

# local imports
from praude.auth import get_token

ACCOUNTS_FILE = "accounts.csv"

class YesWeHack:
    def __init__(self, proxy=None, store_token=False):
        self.base_url = "https://api.yeswehack.com"

        # internal properties
        self.__s = Session()

        proxies = {"http": proxy, "https": proxy} if proxy else None
        if proxies:
            self.__s.proxies.update(proxies)

        token = get_token(proxies=proxies, store=store_token)
        self.__s.headers["Authorization"] = f"Bearer {token}"

    """
    Programs & Scopes
    """

    def get_program_details(self, slug: str):
        """
        Get the details of a given program.
        """

        program = {}

        # program base
        response = self.__s.get(f"{self.base_url}/programs/{slug}")
        program.update(response.json())

        ## program credentials
        response = self.__s.get(f"{self.base_url}/programs/{slug}/credential-pools")
        program.update({"credential_pools": response.json().get("items", {})})
        response = self.__s.get(f"{self.base_url}/programs/{slug}/hunter/credentials")
        program.update({"credentials": response.json()})

        ## hand-maintained accounts (accounts.csv in the current directory)
        manual_accounts = []
        if os.path.exists(ACCOUNTS_FILE):
            with open(ACCOUNTS_FILE, newline="", encoding="utf-8") as f:
                manual_accounts = [row for row in csv.DictReader(f) if row["slug"] == slug]
        program.update({"manual_accounts": manual_accounts})

        # return informations
        return program

    """
    Program data
    """

    def filter_program_data(self, program: dict) -> dict:
        """
        Reduce the program details to the values ready to render in the template.
        """

        business_unit = program.get("business_unit") or {}
        credentials = program.get("credentials") or {}

        in_scope = [
            {
                "target": scope.get("scope"),
                "type": scope.get("scope_type_name"),
                "criticality": scope.get("asset_value"),
                "reports": scope.get("report_count"),
            }
            for scope in program.get("scopes") or []
        ]

        accounts = []
        for cred in credentials.get("credentials", []) or []:
            if cred.get("disabled"):
                continue

            notes = []
            if cred.get("email_alias"):
                notes.append("YesWeHack email alias - self-register / login with this address")
            if not cred.get("password"):
                notes.append("no password provisioned")

            credential_pool = cred.get("credential_pool") or {}

            accounts.append({
                "scope": "",
                "label": credential_pool.get("title") or f"Account {cred.get('id')}",
                "username": cred.get("email") or cred.get("login"),
                "password": cred.get("password") or "",
                "notes": "; ".join(notes),
            })

        # comptes manuels
        for row in program.get("manual_accounts") or []:
            key = ((row.get("scope") or "").strip().lower(), (row.get("username") or "").strip().lower())
            accounts = [
                a for a in accounts
                if ((a.get("scope") or "").strip().lower(), (a.get("username") or "").strip().lower()) != key
            ]
            accounts.append(row)

        return {
            "title": program.get("title"),
            "organization_name": business_unit.get("name"),
            "platform_name": "YesWeHack",
            "program_slug": program.get("slug"),
            "program_type": program.get("type"),
            "business_description": business_unit.get("description"),
            "report_language": ", ".join(program.get("supported_languages") or []),
            "in_scope": in_scope,
            "out_of_scope": program.get("out_of_scope") or [],
            "accounts": accounts,
            "qualifying_vulnerabilities": program.get("qualifying_vulnerability") or [],
            "non_qualifying_vulnerabilities": program.get("non_qualifying_vulnerability") or [],
            "rules": "\n".join(f"> {line}" for line in (program.get("rules") or "").splitlines()),
            "user_agent": program.get("user_agent") or "",
            "vpn_proxy_url": program.get("vpn_ips") if program.get("vpn_active") else "",
            "account_access": "\n".join(f"> {line}" for line in (program.get("account_access") or "").splitlines()),
        }

    def get_instructions_data(self, slug: str) -> dict:
        """
        Fetch and filter a program's data, ready to render templates/instructions.md.
        """
        return self.filter_program_data(self.get_program_details(slug))