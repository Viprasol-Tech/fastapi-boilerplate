"""Part of FastAPI Boilerplate by Viprasol Tech Private Limited (https://viprasol.com).

Reusable FastAPI dependencies: settings, repository, pagination and API-key auth.
"""

from __future__ import annotations

from typing import Annotated

from fastapi import Depends, HTTPException, Query, Request, Security, status
from fastapi.security import APIKeyHeader

from app.config import Settings, get_settings
from app.repository import InMemoryItemRepository, ItemRepository

API_KEY_HEADER = "X-API-Key"

_api_key_header = APIKeyHeader(name=API_KEY_HEADER, auto_error=False)

# A single process-local repository instance for the app lifetime.
_repository = InMemoryItemRepository()


def get_repository() -> ItemRepository:
    """Return the active item repository implementation."""
    return _repository


SettingsDep = Annotated[Settings, Depends(get_settings)]
RepositoryDep = Annotated[ItemRepository, Depends(get_repository)]


def require_api_key(
    settings: SettingsDep,
    api_key: Annotated[str | None, Security(_api_key_header)] = None,
) -> str:
    """Validate the ``X-API-Key`` header against the configured keys."""
    if not api_key or api_key not in settings.allowed_api_keys:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key.",
            headers={"WWW-Authenticate": API_KEY_HEADER},
        )
    return api_key


ApiKeyDep = Annotated[str, Depends(require_api_key)]


class PaginationParams:
    """Validated pagination parameters with computed offset/limit."""

    def __init__(self, request: Request, page: int, size: int) -> None:
        settings = get_settings()
        if size > settings.max_page_size:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"size must not exceed {settings.max_page_size}.",
            )
        self.page = page
        self.size = size
        self.offset = (page - 1) * size
        self.limit = size


def pagination_params(
    request: Request,
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query(ge=1)] = 20,
) -> PaginationParams:
    """Provide validated pagination parameters."""
    return PaginationParams(request, page=page, size=size)


PaginationDep = Annotated[PaginationParams, Depends(pagination_params)]
