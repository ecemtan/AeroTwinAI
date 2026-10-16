"""Headless JSBSim runner for the Cessna 172 (c172p).

Runs a fixed-duration, open-loop simulation and returns SI telemetry.
This is the minimal real path; scenarios, streaming and closed-loop control
are built on top of it (see docs/TEAM_TASKS.md, Flight Simulation).
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from core import units
from simulation.jsbsim_env import JSBSimUnavailableError, _import_jsbsim, jsbsim_status, root_dir
from simulation.schemas import (
    ControlInputs,
    SimulationMetadata,
    SimulationRequest,
    SimulationResult,
    TelemetrySample,
)

# AeroTwin aircraft id -> JSBSim model name.
FDM_MODELS = {"c172": "c172p"}


class SimulationError(RuntimeError):
    pass


def _sample(fdm) -> TelemetrySample:
    return TelemetrySample(
        t_s=fdm["simulation/sim-time-sec"],
        latitude_deg=fdm["position/lat-geod-deg"],
        longitude_deg=fdm["position/long-gc-deg"],
        altitude_m=units.ft_to_m(fdm["position/h-sl-ft"]),
        true_airspeed_mps=units.fps_to_mps(fdm["velocities/vtrue-fps"]),
        groundspeed_mps=units.fps_to_mps(fdm["velocities/vg-fps"]),
        vertical_speed_mps=units.fps_to_mps(fdm["velocities/h-dot-fps"]),
        roll_rad=fdm["attitude/phi-rad"],
        pitch_rad=fdm["attitude/theta-rad"],
        heading_rad=fdm["attitude/psi-rad"],
        p_radps=fdm["velocities/p-rad_sec"],
        q_radps=fdm["velocities/q-rad_sec"],
        r_radps=fdm["velocities/r-rad_sec"],
        alpha_rad=fdm["aero/alpha-rad"],
        beta_rad=fdm["aero/beta-rad"],
    )


def _apply_controls(fdm, controls: ControlInputs) -> None:
    fdm["fcs/throttle-cmd-norm"] = controls.throttle
    fdm["fcs/mixture-cmd-norm"] = controls.mixture
    fdm["fcs/elevator-cmd-norm"] = controls.elevator
    fdm["fcs/aileron-cmd-norm"] = controls.aileron
    fdm["fcs/rudder-cmd-norm"] = controls.rudder
    fdm["fcs/pitch-trim-cmd-norm"] = controls.pitch_trim


def _clip(value: float) -> float:
    return max(-1.0, min(1.0, value))


def run_simulation(request: SimulationRequest) -> SimulationResult:
    status = jsbsim_status()
    if not status.available:
        raise JSBSimUnavailableError(status.error or "JSBSim unavailable")

    jsbsim = _import_jsbsim()
    model_name = FDM_MODELS[request.aircraft_id]
    fdm = jsbsim.FGFDMExec(str(root_dir()))
    fdm.set_debug_level(0)
    if not fdm.load_model(model_name):
        raise SimulationError(f"JSBSim could not load model {model_name!r}")

    ic = request.initial_conditions
    fdm["ic/h-sl-ft"] = units.m_to_ft(ic.altitude_m)
    fdm["ic/vt-fps"] = units.mps_to_fps(ic.true_airspeed_mps)
    fdm["ic/psi-true-rad"] = ic.heading_rad
    fdm["ic/theta-rad"] = ic.pitch_rad
    fdm["ic/phi-rad"] = ic.roll_rad
    fdm["ic/lat-geod-deg"] = ic.latitude_deg
    fdm["ic/long-gc-deg"] = ic.longitude_deg
    if not fdm.run_ic():
        raise SimulationError("JSBSim run_ic() failed")

    fdm["propulsion/set-running"] = -1  # start all engines
    _apply_controls(fdm, request.controls)

    warnings: list[str] = []
    if request.trim:
        try:
            fdm["simulation/do_simple_trim"] = 1  # full steady-level trim
        except Exception as exc:  # jsbsim raises TrimFailureError
            raise SimulationError(f"JSBSim trim failed: {exc}") from exc
        warnings.append(
            "Trim set throttle, pitch trim, aileron and rudder; requested control values "
            "were overridden (see applied_controls)."
        )

    applied = ControlInputs(
        throttle=fdm["fcs/throttle-cmd-norm"],
        mixture=fdm["fcs/mixture-cmd-norm"],
        elevator=_clip(fdm["fcs/elevator-cmd-norm"]),
        aileron=_clip(fdm["fcs/aileron-cmd-norm"]),
        rudder=_clip(fdm["fcs/rudder-cmd-norm"]),
        pitch_trim=_clip(fdm["fcs/pitch-trim-cmd-norm"]),
    )

    dt = fdm.get_delta_t()
    steps_per_sample = max(1, round(1.0 / (request.output_rate_hz * dt)))
    start_t = fdm["simulation/sim-time-sec"]
    samples = [_sample(fdm)]
    step = 0
    while fdm["simulation/sim-time-sec"] - start_t < request.duration_s - dt / 2:
        if not fdm.run():
            raise SimulationError(f"JSBSim stopped at t={fdm['simulation/sim-time-sec']:.3f} s")
        step += 1
        if step % steps_per_sample == 0:
            samples.append(_sample(fdm))

    if samples[-1].altitude_m <= 0.0:
        warnings.append("Altitude reached or went below sea level.")

    metadata = SimulationMetadata(
        run_id=uuid.uuid4().hex,
        created_at=datetime.now(timezone.utc),
        aircraft_id=request.aircraft_id,
        fdm_model=model_name,
        fdm_version=status.version,
        data_origin="live_simulation",
        integration_dt_s=dt,
        trimmed=request.trim,
        applied_controls=applied,
        warnings=warnings,
    )
    return SimulationResult(metadata=metadata, request=request, samples=samples)
