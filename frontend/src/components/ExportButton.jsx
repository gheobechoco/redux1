import { saveAs } from 'file-saver'

export default function ExportButton({ result }) {
  const onExport = (type) => {
    if (!result) return
    if (type === 'json') {
      const blob = new Blob([JSON.stringify(result, null, 2)], { type: 'application/json' })
      saveAs(blob, 'rain_probability.json')
    } else {
      const header = ['metric,value']
      const rows = [
        ['rain_probability', result.rain_probability],
        ['heavy_rain_probability', result.heavy_rain_probability],
        ['mean_precip_mm', result.stats.mean_precip_mm],
        ['median_precip_mm', result.stats.median_precip_mm],
        ['percentile_90_precip_mm', result.stats.percentile_90_precip_mm],
      ]
      const csv = header.concat(rows.map(r => r.join(','))).join('\n')
      const blob = new Blob([csv], { type: 'text/csv' })
      saveAs(blob, 'rain_probability.csv')
    }
  }

  return (
    <div className="flex gap-2">
      <button onClick={() => onExport('json')} className="bg-slate-800 text-white px-3 py-2 rounded">Export JSON</button>
      <button onClick={() => onExport('csv')} className="bg-slate-200 px-3 py-2 rounded">Export CSV</button>
    </div>
  )
}
