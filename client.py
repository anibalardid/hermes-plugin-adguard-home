"""Thin HTTP client for the AdGuard Home REST API."""

import json
import os
from base64 import b64encode
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


def _base_url() -> str:
    host = os.environ.get("ADGUARD_HOST", "http://127.0.0.1:3000")
    return host.rstrip("/") + "/control"


def _auth_header() -> dict:
    user = os.environ.get("ADGUARD_USER", "admin")
    password = os.environ.get("ADGUARD_PASSWORD", "")
    token = b64encode(f"{user}:{password}".encode()).decode()
    return {"Authorization": f"Basic {token}"}


def get(path: str, params: dict | None = None) -> dict | list | str:
    """GET /control{path} with optional query params."""
    url = _base_url() + path
    if params:
        from urllib.parse import urlencode
        url += "?" + urlencode({k: v for k, v in params.items() if v is not None})
    req = Request(url, headers={**_auth_header(), "Accept": "application/json"})
    try:
        with urlopen(req, timeout=10) as resp:
            body = resp.read()
            if not body:
                return {}
            return json.loads(body)
    except HTTPError as e:
        raise RuntimeError(f"HTTP {e.code}: {e.read().decode(errors='replace')}") from e
    except URLError as e:
        raise RuntimeError(
            f"Cannot reach AdGuard Home at {_base_url()}. "
            "Is it running? Check ADGUARD_HOST."
        ) from e


def post(path: str, body: dict | list | None = None) -> dict | list | str:
    """POST /control{path} with optional JSON body."""
    url = _base_url() + path
    data = json.dumps(body).encode() if body is not None else b""
    req = Request(
        url,
        data=data,
        method="POST",
        headers={
            **_auth_header(),
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
    try:
        with urlopen(req, timeout=10) as resp:
            body_resp = resp.read()
            if not body_resp:
                return {}
            return json.loads(body_resp)
    except HTTPError as e:
        raise RuntimeError(f"HTTP {e.code}: {e.read().decode(errors='replace')}") from e
    except URLError as e:
        raise RuntimeError(
            f"Cannot reach AdGuard Home at {_base_url()}. "
            "Is it running? Check ADGUARD_HOST."
        ) from e


def put(path: str, body: dict | list | None = None) -> dict | list | str:
    """PUT /control{path} with optional JSON body."""
    url = _base_url() + path
    data = json.dumps(body).encode() if body is not None else b""
    req = Request(
        url,
        data=data,
        method="PUT",
        headers={
            **_auth_header(),
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
    try:
        with urlopen(req, timeout=10) as resp:
            body_resp = resp.read()
            if not body_resp:
                return {}
            return json.loads(body_resp)
    except HTTPError as e:
        raise RuntimeError(f"HTTP {e.code}: {e.read().decode(errors='replace')}") from e
    except URLError as e:
        raise RuntimeError(
            f"Cannot reach AdGuard Home at {_base_url()}. "
            "Is it running? Check ADGUARD_HOST."
        ) from e
