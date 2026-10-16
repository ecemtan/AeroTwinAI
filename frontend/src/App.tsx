import { useCallback, useState } from 'react'
import { api } from './api/client'
import { useApi } from './api/useApi'
import { AerodynamicsPanel } from './components/AerodynamicsPanel'
import { AircraftDetails } from './components/AircraftDetails'
import { AircraftSelector } from './components/AircraftSelector'
import { AircraftViewer } from './components/AircraftViewer'
import { SimulationPanel } from './components/SimulationPanel'
import { SystemStatus } from './components/SystemStatus'

export default function App() {
  const health = useApi(api.health)
  const aircraftList = useApi(api.listAircraft)
  const [chosenId, setChosenId] = useState<string | null>(null)

  const selectedId =
    chosenId ?? (aircraftList.kind === 'ready' ? aircraftList.data[0]?.aircraft_id ?? null : null)
  const loadConfig = useCallback(
    (signal: AbortSignal) =>
      selectedId ? api.getAircraft(selectedId, signal) : Promise.reject(new Error('Uçak seçilmedi')),
    [selectedId],
  )
  const config = useApi(loadConfig)

  const summary =
    aircraftList.kind === 'ready' ? aircraftList.data.find((a) => a.aircraft_id === selectedId) : undefined
  const geometryAvailable = summary?.geometry_model_available ?? false
  const modules = health.kind === 'ready' ? health.data.modules : null

  return (
    <div className="app">
      <header className="header">
        <div>
          <h1>AeroTwin AI</h1>
          <p className="muted">Aerodinamik analiz · Uçuş dinamiği · Simülasyon tabanlı sanal ikiz</p>
        </div>
        <AircraftSelector aircraft={aircraftList} selectedId={selectedId} onSelect={setChosenId} />
      </header>

      <main className="grid">
        <SystemStatus health={health} />
        <AircraftViewer geometryAvailable={geometryAvailable} />
        <SimulationPanel jsbsim={modules?.jsbsim ?? null} />
        <AerodynamicsPanel openvsp={modules?.openvsp ?? null} geometryAvailable={geometryAvailable} />
        <div className="wide">
          {config.kind === 'ready' && <AircraftDetails config={config.data} />}
          {config.kind === 'error' && selectedId && <section className="panel panel-error">{config.message}</section>}
        </div>
      </main>

      <footer className="footer muted">
        Simülasyon tabanlı sanal ikiz — fiziksel bir uçaktan sensör verisi alınmamaktadır.
      </footer>
    </div>
  )
}
