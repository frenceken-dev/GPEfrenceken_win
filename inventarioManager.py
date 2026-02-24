import tkinter as tk
from tkinter import ttk, messagebox
from db import (
    obtener_nombres_proveedores,
    insertar_factura, insertar_material,
    obtener_id_proveedor_por_nombre,
    obtener_id_factura_por_numero,
    obtener_id_material_por_codigo,
    insertar_detalle_factura,
    codigo_existe
)
from recursos import crear_boton, configurar_toplevel
from databasemanager import DataBaseManager

db_connect = DataBaseManager()
class InventarioManager:
    def __init__(self, root, imagen_panel_tk, volver_menu):
        self.root = root
        self.imagen_panel_tk = imagen_panel_tk
        self.volver_menu = volver_menu
        self.materiales_temporales = []
        self.datos_factura = {
            "proveedor": "",
            "numero_factura": "",
            "fecha": ""
        }
        self.total_actual = []
        self.exite_codigo = False
        self.db_connect = DataBaseManager()  # Asegúrate de que DataBaseManager esté importado

    def limpiar_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

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

        tk.Label(self.form_frame, text="Fecha (DD/MM/AAAA):", bg="#a0b9f0").grid(row=2, column=0, sticky="e")
        self.fecha_entry = tk.Entry(self.form_frame, width=30)
        self.fecha_entry.grid(row=2, column=1, pady=5)

    def actualizar_proveedores(self):
        self.proveedor_combobox["values"] = obtener_nombres_proveedores("")

    def actualizar_opciones_proveedores(self, event):
        texto = self.proveedor_combobox.get()
        proveedores_filtrados = obtener_nombres_proveedores(texto)
        self.proveedor_combobox['values'] = proveedores_filtrados

    def crear_botones_accion(self):
        # Botón Agregar Material
        self.btn_agregar_material = crear_boton(
            self.form_frame,
            texto="Agregar Material",
            ancho=30,
            alto=30,
            color_fondo="#073EAD",
            color_texto="white",
            font=("Arial", 11, "bold"),
            comando=lambda: self.agregar_material_temporal(self.frame),
            state=tk.DISABLED
        )
        self.btn_agregar_material.grid(row=3, column=0, pady=20)

        # Botón Mostrar Datos
        self.btn_mostrar_datos = crear_boton(
            self.form_frame,
            texto="Mostrar Datos Ingresados",
            ancho=30,
            alto=30,
            color_fondo="#324f98",
            color_texto="white",
            font=("Arial", 11, "bold"),
            comando=lambda: [
                self.actualizar_datos_factura(),
                self.mostrar_datos_ingresados()
            ],
            state=tk.DISABLED
        )
        self.btn_mostrar_datos.grid(row=3, column=1, pady=20)

        # Botón Guardar Factura
        self.btn_guardar_factura = crear_boton(
            self.form_frame,
            texto="Guardar Factura",
            ancho=30,
            alto=30,
            color_fondo="#4283fa",
            color_texto="white",
            font=("Arial", 11, "bold"),
            comando=lambda: [
                self.actualizar_datos_factura(),
                self.guardar_factura_y_materiales(self.frame)
            ],
            state=tk.DISABLED
        )
        self.btn_guardar_factura.grid(row=4, column=0, columnspan=2, pady=20)

        # Botón Volver
        self.back_button = crear_boton(
            self.frame_inferior,
            texto="Volver",
            ancho=30,
            alto=30,
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
        botones = [self.btn_agregar_material, self.btn_mostrar_datos, self.btn_guardar_factura]

        for boton in botones:
            if hasattr(boton, "set_state"):
                boton.set_state("normal" if estado_activo else "disabled")
            else:
                boton.config(state=tk.NORMAL if estado_activo else tk.DISABLED)

    def validar_campos_obligatorios(self, proveedor, num_factura, fecha):
        return proveedor.strip() != "" and num_factura.strip() != "" and fecha.strip() != ""

    def actualizar_datos_factura(self):
        self.datos_factura.update({
            "proveedor": self.proveedor_combobox.get(),
            "numero_factura": self.factura_entry.get(),
            "fecha": self.fecha_entry.get()
        })

    def agregar_material_temporal(self, frame_contenido):
        cod_materiales = self.db_connect.obtener_codigo_materiales()
        print(f"Códigos obtenidos para el combobox: {cod_materiales}")

        material_window = tk.Toplevel(frame_contenido)
        configurar_toplevel(material_window, titulo="Agregar Material", ancho_min=300, alto_min=330, color_fondo="#101113")

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
            print(f"Código seleccionado: {codigo}")
            nombre, tipo, tamaño, color = self.db_connect.obtener_materiales(codigo)

            if nombre or tipo or tamaño or color:
                nombre_entry.delete(0, tk.END)
                tipo_entry.delete(0, tk.END)
                tamaño_entry.delete(0, tk.END)
                color_entry.delete(0, tk.END)

                nombre_entry.insert(0, nombre)
                tipo_entry.insert(0, tipo)
                tamaño_entry.insert(0, tamaño)
                color_entry.insert(0, color)

        codigo_entry["postcommand"] = filtrar_codigos_postcommand
        codigo_entry.bind("<<ComboboxSelected>>", lambda event: auto_completar_entry(event))
        codigo_entry.bind("<KeyRelease>", lambda event: filtrar_codigos_key(event))

        def guardar_material():
            codigo = codigo_entry.get()
            precio = self.convertir_a_float(precio_entry.get())
            cantidad = self.convertir_a_float(stock_entry.get())
            costo_unitario = precio / cantidad if cantidad != 0 else 0

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
                "costo_unitario": costo_unitario
            }
            self.materiales_temporales.append(material)
            messagebox.showinfo("Éxito", "Material agregado temporalmente.")
            material_window.destroy()

        def borrar_campos():
            nombre_entry.delete(0, tk.END)
            tipo_entry.delete(0, tk.END)
            tamaño_entry.delete(0, tk.END)
            color_entry.delete(0, tk.END)

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
        boton_guardar_material.grid(row=7, column=0, columnspan=2, padx=15, pady=10)

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
        boton_borrar_campos.grid(row=8, column=0, columnspan=2, padx=15, pady=10)

    def convertir_a_float(self, valor_str):
        try:
            valor_str = str(valor_str).replace(",", ".")
            return float(valor_str)
        except ValueError:
            print(f"⚠️ Error: '{valor_str}' no es un número válido.")
            return None

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
        
        #try:
        insertar_factura(
            self.datos_factura["numero_factura"],
            self.datos_factura["fecha"],
            self.datos_factura["proveedor"]
        )

        id_proveedor = obtener_id_proveedor_por_nombre(self.datos_factura["proveedor"])
        if isinstance(id_proveedor, tuple):
            id_proveedor = id_proveedor[0]  # Extrae el valor si es una tupla
        
        id_factura = obtener_id_factura_por_numero(self.datos_factura["numero_factura"])
        
        for material in self.materiales_temporales:
            try:
                material["costo_unitario"] = round(material["costo_unitario"], 2)
            except:
                print(f"⚠️ Error: El valor {material['costo_unitario']} no es un número válido.")
                material["costo_unitario"] = 0.0
                
            codigo_true = codigo_existe(material["codigo"])
            print(f"El volor de codigo_true: {codigo_true}")
            # Verificar si el material existe en la base de datos
            if codigo_true:
                # Si existe, actualizar el stock y el costo
                exito, mensaje = db_connect.actualizar_material(
                    material["codigo"],
                    int(material["stock"]),
                    material["precio"],
                    material["costo_unitario"]
                )
                if not exito:
                    messagebox.showwarning("Advertencia", mensaje)
            else:
                # Si no existe, insertar el material completo
                insertar_material(
                    material["codigo"],
                    material["nombre"],
                    material["tipo"],
                    material["tamaño"],
                    material["color"],
                    material["stock"],
                    material["precio"],
                    material["costo_unitario"],
                    id_proveedor
                )

            # 4. Obtener el id_material
            id_material = obtener_id_material_por_codigo(material["codigo"])

            # 5. Insertar en Detalle_Factura
            if id_material is not None:
                insertar_detalle_factura(
                    id_factura,
                    id_material,
                    material["stock"],
                    material["precio"],
                    material["costo_unitario"]
                )
            else:
                messagebox.showinfo("No encontrado", f"No se encontró el material con código {material['codigo']}")

        # 6. Mostrar mensaje de éxito
        messagebox.showinfo("Éxito", "Factura y materiales guardados correctamente.")
        self.limpiar_campos(frame_contenido)
        self.materiales_temporales.clear()

        # except Exception as e:
        #     messagebox.showerror("⚠️ Error", f"No se pudo guardar: {e}")

    def mostrar_datos_ingresados(self):
        if not self.materiales_temporales:
            messagebox.showwarning("Advertencia", "No hay materiales ingresados.")
            return

        ventana_datos = tk.Toplevel()
        configurar_toplevel(ventana_datos, titulo="Datos Ingresados", ancho_min=800, alto_min=500)

        frame_principal = ttk.Frame(ventana_datos, padding="10")
        frame_principal.pack(fill=tk.BOTH, expand=True)

        tree = ttk.Treeview(frame_principal, columns=("Código", "Nombre", "Tipo", "Tamaño", "Color", "Cantidad", "Precio", "Precio Unitario"), show="headings")

        for col in tree["columns"]:
            tree.heading(col, text=col)
            tree.column(col, width=80 if col != "Nombre" else 100, anchor=tk.CENTER)

        tree.pack(fill=tk.BOTH, expand=True)

        def cargar_datos():
            for item in tree.get_children():
                tree.delete(item)

            for material in self.materiales_temporales:
                precio = self.convertir_a_float(material["precio"])
                cantidad = self.convertir_a_float(material["stock"])
                precio_uni = precio / cantidad if precio is not None and cantidad is not None and cantidad != 0 else 0
                self.total_actual.append(precio)

                tree.insert("", tk.END, values=(
                    material["codigo"],
                    material["nombre"],
                    material["tipo"],
                    material["tamaño"],
                    material["color"],
                    material["stock"],
                    material["precio"],
                    f"{precio_uni:.2f}"
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
                codigo, nombre, tipo, tamaño, color, cantidad, precio, _ = valores

                material = {
                    "codigo": codigo,
                    "nombre": nombre,
                    "tipo": tipo,
                    "tamaño": tamaño,
                    "color": color,
                    "stock": cantidad,
                    "precio": precio,
                    "costo_unitario": self.convertir_a_float(precio) / self.convertir_a_float(cantidad) if self.convertir_a_float(cantidad) != 0 else 0
                }

                for i, mat in enumerate(self.materiales_temporales):
                    if mat["codigo"] == codigo:
                        self.materiales_temporales[i] = material
                        if i < len(self.total_actual):
                            self.total_actual[i] = self.convertir_a_float(precio)
                        break

            frame_total.config(text=f"{sum(self.total_actual):.2f}", font=("Arial", 12, "bold"))

        def eliminar_dato():
            item = tree.selection()
            if not item:
                messagebox.showwarning("Advertencia", "Selecciona un ítem para eliminar.")
                return

            item_id = item[0]
            valores = tree.item(item_id, "values")
            codigo_a_eliminar = valores[0]

            tree.delete(item_id)

            for i, material in enumerate(self.materiales_temporales):
                if material["codigo"] == codigo_a_eliminar:
                    self.materiales_temporales.pop(i)
                    if i < len(self.total_actual):
                        self.total_actual.pop(i)
                    break

            frame_total.config(text=f"{sum(self.total_actual):.2f}")

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
            comando=guardar_cambios
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
