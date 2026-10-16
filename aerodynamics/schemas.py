"""Aerodynamic analysis data contract (SI units, radians).

Coefficients are non-dimensional and must be reported together with the
reference area, span and chord that were used to compute them.
"""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class AlphaSweepRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    aircraft_id: Literal["c172"] = "c172"
    alpha_start_rad: float = Field(-0.0873, ge=-0.35, le=0.35)
    alpha_end_rad: float = Field(0.2618, ge=-0.35, le=0.35)
    alpha_count: int = Field(9, ge=2, le=50)
    mach: float = Field(0.15, ge=0.0, le=0.6)
    reynolds: float | None = Field(None, gt=0.0, description="Based on reference chord")
    beta_rad: float = 0.0


class CoefficientPoint(BaseModel):
    alpha_rad: float
    CL: float
    CDi: float | None = None
    CDtot: float | None = None
    CMy: float | None = None


class AeroReferenceValues(BaseModel):
    area_m2: float
    span_m: float
    chord_m: float
    moment_reference_point_m: tuple[float, float, float]
    frame: Literal["openvsp"] = "openvsp"


class AlphaSweepResult(BaseModel):
    run_id: str
    created_at: datetime
    solver: Literal["vspaero"] = "vspaero"
    solver_version: str | None
    geometry_file: str
    geometry_sha256: str
    data_origin: Literal["live_analysis", "cached"]
    request: AlphaSweepRequest
    reference: AeroReferenceValues
    points: list[CoefficientPoint]
    validation_status: Literal["unvalidated", "compared", "validated"] = "unvalidated"
    warnings: list[str] = []
