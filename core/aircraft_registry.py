"""Discovery and loading of aircraft configurations.

Only aircraft listed under ``active`` in ``aircraft/registry.json`` are served
by the platform. Legacy aircraft (e.g. the Jet Drone) keep their own files and
schema and are intentionally not loaded here.
"""

from __future__ import annotations

import json
import os
from functools import lru_cache
from pathlib import Path

from core.models import AircraftConfig, AircraftSummary


def project_root() -> Path:
    override = os.environ.get("AEROTWIN_ROOT")
    return Path(override).resolve() if override else Path(__file__).resolve().parents[1]


def aircraft_dir() -> Path:
    return project_root() / "aircraft"


class AircraftNotFoundError(KeyError):
    pass


def _registry() -> dict:
    return json.loads((aircraft_dir() / "registry.json").read_text(encoding="utf-8"))


def active_aircraft_ids() -> list[str]:
    return list(_registry()["active"])


def config_path(aircraft_id: str) -> Path:
    return aircraft_dir() / aircraft_id / "config" / "aircraft_config.json"


@lru_cache(maxsize=None)
def load_aircraft(aircraft_id: str) -> AircraftConfig:
    if aircraft_id not in active_aircraft_ids():
        raise AircraftNotFoundError(aircraft_id)
    data = json.loads(config_path(aircraft_id).read_text(encoding="utf-8"))
    config = AircraftConfig.model_validate(data)
    if config.aircraft_id != aircraft_id:
        raise ValueError(f"{config_path(aircraft_id)} declares aircraft_id {config.aircraft_id!r}")
    return config


def summarize(config: AircraftConfig) -> AircraftSummary:
    geometry_file = config.geometry_model.file
    return AircraftSummary(
        aircraft_id=config.aircraft_id,
        name=config.name,
        category=config.category,
        flight_dynamics_model=(
            config.flight_dynamics_model.model_name if config.flight_dynamics_model else None
        ),
        geometry_model_available=bool(
            geometry_file and (aircraft_dir() / config.aircraft_id / geometry_file).is_file()
        ),
    )


def list_aircraft() -> list[AircraftSummary]:
    return [summarize(load_aircraft(aircraft_id)) for aircraft_id in active_aircraft_ids()]
