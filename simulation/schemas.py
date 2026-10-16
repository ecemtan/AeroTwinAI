"""Simulation data contract (SI units, radians).

Attitude angles are 3-2-1 Euler angles from NED to BODY (see core/frames.py).
Altitude is above mean sea level.
"""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class InitialConditions(BaseModel):
    model_config = ConfigDict(extra="forbid")

    altitude_m: float = Field(914.4, ge=0.0, le=6000.0, description="Altitude MSL [m]")
    true_airspeed_mps: float = Field(51.4, ge=0.0, le=90.0, description="True airspeed [m/s]")
    heading_rad: float = Field(0.0, description="True heading psi [rad]")
    pitch_rad: float = Field(0.0, description="theta [rad]")
    roll_rad: float = Field(0.0, description="phi [rad]")
    latitude_deg: float = Field(0.0, ge=-90.0, le=90.0)
    longitude_deg: float = Field(0.0, ge=-180.0, le=180.0)


class ControlInputs(BaseModel):
    """Constant (open-loop) control positions, normalised as JSBSim expects."""

    model_config = ConfigDict(extra="forbid")

    throttle: float = Field(0.7, ge=0.0, le=1.0)
    mixture: float = Field(1.0, ge=0.0, le=1.0)
    elevator: float = Field(0.0, ge=-1.0, le=1.0)
    aileron: float = Field(0.0, ge=-1.0, le=1.0)
    rudder: float = Field(0.0, ge=-1.0, le=1.0)
    pitch_trim: float = Field(0.0, ge=-1.0, le=1.0)


class SimulationRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    aircraft_id: Literal["c172"] = "c172"
    initial_conditions: InitialConditions = InitialConditions()
    controls: ControlInputs = ControlInputs()
    trim: bool = Field(
        True,
        description="Run JSBSim's steady-level trim first. Trim overrides throttle/elevator.",
    )
    duration_s: float = Field(10.0, gt=0.0, le=600.0)
    output_rate_hz: float = Field(10.0, gt=0.0, le=120.0)


class TelemetrySample(BaseModel):
    t_s: float
    latitude_deg: float
    longitude_deg: float
    altitude_m: float
    true_airspeed_mps: float
    groundspeed_mps: float
    vertical_speed_mps: float
    roll_rad: float
    pitch_rad: float
    heading_rad: float
    p_radps: float
    q_radps: float
    r_radps: float
    alpha_rad: float
    beta_rad: float


class SimulationMetadata(BaseModel):
    run_id: str
    created_at: datetime
    aircraft_id: str
    fdm_engine: Literal["jsbsim"] = "jsbsim"
    fdm_model: str
    fdm_version: str | None
    data_origin: Literal["live_simulation", "replay"]
    """'replay' MUST be shown as such in the UI."""
    integration_dt_s: float
    trimmed: bool
    applied_controls: ControlInputs
    attitude_convention: str = "3-2-1 Euler, NED -> BODY, rad"
    units: str = "SI (m, s, m/s, rad, rad/s)"
    warnings: list[str] = []


class SimulationResult(BaseModel):
    metadata: SimulationMetadata
    request: SimulationRequest
    samples: list[TelemetrySample]
