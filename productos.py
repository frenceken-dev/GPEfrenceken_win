# modulo_productos.py

import tkinter as tk
from tkinter import messagebox, simpledialog
from db import (
    insertar_producto, 
    obtener_materiales, 
    actualizar_stock_material, 
    insertar_detalle_producto, 
    obtener_id_producto_por_codigo, 
    obtener_id_material_por_codigo, 
    obtener_costo_unitario_material,
    buscar_codigos_like,
    obtener_codigo_material_por_nombre_color_tipo_tamaño, 
    obtener_nombre_material_por_codigo, 
    obtener_tipos_por_material_y_color, 
    obtener_tamaños_por_material_color_tipo, 
    obtener_color_por_material,
    obtener_codigo_materiales,
    obtener_material_por_codigo
)
from tkinter import ttk
from inventario import convertir_a_float
from recursos import crear_boton, configurar_toplevel


# productos.py
def crear_producto(root, imagen_panel_tk, volver_menu):
    # Limpiar el frame de contenido
    for widget in root.winfo_children():
        widget.destroy()

    # Variables para el producto
    codigo_producto = ""
    nombre_producto = ""
    tipo_producto = ""
    descripcion_producto = ""
    tiempo_fabricacion = 0
    cantidad_creada = 0
    costo_produccion = 0.0
    precio_venta = 0.0

    # Variables para materiales usados
    materiales_usados = []
    cantidades_usadas = []
    materiales_reales = []

    # Obtener los materiales de la base de datos
    materiales = obtener_materiales()
    articulos = [material[1] for material in materiales]  # Codigo del material
    tipo_material = [material[3] for material in materiales] # El tipo de material
    tamaño_material = [material[4] for material in materiales] # El tamaño del Material
    cantidades = [convertir_a_float(material[6]) for material in materiales]  # Stock del material
    precios_uni = [convertir_a_float(material[8]) for material in materiales]  # Costo unitario del material

    # Obtener tipos y tamaños únicos
    tipos_unicos = list(set(tipo_material))
    tamaños_unicos = list(set(tamaño_material))
    
    # Función para registrar el producto en la base de datos
    def registrar_producto():
        nonlocal codigo_producto, nombre_producto, tipo_producto, tiempo_fabricacion, precio_venta
        # Validar que los campos obligatorios estén completos
        if not codigo_producto or not tipo_producto or tiempo_fabricacion <= 0:
            messagebox.showerror("Error", "Faltan datos obligatorios del producto.")
            return
        # Validar que se hayan ingresado materiales
        if not materiales_usados:
            messagebox.showerror("Error", "No se han ingresado materiales para el producto.")
            return

        # Calcular el costo del producto
        costo_produccion = calcular_costo_producto(materiales_usados)

        # Calcular precio de venta mínimo sugerido
        precio_sugerido = costo_produccion * 5

        # # Mostrar resumen del producto
        resumen = f"=== RESUMEN DEL PRODUCTO ===\n"
        # resumen += f"Código: {codigo_producto}\n"
        # resumen += f"Nombre: {nombre_producto}\n"
        # resumen += f"Tipo: {tipo_producto}\n"
        # resumen += f"Descripción: {descripcion_producto}\n"
        # resumen += f"Materiales usados:\n"
        # for material in materiales_usados:
        #     codigo_material = obtener_nombre_material_por_codigo(material["codigo"])
        #     costo_unitario = obtener_costo_unitario_material(material["codigo"])
        #     resumen += f"- {codigo_material} (Tipo: {material['tipo']}, Tamaño: {material['tamaño']}): {material['cantidad']} unidades (Costo: {costo_unitario * material['cantidad']})\n"
        # resumen += f"Costo de producción: {costo_produccion}\n"
        # resumen += f"\nPrecio de venta sugerido: {precio_sugerido}"

        # Ventana para mostrar el resumen y solicitar el precio de venta
        resumen_window = tk.Toplevel(root)
        configurar_toplevel(resumen_window, titulo="Resumen del Producto", ancho_min=500, alto_min=450)

        tk.Label(resumen_window, text=resumen, justify=tk.LEFT).pack(padx=10, pady=10)
        tk.Label(resumen_window, text="Precio de venta:").pack()
        precio_entry = tk.Entry(resumen_window)
        precio_entry.pack(pady=5)
        precio_entry.insert(0, precio_sugerido)  # Precio sugerido por defecto

        def guardar_producto():
            nonlocal precio_venta
            try:
                precio_venta = round(float(precio_entry.get()), 2)
            except ValueError:
                messagebox.showerror("Error", "Introduce un número válido para el precio")
                return

            materiales_reales = []
            for material in materiales_usados:
                nombre = obtener_nombre_material_por_codigo(material["codigo"])
                materiales_reales.append(nombre)

            # Guardar el producto en la base de datos
            insertar_producto(
                codigo_producto,
                nombre_producto,
                tipo_producto,
                costo_produccion,
                precio_venta,
                materiales_reales,
                tiempo_fabricacion,
                cantidad_creada,
                descripcion_producto
            )

            # Obtener el id_producto recién creado
            id_producto = obtener_id_producto_por_codigo(codigo_producto)

            # Insertar en Detalle_Producto para cada material usado
            for material in materiales_usados:
                id_material = obtener_id_material_por_codigo(material["codigo"])
                if id_material is not None:
                    insertar_detalle_producto(id_producto, id_material, material["cantidad"], material["tipo"], material["tamaño"])
                else:
                    messagebox.showinfo("No encontrado", f"No se encontró el material con código {material['codigo']}")

            # Actualizar el stock de los materiales en la base de datos
            for material in materiales_usados:
                actualizar_stock_material(material["codigo"], material["cantidad"])

            # Mostrar mensaje de éxito
            messagebox.showinfo("Éxito", "Producto creado y guardado correctamente.")
            resumen_window.destroy()
            volver_menu()

        crear_boton(resumen_window, 
                texto="Guardar Producto", 
                ancho=30,
                alto=30,
                color_fondo="#1B8420",                
                color_texto="white",
                font=("Arial", 11, "bold"),
                #bd=0,
                #relief=tk.FLAT,
                hover_color="#2ECC71",
                #activeforeground="black",
                comando=guardar_producto).pack(pady=10)
        crear_boton(resumen_window, 
                texto="Salir",
                ancho=30,
                alto=30,
                color_fondo="#913131",                
                color_texto="white",
                font=("Arial", 11, "bold"),
                #bd=0,
                #relief=tk.FLAT,
                hover_color="#222423",
                #activeforeground="black",
                #bg=0,
                comando=resumen_window.destroy).pack(pady=5)

    # Función para ingresar materiales
    def ingresar_materiales():
        nonlocal costo_produccion
        material_window = tk.Toplevel(root)
        configurar_toplevel(material_window, titulo="Ingresar Materiales", ancho_min=380, alto_min=300, color_fondo="#101113")
        #material_window.configure(bg="#a0b9f0")
        # Campo para seleccionar el material
        tk.Label(material_window, text="Material por Código:", bg="#101113", fg="#ffffff").grid(row=0, column=0, padx=10, pady=5)
        material_entry = ttk.Combobox(material_window, values=articulos)
        material_entry.grid(row=0, column=1, padx=10, pady=5)
        
        # Campo para el color del material
        tk.Label(material_window, text="Color:", bg="#101113", fg="#ffffff").grid(row=1, column=0, padx=10, pady=5)
        color_entry = ttk.Combobox(material_window, state="disabled")
        color_entry.grid(row=1, column=1, padx=10, pady=5)

        # Campo para el tipo de material (usando Combobox)
        tk.Label(material_window, text="Tipo:", bg="#101113", fg="#ffffff").grid(row=2, column=0, padx=10, pady=5)
        tipo_entry = ttk.Combobox(material_window, state="disabled")
        tipo_entry.grid(row=2, column=1, padx=10, pady=5)

        # Campo para la cantidad
        tk.Label(material_window, text="Cantidad:", bg="#101113", fg="#ffffff").grid(row=3, column=0, padx=10, pady=5)
        cantidad_entry = tk.Entry(material_window)
        cantidad_entry.grid(row=3, column=1, padx=10, pady=5)

        # Campo para el tamaño del material (usando Combobox)
        tk.Label(material_window, text="Tamaño:", bg="#101113", fg="#ffffff").grid(row=4, column=0, padx=10, pady=5)
        tamaño_entry = ttk.Combobox(material_window, state="disabled")
        tamaño_entry.grid(row=4, column=1, padx=10, pady=5)

        # Función para obtener codigos por patron.
        def filtrar_codigos(event):
            texto = material_entry.get()

            # Si no hay texto, mostrar todos
            if texto == "":
                material_entry['values'] = articulos
                return

            # Buscar en BD con LIKE
            resultados = buscar_codigos_like(texto)
            print("RESULTADOS DE LA BUSQUEDA POR PATRON: ", resultados)
            # Actualizar el combobox
            material_entry['values'] = resultados

        # Función para actualizar los tipos disponibles según el material seleccionado
        def actualizar_color(event):
            codigo_material = material_entry.get()
            if codigo_material:
                print("CODIGO QUE SE ENVIA A LA CONSULTA", codigo_material)
                color = obtener_color_por_material(codigo_material)
                color_entry['values'] = color
                color_entry.set('')  # Limpiar selección previa
                color_entry.configure(state="readonly")
                tamaño_entry.set('')  # Limpiar selección previa de tamaño
                tamaño_entry.configure(state="disabled")
                tipo_entry.set('') # Limpiar selección previa de tipo
                tipo_entry.configure(state="disabled")
            else:
                color_entry.set('')  # Limpiar selección previa
                color_entry.configure(state="readonly")
                tipo_entry.set('')
                tipo_entry.configure(state="disabled")
                tamaño_entry.set('')
                tamaño_entry.configure(state="disabled")
        # Función para actualizar los tipos disponibles según el material seleccionado
        
        def actualizar_tipos(event):
            codigo_material = material_entry.get()
            color_material = color_entry.get()
            if codigo_material and color_material:
                tipos = obtener_tipos_por_material_y_color(codigo_material, color_material)
                tipo_entry['values'] = tipos
                tipo_entry.set('')  # Limpiar selección previa
                tipo_entry.configure(state="readonly")
                tamaño_entry.set('')  # Limpiar selección previa de tamaño
                tamaño_entry.configure(state="disabled")
            else:
                tipo_entry.set('')
                tipo_entry.configure(state="disabled")
                tamaño_entry.set('')
                tamaño_entry.configure(state="disabled")

        # Función para actualizar los tamaños disponibles según el material y tipo seleccionados
        def actualizar_tamaños(event):
            codigo_material = material_entry.get()
            color_material = color_entry.get()
            tipo_material = tipo_entry.get()
            if codigo_material and color_material and tipo_material:
                tamaños = obtener_tamaños_por_material_color_tipo(codigo_material, color_material, tipo_material)
                tamaño_entry['values'] = tamaños
                tamaño_entry.set('')  # Limpiar selección previa
                tamaño_entry.configure(state="readonly")
            else:
                tamaño_entry.set('')
                tamaño_entry.configure(state="disabled")

        # Vincular eventos para actualizar los Combobox
        material_entry.bind("<KeyRelease>", filtrar_codigos)
        #material_entry.bind("<<ComboboxSelected>>", filtrar_codigos)
        material_entry.bind("<<ComboboxSelected>>", actualizar_color)
        color_entry.bind("<<ComboboxSelected>>", actualizar_tipos)
        tipo_entry.bind("<<ComboboxSelected>>", actualizar_tamaños)

        def agregar_material():
            nonlocal costo_produccion
            material_actual = material_entry.get()
            color_material_actual = color_entry.get()
            tipo_material_actual = tipo_entry.get()
            tamaño_material_actual = tamaño_entry.get()

            try:
                cantidad_necesaria = convertir_a_float(cantidad_entry.get())
            except ValueError:
                messagebox.showerror("Error", "La cantidad debe ser un número entero.")
                return
            print("MATERIAL ACTUAL ES: ", material_actual)
            codigo_material = obtener_codigo_material_por_nombre_color_tipo_tamaño(material_actual, color_material_actual, tipo_material_actual, tamaño_material_actual)

            if codigo_material is not None:
                try:
                    indice = articulos.index(material_actual)
                except ValueError:
                    messagebox.showerror("Error", f"Material {material_actual} no encontrado.")
                    return

                if cantidades[indice] >= cantidad_necesaria:
                    materiales_usados.append({
                        "codigo": codigo_material,
                        "color": color_material_actual,
                        "tipo": tipo_material_actual,
                        "tamaño": tamaño_material_actual,
                        "cantidad": cantidad_necesaria
                    })
                    material_window.destroy()
                    # Mesanje de Agregado con exito.
                    messagebox.showinfo("Éxito", f"Material {material_actual} registrado correctamente.")
                else:
                    messagebox.showerror("Error", f"No hay suficiente stock de {material_actual}. Stock disponible: {cantidades[indice]}")
            else:
                messagebox.showerror("Error", f"No se encontró el material {material_actual} con tipo {tipo_material_actual} y tamaño {tamaño_material_actual}.")

        crear_boton(material_window, 
                texto="Agregar Material", 
                ancho=30,
                alto=30,
                color_fondo="#1B3E84",                
                color_texto="white",
                font=("Arial", 11, "bold"),
                #bd=0,
                #relief=tk.FLAT,
                hover_color="#2ECC71",
                #activeforeground="black",
                comando=agregar_material).grid(row=5, column=0, columnspan=2, pady=10)
        
        crear_boton(material_window, 
                texto="Guardar borrador", 
                ancho=30,
                alto=30,
                color_fondo="#DEE90D",                
                color_texto="white",
                font=("Arial", 11, "bold"),
                #bd=0,
                #relief=tk.FLAT,
                hover_color="#2ECC71",
                #activeforeground="black",
                #comando=agregar_material
                ).grid(row=6, column=0, columnspan=2, pady=10)       
    

    def mostrar_resumen_materiales(materiales_usados, ventana_padre):
        resumen = tk.Toplevel(ventana_padre)
        configurar_toplevel(resumen, titulo="Resumen de Materiales", ancho_min=400, alto_min=350)
        resumen.configure(bg="#a0b9f0")

        # 🔒 Ventana MODAL (muy importante)
        resumen.transient(ventana_padre)
        resumen.grab_set()
        resumen.focus_set()

        frame = tk.Frame(resumen)
        frame.pack(fill=tk.BOTH, expand=True)

        columnas = ("codigo", "color", "tipo", "tamaño", "cantidad")

        tree = ttk.Treeview(
            frame,
            columns=columnas,
            show="headings",
            height=10
        )

        encabezados = {
            "codigo": "Código",
            "color": "Color",
            "tipo": "Tipo",
            "tamaño": "Tamaño",
            "cantidad": "Cantidad"
        }

        for col in columnas:
            tree.heading(col, text=encabezados[col])
            tree.column(col, anchor=tk.CENTER, width=130)

        tree.pack(fill=tk.BOTH, expand=True) # DEBAJO COLOCAR LOS NUEVOS AJUSTES


        # ─────────────────────────────────────────
        # 🧾 Editor embebido debajo del Treeview
        # ─────────────────────────────────────────
        editor = ttk.LabelFrame(frame, text="Editar material seleccionado", padding=10)
        editor.pack(fill=tk.X, padx=10, pady=8)

        ttk.Label(editor, text="Código").grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(editor, text="Color").grid(row=0, column=2, padx=5, pady=5)
        ttk.Label(editor, text="Tipo").grid(row=1, column=0, padx=5, pady=5)
        ttk.Label(editor, text="Tamaño").grid(row=1, column=2, padx=5, pady=5)
        ttk.Label(editor, text="Cantidad").grid(row=2, column=0, padx=5, pady=5)

        codigo_var = tk.StringVar()
        color_var = tk.StringVar()
        tipo_var = tk.StringVar()
        tam_var = tk.StringVar()
        cant_var = tk.StringVar()

        combo_codigo = ttk.Combobox(editor, textvariable=codigo_var, state="readonly", width=18)
        combo_codigo.grid(row=0, column=1, padx=5)

        entry_color = ttk.Entry(editor, textvariable=color_var, state="readonly", width=18)
        entry_color.grid(row=0, column=3, padx=5)

        entry_tipo = ttk.Entry(editor, textvariable=tipo_var, state="readonly", width=18)
        entry_tipo.grid(row=1, column=1, padx=5)

        entry_tam = ttk.Entry(editor, textvariable=tam_var, state="readonly", width=18)
        entry_tam.grid(row=1, column=3, padx=5)

        entry_cant = ttk.Entry(editor, textvariable=cant_var, width=18)
        entry_cant.grid(row=2, column=1, padx=5)

        # 📥 Cargar códigos disponibles
        combo_codigo["values"] = obtener_codigo_materiales()
        print("Codigos disponibles: ", combo_codigo["values"])

        # 📥 Cargar datos
        def cargar():
            tree.delete(*tree.get_children())
            for mat in materiales_usados:
                tree.insert("", tk.END, values=(
                    mat["codigo"],
                    mat["color"],
                    mat["tipo"],
                    mat["tamaño"],
                    mat["cantidad"]
                ))
            resumen.update_idletasks()
            resumen.geometry("")

        cargar()

        # 📌 Cargar datos del Treeview al editor
        def cargar_en_editor(event=None):
            item = tree.selection()
            if not item:
                return

            valores = tree.item(item[0])["values"]
            codigo_var.set(valores[0])
            color_var.set(valores[1])
            tipo_var.set(valores[2])
            tam_var.set(valores[3])
            cant_var.set(valores[4])

            # def aplicar_cambios():
            #     item = tree.selection()
            #     if not item:
            #         return

            #     tree.item(item[0], values=(
            #         codigo_var.get(),
            #         color_var.get(),
            #         tipo_var.get(),
            #         tam_var.get(),
            #         convertir_a_float(cant_var.get())
            #     ))
            
        def actualizar_desde_editor():
            item = tree.selection()
            if not item:
                return

            tree.item(item[0], values=(
                codigo_var.get(),
                color_var.get(),
                tipo_var.get(),
                tam_var.get(),
                convertir_a_float(cant_var.get())
            ))

        # ✏️ Edición por doble clic
        # def editar_celda(event):
        #     region = tree.identify_region(event.x, event.y)
        #     if region != "cell":
        #         return

        #     fila = tree.identify_row(event.y)
        #     col = tree.identify_column(event.x)
        #     if not fila or not col:
        #         return

        #     col_idx = int(col[1:]) - 1
        #     x, y, w, h = tree.bbox(fila, col)

        #     valor_actual = tree.item(fila)["values"][col_idx]

        #     entry = tk.Entry(tree)
        #     entry.place(x=x, y=y, width=w, height=h)
        #     entry.insert(0, valor_actual)
        #     entry.focus()

        #     def guardar(_=None):
        #         valores = list(tree.item(fila)["values"])
        #         valores[col_idx] = entry.get()
        #         tree.item(fila, values=valores)
        #         entry.destroy()

        #     entry.bind("<Return>", guardar)
        #     entry.bind("<FocusOut>", guardar)

        #tree.bind("<Double-1>", editar_celda)
        

        # 🔄 Al cambiar código, actualizar datos automáticamente
        def actualizar_por_codigo(event=None):
            codigo = codigo_var.get()
            if not codigo:
                return
            # REVISAR CONSULTA DE DB
            data = obtener_material_por_codigo(codigo)
            if not data:
                return

            color_var.set(data["color"])
            tipo_var.set(data["tipo"])
            tam_var.set(data["tamaño"])

        tree.bind("<<TreeviewSelect>>", cargar_en_editor)
        tree.bind("<Double-1>", cargar_en_editor)
        combo_codigo.bind("<<ComboboxSelected>>", actualizar_por_codigo)

        # 💾 Guardar cambios en la lista original
        def guardar():
            materiales_usados.clear()
            for item in tree.get_children():
                c, col, t, tam, cant = tree.item(item)["values"]
                materiales_usados.append({
                    "codigo": c,
                    "color": col,
                    "tipo": t,
                    "tamaño": tam,
                    "cantidad": convertir_a_float(cant)
                })

        def eliminar():
            item = tree.selection()
            if not item:
                return
            tree.delete(item[0])

        def cerrar():
            resumen.destroy()

        # 🔘 BOTONES (sin romper tu helper)
        frame_btn = ttk.Frame(resumen, padding=10)
        frame_btn.pack(fill=tk.X)

        crear_boton(frame_btn, texto="Actualizar",
        ancho=30,
        alto=30,
        color_fondo="#1B3E84",                
        color_texto="white",
        font=("Arial", 11, "bold"),
        #bd=0,
        #relief=tk.FLAT,
        hover_color="#2ECC71",
        #activeforeground="black",
        comando=actualizar_desde_editor).pack(side=tk.LEFT, padx=5)

        crear_boton(frame_btn, texto="Guardar", 
        ancho=30,
        alto=30,
        color_fondo="#1B3E84",          
        color_texto="white",
        font=("Arial", 11, "bold"),
        #bd=0,
        #relief=tk.FLAT,
        hover_color="#2ECC71",
        #activeforeground="black",
        comando=guardar).pack(side=tk.LEFT, padx=5)

        crear_boton(frame_btn, texto="Eliminar",  
        ancho=30,
        alto=30,
        color_fondo="#913131",           
        color_texto="white",
        font=("Arial", 11, "bold"),
        #bd=0,
        #relief=tk.FLAT,
        hover_color="#2ECC71",
        #activeforeground="black",
        comando=eliminar).pack(side=tk.LEFT, padx=5)

        crear_boton(frame_btn, texto="Cerrar",  
        ancho=30,
        alto=30,
        color_fondo="#555555",            
        color_texto="white",
        font=("Arial", 11, "bold"),
        #bd=0,
        #relief=tk.FLAT,
        hover_color="#777777",
        #activeforeground="black",
        comando=cerrar).pack(side=tk.RIGHT, padx=5)


    # Función para buscar un material y validar stock
    def buscar_material_para_producto(articulos, cantidades, precios_uni, cantidad_necesaria, material_actual):
        try:
            indice = articulos.index(material_actual)
            return True, indice  # Material encontrado
        except ValueError:
            return False, -1  # Material no encontrado

    # Frame principal
    frame = tk.Frame(root, bg="#a0b9f0", width=800, height=600)
    frame.pack(fill=tk.BOTH, expand=True)

    # Panel izquierdo
    frame_menu = tk.Frame(frame, bg="#2C3E50", width=200, height=800, bd=3, relief="solid")
    frame_menu.pack(side=tk.LEFT, fill=tk.Y)
    frame_menu.pack_propagate(False)
        
    frame_imagen_panel = tk.Frame(frame_menu, bg="#2C3E50", height=70)
    frame_imagen_panel.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

    # Imagen del Logo para el panel izquierdo
    if imagen_panel_tk:
        label_imagen = tk.Label(frame_imagen_panel, image=imagen_panel_tk, bg="#2C3E50")
        label_imagen.pack(side=tk.LEFT, padx=70)
    else:
        label_texto = tk.Label(frame_imagen_panel, text="Ikigai", font=("Arial", 10), bg="#2C3E50")
        label_texto.pack(side=tk.LEFT, padx=70)

    # Frame inferior dentro del menú lateral
    frame_inferior = tk.Frame(frame_menu, bg="#2C3E50")
    frame_inferior.pack(side="bottom", fill="x", pady=20)  # <- este pady sí separa del borde inferior
    
    # Mostrar el título
    frame_titulo = tk.Frame(frame, bg="#a0b9f0")
    frame_titulo.pack(side=tk.TOP, fill=tk.X, pady=15)

    # Formulario para crear el producto
    form_frame = tk.Frame(frame, bg="#a0b9f0", padx=20, pady=20)
    form_frame.place(relx=0.5, rely=0.1, anchor=tk.N)

    # Título
    title_label = tk.Label(
        frame_titulo,
        text="Creación de Nuevos Productos",
        font=("Arial", 16, "bold"),
        bg="#a0b9f0",
        fg="#2C3E50"
    )
    title_label.pack(pady=15)

    # Botón para volver
    back_button = crear_boton(
        frame_inferior,
        texto="Volver",
        ancho=30,
        alto=30,
        color_fondo="#913131",                
        color_texto="white",
        font=("Arial", 11, "bold"),
        #bd=0,
        #relief=tk.FLAT,
        hover_color="#222423",
        #activeforeground="black",
        #bg=0,
        comando=volver_menu 
    )
    back_button.pack(side="bottom", padx=30, pady=30)

    # Campos para ingresar la información del producto
    tk.Label(form_frame, text="Código del producto:", bg="#a0b9f0", anchor="w").grid(row=0, column=0, sticky="w", pady=1)
    codigo_entry = tk.Entry(form_frame, width=30)
    codigo_entry.grid(row=1, column=0, pady=5)

    # tk.Label(form_frame, text="Nombre del producto:", bg="#8e98f5").grid(row=1, column=0, sticky="e")
    # nombre_entry = tk.Entry(form_frame, width=30)
    # nombre_entry.grid(row=1, column=1, pady=5)

    tk.Label(form_frame, text="Tipo (Pulsera/Collar/Aretes/Llavero):", bg="#a0b9f0").grid(row=2, column=0, sticky="w", pady=1)
    tipo_combobox = ttk.Combobox(form_frame, values=["pulsera", "collar", "aretes", "llavero"], width=28)
    tipo_combobox.grid(row=3, column=0, pady=5)
    
    tk.Label(form_frame, text="Descripción:", bg="#a0b9f0").grid(row=8, column=0, sticky="w", pady=1)
    descripcion_entry = tk.Entry(form_frame, width=30)
    descripcion_entry.grid(row=9, column=0, pady=5)
    
    tk.Label(form_frame, text="Tiempo de fabricación (minutos):", bg="#a0b9f0").grid(row=4, column=0, sticky="w", pady=1)
    tiempo_entry = tk.Entry(form_frame, width=30)
    tiempo_entry.grid(row=5, column=0, pady=5)
    
    tk.Label(form_frame, text="Cantidad Creada:", bg="#a0b9f0").grid(row=6, column=0, sticky="w", pady=1)
    cantidad_creada_entry = tk.Entry(form_frame, width=30)
    cantidad_creada_entry.grid(row=7, column=0, pady=5)

    # Función para obtener los valores de los campos
    def obtener_valores():
        nonlocal codigo_producto, nombre_producto, tipo_producto, descripcion_producto, tiempo_fabricacion, cantidad_creada
        codigo_producto = codigo_entry.get()
        #nombre_producto = nombre_entry.get()
        tipo_producto = tipo_combobox.get()
        descripcion_producto = descripcion_entry.get()
        tiempo_fabricacion = convertir_a_float(tiempo_entry.get())
        cantidad_creada = int(cantidad_creada_entry.get())

    # Botones
    crear_boton(
        form_frame,
        texto="Ingresar Materiales",
        ancho=30,
        alto=30,
        color_fondo="#143E86",                
        color_texto="white",
        font=("Arial", 11, "bold"),
        #bd=0,
        #relief=tk.FLAT,
        hover_color="#2ECC71",
        #activeforeground="black",
        comando=lambda: [
            obtener_valores(),
            ingresar_materiales()
        ],
        
    ).grid(row=12, column=0, pady=5)

    crear_boton(
        form_frame,
        texto="Registrar Producto",
        ancho=30,
        alto=30,
        color_fondo="#1B8420",                
        color_texto="white",
        font=("Arial", 11, "bold"),
        #bd=0,
        #relief=tk.FLAT,
        hover_color="#2ECC71",
        #activeforeground="black",
        comando=registrar_producto,
        
    ).grid(row=12, column=1, pady=5)

    crear_boton(form_frame, 
                texto="Resumen Materiales", 
                ancho=30,
                alto=30,
                color_fondo="#DEE90D",                
                color_texto="white",
                font=("Arial", 11, "bold"),
                #bd=0,
                #relief=tk.FLAT,
                hover_color="#2ECC71",
                #activeforeground="black",
                comando=lambda : mostrar_resumen_materiales(materiales_usados, root) # Ajuste para editar materiales
                    ).grid(row=13, column=0, pady=5)
    

def calcular_costo_producto(materiales_usados):
    costo_total = 0.0
    for material in materiales_usados:
        costo_unitario = obtener_costo_unitario_material(material["codigo"])
        costo_total += material["cantidad"] * costo_unitario
    return round(costo_total, 2)

