from pathlib import Path

import requests

from praude import ui

BASE_URL = "https://api.yeswehack.com"
TOKEN_FILE = Path("/tmp/.praude-token")


def _login(proxies):
    email = ui.ask("YesWeHack email:")
    password = ui.ask_secret("Password:")

    data = requests.post(
        f"{BASE_URL}/login",
        json={"email": email, "password": password},
        proxies=proxies,
    ).json()

    if data.get("totp_token"):
        code = ui.ask("2FA code:")
        data = requests.post(
            f"{BASE_URL}/account/totp",
            json={"token": data["totp_token"], "code": code},
            proxies=proxies,
        ).json()

    token = data.get("token")
    if not token:
        raise SystemExit("Authentication failed.")

    return token


def _valid(token, proxies):
    response = requests.get(
        f"{BASE_URL}/user",
        headers={"Authorization": f"Bearer {token}"},
        proxies=proxies,
    )
    return response.status_code == 200


def get_token(proxies=None, store=False):
    """
    Return a valid YesWeHack API token, reusing the one in /tmp/.praude-token
    when it exists and is still valid.
    """
    if TOKEN_FILE.exists():
        token = TOKEN_FILE.read_text().strip()
        if _valid(token, proxies):
            ui.info(f"reusing token from {TOKEN_FILE}")
            return token

    token = _login(proxies)
    ui.info("authenticated")

    if store and ui.confirm(f"Store the YWH token in {TOKEN_FILE}?"):
        TOKEN_FILE.write_text(token)
        ui.info(f"token stored in {TOKEN_FILE}")

    return token
