"""Part of FastAPI Boilerplate by Viprasol Tech Private Limited (https://viprasol.com).

Version 1 of the public API. Aggregates the resource routers under one
:class:`fastapi.APIRouter` mounted at the configured ``/api/v1`` prefix.
"""

from __future__ import annotations

from fastapi import APIRouter

from app.api.v1.items import router as items_router

api_router = APIRouter()
api_router.include_router(items_router)

__all__ = ["api_router"]
