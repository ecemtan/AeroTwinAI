import type { AircraftConfig, AircraftSummary, HealthResponse } from './types'

// Empty base URL = same origin; in development Vite proxies /api and /health
// to FastAPI (see vite.config.ts). Set VITE_API_BASE_URL for other setups.
const BASE_URL: string = import.meta.env.VITE_API_BASE_URL ?? ''
const BACKEND_DOWN = 'Backend erişilemiyor. FastAPI sunucusu çalışıyor mu?'

export class ApiError extends Error {
  readonly status: number | null

  constructor(message: string, status: number | null) {
    super(message)
    this.name = 'ApiError'
    this.status = status
  }
}

async function getJson<T>(path: string, signal?: AbortSignal): Promise<T> {
  let response: Response
  try {
    response = await fetch(`${BASE_URL}${path}`, { signal })
  } catch (error) {
    if (error instanceof DOMException && error.name === 'AbortError') throw error
    throw new ApiError(BACKEND_DOWN, null)
  }
  // The Vite dev proxy answers 502-504 when FastAPI is not running.
  if ([502, 503, 504].includes(response.status)) {
    throw new ApiError(`${BACKEND_DOWN} (HTTP ${response.status})`, response.status)
  }
  if (!response.ok) {
    throw new ApiError(`${path} isteği başarısız: HTTP ${response.status}`, response.status)
  }
  return (await response.json()) as T
}

export const api = {
  health: (signal?: AbortSignal) => getJson<HealthResponse>('/health', signal),
  listAircraft: (signal?: AbortSignal) => getJson<AircraftSummary[]>('/api/aircraft', signal),
  getAircraft: (id: string, signal?: AbortSignal) =>
    getJson<AircraftConfig>(`/api/aircraft/${encodeURIComponent(id)}`, signal),
}
