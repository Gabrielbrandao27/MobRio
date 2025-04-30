import pandas as pd
import os


def fetch_paths(case):
    # Obter o diretório atual do arquivo bus_data.py
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Construir o caminho absoluto para os arquivos
    match case:
        case "routes":
            return os.path.join(current_dir, 'bus_data/routes_final.csv')
        case "stops":
            return os.path.join(current_dir, 'bus_data/stops_final.csv')
        case "route_stops":
            return os.path.join(current_dir, 'bus_data/route_stops_final.csv')

def insert_routes(db):
    routes_df = pd.read_csv(fetch_paths("routes"))
    query = "INSERT IGNORE INTO routes (route_id, route_short_name, route_long_name) VALUES (%s, %s, %s)"
    data = [(row['route_id'], row['route_short_name'], row['route_long_name']) for _, row in routes_df.iterrows()]
    db.execute_many(query, data)

def insert_stops(db):
    stops_df = pd.read_csv(fetch_paths("stops"))
    query = "INSERT IGNORE INTO stops (stop_id, stop_name, stop_lat, stop_lon) VALUES (%s, %s, %s, %s)"
    data = [(row['stop_id'], row['stop_name'], row['stop_lat'], row['stop_lon']) for _, row in stops_df.iterrows()]

    # Dividir os dados em batches
    batch_size = 1000
    for i in range(0, len(data), batch_size):
        batch = data[i:i+batch_size]
        db.execute_many(query, batch)

def insert_route_stops(db):
    route_stops_df = pd.read_csv(fetch_paths("route_stops"))
    query = "INSERT IGNORE INTO route_stops (route_id, stop_id, stop_sequence, direction_id) VALUES (%s, %s, %s, %s)"
    data = [(row['route_id'], row['stop_id'], row['stop_sequence'], row['direction_id']) for _, row in route_stops_df.iterrows()]

    # Dividir os dados em batches
    batch_size = 1000
    for i in range(0, len(data), batch_size):
        batch = data[i:i+batch_size]
        db.execute_many(query, batch)