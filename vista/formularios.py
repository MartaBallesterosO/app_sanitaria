import tkinter as tk
from tkinter import ttk, messagebox
from esquemas.pacientes_esquema import PacienteAltaEsquema

class VistaAltaPaciente(tk.Frame):
    def __init__(self, parent, controlador):
        super().__init__(parent)
        self.controlador = controlador
        
        tk.Label(self, text="NUEVO PACIENTE", font=("Arial", 14, "bold")).pack(pady=20)
        
        form = tk.Frame(self)
        form.pack(pady=10)
        
        # Campos
        tk.Label(form, text="Nombre:").grid(row=0, column=0, sticky="e")
        self.ent_nom = ttk.Entry(form); self.ent_nom.grid(row=0, column=1, pady=5)
        
        tk.Label(form, text="Apellido:").grid(row=1, column=0, sticky="e")
        self.ent_ape = ttk.Entry(form); self.ent_ape.grid(row=1, column=1, pady=5)

        tk.Label(form, text="Género:").grid(row=2, column=0, sticky="e")
        self.combo_gen = ttk.Combobox(form, values=["masculino", "femenino", "otro"], state="readonly")
        self.combo_gen.current(0); self.combo_gen.grid(row=2, column=1, pady=5)

        tk.Label(form, text="F. Nacimiento (AAAA-MM-DD):").grid(row=3, column=0, sticky="e")
        self.ent_fec = ttk.Entry(form); self.ent_fec.insert(0, "2000-01-01")
        self.ent_fec.grid(row=3, column=1, pady=5)

        # Botones
        btns = tk.Frame(self)
        btns.pack(pady=20)
        ttk.Button(btns, text="Guardar", command=self.enviar_datos).pack(side="left", padx=5)
        ttk.Button(btns, text="Cancelar", command=lambda: self.controlador.mostrar_pagina("PaginaPacientes")).pack(side="left", padx=5)

    def enviar_datos(self):
        try:
            # 1. Creamos el ESQUEMA 
            nuevo_paciente = PacienteAltaEsquema(
                nombre=self.ent_nom.get(),
                apellido=self.ent_ape.get(),
                genero=self.combo_gen.get(),
                fecha_nacimiento=self.ent_fec.get()
            )
            
            # 2. Se lo pasamos al CONTROLADOR
            self.controlador.guardar_paciente(nuevo_paciente)
            
            messagebox.showinfo("Éxito", "Paciente guardado")
            self.controlador.app.mostrar_pagina("PaginaPacientes") 
            
        except ValueError as e:
            messagebox.showerror("Error de Validación", str(e))