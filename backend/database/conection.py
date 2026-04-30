from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()  # Carga las variables desde el archivo .env
user = os.getenv("MONGO_USER")
password = os.getenv("MONGO_PASS")
host = os.getenv("MONGO_HOST")
port = os.getenv("MONGO_PORT")
# URI de conexión a MongoDB (ajústala según tu configuración)
MONGO_URL = f"mongodb://{user}:{password}@{host}:{port}/"

# Crear la conexión
client = MongoClient(MONGO_URL)

# Seleccionar la base de datos
db = client["Trytri"]

# Seleccionar la colección
collection = db["usuario"]

