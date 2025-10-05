import { useEffect, useState } from 'react'
import { getPrecipProbability } from '../services/weatherService'

export default function WeatherCard({ location, dateMD, onResult }) {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [data, setData] = useState(null)

  useEffect(() => {
    let cancelled = false
    async function fetchData() {
      setLoading(true)
      setError(null)
      try {
        const res = await getPrecipProbability({
          lat: location.lat,
          lon: location.lon,
          month: dateMD.month,
          day: dateMD.day,
          threshold_mm: 1,
        })
        if (!cancelled) {
          setData(res)
          onResult?.(res)
        }
      } catch (e) {
        if (!cancelled) setError(e.message || 'Failed to fetch')
      } finally {
        if (!cancelled) setLoading(false)
      }
    }
    fetchData()
    return () => { cancelled = true }
  }, [location.lat, location.lon, dateMD.month, dateMD.day])

  return (
    <div className="bg-white rounded shadow p-4">
      <h2 className="font-semibold mb-2">Rain Probability</h2>
      {loading && <div className="text-slate-500">Loading...</div>}
      {error && <div className="text-red-600">{error}</div>}
      {data && (
        <div className="space-y-1">
          <div><span className="text-slate-600">Rain ≥1mm:</span> <b>{data.rain_probability}%</b></div>
          <div><span className="text-slate-600">Heavy ≥20mm:</span> <b>{data.heavy_rain_probability}%</b></div>
          <div className="text-sm text-slate-500">{data.meta.units}, {data.meta.period}</div>
        </div>
      )}
    </div>
  )
}
