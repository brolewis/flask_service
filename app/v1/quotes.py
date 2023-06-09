import json
import os
import urllib.parse

import requests
from flask import current_app, abort, request


def _get_json_data(session: requests.Session, url: str, params dict | None = None) -> list[dict]:
    """
    Helper function to get data from a URL and ensure no errors and that data was
    successfully returned.
    """
    # Get the character data from the API
    res = session.get(url, params=params)

    # Check for API errors and pass through to end user
    try:
        res.raise_for_status()
    except requests.exceptions.HTTPError:
        abort(res.status_code)

    # Check that we got back data
    docs = res.json().get("docs") or []
    if not len(docs):
        abort(404)

    return docs


def _get_quotes(character: str, limit: int | None = None):
    # Note the base URL for this method is working with the character so let that base
    # for consisten reuse
    base_url = urllib.parse.urljoin(current_app.config["API_BASE"], "v2/character")
    # Grab the token from the environment so it's not stored in the codebase
    token = os.getenv("API_TOKEN")
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    # Create reusable session object
    session = requests.Session()
    session.headers.update(headers)

    characters = _get_json_data(session, base_url, params={"name": character})

    char_id = characters[0]["_id"]
    quotes = _get_json_data(
        session, f"{base_url.rstrip('/')}/{char_id}/quote", params={"limit": limit}
    )
    return quotes

def get_quote() -> (str, int):
    """Get a quote for a provided character.

    Parameter:
        character (str): Character name from LotR

    Output:
        JSON:
            dialog: string containing a single quote from a character
    """
    character = request.args.get("name")
    quote = _get_quotes(character, limit=1)[0]
    return json.dumps({"dialog": quote["dialog"]}), 200


def get_quotes() -> (str, int):
    """Get a quote for a provided character.

    Parameter:
        character (str): Character name from LotR

    Output:
        JSON:
            dialog: string containing a single quote from a character
    """
    character = request.args.get("name")
    quote = _get_quotes(character, limit=100)[0]
    return json.dumps({"dialog": quote["dialog"]}), 200
