import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { busLivePositions } from '../api/webService';

function LivePosition() {
  const [positions, setPositions] = useState<any[]>([]);
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
        <table>
          <thead>
            <tr>
              <th>Linha</th>
              <th>Latitude</th>
              <th>Longitude</th>
              <th>Velocidade (km/h)</th>
            </tr>
          </thead>
          <tbody>
            {positions.map((pos, index) => (
              <tr key={index}>
                <td>{pos.route_name}</td>
                <td>{pos.latitude}</td>
                <td>{pos.longitude}</td>
                <td>{pos.velocity}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default LivePosition;
