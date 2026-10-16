"""Aerodynamic analysis service (skeleton).

Pipeline to implement (project lead, weeks 1-2):
    1. Build the Cessna OpenVSP model -> aircraft/c172/geometry/<file>.vsp3
       and record it in aircraft_config.json:geometry_model.file
    2. Generate the VSPAERO inputs (DegenGeom + .vspaero settings)
    3. Run vspaero.exe as a subprocess in a per-run folder under data/runs/
    4. Parse the .polar output into CoefficientPoint values
    5. Return AlphaSweepResult (with geometry hash and reference values)

Until each prerequisite exists this module raises explicit errors instead of
returning placeholder numbers.
"""

from __future__ import annotations

from aerodynamics.schemas import AlphaSweepRequest, AlphaSweepResult
from aerodynamics.vsp_env import openvsp_status
from core.aircraft_registry import aircraft_dir, load_aircraft


class AerodynamicsUnavailableError(RuntimeError):
    """A prerequisite (solver, geometry) is missing; no analysis was run."""


def readiness(aircraft_id: str = "c172") -> list[str]:
    """Return the list of blocking problems. Empty list == ready to run."""
    problems: list[str] = []
    status = openvsp_status()
    if not status.available:
        problems.append(status.error or "VSPAERO unavailable")
    config = load_aircraft(aircraft_id)
    geometry_file = config.geometry_model.file
    if geometry_file is None:
        problems.append(f"No OpenVSP geometry registered for {aircraft_id!r} (geometry_model.file is null).")
    elif not (aircraft_dir() / aircraft_id / geometry_file).is_file():
        problems.append(f"Geometry file not found: aircraft/{aircraft_id}/{geometry_file}")
    return problems


def run_alpha_sweep(request: AlphaSweepRequest) -> AlphaSweepResult:
    problems = readiness(request.aircraft_id)
    if problems:
        raise AerodynamicsUnavailableError("; ".join(problems))
    raise NotImplementedError(
        "VSPAERO alpha sweep is not implemented yet (see module docstring)."
    )
