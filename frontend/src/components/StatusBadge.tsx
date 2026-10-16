import type { DataStatus } from '../api/types'

const LABELS: Record<DataStatus, string> = {
  verified: 'Doğrulanmış',
  reference_model: 'Referans model',
  unverified: 'Doğrulanmamış',
  missing: 'Eksik',
}

export function DataStatusBadge({ status }: { status: DataStatus }) {
  return <span className={`badge badge-${status}`}>{LABELS[status]}</span>
}

export function AvailabilityBadge({ available }: { available: boolean }) {
  return (
    <span className={`badge ${available ? 'badge-ok' : 'badge-off'}`}>
      {available ? 'Hazır' : 'Kullanılamıyor'}
    </span>
  )
}
