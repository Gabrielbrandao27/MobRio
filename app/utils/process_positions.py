import json
import redis
from utils.travel_time import get_eta_from_traveltime
from crud.bus import Bus


r = redis.Redis(host='redis', port=6379, db=0)


def process_live_positions(user_id: int):
    bus_struct = r.get("bus_struct")
    if not bus_struct:
        return {"error": "Nenhum dado de ônibus disponível."}

    bus_struct = json.loads(bus_struct)

    bus_db = Bus()
    user_bus_data = bus_db.fetch_user_bus_relations(user_id)
    bus_db.close()

    relations_dict = {
        item["route_short_name"]: json.loads(item["relations"]) for item in user_bus_data
    }

    live_positions = []

    for item in bus_struct:
        route_name = item["linha"]
        if route_name in relations_dict:
            bus_lat = float(item["latitude"].replace(",", "."))
            bus_lon = float(item["longitude"].replace(",", "."))
            velocity = int(item["velocidade"])

            relation = relations_dict[route_name][0]
            stop_lat = float(relation["stop_lat"])
            stop_lon = float(relation["stop_lon"])

            tempo_chegada = get_eta_from_traveltime(bus_lat, bus_lon, stop_lat, stop_lon)

            live_positions.append({
                "route_name": route_name,
                "latitude": bus_lat,
                "longitude": bus_lon,
                "velocity": velocity,
                "stop_name": relation["stop_name"],
                "tempo_chegada": tempo_chegada,
                "hora_abertura": relation["open_time"],
                "hora_fechamento": relation["close_time"],
            })

    return {"live_positions": live_positions}