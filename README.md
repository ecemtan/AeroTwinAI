# AeroTwin AI
### AI-Powered Aircraft Digital Twin, Aerodynamic Analysis & Flight Simulation Platform

**From Aircraft Geometry to Intelligent Engineering Decisions.**

AeroTwin AI is an AI-assisted aircraft engineering platform designed to connect 3D aircraft geometry, aerodynamic analysis, flight dynamics simulation, engineering validation, and intelligent design optimization within a unified workflow.

The platform aims to help engineers, researchers, and students evaluate aircraft configurations, understand flight performance, identify potential design limitations, and explore improvements supported by physics-based analysis.

> **Project Status:** Active Development — MVP v0.1  
> **Development Start:** October 13, 2026  
> **Initial MVP Target:** November 11, 2026

---

## 1. Project Vision

Traditional aircraft engineering workflows often rely on multiple disconnected tools for CAD modeling, aerodynamic analysis, simulation, and performance evaluation.

AeroTwin AI aims to integrate these processes into an accessible and intelligent engineering environment.

The platform is designed to support:

- Aircraft geometry inspection and parameter extraction
- Aerodynamic performance analysis
- Flight dynamics simulation
- Engineering calculations and validation
- AI-assisted anomaly detection
- Explainable design improvement recommendations
- Design variant comparison and optimization

**Our goal is not simply to simulate aircraft, but to help engineers understand why an aircraft behaves as it does and how its design can be improved.**

## 2. Reference Aircraft — GAYRETLİ Jet Drone

The initial reference aircraft is the **GAYRETLİ Jet Drone**, an electric ducted fan (EDF) vertical take-off and landing (VTOL) unmanned aerial vehicle developed in an Istanbul Gelişim University research project.

The available reference materials include CATIA-derived 3D geometry, STL and 3DXML files, and technical documentation.

The reference aircraft provides a practical case study for developing and evaluating AeroTwin AI's engineering workflows.

### Initial reference parameters

| Parameter | Reference |
|---|---|
| Aircraft category | EDF VTOL UAV |
| Main wing airfoil | NACA 4412 |
| Tail airfoil | NACA 0012 |
| Propulsion configuration | Four tiltable EDF motors |
| CAD source | CATIA-derived 3D model |
| Available geometry | STL, 3DXML |
| Aerodynamic reference | University thesis and engineering calculations |

Some published geometry parameters and calculated values require reconciliation. All unverified parameters will be tracked explicitly rather than treated as validated aircraft specifications.

## 3. System Architecture

```text
Aircraft CAD / Geometry
          |
          v
Geometry Processing & Parameter Extraction
          |
          v
Aerodynamic Analysis (OpenVSP / VSPAERO)
          |
          +-----------------------------+
          |                             |
          v                             v
Engineering Validation           Flight Dynamics
(MATLAB / Python)                (JSBSim / PX4 / Gazebo)
          |                             |
          +--------------+--------------+
                         |
                         v
              Engineering Data Layer
                         |
                         v
               AI Analysis Engine
                         |
                         v
        Diagnosis / Recommendations / Optimization
                         |
                         v
              Physics-Based Revalidation
                         |
                         v
                 AeroTwin AI Dashboard
```

The architecture is modular and intended to support additional aircraft types beyond the initial Jet Drone reference model.

## 4. Technology Stack

| Layer | Technologies |
|---|---|
| Programming | Python, TypeScript |
| Backend | FastAPI |
| Frontend | React |
| CAD and geometry | CATIA source data, OpenVSP |
| Aerodynamics | VSPAERO |
| Flight simulation | JSBSim, PX4, Gazebo |
| Engineering validation | MATLAB, Simulink |
| AI and optimization | Python, NumPy, SciPy, Optuna |
| Data storage | JSON, CSV; PostgreSQL planned |
| Development | Git, GitHub, VS Code |
| Deployment | Docker planned |

Technologies listed above represent the planned architecture. Individual integrations will be implemented and validated incrementally.

## 5. AI Engineering Assistant

The AI module is intended to assist with engineering interpretation rather than replace physical validation.

Planned capabilities include:

**Performance Analysis:** Interpret lift, drag, stability, flight speed, and energy-related outputs.

**Anomaly Detection:** Identify inconsistent geometry, unusual simulation results, and potential design issues.

**Explainable Recommendations:** Produce engineering suggestions with supporting calculations, assumptions, and evidence.

**Design Optimization:** Explore selected geometry parameters and compare candidate configurations.

**Revalidation:** Re-run applicable physics-based analyses before reporting whether an improvement is supported.

AI-generated recommendations will be identified as hypotheses until supported by appropriate analysis or testing.

## 6. Repository Structure

```text
AeroTwinAI/
├── docs/                  # Documentation and architecture
├── aircraft/
│   └── jetdrone/
│       ├── geometry/      # Processed aircraft geometry
│       └── config/        # Aircraft parameters
├── aerodynamics/          # OpenVSP and VSPAERO
├── simulation/            # JSBSim, PX4 and Gazebo
├── validation/            # MATLAB and physics checks
├── ai/                    # AI analysis and optimization
├── backend/               # FastAPI services
├── frontend/              # React dashboard
└── tests/                 # Automated tests
```

Original CAD files, proprietary models, large simulation outputs, and confidential engineering data are not included in the repository by default.

## 7. Development Roadmap

| Phase | Period | Deliverable |
|---|---|---|
| Phase 1 | Oct 13–19, 2026 | Geometry inspection, environment setup, reference data |
| Phase 2 | Oct 20–26, 2026 | Aerodynamic analysis and flight simulation baseline |
| Phase 3 | Oct 27–Nov 2, 2026 | AI engineering analysis and initial web interface |
| Phase 4 | Nov 3–9, 2026 | System integration, comparisons, and testing |
| MVP Delivery | Nov 10–11, 2026 | Documentation, demonstration, AeroTwin AI v0.1 |

## 8. Development Team

The project is organized around four engineering responsibilities:

- **Project Lead & Software Integration:** System architecture, CAD workflow, backend, frontend, integration
- **Flight Simulation Engineering:** PX4, Gazebo, JSBSim, flight scenarios and telemetry
- **AI Engineering:** Data analysis, anomaly detection, explainable recommendations, optimization
- **Aerodynamic & Mathematical Validation:** MATLAB, flight performance calculations, engineering verification

Development uses feature branches and pull requests to keep the main branch stable.

## 9. Engineering Principles

AeroTwin AI development follows five core principles:

1. **Physics before prediction** — Simulation and engineering equations provide the primary technical basis.
2. **Traceable data** — Measurements, assumptions, and calculated values are documented.
3. **Explainable AI** — Recommendations should include technical justification.
4. **Reproducibility** — Analyses should record input parameters and execution conditions.
5. **Modular architecture** — The platform should support different aircraft configurations and future integrations.

## 10. Current Limitations

AeroTwin AI is under active development.

The initial MVP is not a certified flight dynamics environment, an airworthiness assessment system, or a substitute for experimental flight testing.

CAD mesh geometry alone does not define aircraft mass properties, propulsion behavior, aerodynamic coefficients, or flight control dynamics. These elements must be modeled and validated separately.

## 11. Project Repository

GitHub: https://github.com/ecemtan/AeroTwinAI

---

**AeroTwin AI — From Aircraft Geometry to Intelligent Engineering Decisions.**

*Developed for research, engineering experimentation, and AI-assisted aerospace innovation.*