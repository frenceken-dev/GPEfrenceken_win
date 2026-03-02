import tkinter as tk
from tkinter import messagebox
from recursos import configurar_toplevel, crear_boton
from databasemanager import DataBaseManager

db_connect = DataBaseManager()
class CrearEmpaques():
    def __init__(self, root, imagen_panel_tk, volver_menu):
        self.root = root
        self.imagen_panel_tk = imagen_panel_tk
        self.volver_menu = volver_menu
        self.precio = []
        self.cantidad = []
        
        
    def limpiar_pantalla(self):
        for widget in self.root.winfo_children():
            widget.destroy()
            
    def iniciar_intefaz(self):
        self.limpiar_pantalla()
        self.toplevel_pantalla()
        
    def toplevel_pantalla(self):
        """Crea un toplevel para crear el tipo de empaque"""
        
        self.emp_frame = tk.Frame(self.root, bg="#a0b9f0", width=800, height=800)
        self.emp_frame.pack(fill=tk.BOTH, expand=True)
        #configurar_toplevel(self.emp_frame, titulo="Gestión de Empaques:", color_fondo="#101113")
        
        self.frame_menu = tk.Frame(self.emp_frame, bg="#2C3E50", width=200, height=800, bd=3, relief="solid")
        self.frame_menu.pack(side=tk.LEFT, fill=tk.Y)
        self.frame_menu.pack_propagate(False)
        
        self.crear_logo_panel()
        
        # Frame de título
        self.frame_titulo = tk.Frame(self.emp_frame, bg="#a0b9f0")
        self.frame_titulo.pack(side=tk.TOP, fill=tk.X, pady=15)

        # Título
        self.title_label = tk.Label(
            self.frame_titulo,
            text="Registrar Material de Empaque",
            font=("Arial", 16, "bold"),
            bg="#a0b9f0",
            fg="#2C3E50"
        )
        self.title_label.pack(pady=15)
        
        self.frame_campos = tk.Frame(self.emp_frame, bg="#a0b9f0")
        self.frame_campos.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        # Configurar el frame_campos para centrar el contenido
        self.frame_campos.grid_columnconfigure(0, weight=1)  # Columna vacía a la izquierda
        self.frame_campos.grid_columnconfigure(1, weight=1)  # Columna para etiquetas
        self.frame_campos.grid_columnconfigure(2, weight=1)  # Columna para entradas
        self.frame_campos.grid_columnconfigure(3, weight=1)  # Columna vacía a la derecha

        # Campos de entrada (centrados)
        tk.Label(self.frame_campos, text="Código para este Empaque:", bg="#a0b9f0", fg="#2C3E50").grid(row=0, column=1, pady=5, sticky="ns")
        codigo_entry = tk.Entry(self.frame_campos, width=25)
        codigo_entry.grid(row=1, column=1, sticky="ns")

        tk.Label(self.frame_campos, text="Nombre de este Empaque:", bg="#a0b9f0", fg="#2C3E50").grid(row=2, column=1, pady=5, sticky="ns")
        nombre_entry = tk.Entry(self.frame_campos, width=25)
        nombre_entry.grid(row=3, column=1, sticky="ns")

        tk.Label(self.frame_campos, text="Tamaño del empaque:", bg="#a0b9f0", fg="#2C3E50").grid(row=4, column=1, pady=5, sticky="ns")
        tamaño_entry = tk.Entry(self.frame_campos, width=25)
        tamaño_entry.grid(row=5, column=1, sticky="ns")

        tk.Label(self.frame_campos, text="Cantidad del empaque:", bg="#a0b9f0", fg="#2C3E50").grid(row=6, column=1, pady=5, sticky="ns")
        cantidad_entry = tk.Entry(self.frame_campos, width=25)
        cantidad_entry.grid(row=7, column=1, sticky="ns")

        tk.Label(self.frame_campos, text="Precio total:", bg="#a0b9f0", fg="#2C3E50").grid(row=8, column=1, pady=5, sticky="ns")
        precio_entry = tk.Entry(self.frame_campos, width=25)
        precio_entry.grid(row=9, column=1, sticky="ns")

        # Botón para guardar (centrado)
        boton_guardar_material = crear_boton(
            self.frame_campos,
            texto="Guardar Material",
            ancho=30,
            alto=30,
            color_fondo="#4283fa",
            color_texto="white",
            font=("Arial", 11, "bold"),
            comando=lambda: self.comprobar_datos(codigo_entry.get(), 
                                                nombre_entry.get(),
                                                tamaño_entry.get(),
                                                cantidad_entry.get(),
                                                precio_entry.get())
        )
        boton_guardar_material.grid(row=10, column=1, pady=15)
        
        boton_cerrar = crear_boton(
            self.frame_menu,
            texto="Volver",
            ancho=30,
            alto=30,
            color_fondo="#913131",
            color_texto="white",
            font=("Arial", 11, "bold"),
            comando=self.cerrar_ventana
        )
        boton_cerrar.pack(side="bottom", padx=5)
        
    def crear_logo_panel(self):
        frame_imagen_panel = tk.Frame(self.frame_menu, bg="#2C3E50", height=70)
        frame_imagen_panel.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

        if self.imagen_panel_tk:
            label_imagen = tk.Label(frame_imagen_panel, image=self.imagen_panel_tk, bg="#2C3E50")
            label_imagen.pack(side=tk.LEFT, padx=70)
        else:
            label_texto = tk.Label(frame_imagen_panel, text="Ikigai", font=("Arial", 10), bg="#2C3E50")
            label_texto.pack(side=tk.LEFT, padx=70)
            
    def comprobar_datos(self, codigo_entry, nombre_entry, tamaño_entry, cantidad_entry, precio_entry):
        """Comprobar que todos los campos contengan información"""
        if not codigo_entry or not nombre_entry or not tamaño_entry or not cantidad_entry or not precio_entry:
            messagebox.showerror("⚠️ Error", "Por favor Complete todos los Campos.")
            return
        
        self.cantidad = float(cantidad_entry)
        if self.cantidad <= 0:
            messagebox.showerror("⚠️ Error", "La Cantidad no puede ser cero (0)")
            return
        
        self.precio = float(precio_entry)
        if self.precio <= 0:
            messagebox.showerror("⚠️ Error", "El precio Total no puede ser Cero (0)")
            return
        
        self.guardar_paquete(codigo_entry, nombre_entry, tamaño_entry, cantidad_entry, precio_entry)
        
        
    def guardar_paquete(self, codigo, nombre, tamaño, cantidad, precio):
        """Se Calcula el precio unitario y se guardan los datos en la base de datos.

        Args:
            codigo_entry (str): Código unico del Empaque.
            nombre_entry (str): Nombre del Empaque.
            tama (str): describe el tamaño del Empaque.
            cantidad_entry (float): Cantida que se guarda.
            precio_entry (float): El precio total.
        """
        cantidad_int = float(cantidad)
        precio_int = float(precio)
        print(f"La Cantidad ahora es de tipo {type(cantidad_int)}")
        print(f"El Precio ahora es de tipo {type(precio_int)}")
        costo_unitario = float(precio_int / cantidad_int)
        
        exito, mensaje = db_connect.insertar_empaque(codigo, nombre, tamaño, cantidad, precio, round(costo_unitario, 2))
        
        if exito:
            messagebox.showinfo("✅ Guardado", f"{mensaje}")
        else:
            messagebox.showerror("⚠️ Error", f"{mensaje}")
            
    def cerrar_ventana(self):
        self.emp_frame.destroy()
        self.volver_menu()
        