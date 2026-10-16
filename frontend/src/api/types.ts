// Mirrors of the backend Pydantic models (core/models.py, backend/app/routers/health.py).
// Keep in sync with docs/API_CONTRACT.md. Later these can be generated from
// http://127.0.0.1:8000/openapi.json with openapi-typescript.

export type DataStatus = 'verified' | 'reference_model' | 'unverified' | 'missing'

export interface DataSource {
  id: string
  title: string
  kind: 'simulation_model' | 'document' | 'literature' | 'measurement' | 'derived'
  locator: string | null
  notes: string | null
}

export interface SourcedValue {
  status: DataStatus
  source: string | null
  source_value: number | string | null
  source_unit: string | null
  value: number | string | null
  unit: string | null
  frame: string | null
  note: string | null
}

export interface AircraftSummary {
  aircraft_id: string
  name: string
  category: string
  flight_dynamics_model: string | null
  geometry_model_available: boolean
}

export interface AircraftConfig {
  schema_version: string
  aircraft_id: string
  name: string
  category: string
  description: string
  variant_notes: string
  sources: DataSource[]
  flight_dynamics_model: {
    engine: 'jsbsim'
    model_name: string
    variant: string
    source: string
  } | null
  geometry_model: {
    tool: 'openvsp'
    file: string | null
    variant: string | null
    status: DataStatus
    note: string | null
  }
  geometry: Record<string, SourcedValue>
  mass_properties: Record<string, SourcedValue>
  propulsion: Record<string, SourcedValue>
}

export interface JSBSimStatus {
  available: boolean
  version: string | null
  root_dir: string | null
  models: Record<string, boolean>
  error: string | null
}

export interface OpenVSPStatus {
  python_api_available: boolean
  vspaero_path: string | null
  vspscript_path: string | null
  available: boolean
  error: string | null
}

export interface HealthResponse {
  status: 'ok' | 'degraded'
  api_version: string
  timestamp: string
  modules: {
    aircraft_registry: { available: boolean; aircraft_ids: string[]; error: string | null }
    jsbsim: JSBSimStatus
    openvsp: OpenVSPStatus
  }
}
