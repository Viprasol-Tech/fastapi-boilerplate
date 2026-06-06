"""Part of FastAPI Boilerplate by Viprasol Tech Private Limited (https://viprasol.com).

Pydantic models shared across the API layer.
"""

from __future__ import annotations

from datetime import datetime
from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


class ItemBase(BaseModel):
    """Fields shared by item create/update/read models."""

    name: str = Field(min_length=1, max_length=120)
    description: str | None = Field(default=None, max_length=2000)
    price: float = Field(ge=0)


class ItemCreate(ItemBase):
    """Payload for creating an item."""


class ItemUpdate(BaseModel):
    """Payload for partially updating an item."""

    name: str | None = Field(default=None, min_length=1, max_length=120)
    description: str | None = Field(default=None, max_length=2000)
    price: float | None = Field(default=None, ge=0)


class Item(ItemBase):
    """An item as returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


class Page(BaseModel, Generic[T]):
    """A paginated collection of resources."""

    items: list[T]
    total: int
    page: int
    size: int


class HealthStatus(BaseModel):
    """Health/readiness response."""

    status: str
    service: str
    version: str


class ErrorResponse(BaseModel):
    """Uniform error envelope."""

    detail: str
