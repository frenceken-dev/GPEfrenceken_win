import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from db import (
    insertar_producto, obtener_materiales, actualizar_stock_material,
    insertar_detalle_producto, obtener_id_producto_por_codigo,
    obtener_id_material_por_codigo, obtener_costo_unitario_material,
    buscar_codigos_like, obtener_codigo_material_por_nombre_color_tipo_tamaño,
    obtener_nombre_material_por_codigo, obtener_tipos_por_material_y_color,
    obtener_tamaños_por_material_color_tipo, obtener_color_por_material,
    obtener_codigo_materiales, obtener_material_por_codigo,
    guardar_borrador_db, id_usuario_nombre_actual, borradores_pendientes,
    cargar_borrador_db, marcar_borrador_como_creado,
)
from inventario import convertir_a_float
from recursos import crear_boton, configurar_toplevel

class ProductoManager:
    """Clase para gestionar la creación, edición y visualización de productos."""

    def __init__(self, root, imagen_panel_tk, volver_menu):
        print("¡NUEVA INSTANCIA DE ProductoManager CREADA!")  # Depuración
        self.root = root
        self.imagen_panel_tk = imagen_panel_tk
        self.volver_menu = volver_menu
        self.id_usuario_creador = None
        self.nombre_usuario_creador = None
        self.materiales_usados = []
        self.codigo_producto = ""
        self.nombre_producto = ""
        self.tipo_producto = ""
        self.descripcion_producto = ""
        self.tiempo_fabricacion = 0
        self.cantidad_creada = 0
        self.costo_produccion = 0.0
        self.precio_venta = 0.0

    def usuario_actual(self, usuario):
        """Obtiene el usuario actual y su ID."""
        self.nombre_usuario_creador = usuario
        print(f"EL USUARIO EN LA CLASE PRODUCTO ES: {usuario}")
        if self.nombre_usuario_creador:
            self.id_usuario_creador = id_usuario_nombre_actual(self.nombre_usuario_creador)
            print(f"EL ID DEL USUARIO ACTUAL ES: {self.id_usuario_creador}")
            #return self.id_usuario_creador[0][0], self.nombre_usuario_creador

    def crear_producto(self):
        """Crea la interfaz para registrar un nuevo producto."""
        for widget in self.root.winfo_children():
            widget.destroy()

        # Obtener materiales de la base de datos
        materiales = obtener_materiales()
        self.articulos = [material[1] for material in materiales]
        self.tipo_material = [material[3] for material in materiales]
        self.tamaño_material = [material[4] for material in materiales]
        self.cantidades = [convertir_a_float(material[6]) for material in materiales]
        self.precios_uni = [convertir_a_float(material[8]) for material in materiales]
        self.tipos_unicos = list(set(self.tipo_material))
        self.tamaños_unicos = list(set(self.tamaño_material))

        # Crear el frame principal
        frame = tk.Frame(self.root, bg="#a0b9f0", width=800, height=600)
        frame.pack(fill=tk.BOTH, expand=True)

        # Panel izquierdo
        frame_menu = tk.Frame(frame, bg="#2C3E50", width=200, height=800, bd=3, relief="solid")
        frame_menu.pack(side=tk.LEFT, fill=tk.Y)
        frame_menu.pack_propagate(False)

        # Imagen del logo
        frame_imagen_panel = tk.Frame(frame_menu, bg="#2C3E50", height=70)
        frame_imagen_panel.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        if self.imagen_panel_tk:
            label_imagen = tk.Label(frame_imagen_panel, image=self.imagen_panel_tk, bg="#2C3E50")
            label_imagen.pack(side=tk.LEFT, padx=70)
        else:
            label_texto = tk.Label(frame_imagen_panel, text="Ikigai", font=("Arial", 10), bg="#2C3E50")
            label_texto.pack(side=tk.LEFT, padx=70)

        # Frame inferior del menú lateral
        frame_inferior = tk.Frame(frame_menu, bg="#2C3E50")
        frame_inferior.pack(side="bottom", fill="x", pady=20)

        # Botón para volver
        back_button = crear_boton(
            frame_inferior,
            texto="Volver",
            ancho=30,
            alto=30,
            color_fondo="#913131",
            color_texto="white",
            font=("Arial", 11, "bold"),
            hover_color="#222423",
            comando=self.volver_menu
        )
        back_button.pack(side="bottom", padx=30, pady=30)

        # Frame del título
        frame_titulo = tk.Frame(frame, bg="#a0b9f0")
        frame_titulo.pack(side=tk.TOP, fill=tk.X, pady=15)
        title_label = tk.Label(
            frame_titulo,
            text="Creación de Nuevos Productos",
            font=("Arial", 16, "bold"),
            bg="#a0b9f0",
            fg="#2C3E50"
        )
        title_label.pack(pady=15)

        # Formulario para crear el producto
        self.form_frame = tk.Frame(frame, bg="#a0b9f0", padx=20, pady=20)
        self.form_frame.place(relx=0.5, rely=0.1, anchor=tk.N)

        # Campos del formulario
        tk.Label(self.form_frame, text="Código del producto:", bg="#a0b9f0", anchor="w").grid(row=0, column=0, sticky="w", pady=1)
        self.codigo_entry = tk.Entry(self.form_frame, width=30)
        self.codigo_entry.grid(row=1, column=0, pady=5)

        tk.Label(self.form_frame, text="Tipo (Pulsera/Collar/Aretes/Llavero):", bg="#a0b9f0").grid(row=2, column=0, sticky="w", pady=1)
        self.tipo_combobox = ttk.Combobox(self.form_frame, values=["pulsera", "collar", "aretes", "llavero"], width=28)
        self.tipo_combobox.grid(row=3, column=0, pady=5)

        tk.Label(self.form_frame, text="Descripción:", bg="#a0b9f0").grid(row=8, column=0, sticky="w", pady=1)
        self.descripcion_entry = tk.Entry(self.form_frame, width=30)
        self.descripcion_entry.grid(row=9, column=0, pady=5)

        tk.Label(self.form_frame, text="Tiempo de fabricación (minutos):", bg="#a0b9f0").grid(row=4, column=0, sticky="w", pady=1)
        self.tiempo_entry = tk.Entry(self.form_frame, width=30)
        self.tiempo_entry.grid(row=5, column=0, pady=5)
        self.tiempo_entry.insert(0, "5")

        tk.Label(self.form_frame, text="Cantidad Creada:", bg="#a0b9f0").grid(row=6, column=0, sticky="w", pady=1)
        self.cantidad_creada_entry = tk.Entry(self.form_frame, width=30)
        self.cantidad_creada_entry.grid(row=7, column=0, pady=5)
        self.cantidad_creada_entry.insert(0, "1")

        # Botones
        crear_boton(
            self.form_frame,
            texto="Ingresar Materiales",
            ancho=30,
            alto=30,
            color_fondo="#143E86",
            color_texto="white",
            font=("Arial", 11, "bold"),
            hover_color="#2ECC71",
            comando=self.ingresar_materiales
        ).grid(row=12, column=0, padx=5, pady=5)

        crear_boton(
            self.form_frame,
            texto="Registrar Producto",
            ancho=30,
            alto=30,
            color_fondo="#1B8420",
            color_texto="white",
            font=("Arial", 11, "bold"),
            hover_color="#2ECC71",
            comando=self.registrar_producto
        ).grid(row=12, column=1, pady=5)

        crear_boton(
            self.form_frame,
            texto="Resumen Materiales",
            ancho=30,
            alto=30,
            color_fondo="#DEE90D",
            color_texto="white",
            font=("Arial", 11, "bold"),
            hover_color="#2ECC71",
            comando=lambda: self.mostrar_resumen_materiales(self.root)
        ).grid(row=13, column=0, padx=5, pady=5)

        crear_boton(
            self.form_frame,
            texto="Borradores Pendientes",
            ancho=30,
            alto=30,
            color_fondo="#F83403",
            color_texto="white",
            font=("Arial", 11, "bold"),
            hover_color="#15221A",
            comando=self.mostrar_borradores_pendientes
        ).grid(row=13, column=1, pady=5)

    def obtener_valores(self):
        """Obtiene los valores de los campos del formulario."""
        self.codigo_producto = self.codigo_entry.get()
        self.tipo_producto = self.tipo_combobox.get()
        self.descripcion_producto = self.descripcion_entry.get()
        self.tiempo_fabricacion = convertir_a_float(self.tiempo_entry.get())
        self.cantidad_creada = int(self.cantidad_creada_entry.get())
        return self.codigo_producto, self.tipo_producto, self.tiempo_fabricacion, self.cantidad_creada, self.descripcion_producto

    def ingresar_materiales(self):
        """Abre una ventana para ingresar materiales al producto."""
        material_window = tk.Toplevel(self.root)
        configurar_toplevel(material_window, titulo="Ingresar Materiales", ancho_min=380, alto_min=300, color_fondo="#101113")

        # Campos para seleccionar el material
        tk.Label(material_window, text="Material por Código:", bg="#101113", fg="#ffffff").grid(row=0, column=0, padx=10, pady=5)
        material_entry = ttk.Combobox(material_window, values=self.articulos)
        material_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(material_window, text="Color:", bg="#101113", fg="#ffffff").grid(row=1, column=0, padx=10, pady=5)
        color_entry = ttk.Combobox(material_window, state="disabled")
        color_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(material_window, text="Tipo:", bg="#101113", fg="#ffffff").grid(row=2, column=0, padx=10, pady=5)
        tipo_entry = ttk.Combobox(material_window, state="disabled")
        tipo_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(material_window, text="Cantidad:", bg="#101113", fg="#ffffff").grid(row=3, column=0, padx=10, pady=5)
        cantidad_entry = tk.Entry(material_window)
        cantidad_entry.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(material_window, text="Tamaño:", bg="#101113", fg="#ffffff").grid(row=4, column=0, padx=10, pady=5)
        tamaño_entry = ttk.Combobox(material_window, state="disabled")
        tamaño_entry.grid(row=4, column=1, padx=10, pady=5)

        # Vincular eventos para actualizar los Combobox
        material_entry.bind("<KeyRelease>", self.filtrar_codigos)
        material_entry.bind("<<ComboboxSelected>>", lambda event: self.actualizar_color(event, color_entry))
        color_entry.bind("<<ComboboxSelected>>", lambda event: self.actualizar_tipos(event, tipo_entry, material_entry, color_entry))
        tipo_entry.bind("<<ComboboxSelected>>", lambda event: self.actualizar_tamaños(event, tamaño_entry, material_entry, color_entry, tipo_entry))

        # Botones
        crear_boton(
            material_window,
            texto="Agregar Material",
            ancho=30,
            alto=30,
            color_fondo="#1B3E84",
            color_texto="white",
            font=("Arial", 11, "bold"),
            hover_color="#2ECC71",
            comando=lambda: self.agregar_material(material_entry, color_entry, tipo_entry, tamaño_entry, cantidad_entry, material_window)
        ).grid(row=5, column=0, columnspan=2, pady=10)

        crear_boton(
            material_window,
            texto="Guardar borrador",
            ancho=30,
            alto=30,
            color_fondo="#DEE90D",
            color_texto="white",
            font=("Arial", 11, "bold"),
            hover_color="#2ECC71",
            comando=lambda: self.guardar_borrador(material_window)
        ).grid(row=6, column=0, columnspan=2, pady=10)

    def filtrar_codigos(self, event):
        """Filtra los códigos de materiales según el texto ingresado."""
        texto = event.widget.get()
        if texto == "":
            event.widget['values'] = self.articulos
        else:
            resultados = buscar_codigos_like(texto)
            event.widget['values'] = resultados

    def actualizar_color(self, event, color_entry):
        """Actualiza los colores disponibles según el material seleccionado."""
        codigo_material = event.widget.get()
        if codigo_material:
            color = obtener_color_por_material(codigo_material)
            color_entry['values'] = color
            color_entry.set('')
            color_entry.configure(state="readonly")
        else:
            color_entry.set('')
            color_entry.configure(state="disabled")

    def actualizar_tipos(self, event, tipo_entry, material_entry, color_entry):
        """Actualiza los tipos disponibles según el material y color seleccionados."""
        codigo_material = material_entry.get()
        color_material = color_entry.get()
        if codigo_material and color_material:
            tipos = obtener_tipos_por_material_y_color(codigo_material, color_material)
            tipo_entry['values'] = tipos
            tipo_entry.set('')
            tipo_entry.configure(state="readonly")
        else:
            tipo_entry.set('')
            tipo_entry.configure(state="disabled")

    def actualizar_tamaños(self, event, tamaño_entry, material_entry, color_entry, tipo_entry):
        """Actualiza los tamaños disponibles según el material, color y tipo seleccionados."""
        codigo_material = material_entry.get()
        color_material = color_entry.get()
        tipo_material = tipo_entry.get()
        if codigo_material and color_material and tipo_material:
            tamaños = obtener_tamaños_por_material_color_tipo(codigo_material, color_material, tipo_material)
            tamaño_entry['values'] = tamaños
            tamaño_entry.set('')
            tamaño_entry.configure(state="readonly")
        else:
            tamaño_entry.set('')
            tamaño_entry.configure(state="disabled")

    def agregar_material(self, material_entry, color_entry, tipo_entry, tamaño_entry, cantidad_entry, material_window):
        """Agrega un material a la lista de materiales usados."""
        material_actual = material_entry.get()
        color_material_actual = color_entry.get()
        tipo_material_actual = tipo_entry.get()
        tamaño_material_actual = tamaño_entry.get()

        try:
            cantidad_necesaria = convertir_a_float(cantidad_entry.get())
        except ValueError:
            messagebox.showerror("⚠️ Error", "La cantidad debe ser un número entero.")
            return

        codigo_material = obtener_codigo_material_por_nombre_color_tipo_tamaño(
            material_actual, color_material_actual, tipo_material_actual, tamaño_material_actual
        )

        if codigo_material is not None:
            try:
                indice = self.articulos.index(material_actual)
            except ValueError:
                messagebox.showerror("⚠️ Error", f"Material {material_actual} no encontrado.")
                return

            if self.cantidades[indice] >= cantidad_necesaria:
                self.materiales_usados.append({
                    "codigo": codigo_material,
                    "color": color_material_actual,
                    "tipo": tipo_material_actual,
                    "tamaño": tamaño_material_actual,
                    "cantidad": cantidad_necesaria
                })
                material_window.destroy()
                messagebox.showinfo("Éxito", f"Material {material_actual} registrado correctamente.")
            else:
                messagebox.showerror("⚠️ Error", f"No hay suficiente stock de {material_actual}. Stock disponible: {self.cantidades[indice]}")
        else:
            messagebox.showerror("⚠️ Error", f"No se encontró el material {material_actual} con tipo {tipo_material_actual} y tamaño {tamaño_material_actual}.")

    def guardar_borrador(self, material_window):
        """Guarda el producto actual como borrador."""
        print(f"ID usuario en guardar_borrador: {self.id_usuario_creador}")
        print(f"Nombre usuario en guardar_borrador: {self.nombre_usuario_creador}")
        id_creador = self.id_usuario_creador[0][0]
        nombre_creador = str(self.nombre_usuario_creador)
        codigo_producto = self.codigo_entry.get()
        tipo_producto = self.tipo_combobox.get()
        tiempo_invertido = self.tiempo_entry.get()
        cantida_producidas = self.cantidad_creada_entry.get()
        descripcion_producto = self.descripcion_entry.get()
        materiales_actuales = self.materiales_usados.copy()

        if not codigo_producto and not descripcion_producto and not materiales_actuales:
            messagebox.showwarning("Advertencia", "No hay datos para guardar como borrador.")
        else:
            guardar_borrador_db(
                id_creador, nombre_creador, codigo_producto, tipo_producto,
                tiempo_invertido, cantida_producidas, descripcion_producto, materiales_actuales
            )

    def mostrar_resumen_materiales(self, ventana_padre):
        """Muestra un resumen de los materiales usados, ajustando el tamaño de la ventana."""
        # Cerrar cualquier ventana de resumen anterior
        if hasattr(self, 'resumen_window') and self.resumen_window:
            self.resumen_window.destroy()

        # Crear la ventana de resumen
        self.resumen_window = tk.Toplevel(ventana_padre)
        configurar_toplevel(self.resumen_window, titulo="Resumen de Materiales", ancho_min=400, alto_min=350, color_fondo="#101113")
        self.resumen_window.transient(ventana_padre)
        self.resumen_window.grab_set()
        self.resumen_window.focus_set()

        # Frame principal
        frame = tk.Frame(self.resumen_window, bg="#101113")
        frame.pack(fill=tk.BOTH, expand=True)

        # Configuración del Treeview
        columnas = ("codigo", "color", "tipo", "tamaño", "cantidad")
        self.tree = ttk.Treeview(frame, columns=columnas, show="headings", style="mystyle.Treeview")

        # Configurar estilo
        style = ttk.Style()
        style.configure("mystyle.Treeview", background="#101113", fieldbackground="#101113", foreground="#ffffff")

        # Configurar encabezados y columnas
        encabezados = {
            "codigo": "Código",
            "color": "Color",
            "tipo": "Tipo",
            "tamaño": "Tamaño",
            "cantidad": "Cantidad"
        }

        ancho_total = 0
        for col in columnas:
            self.tree.heading(col, text=encabezados[col])
            self.tree.column(col, anchor=tk.CENTER, width=130)
            ancho_total += 130  # Sumar el ancho de cada columna

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Cargar datos en el Treeview
        self.cargar_datos_en_treeview()

        # Ajustar el tamaño de la ventana según el contenido
        self.ajustar_tamano_ventana(ancho_total)

        # Botones
        frame_btn = ttk.Frame(self.resumen_window, style="mystyle.Treeview", padding=10)
        frame_btn.pack(fill=tk.X)

        crear_boton(frame_btn, texto="Guardar", ancho=20, alto=30, color_fondo="#1B3E84", color_texto="white", font=("Arial", 11, "bold"), hover_color="#2ECC71", comando=self.guardar_cambios).pack(side=tk.LEFT, padx=5)
        crear_boton(frame_btn, texto="Eliminar", ancho=20, alto=30, color_fondo="#913131", color_texto="white", font=("Arial", 11, "bold"), hover_color="#2ECC71", comando=self.eliminar_material).pack(side=tk.LEFT, padx=5)
        crear_boton(frame_btn, texto="Cerrar", ancho=20, alto=30, color_fondo="#555555", color_texto="white", font=("Arial", 11, "bold"), hover_color="#777777", comando=self.resumen_window.destroy).pack(side=tk.RIGHT, padx=5)

    def cargar_datos_en_treeview(self):
        """Carga los datos en el Treeview."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        for mat in self.materiales_usados:
            self.tree.insert("", tk.END, values=(
                mat["codigo"],
                mat["color"],
                mat["tipo"],
                mat["tamaño"],
                mat["cantidad"]
            ))

    def ajustar_tamano_ventana(self, ancho_total):
        """Ajusta el tamaño de la ventana según el ancho total de las columnas."""
        # Altura fija (puedes ajustarla según tus necesidades)
        altura = 400

        # Ajustar el tamaño de la ventana
        self.resumen_window.geometry(f"{ancho_total + 50}x{altura}")


        def guardar():
            self.materiales_usados.clear()
            for item in self.tree.get_children():
                c, col, t, tam, cant = self.tree.item(item)["values"]
                self.materiales_usados.append({
                    "codigo": c,
                    "color": col,
                    "tipo": t,
                    "tamaño": tam,
                    "cantidad": convertir_a_float(cant)
                })

        def eliminar():
            item = self.tree.selection()
            if not item:
                return
            self.tree.delete(item[0])

        def cerrar():
            self.resumen_window.destroy()

        frame_btn = ttk.Frame(self.resumen_window, style="mystyle.Treeview", padding=10)
        frame_btn.pack(fill=tk.X)

        crear_boton(frame_btn, texto="Guardar", ancho=20, alto=30, color_fondo="#1B3E84", color_texto="white", font=("Arial", 11, "bold"), hover_color="#2ECC71", comando=guardar).pack(side=tk.LEFT, padx=5)
        crear_boton(frame_btn, texto="Eliminar", ancho=20, alto=30, color_fondo="#913131", color_texto="white", font=("Arial", 11, "bold"), hover_color="#2ECC71", comando=eliminar).pack(side=tk.LEFT, padx=5)
        crear_boton(frame_btn, texto="Cerrar", ancho=20, alto=30, color_fondo="#555555", color_texto="white", font=("Arial", 11, "bold"), hover_color="#777777", comando=cerrar).pack(side=tk.RIGHT, padx=5)


    def limitar_texto(self, texto, limite=20):
        """Limitara la cantidad de caracteres dentro de una columna de borradores pendientes."""
        if len(texto) > limite:
            return texto[:limite] + "..."
        return texto
    
    
    def mostrar_contenido_completo(self, texto, titulo="Información completa"):
        """Mostrará el contenido completo en una ventana emergente si es mayor que el límite al hacer clic."""
        informacion_completa = tk.Toplevel(self.root)
        informacion_completa.title(titulo)
        informacion_completa.geometry("400x200")

        def cerrar_toplevel():
            informacion_completa.grab_release() 
            informacion_completa.destroy()

        texto_label = tk.Label(informacion_completa, text=texto, wraplength=380, justify=tk.LEFT)
        texto_label.pack(padx=10, pady=10)

        btn_cerrar = tk.Button(informacion_completa, text="Cerrar", command=cerrar_toplevel)
        btn_cerrar.pack(pady=10)
        
        # Forzar a Tkinter a dibujar la ventana antes de establecer el grab
        informacion_completa.update_idletasks()
        informacion_completa.grab_set()


    def mostrar_borradores_pendientes(self):
        """Muestra una ventana con los borradores pendientes."""
        borradores_window = tk.Toplevel(self.root)
        configurar_toplevel(borradores_window, titulo="Borradores Pendiente", ancho_min=840, alto_min=300, color_fondo="#101113")
        
        # Crear un frame principal para el Canvas y el Scrollbar
        borradores_main = tk.Frame(borradores_window)
        borradores_main.pack(fill=tk.BOTH, expand=True)
        
        # Crear un Canvas
        canvas = tk.Canvas(borradores_main, bg="#101113")
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(borradores_main, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Crear un Scrollbar vertical
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind("<Configure>", lambda e : canvas.configure(scrollregion=canvas.bbox("all")))
        
        # Crear un Frame dentro del canvas para contener los borradores.
        borradores_frame = tk.Frame(canvas, bg="#101113")
        canvas.create_window((0,0), window=borradores_frame, anchor="nw")
        
        borradores = borradores_pendientes()
        
        # Encabezados
        encabezados = ["ID", "Código", "Creador", "Tipo", "Tiempo Fab.", "Cantidad", "Descripción", "Fecha ini.", "Acciones"]
        for col, encabezado in enumerate(encabezados):
            tk.Label(borradores_frame, text=encabezado, font=("Arial", 10, "bold"), bg="#d1d1d1", fg="#101113").grid(row=0, column=col, padx=5, pady=5, sticky="nsew")

        for i, borrador in enumerate(borradores):
            # Mostrar los datos en las columnas 0 a 7
            for j in range(len(borrador) - 1):  # Solo hasta la penúltima columna
                texto_limitado = self.limitar_texto(str(borrador[j]))
                label = tk.Label(borradores_frame, text=texto_limitado, bg="#101113", fg="#ffffff", cursor="hand2")
                label.grid(row=i+1, column=j, padx=5, pady=5, sticky="nsew")
                label.bind("<Button-1>", lambda e, txt=borrador[j]: self.mostrar_contenido_completo(txt))

            # Botón "Cargar" en la última columna
            btn_cargar = tk.Button(borradores_frame, text="Cargar", bg="#4B82F0", fg="#101113",
                                command=lambda id=borrador[0]: self.cargar_borrador(id, borradores_window))
            btn_cargar.grid(row=i+1, column=8, padx=5, pady=5)

        # Configurar el peso de las columnas para que se ajusten al contenido
        for col in range(len(encabezados)):
            borradores_frame.columnconfigure(col, weight=1)
        
        
    def cargar_borrador(self, borrador_id, borradores_window):
        """Carga un borrador seleccionado."""
        borrador = cargar_borrador_db(borrador_id)
        if borrador:
            self.codigo_entry.delete(0, tk.END)
            self.descripcion_entry.delete(0, tk.END)
            self.tipo_combobox.set('')
            self.tiempo_entry.delete(0, tk.END)
            self.cantidad_creada_entry.delete(0, tk.END)

            self.codigo_entry.insert(0, borrador[0])
            self.descripcion_entry.insert(0, borrador[4])
            self.tipo_combobox.set(borrador[1])
            self.tiempo_entry.insert(0, borrador[2])
            self.cantidad_creada_entry.insert(0, borrador[3])

            self.materiales_usados = eval(borrador[5])

            if self.materiales_usados:
                print(f"Los materiales cargados del borrador son: {self.materiales_usados}")
                crear_boton(self.form_frame,
                    texto="Resumen Materiales",
                    ancho=30,
                    alto=30,
                    color_fondo="#DEE90D",
                    color_texto="white",
                    font=("Arial", 11, "bold"),
                    hover_color="#2ECC71",
                    comando=lambda: self.mostrar_resumen_materiales(self.root)
                ).grid(row=13, column=0, padx=5, pady=5)

            borradores_window.destroy()
            messagebox.showinfo("Éxito", f"Borrador {borrador_id} cargado correctamente.")
        else:
            messagebox.showerror("⚠️ Error", "No se encontró el borrador.")

    def calcular_costo_producto(self):
        """Calcula el costo total de producción del producto."""
        costo_total = 0.0
        for material in self.materiales_usados:
            costo_unitario = obtener_costo_unitario_material(material["codigo"])
            costo_total += material["cantidad"] * costo_unitario
        return round(costo_total, 2)

    def registrar_producto(self):
        """Registra el producto en la base de datos."""
        self.obtener_valores()

        if not self.codigo_producto or not self.tipo_producto or not self.tiempo_fabricacion or not self.descripcion_producto:
            messagebox.showerror("⚠️ Error", "Faltan datos obligatorios del producto.")
            return

        if not self.materiales_usados:
            messagebox.showerror("⚠️ Error", "No se han ingresado materiales para el producto.")
            return

        self.costo_produccion = self.calcular_costo_producto()
        precio_sugerido = self.costo_produccion * 5

        resumen_window = tk.Toplevel(self.root)
        configurar_toplevel(resumen_window, titulo="Resumen del Producto", ancho_min=500, alto_min=450)

        tk.Label(resumen_window, text=f"=== RESUMEN DEL PRODUCTO ===\nCódigo: {self.codigo_producto}\nTipo: {self.tipo_producto}\nDescripción: {self.descripcion_producto}\nMateriales usados: {len(self.materiales_usados)}\nCosto de producción: {self.costo_produccion}\nPrecio de venta sugerido: {precio_sugerido}", justify=tk.LEFT).pack(padx=10, pady=10)
        tk.Label(resumen_window, text="Precio de venta:").pack()
        precio_entry = tk.Entry(resumen_window)
        precio_entry.pack(pady=5)
        precio_entry.insert(0, precio_sugerido)

        def guardar_producto():
            try:
                self.precio_venta = round(float(precio_entry.get()), 2)
            except ValueError:
                messagebox.showerror("⚠️ Error", "Introduce un número válido para el precio")
                return

            materiales_reales = []
            for material in self.materiales_usados:
                nombre = obtener_nombre_material_por_codigo(material["codigo"])
                materiales_reales.append(nombre)

            insertar_producto(
                self.codigo_producto,
                self.nombre_producto,
                self.tipo_producto,
                self.costo_produccion,
                self.precio_venta,
                materiales_reales,
                self.tiempo_fabricacion,
                self.cantidad_creada,
                self.descripcion_producto
            )

            id_producto = obtener_id_producto_por_codigo(self.codigo_producto)

            for material in self.materiales_usados:
                id_material = obtener_id_material_por_codigo(material["codigo"])
                if id_material is not None:
                    insertar_detalle_producto(id_producto, id_material, material["cantidad"], material["tipo"], material["tamaño"])
                else:
                    messagebox.showinfo("No encontrado", f"No se encontró el material con código {material['codigo']}")

            for material in self.materiales_usados:
                actualizar_stock_material(material["codigo"], material["cantidad"])

            marcar_borrador_como_creado(self.codigo_producto)
            messagebox.showinfo("Éxito", "Producto creado y guardado correctamente.")
            resumen_window.destroy()
            self.volver_menu()

        crear_boton(resumen_window,
            texto="Guardar Producto",
            ancho=30,
            alto=30,
            color_fondo="#1B8420",
            color_texto="white",
            font=("Arial", 11, "bold"),
            hover_color="#2ECC71",
            comando=guardar_producto
        ).pack(pady=10)

        crear_boton(resumen_window,
            texto="Salir",
            ancho=30,
            alto=30,
            color_fondo="#913131",
            color_texto="white",
            font=("Arial", 11, "bold"),
            hover_color="#222423",
            comando=resumen_window.destroy
        ).pack(pady=5)
