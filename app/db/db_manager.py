import os
import mysql.connector
from dotenv import load_dotenv
from .insert_bus_data import insert_routes, insert_stops, insert_route_stops

load_dotenv()

class DBManager:
    seeded = False

    def __init__(self):
        self.connection = self.get_connection()
        self.cursor = self.connection.cursor()

        if not DBManager.seeded:
            self.seed_database()
            DBManager.seeded = True

    def seed_database(self):
        # Create a table if it doesn't exist
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL UNIQUE
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS routes (
                route_id VARCHAR(20) NOT NULL PRIMARY KEY,
                route_short_name VARCHAR(20) NOT NULL,
                route_long_name VARCHAR(255) NOT NULL
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS stops (
                stop_id VARCHAR(20) NOT NULL PRIMARY KEY,
                stop_name VARCHAR(255) NOT NULL,
                stop_lat DECIMAL(9, 6) NOT NULL,
                stop_lon DECIMAL(9, 6) NOT NULL
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS route_stops (
                id INT AUTO_INCREMENT PRIMARY KEY,
                route_id VARCHAR(20) NOT NULL,
                stop_id VARCHAR(20) NOT NULL,
                FOREIGN KEY (route_id) REFERENCES routes(route_id),
                FOREIGN KEY (stop_id) REFERENCES stops(stop_id)
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_bus_relation (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                route_stop_id INT NOT NULL,
                open_time TIME NOT NULL,
                close_time TIME NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (route_stop_id) REFERENCES route_stops(id)
            )
        """)

        routes_result = self.fetch_one("SELECT COUNT(*) as total FROM routes")
        if routes_result:
            routes_total = routes_result[0]
        else:
            routes_total = 0

        if routes_total == 0:
            insert_routes(self)
        
        stops_result = self.fetch_one("SELECT COUNT(*) as total FROM stops")
        if stops_result:
            stops_total = stops_result[0]
        else:
            stops_total = 0

        if stops_total == 0:
            insert_stops(self)
        
        route_stops_result = self.fetch_one("SELECT COUNT(*) as total FROM route_stops")
        if route_stops_result:
            route_stops_total = route_stops_result[0]
        else:
            route_stops_total = 0

        if route_stops_total == 0:
            insert_route_stops(self)

        self.connection.commit()

    def get_connection(self):
        return mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE"),
            port=int(os.getenv("MYSQL_PORT", 3306)),
        )

    def close(self):
        self.cursor.close()
        self.connection.close()

    def execute_query(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.connection.rollback()
    
    def execute_many(self, query, data):
        with self.connection.cursor() as cursor:
            cursor.executemany(query, data)
        self.connection.commit()

    def fetch_all(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None
    
    def fetch_one(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchone()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None

    def drop_table(self, table_name):
        try:
            self.cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
            self.connection.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.connection.rollback()
