import pytest

from simulation.jsbsim_env import jsbsim_status
from validation.jsbsim_reference_check import run_checks

STATUS = jsbsim_status()


@pytest.mark.jsbsim
@pytest.mark.skipif(not STATUS.available, reason=f"JSBSim unavailable: {STATUS.error}")
def test_c172_config_matches_jsbsim_files():
    failures = [r for r in run_checks("c172") if not r.ok]
    assert failures == []
