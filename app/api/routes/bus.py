import redis
from fastapi import APIRouter, Depends
from crud.bus import Bus
from dependencies.auth import get_current_user
from utils.process_positions import process_live_positions

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
        user_id = user.get("id")
        return process_live_positions(user_id)
    except Exception as e:
        return {"error": str(e)}