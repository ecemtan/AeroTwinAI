# AeroTwin AI
### AI-Powered Aerospace Engineering & Digital Twin Platform

**From Aircraft Geometry to Intelligent Engineering Decisions.**

AeroTwin AI connects parametric aircraft geometry, aerodynamic analysis, flight dynamics
simulation, a simulation-based virtual twin, engineering validation and (later) AI-assisted
analysis in one modular platform. The goal is a computable, traceable and verifiable link
between an aircraft's geometry, physical properties, aerodynamic behaviour and flight performance.

> **Status:** Active development — MVP v0.1
> **Reference aircraft:** Cessna 172
> **First demo:** November 15, 2026

---

## Quick start (Windows · PowerShell)

Full instructions and troubleshooting: [docs/SETUP.md](docs/SETUP.md).

```powershell
git clone https://github.com/ecemtan/AeroTwinAI.git
cd AeroTwinAI
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
Copy-Item .env.example .env
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --reload --port 8000
```

In a second terminal:

```powershell
cd frontend
npm ci
npm run dev        # http://localhost:5173
```

## What works today

| Module | State |
|---|---|
| `core/` — SI unit layer, coordinate frames, sourced data model, aircraft registry | working, tested |
| `aircraft/c172/` — configuration traced to JSBSim `c172p`, each value tagged with its status | working; OpenVSP geometry **not built yet** |
| `simulation/` — JSBSim `c172p` discovery and headless trimmed run (`python -m simulation run`) | working, tested |
| `backend/` — FastAPI: `GET /health`, `GET /api/aircraft`, `GET /api/aircraft/{id}` | working, tested |
| `frontend/` — React + TypeScript + Vite dashboard, Three.js viewer skeleton | builds; shows live backend data only |
| `aerodynamics/` — OpenVSP/VSPAERO detection and service skeleton | refuses to run until VSPAERO and a Cessna geometry exist |
| `validation/` — config vs JSBSim cross-check (`python -m validation.jsbsim_reference_check`) | working |

The API contract is in [docs/API_CONTRACT.md](docs/API_CONTRACT.md) and the team plan in [docs/TEAM_TASKS.md](docs/TEAM_TASKS.md).

## First demo scope (Nov 15, 2026)

1. The web app opens and the user selects the Cessna 172.
2. The 3D aircraft model is displayed.
3. The user picks a flight scenario; JSBSim computes the flight dynamics.
4. Speed, altitude and attitude are plotted and the 3D model follows the telemetry.
5. VSPAERO aerodynamic results are shown as charts.
6. The user reviews analysis and simulation results.

Real-time control input, AI model training, physical sensor links, CFD and fully coupled
aerodynamics–flight dynamics are out of scope for the first demo. Pre-recorded simulation
data is always labelled as a replay.

## Architecture

```text
User ─▶ React dashboard (Three.js) ─▶ FastAPI backend
                                        ├─ Aircraft configuration ─▶ core / aircraft/
                                        ├─ Aerodynamic analysis    ─▶ OpenVSP / VSPAERO
                                        ├─ Flight simulation       ─▶ JSBSim (c172p)
                                        └─ Validation              ─▶ reference data, numerical tests
```

Details, frames and units: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

**Architectural rule:** VSPAERO and JSBSim use different physical models. Their results are
compared, never silently treated as one model. The OpenVSP geometry variant is not assumed to
match the JSBSim `c172p` (172P) model; differences are documented in
[aircraft/c172/README.md](aircraft/c172/README.md).

## Technology stack

| Layer | Technologies |
|---|---|
| Language | Python 3.12, TypeScript |
| Backend | FastAPI, Pydantic |
| Frontend | React, Vite, Three.js |
| Aerodynamics | OpenVSP, VSPAERO, NumPy, SciPy |
| Flight dynamics | JSBSim |
| Tests | pytest, oxlint, TypeScript compiler |
| Later | scikit-learn / PyTorch (AI work package), PostgreSQL, Docker |

## Repository structure

```text
AeroTwinAI/
├── core/                  # Shared models, SI units, coordinate frames, aircraft registry
├── aircraft/
│   ├── registry.json      # Active vs legacy aircraft
│   ├── c172/              # Active reference aircraft
│   └── jetdrone/          # Legacy Jet Drone work (preserved)
├── aerodynamics/          # OpenVSP/VSPAERO service (+ legacy Jet Drone mesh scripts)
├── simulation/            # JSBSim runner, scenarios, telemetry
├── validation/            # Reference comparisons
├── backend/               # FastAPI application
├── frontend/              # React dashboard
├── ai/                    # Reserved for the post-demo AI work package
├── tests/                 # pytest suite
└── docs/                  # Setup, architecture, API contract, team tasks
```

## Team

| Role | Area |
|---|---|
| Project lead | Architecture, Cessna geometry, OpenVSP/VSPAERO, validation, integration |
| Student 1 | Backend — FastAPI, data models, services, result management |
| Student 2 | Frontend — React, Three.js viewer, dashboard, charts |
| Student 3 | Flight simulation — JSBSim, scenarios, telemetry, simulation tests |

Branch and pull request rules: [CONTRIBUTING.md](CONTRIBUTING.md).

## Engineering principles

1. **Physics before prediction** — physics-based computation first, AI estimation second.
2. **Validation before claims** — unvalidated computations are not presented as reliable results.
3. **Modular architecture** — every module is developed and tested independently.
4. **Reproducibility** — the same inputs reproduce the same analysis.
5. **Traceability** — sources, units, assumptions and model versions are recorded.
6. **No fabricated engineering data** — missing parameters and results stay missing.
7. **Safe development** — changes are tested and merged through reviewed pull requests.

## Legacy: GAYRETLİ Jet Drone

The project started with the GAYRETLİ Jet Drone, an EDF VTOL UAV from an Istanbul Gelişim
University research project. That geometry work (CATIA-derived STL inspection and the
CATIA → OpenVSP coordinate transform) is preserved under `aircraft/jetdrone/` and the mesh
scripts in `aerodynamics/`, but it is not part of the active platform. See
[aircraft/jetdrone/README.md](aircraft/jetdrone/README.md). Original CAD files are not
included in the repository.

## Limitations

AeroTwin AI is not a certified flight dynamics environment, an airworthiness assessment
system or a substitute for flight testing. The first release is a **simulation-based virtual
twin**; it is not synchronised with a physical aircraft.

---

GitHub: https://github.com/ecemtan/AeroTwinAI
