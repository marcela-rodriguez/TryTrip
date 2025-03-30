from pymongo import MongoClient

# URI de conexión a MongoDB (ajústala según tu configuración)
MONGO_URI = "mongodb://localhost:27017"

# Crear la conexión
client = MongoClient(MONGO_URI)

# Seleccionar la base de datos
db = client["Trytri"]

# Seleccionar la colección
collection = db["usuario"]

