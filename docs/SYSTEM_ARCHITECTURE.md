
> **Superseded:** This document describes the Jet Drone era (v0.1.0 draft).
> The current architecture is [ARCHITECTURE.md](ARCHITECTURE.md). Kept for history.

# AeroTwin AI — System Architecture

Version: 0.1.0
Status: MVP Architecture
Reference Aircraft: Jet Drone

## 1. Project Objective

AeroTwin AI is a modular aircraft engineering and
digital twin platform integrating:

- CAD geometry processing
- Aerodynamic analysis
- Flight dynamics simulation
- Engineering validation
- AI-assisted diagnostics and optimization
- Web-based visualization

## 2. Core Modules

### Aircraft Configuration
Path: aircraft/jetdrone/config/

Responsibilities:
- Aircraft geometry metadata
- Coordinate systems and units
- Mass and inertia properties
- Wing and tail parameters
- Propulsion parameters
- Engineering assumptions

### Aerodynamics
Path: aerodynamics/

Tools:
- OpenVSP
- VSPAERO
- Python
- Trimesh

Outputs:
- Geometry analysis
- Aerodynamic coefficients
- Analysis conditions
- Geometry transformation metadata

### Flight Simulation
Path: simulation/

Tools:
- JSBSim
- PX4 / Gazebo (later integration)

Outputs:
- Position
- Velocity
- Attitude
- Angular rates
- Control inputs
- Simulation timestamps

### Engineering Validation
Path: validation/

Tools:
- MATLAB
- Python

Outputs:
- Analytical calculations
- Model comparison results
- Error metrics
- Validation reports

### AI Analysis
Path: ai/

Responsibilities:
- Anomaly detection
- Performance assessment
- Optimization recommendations
- Model evaluation

### Backend
Path: backend/

Technology:
- Python
- FastAPI

Responsibilities:
- Data validation
- API endpoints
- Module integration
- Result delivery

### Frontend
Path: frontend/

Technology:
- React
- TypeScript

Responsibilities:
- Aircraft dashboard
- Engineering visualizations
- Simulation telemetry
- AI analysis display

## 3. Engineering Standards

Internal units:
- Length: meters (m)
- Mass: kilograms (kg)
- Time: seconds (s)
- Force: newtons (N)
- Moment: newton-meters (N*m)
- Angle: radians (rad)

All coordinate frames must be explicitly identified.

Unknown physical parameters must remain null
until verified.

## 4. Data Exchange

Configuration: JSON
Analysis summaries: JSON
Time-series telemetry: CSV or Parquet
3D geometry: STL / OpenVSP native formats

Each analysis result should include:
- Aircraft identifier
- Model version
- Analysis type
- Input parameters
- Output parameters
- Units
- Coordinate frame
- Data source
- Validation status

## 5. MVP Integration Flow

Aircraft Configuration
    |
    +--> Aerodynamics
    |
    +--> Flight Simulation
    |
    +--> Engineering Validation
    |
    +--> AI Analysis
              |
              v
        FastAPI Backend
              |
              v
        React Dashboard

## 6. Engineering Rules

1. Do not invent missing aircraft parameters.
2. Record assumptions and data provenance.
3. Separate simulated and measured data.
4. Validate coordinate transformations.
5. Keep engineering modules independently testable.
6. Do not treat STL mesh area as wing reference area.
7. Do not assume CAD geometry alone is a flight model.

## 7. MVP Acceptance Criteria

- Aircraft geometry is parsed successfully.
- Aircraft configuration is available as JSON.
- At least one aerodynamic analysis is reproducible.
- At least one flight simulation scenario runs.
- Engineering results have documented validation.
- AI analysis produces interpretable output.
- Backend exposes module results.
- Frontend displays integrated engineering data.
