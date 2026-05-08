import tkinter as tk
from modelo.conexion import Conexion
from modelo.consultas import Consultas
from controlador.paciente_controlador import PacienteControlador
from vista.paginas import LayoutPrincipal, PaginaPacientes, VistaAltaPaciente

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("App Sanitaria")
        self.modelo = Consultas(Conexion())
        self.controlador = PacienteControlador(self)
        self.layout = LayoutPrincipal(self, self.controlador)
        self.layout.pack(fill="both", expand=True)
        self.paginas = {}
        for P in (PaginaPacientes, VistaAltaPaciente):
            p = P(self.layout.cuerpo, self.controlador)
            self.paginas[P.__name__] = p
            p.grid(row=0, column=0, sticky="nsew")
        self.mostrar_pagina("PaginaPacientes")

    
    def mostrar_pagina(self, nombre):
        p = self.paginas[nombre]

        if nombre == "PaginaPacientes":
            datos = self.modelo.listar_pacientes()
            p.actualizar_tabla(datos)
        p.tkraise()

if __name__ == "__main__":
    App().mainloop()