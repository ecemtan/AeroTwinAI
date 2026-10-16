"""Locate JSBSim and its aircraft models without running a simulation."""

from __future__ import annotations

import os
from pathlib import Path

from pydantic import BaseModel

REQUIRED_MODELS = ("c172p",)


class JSBSimStatus(BaseModel):
    available: bool
    version: str | None = None
    root_dir: str | None = None
    models: dict[str, bool] = {}
    error: str | None = None


class JSBSimUnavailableError(RuntimeError):
    pass


def _import_jsbsim():
    try:
        import jsbsim  # noqa: PLC0415 - optional dependency, imported lazily
    except ImportError as exc:
        raise JSBSimUnavailableError(
            "The 'jsbsim' Python package is not installed. Run: pip install -e \".[dev]\""
        ) from exc
    return jsbsim


def root_dir() -> Path:
    """JSBSim data root (contains aircraft/, engine/, systems/).

    ``JSBSIM_ROOT`` overrides the data bundled with the Python package.
    """
    override = os.environ.get("JSBSIM_ROOT")
    if override:
        return Path(override)
    return Path(_import_jsbsim().get_default_root_dir())


def model_file(model_name: str) -> Path:
    return root_dir() / "aircraft" / model_name / f"{model_name}.xml"


def jsbsim_status() -> JSBSimStatus:
    try:
        jsbsim = _import_jsbsim()
        root = root_dir()
    except JSBSimUnavailableError as exc:
        return JSBSimStatus(available=False, error=str(exc))
    models = {name: model_file(name).is_file() for name in REQUIRED_MODELS}
    error = None
    if not root.is_dir():
        error = f"JSBSim root directory not found: {root}"
    elif not all(models.values()):
        missing = ", ".join(name for name, ok in models.items() if not ok)
        error = f"Missing JSBSim aircraft model(s): {missing}"
    return JSBSimStatus(
        available=error is None,
        version=getattr(jsbsim, "__version__", None),
        root_dir=str(root),
        models=models,
        error=error,
    )
