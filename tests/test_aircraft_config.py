import pytest
from pydantic import ValidationError

from core.aircraft_registry import AircraftNotFoundError, active_aircraft_ids, list_aircraft, load_aircraft
from core.models import DataStatus, SourcedValue


def test_registry_lists_only_active_c172():
    assert active_aircraft_ids() == ["c172"]
    with pytest.raises(AircraftNotFoundError):
        load_aircraft("jetdrone")  # legacy, intentionally not served


def test_c172_config_loads_and_converts_to_si():
    config = load_aircraft("c172")
    span = config.geometry["wing_span"]
    assert span.unit == "m"
    assert span.value == pytest.approx(35.8 * 0.3048)
    assert config.flight_dynamics_model.model_name == "c172p"


def test_c172_has_no_unbacked_values():
    config = load_aircraft("c172")
    for section in (config.geometry, config.mass_properties, config.propulsion):
        for key, item in section.items():
            if item.status is DataStatus.MISSING:
                assert item.value is None, key
            else:
                assert item.source is not None, key
    # Nothing in the starter config is claimed as team-verified.
    assert not any(
        item.status is DataStatus.VERIFIED
        for section in (config.geometry, config.mass_properties, config.propulsion)
        for item in section.values()
    )


def test_placeholder_openvsp_geometry_is_not_used():
    config = load_aircraft("c172")
    assert config.geometry_model.file is None
    assert config.geometry_model.status is DataStatus.MISSING
    assert list_aircraft()[0].geometry_model_available is False


def test_sourced_value_rules():
    with pytest.raises(ValidationError):
        SourcedValue(status="missing", source_value=1.0, source_unit="m")
    with pytest.raises(ValidationError):
        SourcedValue(status="unverified", source_value=1.0, source_unit="m")  # no source
    with pytest.raises(ValidationError):
        SourcedValue(status="reference_model", source="x", source_value=1.0)  # no unit
    ok = SourcedValue(status="unverified", source="x", source_value="NACA 2412")
    assert ok.value == "NACA 2412" and ok.unit is None
