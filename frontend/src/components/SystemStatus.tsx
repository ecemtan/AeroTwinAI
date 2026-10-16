import type { ApiState } from '../api/useApi'
import type { HealthResponse } from '../api/types'
import { AvailabilityBadge } from './StatusBadge'

export function SystemStatus({ health }: { health: ApiState<HealthResponse> }) {
  if (health.kind === 'loading') return <section className="panel">Sistem durumu yükleniyor…</section>
  if (health.kind === 'error') {
    return (
      <section className="panel panel-error">
        <h2>Sistem durumu</h2>
        <p>{health.message}</p>
        <p className="hint">Backend: <code>uvicorn backend.app.main:app --reload --port 8000</code></p>
      </section>
    )
  }

  const { modules } = health.data
  const rows = [
    { name: 'Uçak kayıtları', available: modules.aircraft_registry.available, detail: modules.aircraft_registry.error ?? modules.aircraft_registry.aircraft_ids.join(', ') },
    { name: `JSBSim ${modules.jsbsim.version ?? ''}`, available: modules.jsbsim.available, detail: modules.jsbsim.error ?? 'c172p modeli bulundu' },
    { name: 'OpenVSP / VSPAERO', available: modules.openvsp.available, detail: modules.openvsp.error ?? modules.openvsp.vspaero_path ?? '' },
  ]

  return (
    <section className="panel">
      <h2>
        Sistem durumu <span className={`badge ${health.data.status === 'ok' ? 'badge-ok' : 'badge-warn'}`}>{health.data.status}</span>
      </h2>
      <table className="table">
        <tbody>
          {rows.map((row) => (
            <tr key={row.name}>
              <td>{row.name}</td>
              <td><AvailabilityBadge available={row.available} /></td>
              <td className="muted">{row.detail}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  )
}
