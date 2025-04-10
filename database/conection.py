from pymongo import MongoClient
from local_setings import MONGO_URL

# URI de conexión a MongoDB (ajústala según tu configuración)
MONGO_URI = MONGO_URL

# Crear la conexión
client = MongoClient(MONGO_URI)

# Seleccionar la base de datos
db = client["Trytri"]

# Seleccionar la colección
collection = db["usuario"]

