import os
import mysql.connector
from dotenv import load_dotenv

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
        self.connection.commit()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_bus_relation (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                bus_line VARCHAR(255) NOT NULL,
                bus_stop VARCHAR(255) NOT NULL,
                open_time TIME NOT NULL,
                close_time TIME NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
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
