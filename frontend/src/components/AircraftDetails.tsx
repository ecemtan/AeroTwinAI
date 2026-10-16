import type { AircraftConfig, SourcedValue } from '../api/types'
import { DataStatusBadge } from './StatusBadge'

const SECTIONS: { key: 'geometry' | 'mass_properties' | 'propulsion'; title: string }[] = [
  { key: 'geometry', title: 'Geometri' },
  { key: 'mass_properties', title: 'Kütle özellikleri' },
  { key: 'propulsion', title: 'İtki' },
]

function formatValue(item: SourcedValue): string {
  if (item.value === null) return '—'
  if (typeof item.value === 'number') {
    const value = Number.isInteger(item.value) ? item.value.toString() : item.value.toPrecision(5)
    return item.unit ? `${value} ${item.unit}` : value
  }
  return item.value
}

function formatSource(item: SourcedValue): string {
  if (item.source_value === null) return ''
  return item.source_unit ? `${item.source_value} ${item.source_unit}` : ''
}

export function AircraftDetails({ config }: { config: AircraftConfig }) {
  const sourceTitles = new Map(config.sources.map((s) => [s.id, s.title]))

  return (
    <section className="panel">
      <h2>{config.name} — parametreler</h2>
      <p className="muted">{config.description}</p>
      <p className="notice">{config.variant_notes}</p>
      {SECTIONS.map((section) => (
        <div key={section.key}>
          <h3>{section.title}</h3>
          <table className="table">
            <thead>
              <tr>
                <th>Parametre</th>
                <th>Değer (SI)</th>
                <th>Kaynaktaki değer</th>
                <th>Durum</th>
                <th>Kaynak</th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(config[section.key]).map(([name, item]) => (
                <tr key={name}>
                  <td><code>{name}</code>{item.frame ? <span className="muted"> ({item.frame})</span> : null}</td>
                  <td>{formatValue(item)}</td>
                  <td className="muted">{formatSource(item)}</td>
                  <td><DataStatusBadge status={item.status} /></td>
                  <td className="muted" title={item.note ?? undefined}>
                    {item.source ? sourceTitles.get(item.source) ?? item.source : item.note ?? ''}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ))}
    </section>
  )
}
