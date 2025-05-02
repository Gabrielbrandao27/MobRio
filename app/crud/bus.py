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
    
    def fetch_user_bus_relations(self, user_id):
        try:
            sql = """
                SELECT 
                    ub.user_id,
                    r.route_name,
                    JSON_ARRAYAGG(
                        JSON_OBJECT(
                            'route_stop_id', ub.route_stop_id,
                            'open_time', ub.open_time,
                            'close_time', ub.close_time,
                            'stop_id', rs.stop_id,
                            'stop_name', s.stop_name,
                            'stop_lat', s.stop_lat,
                            'stop_lon', s.stop_lon
                        )
                    ) AS relations
                FROM user_bus_relation ub
                JOIN route_stops rs ON ub.route_stop_id = rs.route_stop_id
                JOIN stops s ON rs.stop_id = s.stop_id
                JOIN routes r ON rs.route_id = r.route_id
                WHERE ub.user_id = %s
                GROUP BY ub.user_id, r.route_name;
            """
            result = self.db.fetch_all(sql, (user_id,))
            return result
        except Exception as e:
            return {"error": str(e)}

    def close(self):
        self.db.close()
