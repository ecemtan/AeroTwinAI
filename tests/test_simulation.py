import math

import pytest

from simulation.jsbsim_env import JSBSimUnavailableError, jsbsim_status
from simulation.runner import run_simulation
from simulation.schemas import InitialConditions, SimulationRequest

STATUS = jsbsim_status()
requires_jsbsim = pytest.mark.skipif(not STATUS.available, reason=f"JSBSim unavailable: {STATUS.error}")


def test_status_is_structured():
    assert isinstance(STATUS.available, bool)
    if not STATUS.available:
        assert STATUS.error


def test_unavailable_jsbsim_is_reported_not_faked(monkeypatch):
    monkeypatch.setenv("JSBSIM_ROOT", "Z:/definitely/not/here")
    assert jsbsim_status().available is False
    with pytest.raises(JSBSimUnavailableError):
        run_simulation(SimulationRequest(duration_s=1.0))


@pytest.mark.jsbsim
@requires_jsbsim
def test_c172p_model_found():
    assert STATUS.models == {"c172p": True}


@pytest.mark.jsbsim
@requires_jsbsim
def test_trimmed_cruise_holds_state():
    ic = InitialConditions(altitude_m=1000.0, true_airspeed_mps=50.0, heading_rad=math.radians(90))
    result = run_simulation(SimulationRequest(initial_conditions=ic, duration_s=5.0, output_rate_hz=10.0))

    assert result.metadata.data_origin == "live_simulation"
    assert result.metadata.fdm_model == "c172p"
    assert len(result.samples) == 51
    assert result.samples[-1].t_s == pytest.approx(5.0, abs=0.01)

    times = [s.t_s for s in result.samples]
    assert times == sorted(times)
    for sample in result.samples:
        for value in sample.model_dump().values():
            assert math.isfinite(value)

    # A converged steady-level trim should barely move in 5 s.
    end = result.samples[-1]
    assert end.altitude_m == pytest.approx(1000.0, abs=5.0)
    assert end.true_airspeed_mps == pytest.approx(50.0, abs=1.0)
    assert end.heading_rad == pytest.approx(math.radians(90), abs=math.radians(1))
    assert 0.0 < result.metadata.applied_controls.throttle <= 1.0
