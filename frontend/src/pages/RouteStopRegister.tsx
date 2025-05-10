import { useState } from 'react';
import { busRoutes, busStops, userBusRelation } from '../api/webService';

function HomePage() {
  const [routes, setRoutes] = useState([]);
  const [selectedRoute, setSelectedRoute] = useState('');
  const [stops, setStops] = useState([]);
  const [selectedStop, setSelectedStop] = useState('');
  const [openTime, setOpenTime] = useState('');
  const [closeTime, setCloseTime] = useState('');

  const handleLoadRoutes = async () => {
    try {
      const response = await busRoutes();
      setRoutes(response.lines);
    } catch (error) {
      console.error('Erro ao buscar rotas:', error);
    }
  };

  const handleLoadStops = async () => {
    if (!selectedRoute) {
      alert('Selecione uma linha primeiro!');
      return;
    }
    try {
      const response = await busStops(selectedRoute, 0);
      setStops(response.stops);
    } catch (error) {
      console.error('Erro ao buscar paradas:', error);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const formattedOpenTime = `${openTime}:00`;
      const formattedCloseTime = `${closeTime}:00`;
      await userBusRelation(selectedStop, formattedOpenTime, formattedCloseTime);
      alert('Relação salva com sucesso!');
    } catch (error) {
      alert('Erro ao salvar relação.');
      console.error(error);
    }
  };

  return (
    <div className="form-container">
      <h2>Configuração do Monitoramento</h2>

      <button type="button" onClick={handleLoadRoutes}>
        Carregar Linhas
      </button>

      {routes.length > 0 && (
        <>
          <label>Escolha a linha:</label>
          <select
            value={selectedRoute}
            onChange={(e) => setSelectedRoute(e.target.value)}
            required
          >
            <option value="">Selecione</option>
            {routes.map((route: any) => (
              <option key={route.route_id} value={route.route_id}>
                {route.route_short_name} - {route.route_long_name}
              </option>
            ))}
          </select>

          <button type="button" onClick={handleLoadStops}>
            Carregar Paradas da Linha
          </button>
        </>
      )}

      {stops.length > 0 && (
        <form onSubmit={handleSubmit}>
          <label>Escolha o ponto:</label>
          <select
            value={selectedStop}
            onChange={(e) => setSelectedStop(e.target.value)}
            required
          >
            <option value="">Selecione</option>
            {stops.map((stop: any) => (
              <option key={stop.route_stop_id} value={stop.route_stop_id}>
                {stop.stop_name}
              </option>
            ))}
          </select>

          <label>Horário de abertura:</label>
          <input
            type="time"
            value={openTime}
            onChange={(e) => setOpenTime(e.target.value)}
            required
          />

          <label>Horário de fechamento:</label>
          <input
            type="time"
            value={closeTime}
            onChange={(e) => setCloseTime(e.target.value)}
            required
          />

          <button type="submit">Enviar</button>
        </form>
      )}
    </div>
  );
}

export default HomePage;
