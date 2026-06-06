"""Part of FastAPI Boilerplate by Viprasol Tech Private Limited (https://viprasol.com).

Example CRUD resource: ``/items``.

All write operations are protected by the API-key dependency; reads are public to
keep the example easy to explore. Swap :data:`RepositoryDep` for a database-backed
implementation to take this to production.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Response, status

from app.dependencies import ApiKeyDep, PaginationDep, RepositoryDep
from app.schemas import ErrorResponse, Item, ItemCreate, ItemUpdate, Page

router = APIRouter(prefix="/items", tags=["items"])


@router.get("", response_model=Page[Item])
def list_items(repo: RepositoryDep, pagination: PaginationDep) -> Page[Item]:
    """Return a paginated list of items."""
    items, total = repo.list(offset=pagination.offset, limit=pagination.limit)
    return Page(items=items, total=total, page=pagination.page, size=pagination.size)


@router.get(
    "/{item_id}",
    response_model=Item,
    responses={status.HTTP_404_NOT_FOUND: {"model": ErrorResponse}},
)
def get_item(item_id: int, repo: RepositoryDep) -> Item:
    """Return a single item by id."""
    item = repo.get(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found.")
    return item


@router.post(
    "",
    response_model=Item,
    status_code=status.HTTP_201_CREATED,
    responses={status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponse}},
)
def create_item(data: ItemCreate, repo: RepositoryDep, _: ApiKeyDep) -> Item:
    """Create a new item (requires a valid API key)."""
    return repo.create(data)


@router.patch(
    "/{item_id}",
    response_model=Item,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponse},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse},
    },
)
def update_item(item_id: int, data: ItemUpdate, repo: RepositoryDep, _: ApiKeyDep) -> Item:
    """Partially update an existing item (requires a valid API key)."""
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found.")
    return item


@router.delete(
    "/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponse},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse},
    },
)
def delete_item(item_id: int, repo: RepositoryDep, _: ApiKeyDep) -> Response:
    """Delete an item by id (requires a valid API key)."""
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
