from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()  # Carga las variables desde el archivo .env

# URI de conexión a MongoDB (ajústala según tu configuración)
MONGO_URL = os.getenv("MONGO_URL")

# Crear la conexión
client = MongoClient(MONGO_URL)

# Seleccionar la base de datos
db = client["Trytri"]

# Seleccionar la colección
collection = db["usuario"]

