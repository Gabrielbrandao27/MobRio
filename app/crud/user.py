from app.db.db_manager import DBManager


class User:
    def __init__(self):
        self.db = DBManager()

    def register_user(self, user):
        try:
            sql = """
                INSERT IGNORE INTO users (name, password, email)
                VALUES (%s, %s, %s)
            """
            self.db.execute_query(sql, (
                user.name,
                user.password,
                user.email
            ))
            return {"message": "User inserted successfully"}
        except Exception as e:
            return {"error": str(e)}


    def login_user(self, user):
        try:
            sql = """
                SELECT * FROM users WHERE email = %s
            """
            query_user = self.db.fetch_one(sql, (user.email,))

            if not query_user:
                return {"error": "Invalid email"}
            
            obj_user = {
                "name": query_user[1],
                "password": query_user[2],
                "email": query_user[3]
            }

            if obj_user["password"] != user.password:
                return {"error": "Invalid password"}
            return obj_user
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
    

    def delete_user(self, user):
        try:
            sql = """
                DELETE FROM users WHERE email = %s
            """
            self.db.execute_query(sql, (user.email,))
            return {"message": "User deleted successfully"}
        except Exception as e:
            return {"error": str(e)}
    
    def drop_table(self, table_name):
        try:
            self.db.drop_table(table_name)
            return {"message": f"Table {table_name} dropped successfully"}
        except Exception as e:
            return {"error": str(e)}

    def close(self):
        self.db.close()