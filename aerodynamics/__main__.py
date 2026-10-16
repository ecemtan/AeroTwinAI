"""python -m aerodynamics check  -- report OpenVSP/VSPAERO and geometry readiness."""

from __future__ import annotations

import sys

from aerodynamics.service import readiness
from aerodynamics.vsp_env import openvsp_status


def main() -> int:
    if sys.argv[1:] != ["check"]:
        print("usage: python -m aerodynamics check", file=sys.stderr)
        return 2
    print(openvsp_status().model_dump_json(indent=2))
    problems = readiness("c172")
    if problems:
        print("\nc172 aerodynamic analysis NOT ready:")
        for problem in problems:
            print(f"  - {problem}")
        return 1
    print("\nc172 aerodynamic analysis prerequisites are present.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
