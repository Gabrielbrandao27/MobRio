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
    
    def fetch_stops(self, route_id):
        try:
            sql = """
                SELECT * FROM route_stops WHERE route_id = %s
            """
            stops = self.db.fetch_all(sql, (route_id,))
            stop_ids = [stop[2] for stop in stops]

            if not stop_ids:
                return {"stops": []}

            sql = """
                SELECT * FROM stops WHERE stop_id IN (%s)
            """ % ','.join(['%s'] * len(stop_ids))
            stops = self.db.fetch_all(sql, stop_ids)
            return {"stops": stops}
        except Exception as e:
            return {"error": str(e)}
    
    def close(self):
        self.db.close()