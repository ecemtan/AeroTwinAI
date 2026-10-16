"""Locate OpenVSP (Python API) and the VSPAERO solver.

OpenVSP is not distributed on PyPI. Install it from https://openvsp.org and
point AeroTwin at it with environment variables (see .env.example):

    OPENVSP_ROOT   folder that contains vsp(.exe), vspaero(.exe), vspscript(.exe)
    VSPAERO_EXE    full path to vspaero(.exe); overrides OPENVSP_ROOT

The ``openvsp`` Python module is optional for the first milestone: VSPAERO
can be driven through its command-line executables.
"""

from __future__ import annotations

import importlib.util
import os
import shutil
from pathlib import Path

from pydantic import BaseModel


class OpenVSPStatus(BaseModel):
    python_api_available: bool
    vspaero_path: str | None
    vspscript_path: str | None
    available: bool
    """True when VSPAERO can be executed (minimum for running an analysis)."""
    error: str | None = None


def _find_executable(name: str, env_var: str | None = None) -> Path | None:
    if env_var and os.environ.get(env_var):
        candidate = Path(os.environ[env_var])
        return candidate if candidate.is_file() else None
    root = os.environ.get("OPENVSP_ROOT")
    if root:
        for suffix in (".exe", ""):
            candidate = Path(root) / f"{name}{suffix}"
            if candidate.is_file():
                return candidate
    found = shutil.which(name)
    return Path(found) if found else None


def openvsp_status() -> OpenVSPStatus:
    vspaero = _find_executable("vspaero", "VSPAERO_EXE")
    vspscript = _find_executable("vspscript")
    python_api = importlib.util.find_spec("openvsp") is not None
    error = None
    if vspaero is None:
        error = (
            "VSPAERO executable not found. Install OpenVSP and set OPENVSP_ROOT or "
            "VSPAERO_EXE (see docs/SETUP.md)."
        )
    return OpenVSPStatus(
        python_api_available=python_api,
        vspaero_path=str(vspaero) if vspaero else None,
        vspscript_path=str(vspscript) if vspscript else None,
        available=vspaero is not None,
        error=error,
    )
