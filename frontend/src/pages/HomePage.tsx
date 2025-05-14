import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { busLivePositions } from '../api/webService';
import BusMap from '../components/BusMap';
import type { LivePosition } from '../types/bus';

function HomePage() {
  const [positions, setPositions] = useState<LivePosition[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchPositions = async () => {
    try {
      const response = await busLivePositions();
      setPositions(response.live_positions);
      setLoading(false);
    } catch (error) {
      console.error('Erro ao buscar posições ao vivo:', error);
    }
  };

  useEffect(() => {
    fetchPositions();
    const interval = setInterval(fetchPositions, 60_000); // a cada 1 min
    return () => clearInterval(interval); // limpa no unmount
  }, []);

  return (
    <div className="live-position-container">
      <h3>
        Cadastrar linhas de ônibus? Vá para{' '}
        <Link to="/route-stop-register">Cadastro de Ônibus</Link>
      </h3>

      <h2>Posições ao Vivo</h2>
      {loading ? (
        <p>Carregando...</p>
      ) : positions.length === 0 ? (
        <p>Nenhum dado disponível.</p>
      ) : (
        <div style={{ display: 'flex', gap: '20px' }}>
          <div style={{ width: '40%' }}>
            <table className="bus-table">
              <thead>
                <tr>
                  <th>Linha</th>
                  <th>Latitude</th>
                  <th>Longitude</th>
                  <th>Velocidade (km/h)</th>
                  <th>Tempo Chegada (min)</th>
                </tr>
              </thead>
              <tbody>
                {positions.map((pos, index) => (
                  <tr key={index}>
                    <td>{pos.route_name}</td>
                    <td>{pos.latitude}</td>
                    <td>{pos.longitude}</td>
                    <td>{pos.velocity}</td>
                    <td>{pos.tempo_chegada}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <div style={{ width: '60%' }}>
            <BusMap positions={positions} />
          </div>
        </div>
      )}
    </div>
  );
}

export default HomePage;
