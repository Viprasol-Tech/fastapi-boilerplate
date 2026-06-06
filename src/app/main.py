"""Part of FastAPI Boilerplate by Viprasol Tech Private Limited (https://viprasol.com).

Application factory.

:func:`create_app` wires together configuration, logging, CORS, exception
handlers, health/readiness endpoints and the versioned API router.
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import __version__
from app.api.v1 import api_router
from app.config import Settings, get_settings
from app.errors import register_exception_handlers
from app.logging import configure_logging, get_logger
from app.schemas import HealthStatus

logger = get_logger("app.main")


def create_app(settings: Settings | None = None) -> FastAPI:
    """Build and return a configured :class:`~fastapi.FastAPI` application."""
    settings = settings or get_settings()
    configure_logging()

    app = FastAPI(
        title=settings.app_name,
        version=__version__,
        debug=settings.debug,
        summary="Production-ready FastAPI starter by Viprasol Tech.",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Ensure dependencies that read settings use *this* app's settings instance
    # (important when create_app is called with an explicit Settings in tests).
    app.dependency_overrides[get_settings] = lambda: settings

    register_exception_handlers(app)

    @app.get("/health", response_model=HealthStatus, tags=["meta"])
    def health() -> HealthStatus:
        """Liveness probe — always returns OK if the process is running."""
        return HealthStatus(status="ok", service=settings.app_name, version=__version__)

    @app.get("/ready", response_model=HealthStatus, tags=["meta"])
    def ready() -> HealthStatus:
        """Readiness probe — extend with real dependency checks as needed."""
        return HealthStatus(status="ready", service=settings.app_name, version=__version__)

    app.include_router(api_router, prefix=settings.api_v1_prefix)

    logger.info("Application initialised", extra={"environment": settings.environment})
    return app


app = create_app()
