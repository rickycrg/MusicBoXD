import os
import requests

from dotenv import load_dotenv

load_dotenv()


class D1Error(Exception):
    pass

def query(sql, params=None):
    """
    Run one SQL statement on the Cloudflare D1 database through the REST API.
    Returns the list of result rows as dicts.
    """
    account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID")
    api_token = os.getenv("CLOUDFLARE_API_TOKEN")
    database_id = os.getenv("CLOUDFLARE_D1_DATABASE")

    if not account_id or not api_token:
        raise ValueError("Missing Cloudflare credentials in environment.")

    url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/d1/database/{database_id}/query"
    response = requests.post(
        url,
        headers={"Authorization": f"Bearer {api_token}"},
        json={"sql": sql, "params": params or []},
        timeout=30,
    )

    try:
        data = response.json()
    except ValueError:
        raise D1Error(f"D1 request failed with status {response.status_code}")

    if not data.get("success"):
        messages = "; ".join(e.get("message", "") for e in data.get("errors", []))
        raise D1Error(messages or f"D1 request failed with status {response.status_code}")

    return data["result"][0]["results"]

def query_one(sql, params=None):
    rows = query(sql, params)
    return rows[0] if rows else None
