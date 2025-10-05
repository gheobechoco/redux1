import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

export async function getPrecipProbability({ lat, lon, month, day, threshold_mm }) {
  const res = await axios.get(`${API_BASE}/api/probability/precipitation`, {
    params: { lat, lon, month, day, threshold_mm }
  })
  return res.data
}
