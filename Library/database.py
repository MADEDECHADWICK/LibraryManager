import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST","localhost"),
            database=os.getenv("DB_NAME","library"),
            user=os.getenv("DB_USER","root"),
            password=os.getenv("DB_PASSWORD","123456")
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None