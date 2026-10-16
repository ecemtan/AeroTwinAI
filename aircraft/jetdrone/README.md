# GAYRETLİ Jet Drone — legacy work (preserved)

Earlier geometry work on the Jet Drone EDF VTOL UAV. It is kept for reference
and is **not** part of the active Cessna 172 platform:

- Not listed as `active` in `aircraft/registry.json`; the API does not serve it.
- `config/*.json` use the earlier, pre-1.0 config format.
- Mesh scripts live in `aerodynamics/` (`geometry_analyzer.py`,
  `coordinate_transform.py`, `visualize_geometry.py`, `inspect_mesh_parts.py`,
  `visualize_mesh_parts.py`, `wing_top_view.py`). They need the original
  `geometry/original/jetDron.stl`, which is git-ignored (confidential CAD data),
  and the optional dependencies: `pip install -e ".[legacy]"`.
- `geometry/processed/jetDrone.vsp3` is an OpenVSP default placeholder, not a
  Jet Drone model.
