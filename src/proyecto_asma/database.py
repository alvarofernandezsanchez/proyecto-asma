import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()
password = os.getenv("DB_PASSWORD")

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=password,
    database="MUIAAP"
)