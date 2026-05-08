from bson.objectid import ObjectId

class Consultas:
    def __init__(self, conexion):
        self.db = conexion.db

    def listar_pacientes(self):
        return list(self.db.pacientes.find())

    def insertar_paciente(self, datos):
        return self.db.pacientes.insert_one(datos)

    def borrar_paciente(self, id_p):
        return self.db.pacientes.delete_one({'_id': ObjectId(id_p)})

    def obtener_tensiones_por_paciente(self, id_paciente):
        """Busca todas las tensiones que tengan el ID de este paciente"""
        try:
            query = {"id_paciente": str(id_paciente)} 

            return list(self.db.tensiones.find(query).sort("fecha", -1))
        except Exception as e:
            print(f"Error en el modelo al buscar tensiones: {e}")
            return []
    def insertar_tension(self, datos):
        return self.db.tensiones.insert_one(datos)
    
    def insertar_paciente(self, datos):
        try:
            resultado = self.db.pacientes.insert_one(datos)
            print(f"✅ Paciente insertado con ID: {resultado.inserted_id}")
            return True
        except Exception as e:
            print(f"❌ Error al insertar en MongoDB: {e}")
            return False