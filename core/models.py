"""Shared Pydantic data models (the cross-module data contract).

Rule: no engineering value without provenance. Every parameter is a
``SourcedValue`` that records where it came from and how far it can be
trusted. Missing values stay ``None`` with status ``missing``; they are never
filled with guesses.
"""

from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from core.units import to_si

SCHEMA_VERSION = "1.0"


class DataStatus(str, Enum):
    VERIFIED = "verified"
    """Checked by the team against a primary source (e.g. POH, measurement)."""
    REFERENCE_MODEL = "reference_model"
    """Copied from a third-party model (e.g. JSBSim c172p); not independently verified."""
    UNVERIFIED = "unverified"
    """From literature or memory; must be checked before it is relied on."""
    MISSING = "missing"
    """Not known. Value is null."""


class DataSource(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    title: str
    kind: Literal["simulation_model", "document", "literature", "measurement", "derived"]
    locator: str | None = Field(None, description="File path, URL or document section")
    notes: str | None = None


class SourcedValue(BaseModel):
    """A parameter with provenance.

    Numeric values are given in the source's own unit (``source_value`` /
    ``source_unit``); ``value`` / ``unit`` hold the SI conversion and are filled
    automatically.
    """

    model_config = ConfigDict(extra="forbid")

    status: DataStatus
    source: str | None = Field(None, description="DataSource.id")
    source_value: float | str | None = None
    source_unit: str | None = None
    value: float | str | None = None
    unit: str | None = None
    frame: str | None = Field(None, description="core.frames.Frame value for positions")
    note: str | None = None

    @model_validator(mode="after")
    def _normalise(self) -> "SourcedValue":
        if self.status is DataStatus.MISSING:
            if self.source_value is not None or self.value is not None:
                raise ValueError("A 'missing' value must not carry a value")
            return self
        if self.source_value is None:
            raise ValueError(f"Status {self.status.value!r} requires source_value")
        if self.source is None:
            raise ValueError(f"Status {self.status.value!r} requires a source id")
        if isinstance(self.source_value, (int, float)) and not isinstance(self.source_value, bool):
            if self.source_unit is None:
                raise ValueError("Numeric source_value requires source_unit")
            si_value, si_unit = to_si(float(self.source_value), self.source_unit)
            self.value, self.unit = si_value, si_unit
        else:
            self.value, self.unit = self.source_value, None
        return self


class FlightDynamicsModelRef(BaseModel):
    model_config = ConfigDict(extra="forbid")

    engine: Literal["jsbsim"]
    model_name: str
    variant: str
    source: str


class GeometryModelRef(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tool: Literal["openvsp"]
    file: str | None = Field(None, description="Path relative to the aircraft folder")
    variant: str | None = None
    status: DataStatus
    note: str | None = None


class AircraftConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["1.0"]
    aircraft_id: str
    name: str
    category: str
    description: str
    variant_notes: str
    sources: list[DataSource]
    flight_dynamics_model: FlightDynamicsModelRef | None = None
    geometry_model: GeometryModelRef
    geometry: dict[str, SourcedValue]
    mass_properties: dict[str, SourcedValue]
    propulsion: dict[str, SourcedValue]

    @model_validator(mode="after")
    def _check_source_ids(self) -> "AircraftConfig":
        known = {s.id for s in self.sources}
        sections = {
            "geometry": self.geometry,
            "mass_properties": self.mass_properties,
            "propulsion": self.propulsion,
        }
        for section_name, section in sections.items():
            for key, item in section.items():
                if item.source is not None and item.source not in known:
                    raise ValueError(f"{section_name}.{key}: unknown source id {item.source!r}")
        if self.flight_dynamics_model and self.flight_dynamics_model.source not in known:
            raise ValueError("flight_dynamics_model: unknown source id")
        return self


class AircraftSummary(BaseModel):
    aircraft_id: str
    name: str
    category: str
    flight_dynamics_model: str | None
    geometry_model_available: bool
