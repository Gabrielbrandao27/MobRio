export interface Route {
  route_id: number;
  route_short_name: string;
  route_long_name: string;
}

export interface Stop {
  route_stop_id: number;
  stop_id: number;
  stop_name: string;
  stop_lat: number;
  stop_lon: number;
  stop_sequence: number;
}

export interface LivePosition {
  route_name: string;
  latitude: number;
  longitude: number;
  velocity: number;
  stop_name: string;
  tempo_chegada: string;
}
