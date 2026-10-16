import type { JSBSimStatus } from '../api/types'
import { AvailabilityBadge } from './StatusBadge'

/**
 * Flight simulation screen skeleton.
 *
 * Planned contract (docs/API_CONTRACT.md): POST /api/simulation/runs returns a
 * SimulationResult whose metadata.data_origin is 'live_simulation' or 'replay'.
 * A replay MUST be labelled as such in this panel.
 */
export function SimulationPanel({ jsbsim }: { jsbsim: JSBSimStatus | null }) {
  return (
    <section className="panel">
      <h2>
        Uçuş simülasyonu {jsbsim && <AvailabilityBadge available={jsbsim.available} />}
      </h2>
      <p className="empty">
        Simülasyon sonucu yok. Backend simülasyon endpoint'i henüz bağlanmadı; bu alanda
        gösterilen bir veri yoktur.
      </p>
      <ul className="muted">
        <li>Senaryo seçimi — yapılacak</li>
        <li>Hız / irtifa / yönelim grafikleri — yapılacak</li>
        <li>Telemetri ile 3B model hareketi — yapılacak</li>
      </ul>
    </section>
  )
}
