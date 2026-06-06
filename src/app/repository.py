"""Part of FastAPI Boilerplate by Viprasol Tech Private Limited (https://viprasol.com).

Repository abstraction for the example CRUD resource.

The :class:`ItemRepository` protocol defines a storage-agnostic interface so the
default in-memory implementation can be swapped for a SQL/NoSQL backend without
touching the API layer.
"""

from __future__ import annotations

from datetime import UTC, datetime
from itertools import count
from typing import Protocol, runtime_checkable

from app.schemas import Item, ItemCreate, ItemUpdate


@runtime_checkable
class ItemRepository(Protocol):
    """Storage-agnostic interface for item persistence."""

    def list(self, *, offset: int, limit: int) -> tuple[list[Item], int]:
        """Return a page of items and the total count."""
        ...

    def get(self, item_id: int) -> Item | None:
        """Return a single item or ``None`` if it does not exist."""
        ...

    def create(self, data: ItemCreate) -> Item:
        """Persist and return a new item."""
        ...

    def update(self, item_id: int, data: ItemUpdate) -> Item | None:
        """Apply a partial update; return the item or ``None`` if missing."""
        ...

    def delete(self, item_id: int) -> bool:
        """Delete an item; return ``True`` if it existed."""
        ...


class InMemoryItemRepository:
    """A thread-unsafe, process-local repository — ideal for tests and demos."""

    def __init__(self) -> None:
        self._items: dict[int, Item] = {}
        self._ids = count(1)

    def list(self, *, offset: int, limit: int) -> tuple[list[Item], int]:
        ordered = sorted(self._items.values(), key=lambda item: item.id)
        return ordered[offset : offset + limit], len(ordered)

    def get(self, item_id: int) -> Item | None:
        return self._items.get(item_id)

    def create(self, data: ItemCreate) -> Item:
        item = Item(
            id=next(self._ids),
            created_at=datetime.now(tz=UTC),
            **data.model_dump(),
        )
        self._items[item.id] = item
        return item

    def update(self, item_id: int, data: ItemUpdate) -> Item | None:
        existing = self._items.get(item_id)
        if existing is None:
            return None
        updated = existing.model_copy(update=data.model_dump(exclude_unset=True))
        self._items[item_id] = updated
        return updated

    def delete(self, item_id: int) -> bool:
        return self._items.pop(item_id, None) is not None
