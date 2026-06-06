"""Pytest fixtures for the offline FastAPI Boilerplate test-suite (Viprasol Tech)."""

from __future__ import annotations

from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from app.config import Settings
from app.dependencies import get_repository
from app.main import create_app
from app.repository import InMemoryItemRepository

API_KEY = "test-key"


@pytest.fixture
def client() -> Iterator[TestClient]:
    """Yield a TestClient with an isolated in-memory repository and known API key."""
    settings = Settings(api_keys=API_KEY, cors_origins="*")
    app = create_app(settings)

    repo = InMemoryItemRepository()
    app.dependency_overrides[get_repository] = lambda: repo

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def auth_headers() -> dict[str, str]:
    """Return headers carrying a valid API key."""
    return {"X-API-Key": API_KEY}
