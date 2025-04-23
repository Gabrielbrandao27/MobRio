from app.db.db_manager import DBManager


class User:
    def __init__(self):
        self.db = DBManager()

    def insert_user(self, payload):
        try:
            sql = """
                INSERT IGNORE INTO users (name, password, email, bus_line, bus_stop, open_time, close_time)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            self.db.execute_query(sql, (
                payload["name"],
                payload["password"],
                payload["email"],
                payload["bus_line"],
                payload["bus_stop"],
                payload["open_time"],
                payload["close_time"]
            ))
            return {"message": "User inserted successfully"}
        except Exception as e:
            return {"error": str(e)}


    def fetch_user(self, user_id):
        try:
            sql = """
                SELECT * FROM users WHERE id = %s
            """
            user = self.db.fetch_one(sql, (user_id,))
            return {"user": user}
        except Exception as e:
            return {"error": str(e)}
    

    def fetch_all_users(self):
        try:
            sql = """
                SELECT * FROM users
            """
            users = self.db.fetch_all(sql)
            return {"users": users}
        except Exception as e:
            return {"error": str(e)}
    

    def delete_user(self, payload):
        try:
            sql = """
                DELETE FROM users WHERE email = %s
            """
            self.db.execute_query(sql, (payload["email"],))
            return {"message": "User deleted successfully"}
        except Exception as e:
            return {"error": str(e)}

    def close(self):
        self.db.close()