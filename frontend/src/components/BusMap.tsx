import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { MapContainer, Marker, Popup, TileLayer } from 'react-leaflet';
import type { LivePosition } from '../types/bus';

// Corrige os ícones padrão do Leaflet (senão ficam quebrados no React)
import markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png';
import markerIcon from 'leaflet/dist/images/marker-icon.png';
import markerShadow from 'leaflet/dist/images/marker-shadow.png';

delete (L.Icon.Default.prototype as { _getIconUrl?: unknown })._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: markerIcon2x,
  iconUrl: markerIcon,
  shadowUrl: markerShadow,
});

function BusMap({ positions }: { positions: LivePosition[] }) {
  // Define o centro do mapa (pode ajustar)
  const center: [number, number] = [-22.9, -43.2];

  return (
    <MapContainer center={center} zoom={12} style={{ height: '500px', width: '100%' }}>
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution="&copy; OpenStreetMap contributors"
      />
      {positions.map((pos, index) => (
        <Marker key={index} position={[pos.latitude, pos.longitude]}>
          <Popup>
            <strong>Linha:</strong> {pos.route_name} <br />
            <strong>Velocidade:</strong> {pos.velocity} km/h <br />
            <strong>Sua parada:</strong> {pos.stop_name} <br />
            <strong>Tempo de chegada:</strong> {pos.tempo_chegada || 'N/D'}
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
}

export default BusMap;
