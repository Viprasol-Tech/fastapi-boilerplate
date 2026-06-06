"""Part of FastAPI Boilerplate by Viprasol Tech Private Limited (https://viprasol.com).

A self-contained, offline example that drives the API via FastAPI's TestClient.

Run it with::

    python examples/usage.py

No server, database or network connection is required.
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app

API_KEY = "demo-key"


def main() -> None:
    """Exercise the health, create, list and get endpoints end-to-end."""
    app = create_app(Settings(api_keys=API_KEY))
    headers = {"X-API-Key": API_KEY}

    with TestClient(app) as client:
        print("health:", client.get("/health").json())

        created = client.post(
            "/api/v1/items",
            json={"name": "Starter Plan", "description": "Example item", "price": 49.0},
            headers=headers,
        ).json()
        print("created:", created)

        listing = client.get("/api/v1/items").json()
        print("list:", listing)

        fetched = client.get(f"/api/v1/items/{created['id']}").json()
        print("fetched:", fetched)


if __name__ == "__main__":
    main()
