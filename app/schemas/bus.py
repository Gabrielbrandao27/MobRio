from pydantic import BaseModel, field_validator

class BusRoutes(BaseModel):
    route_id: int
    route_short_name: str
    route_long_name: str

class BusStops(BaseModel):
    stop_id: int
    stop_name: str
    stop_lat: float
    stop_lon: float

class RouteStops(BaseModel):
    route_stop_id: int
    route_id: int
    stop_id: int
    stop_sequence: int
