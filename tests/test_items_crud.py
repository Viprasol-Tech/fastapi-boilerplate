"""CRUD lifecycle tests for the example items resource (offline)."""

from __future__ import annotations

from fastapi.testclient import TestClient

BASE = "/api/v1/items"


def _create(client: TestClient, headers: dict[str, str], name: str = "Widget") -> dict[str, object]:
    response = client.post(
        BASE,
        json={"name": name, "description": "A test item", "price": 9.99},
        headers=headers,
    )
    assert response.status_code == 201, response.text
    return response.json()


def test_create_and_get(client: TestClient, auth_headers: dict[str, str]) -> None:
    created = _create(client, auth_headers)
    assert created["id"] >= 1
    assert created["name"] == "Widget"
    assert "created_at" in created

    fetched = client.get(f"{BASE}/{created['id']}")
    assert fetched.status_code == 200
    assert fetched.json()["id"] == created["id"]


def test_list_pagination(client: TestClient, auth_headers: dict[str, str]) -> None:
    for i in range(3):
        _create(client, auth_headers, name=f"Item {i}")

    response = client.get(BASE, params={"page": 1, "size": 2})
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 3
    assert len(body["items"]) == 2
    assert body["page"] == 1
    assert body["size"] == 2


def test_update_item(client: TestClient, auth_headers: dict[str, str]) -> None:
    created = _create(client, auth_headers)
    response = client.patch(
        f"{BASE}/{created['id']}",
        json={"price": 19.5},
        headers=auth_headers,
    )
    assert response.status_code == 200
    body = response.json()
    assert body["price"] == 19.5
    assert body["name"] == "Widget"  # unchanged


def test_delete_item(client: TestClient, auth_headers: dict[str, str]) -> None:
    created = _create(client, auth_headers)
    deleted = client.delete(f"{BASE}/{created['id']}", headers=auth_headers)
    assert deleted.status_code == 204

    missing = client.get(f"{BASE}/{created['id']}")
    assert missing.status_code == 404


def test_get_missing_returns_404(client: TestClient) -> None:
    response = client.get(f"{BASE}/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found."


def test_update_missing_returns_404(client: TestClient, auth_headers: dict[str, str]) -> None:
    response = client.patch(f"{BASE}/99999", json={"price": 1.0}, headers=auth_headers)
    assert response.status_code == 404
