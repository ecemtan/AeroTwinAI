import type { OpenVSPStatus } from '../api/types'
import { AvailabilityBadge } from './StatusBadge'

/**
 * Aerodynamic analysis screen skeleton.
 *
 * Planned contract (docs/API_CONTRACT.md): VSPAERO alpha sweep -> CL, CD, Cm
 * versus alpha, always shown together with reference area/span/chord and the
 * validation status of the run.
 */
export function AerodynamicsPanel({ openvsp, geometryAvailable }: { openvsp: OpenVSPStatus | null; geometryAvailable: boolean }) {
  return (
    <section className="panel">
      <h2>
        Aerodinamik analiz {openvsp && <AvailabilityBadge available={openvsp.available && geometryAvailable} />}
      </h2>
      <p className="empty">VSPAERO analiz sonucu yok.</p>
      <ul className="muted">
        <li>VSPAERO: {openvsp?.available ? 'bulundu' : 'kurulu değil / bulunamadı'}</li>
        <li>Cessna 172 OpenVSP geometrisi: {geometryAvailable ? 'var' : 'henüz oluşturulmadı'}</li>
        <li>CL–α, CD–α, Cm–α grafikleri — yapılacak</li>
      </ul>
    </section>
  )
}
