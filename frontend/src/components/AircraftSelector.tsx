import type { AircraftSummary } from '../api/types'
import type { ApiState } from '../api/useApi'

interface Props {
  aircraft: ApiState<AircraftSummary[]>
  selectedId: string | null
  onSelect: (id: string) => void
}

export function AircraftSelector({ aircraft, selectedId, onSelect }: Props) {
  if (aircraft.kind === 'loading') return <div className="selector">Uçaklar yükleniyor…</div>
  if (aircraft.kind === 'error') return <div className="selector error-text">Uçak listesi alınamadı</div>

  return (
    <label className="selector">
      <span>Uçak</span>
      <select value={selectedId ?? ''} onChange={(event) => onSelect(event.target.value)}>
        {aircraft.data.map((item) => (
          <option key={item.aircraft_id} value={item.aircraft_id}>
            {item.name}
          </option>
        ))}
      </select>
    </label>
  )
}
