"""Command line entry point.

    python -m simulation check                 # is JSBSim + c172p available?
    python -m simulation run --duration 10     # headless trimmed cruise run
    python -m simulation run --out run.json    # save full SimulationResult
"""

from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

from simulation.jsbsim_env import JSBSimUnavailableError, jsbsim_status
from simulation.runner import SimulationError, run_simulation
from simulation.schemas import SimulationRequest


def _check() -> int:
    status = jsbsim_status()
    print(status.model_dump_json(indent=2))
    return 0 if status.available else 1


def _run(args: argparse.Namespace) -> int:
    request = SimulationRequest(duration_s=args.duration, trim=not args.no_trim)
    try:
        result = run_simulation(request)
    except (JSBSimUnavailableError, SimulationError) as exc:
        print(f"SIMULATION NOT RUN: {exc}", file=sys.stderr)
        return 1
    first, last = result.samples[0], result.samples[-1]
    print(f"run_id={result.metadata.run_id} origin={result.metadata.data_origin} "
          f"model={result.metadata.fdm_model} jsbsim={result.metadata.fdm_version}")
    print(f"samples={len(result.samples)} dt={result.metadata.integration_dt_s:.5f} s")
    for label, s in (("start", first), ("end", last)):
        print(f"{label:>5}: t={s.t_s:7.2f} s  alt={s.altitude_m:8.1f} m  "
              f"TAS={s.true_airspeed_mps:6.2f} m/s  pitch={math.degrees(s.pitch_rad):6.2f} deg  "
              f"heading={math.degrees(s.heading_rad):7.2f} deg")
    for warning in result.metadata.warnings:
        print(f"warning: {warning}")
    if args.out:
        Path(args.out).write_text(result.model_dump_json(indent=2), encoding="utf-8")
        print(f"saved: {args.out}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m simulation")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("check", help="Report JSBSim and c172p availability")
    run = sub.add_parser("run", help="Run a headless c172p simulation")
    run.add_argument("--duration", type=float, default=10.0)
    run.add_argument("--no-trim", action="store_true")
    run.add_argument("--out", help="Write the SimulationResult JSON to this file")
    args = parser.parse_args(argv)
    return _check() if args.command == "check" else _run(args)


if __name__ == "__main__":
    sys.exit(main())
