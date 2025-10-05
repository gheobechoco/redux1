import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

export async function searchGranules(params) {
  const res = await axios.get(`${API_BASE}/api/nasa/cmr/granules`, { params })
  return res.data
}
