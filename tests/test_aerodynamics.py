import pytest

from aerodynamics.schemas import AlphaSweepRequest
from aerodynamics.service import AerodynamicsUnavailableError, readiness, run_alpha_sweep
from aerodynamics.vsp_env import openvsp_status


def test_status_is_structured():
    status = openvsp_status()
    assert status.available == (status.vspaero_path is not None)
    if not status.available:
        assert status.error


def test_missing_geometry_blocks_analysis():
    problems = readiness("c172")
    assert any("No OpenVSP geometry" in p for p in problems)


def test_sweep_raises_instead_of_returning_fake_numbers():
    with pytest.raises(AerodynamicsUnavailableError):
        run_alpha_sweep(AlphaSweepRequest())


def test_vspaero_env_override(monkeypatch, tmp_path):
    fake = tmp_path / "vspaero.exe"
    fake.write_bytes(b"")
    monkeypatch.setenv("VSPAERO_EXE", str(fake))
    assert openvsp_status().vspaero_path == str(fake)
    monkeypatch.setenv("VSPAERO_EXE", str(tmp_path / "missing.exe"))
    assert openvsp_status().available is False
