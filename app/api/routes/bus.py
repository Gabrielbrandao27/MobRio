from decimal import Decimal
import json
import redis
from fastapi import APIRouter, Depends
from app.crud.bus import Bus
from app.dependencies.auth import get_current_user
from app.utils.distance import calculate_eta

router = APIRouter()
r = redis.Redis(host='localhost', port=6379, db=0)

@router.get("/bus/routes")
def get_routes(_: dict = Depends(get_current_user)):
    try:
        bus_db = Bus()
        bus_lines = bus_db.fetch_routes()
        bus_db.close()
        return bus_lines
    except Exception as e:
        return {"error": str(e)}

@router.get("/bus/stops")
def get_stops(route_id: str, direction_id: int, _: dict = Depends(get_current_user)):
    try:
        bus_db = Bus()
        bus_stops = bus_db.fetch_stops(route_id, direction_id)
        bus_db.close()
        return bus_stops
    except Exception as e:
        return {"error": str(e)}

@router.get("/bus/live_positions")
def get_live_positions(user: dict = Depends(get_current_user)):
    try:
        bus_struct = r.get("bus_struct")
        if bus_struct:
            bus_struct = json.loads(bus_struct)

        user_id = user.get("id")
        bus_db = Bus()
        user_bus_data = bus_db.fetch_user_bus_relations(user_id)
        bus_db.close()

        relations_dict = {
            item["route_short_name"]: json.loads(item["relations"]) for item in user_bus_data
        }
        print(relations_dict)

        live_positions = []

        for item in bus_struct:
            route_name = item["linha"]
            if route_name in relations_dict:
                lat = Decimal(item["latitude"].replace(",", "."))
                lon = Decimal(item["longitude"].replace(",", "."))
                velocity = int(item["velocidade"])

                relation = relations_dict[route_name][0]
                tempo_chegada = calculate_eta(lat, lon, relation["stop_lat"], relation["stop_lon"], velocity)

                live_positions.append({
                    "route_name": route_name,
                    "latitude": lat,
                    "longitude": lon,
                    "velocity": velocity,
                    "stop_name": relation["stop_name"],
                    "tempo_chegada": tempo_chegada
                })

        return {"live_positions": live_positions}
    except Exception as e:
        return {"error": str(e)}