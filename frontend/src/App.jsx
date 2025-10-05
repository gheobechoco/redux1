import { useState } from 'react'
import MapSelector from './components/MapSelector'
import DatePicker from './components/DatePicker'
import WeatherCard from './components/WeatherCard'
import ProbabilityChart from './components/ProbabilityChart'
import ExportButton from './components/ExportButton'

function App() {
  const [location, setLocation] = useState({ lat: 48.8566, lon: 2.3522 })
  const [dateMD, setDateMD] = useState({ month: 6, day: 15 })
  const [result, setResult] = useState(null)

  return (
    <div className="min-h-full flex flex-col">
      <header className="p-4 bg-indigo-600 text-white">
        <h1 className="text-xl font-semibold">Will It Rain On My Parade?</h1>
      </header>
      <main className="flex-1 p-4 grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div className="lg:col-span-2 space-y-4">
          <MapSelector value={location} onChange={setLocation} />
          <DatePicker value={dateMD} onChange={setDateMD} />
        </div>
        <div className="space-y-4">
          <WeatherCard location={location} dateMD={dateMD} onResult={setResult} />
          <ProbabilityChart result={result} />
          <ExportButton result={result} />
        </div>
      </main>
    </div>
  )
}

export default App
