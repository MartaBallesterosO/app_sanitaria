from pymongo import MongoClient

class Conexion:
    def __init__(self):
        try:
            self.client = MongoClient('mongodb://localhost:27017/')
            
            self.db = self.client['gestion_sanitaria'] 
            
            self.client.server_info() 
            print("✅ Conexión a MongoDB establecida con éxito")
            
        except Exception as e:
            print(f"❌ Error al conectar a MongoDB: {e}")
            self.db = None