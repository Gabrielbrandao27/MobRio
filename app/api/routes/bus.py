from fastapi import APIRouter, Depends
from app.crud.bus import Bus
from app.dependencies.auth import get_current_user
from app.tasks.celery_tasks import bus_struct
from app.utils.distance import calculate_eta

router = APIRouter()

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
        user_id = user.get("id")
        bus_db = Bus()
        user_bus_data = bus_db.fetch_user_bus_relations(user_id)
        bus_db.close()

        # Criar um dicionário indexado por route_name para acesso rápido
        relations_dict = {relation["route_name"]: relation for relation in user_bus_data["relations"]}

        live_positions = []

        for item in bus_struct:
            route_name = item["linha"]
            if route_name in relations_dict:
                # Dados do ônibus
                lat = item["latitude"]
                lon = item["longitude"]
                velocity = item["velocidade"]

                # Dados da relação do usuário
                relation = relations_dict[route_name]

                # Calcular tempo de chegada (ETA)
                tempo_chegada = calculate_eta(lat, lon, relation["stop_lat"], relation["stop_lon"], velocity)

                # Adicionar ao resultado
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