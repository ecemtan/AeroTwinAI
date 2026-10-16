"""FastAPI application.

    uvicorn backend.app.main:app --reload --port 8000
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app import API_VERSION
from backend.app.routers import aircraft, health
from backend.app.settings import get_settings


def create_app() -> FastAPI:
    app = FastAPI(
        title="AeroTwin AI API",
        version=API_VERSION,
        description="Aircraft configuration, aerodynamic analysis and flight simulation services.",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=get_settings().cors_origins,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(health.router)
    app.include_router(aircraft.router, prefix="/api")
    return app


app = create_app()
