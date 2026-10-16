from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel

from aerodynamics.vsp_env import OpenVSPStatus, openvsp_status
from backend.app import API_VERSION
from core.aircraft_registry import list_aircraft
from simulation.jsbsim_env import JSBSimStatus, jsbsim_status

router = APIRouter(tags=["health"])


class AircraftRegistryStatus(BaseModel):
    available: bool
    aircraft_ids: list[str] = []
    error: str | None = None


class ModuleStatus(BaseModel):
    aircraft_registry: AircraftRegistryStatus
    jsbsim: JSBSimStatus
    openvsp: OpenVSPStatus


class HealthResponse(BaseModel):
    status: Literal["ok", "degraded"]
    """'ok' only when every module is available; the API itself is up either way."""
    api_version: str
    timestamp: datetime
    modules: ModuleStatus


def _registry_status() -> AircraftRegistryStatus:
    try:
        ids = [a.aircraft_id for a in list_aircraft()]
    except Exception as exc:  # report, never crash the health check
        return AircraftRegistryStatus(available=False, error=f"{type(exc).__name__}: {exc}")
    return AircraftRegistryStatus(available=True, aircraft_ids=ids)


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    modules = ModuleStatus(
        aircraft_registry=_registry_status(),
        jsbsim=jsbsim_status(),
        openvsp=openvsp_status(),
    )
    all_ok = modules.aircraft_registry.available and modules.jsbsim.available and modules.openvsp.available
    return HealthResponse(
        status="ok" if all_ok else "degraded",
        api_version=API_VERSION,
        timestamp=datetime.now(timezone.utc),
        modules=modules,
    )
