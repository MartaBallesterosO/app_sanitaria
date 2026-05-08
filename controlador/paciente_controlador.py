class PacienteControlador:
    def __init__(self, app):
        self.app = app

    def guardar_paciente(self, esquema_paciente):
        datos = esquema_paciente.serializar()
        print(f"DEBUG: Intentando guardar estos datos: {datos}") 
        return self.app.modelo.insertar_paciente(datos)

    def guardar_tension(self, esquema_tension):
        datos = esquema_tension.serializar()
        return self.app.modelo.insertar_tension(datos)

    def eliminar_paciente(self, id_mongo):
        return self.app.modelo.borrar_paciente(id_mongo)
    
    def obtener_tensiones(self, id_paciente):

        return self.app.modelo.obtener_tensiones_por_paciente(id_paciente)
    def mostrar_pagina(self, nombre):
        self.app.mostrar_pagina(nombre)
    def actualizar_listado_en_vista(self):
        """Pide al modelo los datos nuevos y actualiza la tabla de la vista"""
        datos_actualizados = self.app.modelo.listar_pacientes()

        self.app.paginas["PaginaPacientes"].actualizar_tabla(datos_actualizados)