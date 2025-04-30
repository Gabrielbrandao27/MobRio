from fastapi import APIRouter, Depends
from app.crud.bus import Bus
from app.dependencies.auth import get_current_user

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