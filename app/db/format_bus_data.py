import pandas as pd
import os

def load_gtfs_data():
    # Obter o diretório atual do arquivo bus_data.py
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Construir o caminho absoluto para os arquivos
    routes_path = os.path.join(current_dir, 'bus_data/routes.txt')
    trips_path = os.path.join(current_dir, 'bus_data/trips.txt')
    stop_times_path = os.path.join(current_dir, 'bus_data/stop_times.txt')
    stops_path = os.path.join(current_dir, 'bus_data/stops.txt')

    # Ler arquivos GTFS
    routes = pd.read_csv(routes_path)
    trips = pd.read_csv(trips_path)
    stop_times = pd.read_csv(stop_times_path)
    stops = pd.read_csv(stops_path)

    # Selecionar colunas úteis
    routes = routes[['route_id', 'route_short_name', 'route_long_name']]
    trips = trips[['route_id', 'trip_id', 'direction_id']]
    stop_times = stop_times[['trip_id', 'stop_id', 'stop_sequence']]
    stops = stops[['stop_id', 'stop_name', 'stop_lat', 'stop_lon']]

    # Relacionar trip -> route
    trip_route = pd.merge(trips, routes, on='route_id')

    # Relacionar trip -> stop_times
    trip_stop = pd.merge(stop_times, trip_route, on='trip_id')
    trip_route = trip_route[['route_id', 'route_short_name', 'route_long_name']]

    # Relacionar stop_times -> stops
    trip_stop = pd.merge(trip_stop, stops, on='stop_id')

    # Agora temos stop_id, route_id e route_long_name juntos
    route_stops = trip_stop[['route_id', 'stop_id', 'stop_sequence', 'direction_id']].drop_duplicates()
    trip_stop = trip_stop[['stop_id', 'stop_name', 'stop_lat', 'stop_lon']]

    # Depois de montar os DataFrames finais
    trip_route.to_csv('bus_data/routes_final.csv', index=False)
    trip_stop.to_csv('bus_data/stops_final.csv', index=False)
    route_stops.to_csv('bus_data/route_stops_final.csv', index=False)


if __name__ == "__main__":
    load_gtfs_data()
