import { MapContainer, TileLayer, Marker, useMapEvents } from 'react-leaflet'
import 'leaflet/dist/leaflet.css'

function ClickHandler({ onChange }) {
  useMapEvents({
    click(e) {
      const { lat, lng } = e.latlng
      onChange({ lat, lon: lng })
    }
  })
  return null
}

export default function MapSelector({ value, onChange }) {
  const position = [value.lat, value.lon]
  return (
    <div className="h-80 bg-white rounded shadow">
      <MapContainer center={position} zoom={6} className="h-full w-full">
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <Marker position={position} />
        <ClickHandler onChange={onChange} />
      </MapContainer>
    </div>
  )
}
