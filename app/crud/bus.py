from app.db.db_manager import DBManager


class Bus:
    def __init__(self):
        self.db = DBManager()
    
    def fetch_routes(self):
        try:
            sql = """
                SELECT * FROM routes
            """
            lines = self.db.fetch_all(sql)
            return {"lines": lines}
        except Exception as e:
            return {"error": str(e)}
    
    def fetch_stops(self, route_id, direction_id):
        try:
            sql = """
                SELECT 
                    rs.route_stop_id AS route_stop_id,
                    s.stop_id,
                    s.stop_name,
                    s.stop_lat,
                    s.stop_lon,
                    rs.stop_sequence
                FROM route_stops rs
                JOIN stops s ON rs.stop_id = s.stop_id
                WHERE rs.route_id = %s
                AND rs.direction_id = %s
                ORDER BY rs.stop_sequence
            """
            stops = self.db.fetch_all(sql, (route_id, direction_id))
            return {"stops": stops}
        except Exception as e:
            return {"error": str(e)}

    
    def close(self):
        self.db.close()