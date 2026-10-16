import math

import pytest

from core import units


def test_exact_length_definitions():
    assert units.ft_to_m(1.0) == 0.3048
    assert units.in_to_m(12.0) == pytest.approx(0.3048, rel=1e-15)
    assert units.kt_to_mps(1.0) == pytest.approx(1852.0 / 3600.0, rel=1e-15)


def test_slug_is_lbf_s2_per_ft():
    # 1 slug accelerated at 1 ft/s^2 needs 1 lbf
    assert units.slug_to_kg(1.0) * units.M_PER_FT == pytest.approx(units.lbf_to_n(1.0), rel=1e-12)
    assert units.slug_to_kg(1.0) == pytest.approx(14.593903, rel=1e-6)


@pytest.mark.parametrize(
    ("forward", "backward", "value"),
    [
        (units.ft_to_m, units.m_to_ft, 3000.0),
        (units.in_to_m, units.m_to_in, 41.0),
        (units.lbm_to_kg, units.kg_to_lbm, 2400.0),
        (units.kt_to_mps, units.mps_to_kt, 100.0),
        (units.fps_to_mps, units.mps_to_fps, 168.78),
        (units.deg_to_rad, units.rad_to_deg, 15.0),
    ],
)
def test_round_trip(forward, backward, value):
    assert backward(forward(value)) == pytest.approx(value, rel=1e-12)


def test_to_si_generic():
    assert units.to_si(174.0, "ft2") == (pytest.approx(16.16512896), "m2")
    value, unit = units.to_si(180.0, "deg")
    assert unit == "rad" and value == pytest.approx(math.pi)
    with pytest.raises(ValueError):
        units.to_si(1.0, "furlong")
