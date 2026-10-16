# Cessna 172 — aircraft data

Active reference aircraft of AeroTwin AI.

| Path | Content | Status |
|---|---|---|
| `config/aircraft_config.json` | Parameters with provenance (schema: `core/models.py`) | in use |
| `geometry/` | OpenVSP model (`.vsp3`) and viewer export (`.glb`) | **not created yet** |
| JSBSim model | `c172p`, bundled with the `jsbsim` pip package (`python -m simulation check`) | in use |

## Variant policy

- Flight dynamics: JSBSim **c172p** (Cessna 172P). The model header says it was
  built from public data, textbooks and guesses, for educational use. Its values
  are stored with status `reference_model`, not `verified`.
- Geometry: the OpenVSP model will be built by the project lead. If it represents
  another variant (e.g. 172S), list every difference below before comparing
  VSPAERO results with JSBSim.
- `aircraft/jetdrone/geometry/processed/jetDrone.vsp3` is an OpenVSP default
  placeholder (18 m span, 30° sweep). It is **not** a Cessna model and must not be used.

## Data status rules

| Status | Meaning |
|---|---|
| `verified` | Checked by the team against a primary source (POH, measurement). |
| `reference_model` | Copied from a third-party model (JSBSim). Cross-checked automatically by `python -m validation.jsbsim_reference_check`. |
| `unverified` | From literature; check before relying on it. |
| `missing` | Unknown; value is `null`. Never fill with a guess. |

To promote a value to `verified`, add the primary source to `sources`, cite the
page/section in `locator`, and get the change reviewed in a pull request.

## Known variant differences

_None recorded yet (no OpenVSP geometry exists)._
