from __future__ import annotations

from fastapi import APIRouter, HTTPException

from core.aircraft_registry import AircraftNotFoundError, list_aircraft, load_aircraft
from core.models import AircraftConfig, AircraftSummary

router = APIRouter(prefix="/aircraft", tags=["aircraft"])


@router.get("", response_model=list[AircraftSummary])
def get_aircraft_list() -> list[AircraftSummary]:
    return list_aircraft()


@router.get("/{aircraft_id}", response_model=AircraftConfig)
def get_aircraft(aircraft_id: str) -> AircraftConfig:
    try:
        return load_aircraft(aircraft_id)
    except AircraftNotFoundError:
        raise HTTPException(status_code=404, detail=f"Aircraft {aircraft_id!r} not found") from None
