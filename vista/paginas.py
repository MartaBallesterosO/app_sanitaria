import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


from esquemas.pacientes_esquema import PacienteAltaEsquema
from esquemas.tensiones_esquema import TensionEsquema

class LayoutPrincipal(tk.Frame):
    def __init__(self, parent, controlador):
        super().__init__(parent)
        self.controlador = controlador
        
        # Cabecera
        self.cab = tk.Frame(self, bg="#2c3e50", height=60)
        self.cab.pack(side="top", fill="x")
        tk.Label(self.cab, text="SISTEMA MÉDICO - GESTIÓN SANITARIA", fg="white", 
                 font=("Arial", 14, "bold"), bg="#2c3e50").pack(pady=15)
        
        # Contenedor central 
        self.cuerpo = tk.Frame(self)
        self.cuerpo.pack(side="top", fill="both", expand=True)

class PaginaPacientes(tk.Frame):
    def __init__(self, parent, controlador):
        super().__init__(parent)
        self.controlador = controlador
        
        tk.Label(self, text="PANEL DE PACIENTES", font=("Arial", 16, "bold")).pack(pady=10)
        tk.Label(self, text="(Doble clic para ver historial de tensiones)", 
                 font=("Arial", 9, "italic"), fg="gray").pack()
        
        # Tabla de pacientes
        self.tabla = ttk.Treeview(self, columns=("N", "A", "G", "F"), show="headings")
        self.tabla.heading("N", text="Nombre")
        self.tabla.heading("A", text="Apellido")
        self.tabla.heading("G", text="Género")
        self.tabla.heading("F", text="F. Nacimiento")
        self.tabla.pack(fill="both", expand=True, padx=30, pady=10)

        # EVENTO: Doble clic para abrir el historial
        self.tabla.bind("<Double-1>", self.ver_tensiones_paciente)

        # Botonera
        frame_btns = tk.Frame(self)
        frame_btns.pack(pady=20)

        ttk.Button(frame_btns, text="+ Nuevo Paciente", 
                   command=lambda: self.controlador.mostrar_pagina("VistaAltaPaciente")).pack(side="left", padx=10)
        
        ttk.Button(frame_btns, text="- Eliminar Seleccionado", 
                   command=self.borrar_paciente).pack(side="left", padx=10)
        
        ttk.Button(frame_btns, text="⚡ Registrar Tensión", 
                   command=self.abrir_formulario_tension).pack(side="left", padx=10)

    def actualizar_tabla(self, datos):
        for i in self.tabla.get_children():
            self.tabla.delete(i)
        
        for p in datos:
            # 1. BUSCAR EL GÉNERO 
            genero = p.get("genero") or p.get("género") or "S/N"

            # 2. BUSCAR LA FECHA 
            fec = p.get("fecha_nacimiento") or p.get("fechaNacimiento") or ""
            
            fec_limpia = "S/N"
            try:
                if isinstance(fec, dict):

                    if '$date' in fec:
                        val = fec['$date']
                        if isinstance(val, dict) and '$numberLong' in val:
                            ms = int(val['$numberLong'])
                            fec_limpia = datetime.fromtimestamp(ms / 1000.0).strftime('%Y-%m-%d')
                        else:
                            fec_limpia = str(val)[:10]
                    elif '$numberLong' in fec:
                        ms = int(fec['$numberLong'])
                        fec_limpia = datetime.fromtimestamp(ms / 1000.0).strftime('%Y-%m-%d')
                else:
                    # Si es texto normal o datetime de Python
                    fec_limpia = str(fec)[:10]
            except:
                fec_limpia = "Error"

            # 3. INSERTAR EN LA TABLA
            self.tabla.insert("", "end", values=(
                p.get("nombre", ""), 
                p.get("apellido", ""), 
                genero, 
                fec_limpia
            ), tags=(str(p.get("_id")),))
    def ver_tensiones_paciente(self, event):
        """Captura el ID del paciente y abre la ventana de historial"""
        seleccion = self.tabla.selection()
        if not seleccion: return
        
        id_p = self.tabla.item(seleccion)['tags'][0]
        nombre = f"{self.tabla.item(seleccion)['values'][0]} {self.tabla.item(seleccion)['values'][1]}"
        
        # Pedimos los datos al controlador
        lista_t = self.controlador.obtener_tensiones(id_p)
        
        if lista_t:
            VentanaTensiones(self, nombre, lista_t)
        else:
            messagebox.showinfo("Información", f"{nombre} no tiene tensiones registradas.")

    def borrar_paciente(self):
        seleccion = self.tabla.selection()
        if not seleccion: return
        
        if messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar este paciente?"):
            id_p = self.tabla.item(seleccion)['tags'][0]
            self.controlador.eliminar_paciente(id_p)
            self.controlador.mostrar_pagina("PaginaPacientes")

    def abrir_formulario_tension(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Selecciona un paciente primero")
            return
            
        id_p = self.tabla.item(seleccion)['tags'][0]
        nombre = self.tabla.item(seleccion)['values'][0]
        VentanaNuevaTension(self, id_p, nombre, self.controlador)

class VistaAltaPaciente(tk.Frame):
    def __init__(self, parent, controlador):
        super().__init__(parent)
        self.controlador = controlador
        
        tk.Label(self, text="ALTA DE NUEVO PACIENTE", font=("Arial", 14, "bold")).pack(pady=20)

        # Formulario
        tk.Label(self, text="Nombre:").pack()
        self.ent_nom = ttk.Entry(self); self.ent_nom.pack(pady=5)

        tk.Label(self, text="Apellido:").pack()
        self.ent_ape = ttk.Entry(self); self.ent_ape.pack(pady=5)

        tk.Label(self, text="Género:").pack()
        self.combo_gen = ttk.Combobox(self, values=["masculino", "femenino", "otro"], state="readonly")
        self.combo_gen.current(0); self.combo_gen.pack(pady=5)

        tk.Label(self, text="Fecha Nacimiento:").pack()
        self.ent_fec = ttk.Entry(self); self.ent_fec.insert(0, "YYYY-MM-DD"); self.ent_fec.pack(pady=5)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="Guardar", command=self.intentar_guardar).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="Cancelar", 
                   command=lambda: self.controlador.mostrar_pagina("PaginaPacientes")).pack(side="left", padx=10)

    def intentar_guardar(self):
        try:
            esquema = PacienteAltaEsquema(
                nombre=self.ent_nom.get(),
                apellido=self.ent_ape.get(),
                genero=self.combo_gen.get(),
                fecha_nacimiento=self.ent_fec.get()
            )
            
            self.controlador.guardar_paciente(esquema)
            messagebox.showinfo("Éxito", "Paciente guardado correctamente")
            

            self.controlador.actualizar_listado_en_vista() 
            self.controlador.mostrar_pagina("PaginaPacientes")

        except Exception as e:
            messagebox.showerror("Error de Validación", str(e))

# VENTANAS EMERGENTES 
class VentanaTensiones(tk.Toplevel):
    def __init__(self, parent, nombre, datos):
        super().__init__(parent)
        self.title(f"Historial: {nombre}")
        self.geometry("500x350")
        
        tk.Label(self, text=f"Historial de {nombre}", font=("Arial", 12, "bold")).pack(pady=10)
        
        tabla = ttk.Treeview(self, columns=("F", "V", "E"), show="headings")
        tabla.heading("F", text="Fecha")
        tabla.heading("V", text="Valoración")
        tabla.heading("E", text="Estado")
        tabla.pack(fill="both", expand=True, padx=20, pady=10)

        for d in datos:
            # Formateamos la fecha si viene de MongoDB
            fec = str(d.get("fecha", ""))[:16]
            tabla.insert("", "end", values=(fec, d.get("valoracion", ""), d.get("estado", "")))

class VentanaNuevaTension(tk.Toplevel):
    def __init__(self, parent, id_p, nombre, controlador):
        super().__init__(parent)
        self.controlador = controlador
        self.id_p = id_p
        self.title("Nueva Tensión")
        self.geometry("300x300")

        tk.Label(self, text=f"Registrar para: {nombre}", font=("Arial", 9, "bold")).pack(pady=10)
        
        tk.Label(self, text="Valoración:").pack()
        self.combo = ttk.Combobox(self, values=["Normal", "Elevada", "Hipertensión Etapa 1", "Hipertensión Etapa 2"], state="readonly")
        self.combo.current(0); self.combo.pack(pady=5)

        tk.Label(self, text="Estado:").pack()
        self.ent_est = ttk.Entry(self); self.ent_est.insert(0, "final"); self.ent_est.pack(pady=5)

        ttk.Button(self, text="Guardar", command=self.enviar_tension).pack(pady=20)

    def enviar_tension(self):
        try:
            # VALIDACIÓN CON PYDANTIC
            esquema_t = TensionEsquema(
                id_paciente=self.id_p,
                valoracion=self.combo.get(),
                estado=self.ent_est.get()
            )
            self.controlador.guardar_tension(esquema_t)
            messagebox.showinfo("Éxito", "Tensión registrada")
            self.destroy() # Cerramos la ventana emergente
        except Exception as e:
            messagebox.showerror("Error", str(e))