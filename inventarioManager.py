import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from recursos import crear_boton, configurar_toplevel
from decimal import Decimal, getcontext
from databasemanager import DataBaseManager
from empaqueManager import CrearEmpaques
import json


db_connect = DataBaseManager()

class InventarioManager:
    def __init__(self, root, imagen_panel_tk, volver_menu):
        self.root = root
        self.imagen_panel_tk = imagen_panel_tk
        self.volver_menu = volver_menu
        self.id_usuario_creador = None
        self.nombre_usuario_creador = None
        self.materiales_temporales = []
        self.empaques_temporales = []
        self.materia_prima = []
        self.datos_factura = {
            "proveedor": "",
            "numero_factura": "",
            "fecha": ""
        }
        self.total_actual = []
        self.exite_codigo = False
        self.db_connect = DataBaseManager()  # Asegúrate de que DataBaseManager esté importado
        self.agregar_empaque = CrearEmpaques(root, imagen_panel_tk, volver_menu)
        self.son_metros = None
        self.emb_metros = None

    def limpiar_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def usuario_actual(self, usuario):
            """Obtiene el usuario actual y su ID."""
            self.nombre_usuario_creador = usuario
            print(f"EL USUARIO EN LA CLASE INVENTARIO ES: {usuario}")
            if self.nombre_usuario_creador:
                self.id_usuario_creador = db_connect.id_usuario_nombre_actual(self.nombre_usuario_creador)
                print(f"EL ID DEL USUARIO ACTUAL ES: {self.id_usuario_creador}")
                #return self.id_usuario_creador[0][0], self.nombre_usuario_creador
    
    def iniciar_interfaz(self):
        self.limpiar_frame()
        self.crear_interfaz_principal()
        self.crear_formulario_factura()
        self.crear_botones_accion()

    def crear_interfaz_principal(self):
        # Frame principal
        self.frame = tk.Frame(self.root, bg="#a0b9f0", width=800, height=600)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Panel izquierdo
        self.frame_menu = tk.Frame(self.frame, bg="#2C3E50", width=200, height=800, bd=3, relief="solid")
        self.frame_menu.pack(side=tk.LEFT, fill=tk.Y)
        self.frame_menu.pack_propagate(False)

        # Imagen del Logo para el panel izquierdo
        self.crear_logo_panel()

        # Frame inferior dentro del menú lateral
        self.frame_inferior = tk.Frame(self.frame_menu, bg="#2C3E50")
        self.frame_inferior.pack(side="bottom", fill="x", pady=20)

        # Frame de título
        self.frame_titulo = tk.Frame(self.frame, bg="#a0b9f0")
        self.frame_titulo.pack(side=tk.TOP, fill=tk.X, pady=15)

        # Título
        self.title_label = tk.Label(
            self.frame_titulo,
            text="Aumento de inventario por facturas",
            font=("Arial", 16, "bold"),
            bg="#a0b9f0",
            fg="#2C3E50"
        )
        self.title_label.pack(pady=15)

    def crear_logo_panel(self):
        frame_imagen_panel = tk.Frame(self.frame_menu, bg="#2C3E50", height=70)
        frame_imagen_panel.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

        if self.imagen_panel_tk:
            label_imagen = tk.Label(frame_imagen_panel, image=self.imagen_panel_tk, bg="#2C3E50")
            label_imagen.pack(side=tk.LEFT, padx=70)
        else:
            label_texto = tk.Label(frame_imagen_panel, text="Ikigai", font=("Arial", 10), bg="#2C3E50")
            label_texto.pack(side=tk.LEFT, padx=70)

    def crear_formulario_factura(self):
        self.form_frame = tk.Frame(self.frame, bg="#a0b9f0", padx=20, pady=20)
        self.form_frame.place(relx=0.5, rely=0.1, anchor=tk.N)

        # Campos de la factura
        tk.Label(self.form_frame, text="Proveedor:", bg="#a0b9f0").grid(row=0, column=0, sticky="e")
        self.proveedor_combobox = ttk.Combobox(self.form_frame, width=28)
        self.proveedor_combobox.grid(row=0, column=1, pady=5)

        # Obtener nombres de proveedores desde BD
        self.actualizar_proveedores()

        # Vincular evento para filtrar proveedores
        self.proveedor_combobox.bind('<KeyRelease>', self.actualizar_opciones_proveedores)

        # Campos de número de factura y fecha
        tk.Label(self.form_frame, text="Número de Factura:", bg="#a0b9f0").grid(row=1, column=0, sticky="e")
        self.factura_entry = tk.Entry(self.form_frame, width=30)
        self.factura_entry.grid(row=1, column=1, pady=5)

        tk.Label(self.form_frame, text="Fecha (DD.MM.AAAA):", bg="#a0b9f0").grid(row=2, column=0, sticky="e")
        self.fecha_entry = tk.Entry(self.form_frame, width=30)
        self.fecha_entry.grid(row=2, column=1, pady=5)

    def actualizar_proveedores(self):
        self.proveedor_combobox["values"] = db_connect.obtener_proveedores()

    def actualizar_opciones_proveedores(self, event):
        texto = self.proveedor_combobox.get()
        proveedores_filtrados = db_connect.obtener_nombres_()
        self.proveedor_combobox['values'] = proveedores_filtrados

    def crear_botones_accion(self):
        # Botón Agregar Material
        self.btn_agregar_material = crear_boton(
            self.form_frame,
            texto="Agregar Material",
            ancho=20,
            alto=25,
            color_fondo="#073EAD",
            color_texto="white",
            font=("Arial", 11, "bold"),
            comando=lambda: self.agregar_material_temporal(self.frame),
            state=tk.DISABLED
        )
        self.btn_agregar_material.grid(row=3, column=0, pady=20)
        
        self.btn_agregar_empaque = crear_boton(
            self.form_frame,
            texto="Agregar Empaque",
            ancho=20,
            alto=25,
            color_fondo="#9E6D3F",
            color_texto="white",
            font=("Arial", 11, "bold"),
            comando=lambda: self.agregar_empaque_temporal(self.frame),
            state=tk.DISABLED
        )
        self.btn_agregar_empaque.grid(row=3, column=1, pady=20)

        # Botón Mostrar Datos
        self.btn_mostrar_datos = crear_boton(
            self.form_frame,
            texto="Ver Datos Ingresados",
            ancho=20,
            alto=25,
            color_fondo="#324f98",
            color_texto="white",
            font=("Arial", 11, "bold"),
            comando=lambda: [
                self.actualizar_datos_factura(),
                self.mostrar_datos_ingresados()
            ],
            state=tk.DISABLED
        )
        self.btn_mostrar_datos.grid(row=3, column=2, pady=20)

        # Botón Guardar Factura
        self.btn_guardar_factura = crear_boton(
            self.form_frame,
            texto="Guardar Factura",
            ancho=20,
            alto=25,
            color_fondo="#4283fa",
            color_texto="white",
            font=("Arial", 11, "bold"),
            comando=lambda: [
                self.actualizar_datos_factura(),
                self.guardar_factura_y_materiales(self.frame)
            ],
            state=tk.DISABLED
        )
        self.btn_guardar_factura.grid(row=4, column=1, pady=20) # , columnspan=2
        
        self.btn_guardar_borrador = crear_boton(self.form_frame,
                    texto="Guardar borrador",
                    ancho=20,
                    alto=25,
                    color_fondo="#DEE90D",
                    color_texto="white",
                    font=("Arial", 11, "bold"),
                    hover_color="#2ECC71",
                    comando=lambda: self.guardar_borrador(),
                    state=tk.DISABLED
        )
        self.btn_guardar_borrador.grid(row=4, column=0, pady=20)  # columnspan=2,
        
        self.btn_ver_borradores = crear_boton(
            self.form_frame,
            texto="Ver Borradores",
            ancho=20,
            alto=25,
            color_fondo="#324f98",
            color_texto="white",
            font=("Arial", 11, "bold"),
            comando=self.mostrar_borradores_pendientes
        )
        self.btn_ver_borradores.grid(row=4, column=2, pady=20)

        # Botón Volver
        self.back_button = crear_boton(
            self.frame_inferior,
            texto="Volver",
            ancho=20,
            alto=25,
            color_fondo="#913131",
            color_texto="white",
            font=("Arial", 11, "bold"),
            comando=self.volver_menu
        )
        self.back_button.pack(side="bottom", padx=30, pady=30)

        # Vincular eventos para validar campos
        self.proveedor_combobox.bind("<<ComboboxSelected>>", lambda _: self.on_campo_cambiado())
        self.proveedor_combobox.bind("<KeyRelease>", lambda _: self.on_campo_cambiado())
        self.factura_entry.bind("<KeyRelease>", lambda _: self.on_campo_cambiado())
        self.fecha_entry.bind("<KeyRelease>", lambda _: self.on_campo_cambiado())

    def on_campo_cambiado(self):
        self.actualizar_estado_botones(
            self.proveedor_combobox.get(),
            self.factura_entry.get(),
            self.fecha_entry.get()
        )

    def actualizar_estado_botones(self, proveedor, num_factura, fecha):
        estado_activo = self.validar_campos_obligatorios(proveedor, num_factura, fecha)
        botones = [self.btn_agregar_material, self.btn_agregar_empaque, self.btn_mostrar_datos,
                self.btn_guardar_factura, self.btn_guardar_borrador, self.btn_ver_borradores]

        for boton in botones:
            if hasattr(boton, "set_state"):
                boton.set_state("normal" if estado_activo else "disabled")
            else:
                boton.config(state=tk.NORMAL if estado_activo else tk.DISABLED)

    def validar_campos_obligatorios(self, proveedor, num_factura, fecha):
        return proveedor.strip() != "" and num_factura.strip() != "" and fecha.strip() != ""
    
    def validar_fecha(self, fecha_str):
        try:
            dia, mes, anio = map(int, fecha_str.split('.'))
            datetime(day=dia, month=mes, year=anio)  # Lanza ValueError si la fecha no existe
            return True
        except ValueError:
            return False

    def actualizar_datos_factura(self):
        fecha_ingresada = self.fecha_entry.get()
        
        if self.validar_fecha(fecha_ingresada):
            self.datos_factura.update({
            "proveedor": self.proveedor_combobox.get(),
            "numero_factura": self.factura_entry.get(),
            "fecha": fecha_ingresada
        })
        
        else:
            messagebox.showerror("Error", "Fecha inválida. Usa DD.MM.AAAA y asegúrate de que exista.")
            return  #  NUEVO AGREGADO PARA PROBAR

    def agregar_material_temporal(self, frame_contenido):
        cod_materiales = self.db_connect.obtener_codigo_materiales()

        material_window = tk.Toplevel(frame_contenido)
        configurar_toplevel(material_window, titulo="Agregar Material", ancho_min=300, alto_min=390, color_fondo="#101113")

        # Campos para el material
        tk.Label(material_window, text="Código:", bg="#101113", fg="#ffffff").grid(row=0, column=0, padx=10, pady=5)
        codigo_entry = ttk.Combobox(material_window, values=cod_materiales, state="normal")
        codigo_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(material_window, text="Nombre:", bg="#101113", fg="#ffffff").grid(row=1, column=0, padx=10, pady=5)
        nombre_entry = tk.Entry(material_window)
        nombre_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(material_window, text="Tipo:", bg="#101113", fg="#ffffff").grid(row=2, column=0, padx=10, pady=5)
        tipo_entry = tk.Entry(material_window)
        tipo_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(material_window, text="Tamaño:", bg="#101113", fg="#ffffff").grid(row=3, column=0, padx=10, pady=5)
        tamaño_entry = tk.Entry(material_window)
        tamaño_entry.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(material_window, text="Color:", bg="#101113", fg="#ffffff").grid(row=4, column=0, padx=10, pady=5)
        color_entry = tk.Entry(material_window)
        color_entry.grid(row=4, column=1, padx=10, pady=5)

        tk.Label(material_window, text="Cantidad:", bg="#101113", fg="#ffffff").grid(row=5, column=0, padx=10, pady=5)
        stock_entry = tk.Entry(material_window)
        stock_entry.grid(row=5, column=1, padx=10, pady=5)

        tk.Label(material_window, text="Precio:", bg="#101113", fg="#ffffff").grid(row=6, column=0, padx=10, pady=5)
        precio_entry = tk.Entry(material_window)
        precio_entry.grid(row=6, column=1, padx=10, pady=5)
        
        tk.Label(material_window, text="Es por metro?:", bg="#101113", fg="#ffffff").grid(row=7, column=0, sticky="ns")
        es_por_metro = ttk.Combobox(material_window, values=["Si", "No"], state="readonly")
        es_por_metro.grid(row=7, column=1, sticky="ns", pady=5)

        def filtrar_codigos_key(event):
            texto_actual = codigo_entry.get().upper()
            codigos_filtrados = [codigo for codigo in cod_materiales if codigo.startswith(texto_actual)]
            codigo_entry["values"] = codigos_filtrados

        def filtrar_codigos_postcommand():
            texto_actual = codigo_entry.get().upper()
            codigos_filtrados = [codigo for codigo in cod_materiales if codigo.startswith(texto_actual)]
            codigo_entry["values"] = codigos_filtrados

        def auto_completar_entry(event):
            codigo = codigo_entry.get()
            nombre, tipo, tamaño, color = self.db_connect.obtener_material_por_codigo(codigo)

            if nombre or tipo or tamaño or color:
                nombre_entry.delete(0, tk.END)
                tipo_entry.delete(0, tk.END)
                tamaño_entry.delete(0, tk.END)
                color_entry.delete(0, tk.END)

                nombre_entry.insert(0, nombre)
                tipo_entry.insert(0, tipo)
                tamaño_entry.insert(0, tamaño)
                color_entry.insert(0, color)
        
        def es_por_metros(event):
            # Capturamos la selección del usuario.
            self.son_metros = es_por_metro.get()
            #print(f"Es <> {self.son_metros}")

        codigo_entry["postcommand"] = filtrar_codigos_postcommand
        codigo_entry.bind("<<ComboboxSelected>>", lambda event: auto_completar_entry(event))
        codigo_entry.bind("<KeyRelease>", lambda event: filtrar_codigos_key(event))
        es_por_metro.bind("<<ComboboxSelected>>", lambda event: es_por_metros(event))
        
        
        def guardar_material():
            codigo = codigo_entry.get()
            precio = self.convertir_a_float(precio_entry.get())
            cantidad = self.convertir_a_float(stock_entry.get())
            costo_unitario = precio / cantidad if cantidad != 0 else 0
            es_por_metro_ = es_por_metro.get()
            try:
                cantidad_float = float(cantidad)
                precio_float = float(precio)
            except ValueError:
                messagebox.showerror("⚠️ Error", "La cantidad y el precio deben ser números válidos.")
                return

            material = {
                "codigo": codigo_entry.get(),
                "nombre": nombre_entry.get(),
                "tipo": tipo_entry.get(),
                "tamaño": tamaño_entry.get(),
                "color": color_entry.get(),
                "stock": stock_entry.get(),
                "precio": precio_entry.get(),
                "costo_unitario": costo_unitario,
                "es_por_metro": es_por_metro_#self.son_metros  #es_por_metro.get() SI o NO
            }
            # Agregar en temporales para ver datos y insertar DB. 
            self.materiales_temporales.append(material)
            print(f"Inicio de guardado materiales temporales -> {self.materiales_temporales}")
            self.materia_prima.append(material)
            
            messagebox.showinfo("Éxito", "Material agregado temporalmente.")
            material_window.destroy()

        def borrar_campos():
            nombre_entry.delete(0, tk.END)
            tipo_entry.delete(0, tk.END)
            tamaño_entry.delete(0, tk.END)
            color_entry.delete(0, tk.END)
            es_por_metro.delete(0, tk.END)

        boton_guardar_material = crear_boton(
            material_window,
            texto="Guardar Material",
            ancho=30,
            alto=30,
            color_fondo="#4283fa",
            color_texto="white",
            font=("Arial", 11, "bold"),
            comando=guardar_material
        )
        boton_guardar_material.grid(row=8, column=0, columnspan=2, padx=15, pady=10)

        boton_borrar_campos = crear_boton(
            material_window,
            texto="Borrar Materiales",
            ancho=30,
            alto=30,
            color_fondo="#fa4242",
            color_texto="white",
            font=("Arial", 11, "bold"),
            comando=borrar_campos
        )
        boton_borrar_campos.grid(row=9, column=0, columnspan=2, padx=15, pady=10)
        
    def agregar_empaque_temporal(self, frame_contenido):
        cod_empaques = self.db_connect.codigo_empaques()  # Llega una tupla

        empaque_window = tk.Toplevel(frame_contenido)
        configurar_toplevel(empaque_window, titulo="Agregar Empaque", ancho_min=370, alto_min=340, color_fondo="#101113")

        # Campos de entrada (centrados)
        tk.Label(empaque_window, text="Código Empaque:", bg="#101113", fg="#ffffff").grid(row=1, column=0, sticky="ns")
        codigo_entry = ttk.Combobox(empaque_window, values=cod_empaques, state="normal")
        codigo_entry.grid(row=1, column=1, sticky="ns", pady=5)

        tk.Label(empaque_window, text="Nombre Empaque:", bg="#101113", fg="#ffffff").grid(row=2, column=0, sticky="ns")
        nombre_entry = tk.Entry(empaque_window, width=25)
        nombre_entry.grid(row=2, column=1, sticky="ns", pady=5)

        tk.Label(empaque_window, text="Tamaño empaque:", bg="#101113", fg="#ffffff").grid(row=3, column=0, sticky="ns")
        tamaño_entry = tk.Entry(empaque_window, width=25)
        tamaño_entry.grid(row=3, column=1, sticky="ns", pady=5)

        tk.Label(empaque_window, text="Cantidad empaque:", bg="#101113", fg="#ffffff").grid(row=4, column=0, sticky="ns")
        cantidad_entry = tk.Entry(empaque_window, width=25)
        cantidad_entry.grid(row=4, column=1, sticky="ns", pady=5)

        tk.Label(empaque_window, text="Precio total:", bg="#101113", fg="#ffffff").grid(row=5, column=0, sticky="ns")
        precio_entry = tk.Entry(empaque_window, width=25)
        precio_entry.grid(row=5, column=1, sticky="ns", pady=5)
        
        tk.Label(empaque_window, text="Es por metro?:", bg="#101113", fg="#ffffff").grid(row=6, column=0, sticky="ns")
        es_por_metro = ttk.Combobox(empaque_window, values=["Si", "No"], state="readonly")
        es_por_metro.grid(row=6, column=1, sticky="ns", pady=5)

        def filtrar_codigos_key(event):
            texto_actual = codigo_entry.get().upper()
            codigos_filtrados = [codigo for codigo in cod_empaques if codigo.startswith(texto_actual)] # ERROR AQUI
            codigo_entry["values"] = codigos_filtrados

        def filtrar_codigos_postcommand():
            texto_actual = codigo_entry.get().upper()
            codigos_filtrados = [codigo for codigo in cod_empaques if codigo.startswith(texto_actual)]
            codigo_entry["values"] = codigos_filtrados

        def auto_completar_entry(event):
            codigo = codigo_entry.get()
            nombre, tamaño, cantidad, precio = self.db_connect.selecciona_empaque_por_codigo (codigo) # Cambiar consulta

            if nombre or tamaño or cantidad or precio:
                nombre_entry.delete(0, tk.END)
                tamaño_entry.delete(0, tk.END)
                cantidad_entry.delete(0, tk.END)
                precio_entry.delete(0, tk.END)

                nombre_entry.insert(0, nombre)
                tamaño_entry.insert(0, tamaño)
                #cantidad_entry.insert(0, cantidad)
                #precio_entry.insert(0, precio)
        
        def emb_por_metro(event):
            # Capturamos la selección de usuario.
            self.emb_metros = es_por_metro.get()
            #print(f"Es <> {self.emb_metros}")

        codigo_entry["postcommand"] = filtrar_codigos_postcommand
        codigo_entry.bind("<<ComboboxSelected>>", lambda event: auto_completar_entry(event))
        codigo_entry.bind("<KeyRelease>", lambda event: filtrar_codigos_key(event))
        es_por_metro.bind("<<ComboboxSelected>>", lambda event: emb_por_metro(event))

        def guardar_material():
            codigo = codigo_entry.get()
            precio = self.convertir_a_float(precio_entry.get())
            cantidad = self.convertir_a_float(cantidad_entry.get())
            costo_unitario = precio / cantidad if cantidad != 0 else 0

            try:
                cantidad_float = float(cantidad)
                precio_float = float(precio)
            except ValueError:
                messagebox.showerror("⚠️ Error", "La cantidad y el precio deben ser números válidos.")
                return

            empaque = {
                "codigo": codigo_entry.get(),
                "nombre": nombre_entry.get(),
                "tamaño": tamaño_entry.get(),
                "stock": cantidad_entry.get(),
                "precio": precio_entry.get(),
                "costo_unitario": costo_unitario,
                "es_por_metro": self.emb_metros
            }
            # Agregar en temporales para ver datos y insertar DB.
            self.materiales_temporales.append(empaque)
            self.empaques_temporales.append(empaque)
            
            messagebox.showinfo("Éxito", "Material agregado temporalmente.")
            empaque_window.destroy()

        def borrar_campos():
            nombre_entry.delete(0, tk.END)
            tamaño_entry.delete(0, tk.END)
            cantidad_entry.delete(0, tk.END)
            precio_entry.delete(0, tk.END)
            es_por_metro.delete(0, tk.END)

        boton_guardar_material = crear_boton(
            empaque_window,
            texto="Guardar Empaque",
            ancho=30,
            alto=30,
            color_fondo="#4283fa",
            color_texto="white",
            font=("Arial", 11, "bold"),
            comando=guardar_material
        )
        boton_guardar_material.grid(row=7, column=0, columnspan=2, padx=15, pady=10)

        boton_borrar_campos = crear_boton(
            empaque_window,
            texto="Borrar Empaques",
            ancho=30,
            alto=30,
            color_fondo="#fa4242",
            color_texto="white",
            font=("Arial", 11, "bold"),
            comando=borrar_campos
        )
        boton_borrar_campos.grid(row=8, column=0, columnspan=2, padx=15, pady=10)


    def convertir_a_float(self, valor_str):
        """Recibe un valor numerico y lo convierte en un dato float, sino retora 0.0"""
        if not valor_str or valor_str == "" or valor_str is None:
            return 0.0
        
        try:
            valor_str = str(valor_str).replace(",", ".")
            return float(valor_str)
        except ValueError:
            messagebox.showerror(f"⚠️ Error: '{valor_str}' no es un número válido.")
            return 0.0

    def limpiar_campos(self, frame_contenido):
        for widget in frame_contenido.winfo_children():
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, tk.Entry):
                        child.delete(0, tk.END)
                    elif isinstance(child, ttk.Combobox):
                        child.set('')

    def guardar_factura_y_materiales(self, frame_contenido):
        
        if not self.datos_factura["proveedor"] or not self.datos_factura["numero_factura"] or not self.datos_factura["fecha"]:
            messagebox.showerror("⚠️ Error", "Faltan datos de la factura (proveedor, número o fecha).")
            return

        if not self.materiales_temporales:
            messagebox.showerror("⚠️ Error", "No se han ingresado materiales.")
            return
        
        try:
            id_factura = db_connect.insertar_factura(
                self.datos_factura["numero_factura"],
                self.datos_factura["fecha"],
                self.datos_factura["proveedor"]
            )
            # Obtener nombres de proveedores desde BD
            self.actualizar_proveedores()
            
            id_proveedor = db_connect.obtener_id_proveedor_por_nombre(self.datos_factura["proveedor"])
            if isinstance(id_proveedor, tuple):
                id_proveedor = id_proveedor[0]  # Extrae el valor si es una tupla
            
            id_factura = db_connect.obtener_id_factura_por_numero(self.datos_factura["numero_factura"])
            print(f"Materiales antes del round = {self.materia_prima}")
            for material in self.materia_prima: #self.materiales_temporales:
                #print(f"Materiales antes del round TIPO = {type(material["costo_unitario"])}  -> {material}")
                try:
                    material["costo_unitario"] = round(self.convertir_a_float(material["costo_unitario"]), 4)
                    
                except:
                    messagebox.showerror(f"⚠️ Error",  f"El valor {material['costo_unitario']} no es un número válido.")
                    material["costo_unitario"] = 0.0
                    
                codigo_true = db_connect.codigo_existe(material["codigo"])

                # Verificar si el material existe en la base de datos
                if codigo_true:
                    # Si existe, actualizar el stock y el costo
                    exito, mensaje = db_connect.actualizar_material(
                        material["codigo"],
                        self.convertir_a_float(material["stock"]),
                        self.convertir_a_float(material["precio"]),
                        material["costo_unitario"],
                        material["es_por_metro"]
                    )
                    messagebox.showinfo("✅ Exito", mensaje)
                    
                    if not exito:
                        messagebox.showwarning("Advertencia", mensaje)
                else:
                    # Si no existe, insertar el material completo
                    id_material = db_connect.insertar_material(
                        material["codigo"],
                        material["nombre"],
                        material["tipo"],
                        material["tamaño"],
                        material["color"],
                        material["stock"],
                        material["precio"],
                        material["costo_unitario"],
                        material["es_por_metro"],
                        id_proveedor
                    )

                # 4. Obtener el id_material
                id_material = db_connect.obtener_id_material_por_codigo(material["codigo"])
                
                # 5. Insertar en Detalle_Factura
                if id_material is not None:
                    id_detalle = db_connect.insertar_detalle_factura(
                        id_factura,
                        id_material,
                        material["stock"],
                        material["precio"],
                        material["costo_unitario"]
                    )
                else:
                    messagebox.showinfo("No encontrado", f"No se encontró el material con código {material['codigo']}")
                
            # Guardar Empaques  OJO al guardar una lista vacia.
            for material in self.empaques_temporales: #self.materiales_temporales:
                try:
                    material["costo_unitario"] = round(self.convertir_a_float(material["costo_unitario"]), 4)
                except:
                    messagebox.showerror(f"⚠️ Error: El valor {material['costo_unitario']} no es un número válido.")
                    material["costo_unitario"] = 0.0
                    
                codigo_true = db_connect.codigo_existe_emp(material["codigo"])
                
                # Verificar si el material existe en la base de datos
                if codigo_true:
                    # Si existe, actualizar el stock y el costo
                    exito, mensaje, = db_connect.actualizar_empaque(
                        material["codigo"],
                        self.convertir_a_float(material["stock"]),
                        self.convertir_a_float(material["precio"]),
                        material["costo_unitario"],
                        material["es_por_metro"]
                        
                    )
                    messagebox.showinfo("✅ Exito", mensaje)
                    
                    if not exito:
                        messagebox.showwarning("Advertencia", mensaje)
                else:
                    # Si no existe, insertar el material completo
                    id_material = db_connect.insertar_empaque(
                        material["codigo"],
                        material["nombre"],
                        material["tamaño"],
                        material["stock"],
                        material["precio"],
                        material["costo_unitario"],
                        material["es_por_metro"]
                    )
                    
            # Marcar el borrador como finalizado si existía
            id_borrador = db_connect.existe_borrador_factura(self.datos_factura["numero_factura"])
            if id_borrador:
                db_connect.finalizar_borrador_factura(id_borrador)
                
            # 6. Mostrar mensaje de éxito
            messagebox.showinfo("Éxito", "Factura y materiales guardados correctamente.")
            self.limpiar_campos(frame_contenido)
            self.materiales_temporales.clear()
            self.materia_prima.clear()
            self.empaques_temporales.clear()

        except Exception as e:
            messagebox.showerror("⚠️ Error", f"No se pudo guardar: {e}")

    def mostrar_datos_ingresados(self):
        getcontext().prec = 6  # Maneja la cantidad de números de hasta 6 digitos.
        if not self.materiales_temporales:
            messagebox.showwarning("Advertencia", "No hay materiales ingresados.")
            return

        ventana_datos = tk.Toplevel()
        configurar_toplevel(ventana_datos, titulo="Datos Ingresados", ancho_min=850, alto_min=500)

        frame_principal = ttk.Frame(ventana_datos, padding="10")
        frame_principal.pack(fill=tk.BOTH, expand=True)

        style = ttk.Style()
        style.configure("mystyle.Treeview", background="#101113", fieldbackground="#101113", foreground="#ffffff")
        
        tree = ttk.Treeview(frame_principal, columns=("Código",
                                                    "Nombre", 
                                                    "Tipo", 
                                                    "Tamaño", 
                                                    "Color", 
                                                    "Cantidad", 
                                                    "Precio", 
                                                    "Precio Unitario",
                                                    "Es por Metro"), show="headings", style="mystyle.Treeview")

        for col in tree["columns"]:
            tree.heading(col, text=col)
            tree.column(col, width=80 if col != "Nombre" else 100, anchor=tk.CENTER)

        tree.pack(fill=tk.BOTH, expand=True)

        def cargar_datos():
            for item in tree.get_children():
                tree.delete(item)
            print(f"Materiales Temporales: {self.materiales_temporales}")
            for material in self.materiales_temporales:
                print(f"Materiales Temporales bucle for: {material}")
                precio = self.convertir_a_float(material["precio"])
                cantidad = self.convertir_a_float(material["stock"])
                
                precio_uni = precio / cantidad if precio is not None and cantidad is not None and cantidad != 0 else 0
                self.total_actual.append(precio)

                tree.insert("", tk.END, values=(
                    material.get("codigo", "-"),
                    material.get("nombre", "-"),
                    material.get("tipo", "-"),
                    material.get("tamaño", "-"),
                    material.get("color", "-"),
                    material.get("stock", "-"),
                    material.get("precio", "-"),
                    f"{round(precio_uni, 4)}",
                    material.get("es_por_metro")
                ))

            frame_total.config(text=f"{sum(self.total_actual):.2f}", font=("Arial", 12, "bold"))

        def editar_celda(event):
            region = tree.identify_region(event.x, event.y)
            if region == "cell":
                columna = tree.identify_column(event.x)
                fila = tree.identify_row(event.y)

                if fila and columna:
                    columna_idx = int(columna[1:]) - 1
                    item = tree.selection()[0]
                    valores = tree.item(item, "values")

                    entrada = tk.Entry(frame_principal, width=15)
                    entrada.place(x=event.x_root - ventana_datos.winfo_rootx(), y=event.y_root - ventana_datos.winfo_rooty())

                    def guardar_cambio(event=None):
                        nuevo_valor = entrada.get()
                        nuevos_valores = list(valores)
                        nuevos_valores[columna_idx] = nuevo_valor
                        tree.item(item, values=nuevos_valores)
                        entrada.destroy()

                    entrada.insert(0, valores[columna_idx])
                    entrada.bind("<Return>", guardar_cambio)
                    entrada.bind("<FocusOut>", guardar_cambio)
                    entrada.focus_set()

        tree.bind("<Double-1>", editar_celda)

        def guardar_cambios():
            for item in tree.get_children():
                valores = tree.item(item, "values")
                print(f"Guardar Cambios Valor: {valores}")
                codigo, nombre, tipo, tamaño, color, cantidad, precio, precio_unit, es_metro_tree = valores

                for i, mat in enumerate(self.materiales_temporales):
                    if mat["codigo"] == codigo:
                        # ✅ Preservar es_por_metro (y cualquier otro campo que el Treeview no muestra)
                        es_por_metro = es_metro_tree if es_metro_tree in ("Si", "No") else mat.get("es_por_metro")
                        material = {
                            "codigo": codigo,
                            "nombre": nombre,
                            "tipo": tipo,
                            "tamaño": tamaño,
                            "color": color,
                            "stock": self.convertir_a_float(cantidad),
                            "precio": self.convertir_a_float(precio),
                            "costo_unitario": self.convertir_a_float(precio_unit), # self.convertir_a_float(precio) / self.convertir_a_float(cantidad) if self.convertir_a_float(cantidad) != 0 else 0
                            "es_por_metro": es_por_metro
                        }
                        self.materiales_temporales[i] = material
                        
                        # ✅ Sincronizar también materia_prima (misma posición o buscar por código)
                        for k, mp in enumerate(self.materia_prima):
                            if mp["codigo"] == codigo:
                                self.materia_prima[k] = material
                                break
                            
                        if i < len(self.total_actual):
                            self.total_actual[i] = self.convertir_a_float(precio)
                        break

            frame_total.config(text=f"{sum(self.total_actual):.2f}", font=("Arial", 12, "bold"))
            messagebox.showinfo("Información", "✅ El cambio se ha guardado")
            
        def eliminar_dato():
            item = tree.selection()
            if not item:
                messagebox.showwarning("Advertencia", "Selecciona un ítem para eliminar.")
                return

            item_id = item[0]
            valores = tree.item(item_id, "values")
            codigo_a_eliminar = valores[0]

            tree.delete(item_id)

            # Eliminar de todas las listas donde pueda estar
            self.materiales_temporales = [m for m in self.materiales_temporales if m["codigo"] != codigo_a_eliminar]
            self.materia_prima = [m for m in self.materia_prima if m["codigo"] != codigo_a_eliminar]
            self.empaques_temporales = [m for m in self.empaques_temporales if m["codigo"] != codigo_a_eliminar]

            self.total_actual = [t for i, t in enumerate(self.total_actual) if i < len(self.materiales_temporales)]

            frame_total.config(text=f"{sum(self.total_actual):.2f}")

        # def eliminar_dato():
        #     item = tree.selection()
        #     if not item:
        #         messagebox.showwarning("Advertencia", "Selecciona un ítem para eliminar.")
        #         return

        #     item_id = item[0]
        #     valores = tree.item(item_id, "values")
        #     codigo_a_eliminar = valores[0]

        #     tree.delete(item_id)

        #     for i, material in enumerate(self.materiales_temporales):
        #         if material["codigo"] == codigo_a_eliminar:
        #             self.materiales_temporales.pop(i)
        #             if i < len(self.total_actual):
        #                 self.total_actual.pop(i)
        #             break

        #     frame_total.config(text=f"{sum(self.total_actual):.2f}")

        def cerrar_ventana():
            ventana_datos.destroy()
            self.total_actual.clear()

        def on_closing():
            self.total_actual.clear()
            ventana_datos.destroy()

        ventana_datos.protocol("WM_DELETE_WINDOW", on_closing)

        frame_botones = tk.Frame(ventana_datos)
        frame_botones.pack(fill=tk.X, padx=10, pady=10)

        frame_total = tk.Label(frame_botones)
        frame_total.pack(side=tk.RIGHT, padx=30)

        frame_label_total = tk.Label(frame_botones, text="Total Factura: ")
        frame_label_total.pack(side=tk.RIGHT, padx=7)

        boton_guardar = crear_boton(
            frame_botones,
            texto="Guardar Factura",
            ancho=20,
            alto=30,
            color_fondo="#4283fa",
            color_texto="white",
            font=("Arial", 11, "bold"),
            comando= lambda : guardar_cambios()
        )
        boton_guardar.pack(side=tk.LEFT, padx=5)

        boton_eliminar = crear_boton(
            frame_botones,
            texto="Eliminar",
            ancho=20,
            alto=30,
            color_fondo="#4283fa",
            color_texto="white",
            font=("Arial", 11, "bold"),
            comando=eliminar_dato
        )
        boton_eliminar.pack(side=tk.LEFT, padx=5)

        boton_cerrar = crear_boton(
            frame_botones,
            texto="Volver",
            ancho=30,
            alto=30,
            color_fondo="#913131",
            color_texto="white",
            font=("Arial", 11, "bold"),
            comando=cerrar_ventana
        )
        boton_cerrar.pack(side=tk.LEFT, padx=5)

        cargar_datos()
        

    def guardar_borrador(self):
        """Guarda la factura actual como borrador."""
        proveedor = self.proveedor_combobox.get()
        numero_factura = self.factura_entry.get()
        fecha_factura = self.fecha_entry.get()

        if not numero_factura and not proveedor and not self.materiales_temporales and not self.empaques_temporales:
            messagebox.showwarning("Advertencia", "No hay datos para guardar como borrador.")
            return

        if not numero_factura:
            messagebox.showwarning("Advertencia", "Ingresa al menos el número de factura.")
            return
        
        print(f"GUARDAR BORRADOR : {self.materiales_temporales}")
        materiales_json = json.dumps(self.materiales_temporales)
        empaques_json = json.dumps(self.empaques_temporales)

        borrador_existente = db_connect.existe_borrador_factura(numero_factura)

        if borrador_existente is not None:
            db_connect.actualizar_borrador_factura(
                self.id_usuario_creador, self.nombre_usuario_creador,
                proveedor, numero_factura, fecha_factura,
                materiales_json, empaques_json
            )
            messagebox.showinfo("Éxito", "Borrador actualizado correctamente.")
        else:
            db_connect.guardar_borrador_factura_db(
                self.id_usuario_creador, self.nombre_usuario_creador,
                proveedor, numero_factura, fecha_factura,
                materiales_json, empaques_json
            )
            messagebox.showinfo("Éxito", "Borrador guardado correctamente.")
    
    
    def mostrar_borradores_pendientes(self):
        """Muestra una ventana con los borradores de facturas pendientes."""
        borradores_window = tk.Toplevel(self.root)
        configurar_toplevel(borradores_window, titulo="Borradores de Facturas",
                            ancho_min=830, alto_min=300, color_fondo="#101113")

        borradores_main = tk.Frame(borradores_window)
        borradores_main.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(borradores_main, bg="#101113")
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(borradores_main, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        borradores_frame = tk.Frame(canvas, bg="#101113")
        canvas.create_window((0, 0), window=borradores_frame, anchor="nw")

        # Doble protección: [] si la BD devuelve None
        borradores = db_connect.borradores_facturas_pendientes() or []
        #print(f"Borrador Factura: {borradores}")
        encabezados = ["ID", "Creador", "Proveedor", "N° Factura", "Fecha Factura", "Materiales", "Empaques", "Fecha inicio", "Acciones"]
        for col, encabezado in enumerate(encabezados):
            tk.Label(borradores_frame, text=encabezado, font=("Arial", 10, "bold"),
                    bg="#d1d1d1", fg="#101113").grid(row=0, column=col, padx=5, pady=5, sticky="nsew")
        
        orden_campos = [
                            "usuario_creador_id",
                            "nombre_usuario_creador",
                            "proveedor",
                            "numero_factura",
                            "fecha_factura",
                            "materiales",
                            "empaques",
                            "fecha_creacion",
                            
                        ]
        for i, borrador in enumerate(borradores):
            # Columnas 0 a 9 (datos)
            #print(f"for i = {i}")
            #print(f"for borrador = {borrador}")
            for j, orden_campos in enumerate(borrador):
                valor = borrador[orden_campos] if borrador[orden_campos] is not None else ""
                texto_limitado = self.limitar_texto(str(valor))
                label = tk.Label(borradores_frame, text=texto_limitado, bg="#101113",
                                fg="#ffffff", cursor="hand2")
                label.grid(row=i + 1, column=j, padx=5, pady=5, sticky="nsew")
                label.bind("<Button-1>", lambda e, txt=valor: self.mostrar_contenido_completo(txt))

            # Botón "Cargar" en la columna 6
            btn_cargar = tk.Button(borradores_frame, text="Cargar", bg="#4B82F0", fg="#101113",
                                command=lambda id=borrador["id"]: self.cargar_borrador(id, borradores_window))
            btn_cargar.grid(row=i + 1, column=8, padx=5, pady=5)

        for col in range(len(encabezados)):
            borradores_frame.columnconfigure(col, weight=1)
    
    
    def cargar_borrador(self, borrador_id, borradores_window):
        """Carga un borrador de factura seleccionado en el formulario."""
        borrador = db_connect.cargar_borrador_factura_db(borrador_id)

        if not borrador:
            messagebox.showerror("⚠️ Error", "No se encontró el borrador.")
            return

        # Limpiar el formulario actual
        self.proveedor_combobox.set('')
        self.factura_entry.delete(0, tk.END)
        self.fecha_entry.delete(0, tk.END)
        self.materiales_temporales.clear()
        self.materia_prima.clear()
        self.empaques_temporales.clear()

        # Cargar datos de la factura
        self.proveedor_combobox.set(borrador["proveedor"] or "")
        self.factura_entry.insert(0, borrador["numero_factura"] or "")
        self.fecha_entry.insert(0, borrador["fecha_factura"] or "")

        # Deserializar con json.loads (NUNCA eval)
        try:
            self.materiales_temporales = json.loads(borrador["materiales"]) if borrador["materiales"] else []
            self.empaques_temporales = json.loads(borrador["empaques"]) if borrador["empaques"] else []
            
            # Normalizar valores faltantes
            for material in self.materiales_temporales:
                if material.get("es_por_metro") is None:
                    material["es_por_metro"] = "No"

            for empaque in self.empaques_temporales:
                if empaque.get("es_por_metro") is None:
                    empaque["es_por_metro"] = "No"
                    
        except json.JSONDecodeError:
            messagebox.showerror("⚠️ Error", "El borrador contiene datos corruptos.")
            return

        # Reconstruir materia_prima (materiales que van a la tabla Materiales, no empaques)
        self.materia_prima = self.materiales_temporales.copy()
        #print(f"Materia Prima AL cargar borrador {self.materia_prima}")
        #print(f"Materia Prima AL cargar borrador (TYPE) {type(self.materia_prima)}")

        # Actualizar el estado de los botones con los datos cargados
        self.on_campo_cambiado()

        borradores_window.destroy()
        messagebox.showinfo("Éxito", f"Borrador {borrador_id} cargado correctamente.")      
    
    def limitar_texto(self, texto, limite=15):
            """Limitara la cantidad de caracteres dentro de una columna de borradores pendientes."""
            if len(texto) > limite:
                return texto[:limite] + "..."
            return texto
    
    def mostrar_contenido_completo(self, texto, titulo="Información completa"):
        """Muestra la información completa de la columna."""        
        informacion_completa = tk.Toplevel(self.frame)
        informacion_completa.title(titulo)
        informacion_completa.geometry("400x200")

        def cerrar_toplevel():
            informacion_completa.grab_release()
            informacion_completa.destroy()

        # ✕ de la ventana también libera el grab
        informacion_completa.protocol("WM_DELETE_WINDOW", cerrar_toplevel)

        texto_label = tk.Label(informacion_completa, text=texto, wraplength=380, justify=tk.LEFT)
        texto_label.pack(padx=10, pady=10)

        btn_cerrar = tk.Button(informacion_completa, text="Cerrar", command=cerrar_toplevel)
        btn_cerrar.pack(pady=10)

        informacion_completa.update_idletasks()
        informacion_completa.grab_set()
        informacion_completa.lift()          # Trae la ventana al frente
        informacion_completa.focus_force() 