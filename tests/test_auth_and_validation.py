"""Authentication and validation error tests (offline)."""

from __future__ import annotations

from fastapi.testclient import TestClient

BASE = "/api/v1/items"


def test_create_requires_api_key(client: TestClient) -> None:
    response = client.post(BASE, json={"name": "NoAuth", "price": 1.0})
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid or missing API key."


def test_create_rejects_wrong_api_key(client: TestClient) -> None:
    response = client.post(
        BASE,
        json={"name": "BadAuth", "price": 1.0},
        headers={"X-API-Key": "nope"},
    )
    assert response.status_code == 401


def test_validation_error_on_missing_field(
    client: TestClient, auth_headers: dict[str, str]
) -> None:
    response = client.post(BASE, json={"description": "no name or price"}, headers=auth_headers)
    assert response.status_code == 422
    body = response.json()
    assert body["detail"] == "Validation error."
    assert isinstance(body["errors"], list)


def test_validation_error_on_negative_price(
    client: TestClient, auth_headers: dict[str, str]
) -> None:
    response = client.post(
        BASE,
        json={"name": "Cheap", "price": -5},
        headers=auth_headers,
    )
    assert response.status_code == 422


def test_pagination_rejects_oversized_size(client: TestClient) -> None:
    response = client.get(BASE, params={"size": 99999})
    assert response.status_code == 422
