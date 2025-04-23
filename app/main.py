from fastapi import FastAPI
from app.db_manager import DBManager

app = FastAPI()

@app.get("/")
def read_root():
    try:
        db = DBManager()
        sql = """
            INSERT INTO users (name, password, email, bus_line, bus_stop, open_time, close_time)
            VALUES ('Gabriel Brandão', 'senha123', 'email@email.com', '855', 'Praia do Flamengo, 200', '14:00:00', '16:00:00')
        """
        db.execute_query(sql)

        sql = """
            SELECT * FROM users
        """
        db.execute_query(sql)
        users = db.fetch_all(sql)
        print(users)
        db.close()
        return {"users": users}
    except Exception as e:
        return {"error": str(e)}
