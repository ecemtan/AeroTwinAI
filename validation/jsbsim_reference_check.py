"""Cross-check aircraft_config.json values against the installed JSBSim files.

Every config value with status ``reference_model`` must match the JSBSim XML it
cites. This keeps the configuration traceable: if JSBSim (or the config) is
changed, this check fails instead of silently drifting.

    python -m validation.jsbsim_reference_check
"""

from __future__ import annotations

import math
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from pydantic import BaseModel

from core.aircraft_registry import load_aircraft
from core.models import DataStatus
from core.units import to_si
from simulation.jsbsim_env import root_dir

AIRCRAFT_XML = "aircraft/c172p/c172p.xml"
ENGINE_XML = "engine/eng_io320.xml"
PROP_XML = "engine/prop_75in2f.xml"

XML_UNITS = {"FT2": "ft2", "FT": "ft", "IN": "in", "LBS": "lbm", "SLUG*FT2": "slug*ft2"}

# (section, key) -> (file, element path, unit attribute owner path or fixed unit)
NUMERIC_CHECKS: dict[tuple[str, str], tuple[str, str, str]] = {
    ("geometry", "wing_area"): (AIRCRAFT_XML, "metrics/wingarea", "@"),
    ("geometry", "wing_span"): (AIRCRAFT_XML, "metrics/wingspan", "@"),
    ("geometry", "mean_aerodynamic_chord"): (AIRCRAFT_XML, "metrics/chord", "@"),
    ("geometry", "htail_area"): (AIRCRAFT_XML, "metrics/htailarea", "@"),
    ("geometry", "htail_arm"): (AIRCRAFT_XML, "metrics/htailarm", "@"),
    ("geometry", "vtail_area"): (AIRCRAFT_XML, "metrics/vtailarea", "@"),
    ("geometry", "aero_reference_point_x"): (AIRCRAFT_XML, "metrics/location[@name='AERORP']/x", "parent"),
    ("geometry", "aero_reference_point_z"): (AIRCRAFT_XML, "metrics/location[@name='AERORP']/z", "parent"),
    ("mass_properties", "empty_mass"): (AIRCRAFT_XML, "mass_balance/emptywt", "@"),
    ("mass_properties", "cg_x"): (AIRCRAFT_XML, "mass_balance/location[@name='CG']/x", "parent"),
    ("mass_properties", "cg_z"): (AIRCRAFT_XML, "mass_balance/location[@name='CG']/z", "parent"),
    ("mass_properties", "ixx"): (AIRCRAFT_XML, "mass_balance/ixx", "@"),
    ("mass_properties", "iyy"): (AIRCRAFT_XML, "mass_balance/iyy", "@"),
    ("mass_properties", "izz"): (AIRCRAFT_XML, "mass_balance/izz", "@"),
    ("propulsion", "max_power"): (ENGINE_XML, "maxhp", "hp"),
    ("propulsion", "propeller_diameter"): (PROP_XML, "diameter", "@"),
}


class CheckResult(BaseModel):
    key: str
    config_value: float | str | None
    model_value: float | str | None
    unit: str | None
    ok: bool
    message: str | None = None


def _read_numeric(root: Path, file: str, path: str, unit_rule: str) -> tuple[float, str]:
    tree = ET.parse(root / file).getroot()
    element = tree.find(path)
    if element is None or element.text is None:
        raise LookupError(f"{file}: element {path!r} not found")
    if unit_rule == "@":
        unit = XML_UNITS[element.attrib["unit"]]
    elif unit_rule == "parent":
        parent = tree.find(path.rsplit("/", 1)[0])
        unit = XML_UNITS[parent.attrib["unit"]]
    else:
        unit = unit_rule
    return to_si(float(element.text), unit)


def _fuel_capacity(root: Path) -> tuple[float, str]:
    tree = ET.parse(root / AIRCRAFT_XML).getroot()
    total = 0.0
    for capacity in tree.findall("propulsion/tank/capacity"):
        total += to_si(float(capacity.text), XML_UNITS[capacity.attrib["unit"]])[0]
    return total, "kg"


def run_checks(aircraft_id: str = "c172") -> list[CheckResult]:
    config = load_aircraft(aircraft_id)
    root = root_dir()
    results: list[CheckResult] = []

    for (section, key), (file, path, unit_rule) in NUMERIC_CHECKS.items():
        item = getattr(config, section)[key]
        model_value, unit = _read_numeric(root, file, path, unit_rule)
        ok = (
            item.status is DataStatus.REFERENCE_MODEL
            and isinstance(item.value, float)
            and item.unit == unit
            and math.isclose(item.value, model_value, rel_tol=1e-9)
        )
        results.append(CheckResult(key=f"{section}.{key}", config_value=item.value,
                                   model_value=model_value, unit=unit, ok=ok))

    fuel = config.propulsion["fuel_capacity_total"]
    model_fuel, unit = _fuel_capacity(root)
    results.append(CheckResult(
        key="propulsion.fuel_capacity_total", config_value=fuel.value, model_value=model_fuel,
        unit=unit, ok=isinstance(fuel.value, float) and math.isclose(fuel.value, model_fuel, rel_tol=1e-9),
    ))

    engine = config.propulsion["engine_model"]
    engine_file = ET.parse(root / AIRCRAFT_XML).getroot().find("propulsion/engine").attrib["file"]
    results.append(CheckResult(key="propulsion.engine_model", config_value=engine.value,
                               model_value=engine_file, unit=None, ok=engine.value == engine_file))

    # Any reference_model value without a check is a traceability gap.
    checked = {r.key for r in results}
    for section in ("geometry", "mass_properties", "propulsion"):
        for key, item in getattr(config, section).items():
            name = f"{section}.{key}"
            if item.status is DataStatus.REFERENCE_MODEL and name not in checked:
                results.append(CheckResult(key=name, config_value=item.value, model_value=None,
                                           unit=item.unit, ok=False,
                                           message="reference_model value has no automated check"))
    return results


def main() -> int:
    results = run_checks()
    for r in results:
        flag = "OK  " if r.ok else "FAIL"
        print(f"{flag} {r.key:42s} config={r.config_value!s:>22} jsbsim={r.model_value!s:>22} {r.unit or ''}"
              + (f"  ({r.message})" if r.message else ""))
    failed = [r for r in results if not r.ok]
    print(f"\n{len(results) - len(failed)}/{len(results)} checks passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
