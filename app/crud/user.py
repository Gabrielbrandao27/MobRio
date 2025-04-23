from app.db.db_manager import DBManager


class User:
    def __init__(self):
        self.db = DBManager()

    def register_user(self, payload):
        try:
            sql = """
                INSERT IGNORE INTO users (name, password, email)
                VALUES (%s, %s, %s)
            """
            self.db.execute_query(sql, (
                payload["name"],
                payload["password"],
                payload["email"]
            ))
            return {"message": "User inserted successfully"}
        except Exception as e:
            return {"error": str(e)}


    def login_user(self, payload):
        try:
            sql = """
                SELECT * FROM users WHERE email = %s
            """
            user = self.db.fetch_one(sql, (payload["email"],))
            if not user:
                return {"error": "Invalid email"}
            if user["password"] != payload["password"]:
                return {"error": "Invalid password"}
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