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
    obtener_codigo_material_por_nombre_color_tipo_tamaño, 
    obtener_nombre_material_por_codigo, 
    obtener_tipos_por_material_y_color, 
    obtener_tamaños_por_material_color_tipo, 
    obtener_color_por_material
)
from tkinter import ttk
from inventario import convertir_a_float

# productos.py
def crear_producto(frame_contenido, volver_menu):
    # Limpiar el frame de contenido
    for widget in frame_contenido.winfo_children():
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
    articulos = [material[2] for material in materiales]  # Nombre del material
    tipo_material = [material[3] for material in materiales] # El tipo de material
    tamaño_material = [material[4] for material in materiales] # El tamaño del Material
    cantidades = [float(material[6]) for material in materiales]  # Stock del material
    precios_uni = [float(material[8]) for material in materiales]  # Costo unitario del material

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
        precio_sugerido = costo_produccion * 2

        # Mostrar resumen del producto
        resumen = f"=== RESUMEN DEL PRODUCTO ===\n"
        resumen += f"Código: {codigo_producto}\n"
        resumen += f"Nombre: {nombre_producto}\n"
        resumen += f"Tipo: {tipo_producto}\n"
        resumen += f"Descripción: {descripcion_producto}\n"
        resumen += f"Materiales usados:\n"
        for material in materiales_usados:
            nombre_material = obtener_nombre_material_por_codigo(material["codigo"])
            costo_unitario = obtener_costo_unitario_material(material["codigo"])
            resumen += f"- {nombre_material} (Tipo: {material['tipo']}, Tamaño: {material['tamaño']}): {material['cantidad']} unidades (Costo: {costo_unitario * material['cantidad']})\n"
        resumen += f"Costo de producción: {costo_produccion}\n"
        resumen += f"\nPrecio de venta sugerido: {precio_sugerido}"

        # Ventana para mostrar el resumen y solicitar el precio de venta
        resumen_window = tk.Toplevel(frame_contenido)
        resumen_window.title("Resumen del Producto")
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

        tk.Button(resumen_window, text="Guardar Producto", command=guardar_producto).pack(pady=10)
        tk.Button(resumen_window, text="Salir", command=resumen_window.destroy).pack(pady=5)

    # Función para ingresar materiales
    def ingresar_materiales():
        nonlocal costo_produccion
        material_window = tk.Toplevel(frame_contenido)
        material_window.title("Ingresar Materiales")

        # Campo para seleccionar el material
        tk.Label(material_window, text="Material:").grid(row=0, column=0, padx=10, pady=5)
        material_entry = ttk.Combobox(material_window, values=articulos)
        material_entry.grid(row=0, column=1, padx=10, pady=5)
        
        # Campo para el color del material
        tk.Label(material_window, text="Color:").grid(row=1, column=0, padx=10, pady=5)
        color_entry = ttk.Combobox(material_window, state="disabled")
        color_entry.grid(row=1, column=1, padx=10, pady=5)

        # Campo para el tipo de material (usando Combobox)
        tk.Label(material_window, text="Tipo:").grid(row=2, column=0, padx=10, pady=5)
        tipo_entry = ttk.Combobox(material_window, state="disabled")
        tipo_entry.grid(row=2, column=1, padx=10, pady=5)

        # Campo para la cantidad
        tk.Label(material_window, text="Cantidad:").grid(row=3, column=0, padx=10, pady=5)
        cantidad_entry = tk.Entry(material_window)
        cantidad_entry.grid(row=3, column=1, padx=10, pady=5)

        # Campo para el tamaño del material (usando Combobox)
        tk.Label(material_window, text="Tamaño:").grid(row=4, column=0, padx=10, pady=5)
        tamaño_entry = ttk.Combobox(material_window, state="disabled")
        tamaño_entry.grid(row=4, column=1, padx=10, pady=5)

        # Función para actualizar los tipos disponibles según el material seleccionado
        def actualizar_color(event):
            nombre_material = material_entry.get()
            if nombre_material:
                color = obtener_color_por_material(nombre_material)
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
            nombre_material = material_entry.get()
            color_material = color_entry.get()
            if nombre_material and color_material:
                tipos = obtener_tipos_por_material_y_color(nombre_material, color_material)
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
            nombre_material = material_entry.get()
            color_material = color_entry.get()
            tipo_material = tipo_entry.get()
            if nombre_material and color_material and tipo_material:
                tamaños = obtener_tamaños_por_material_color_tipo(nombre_material, color_material, tipo_material)
                tamaño_entry['values'] = tamaños
                tamaño_entry.set('')  # Limpiar selección previa
                tamaño_entry.configure(state="readonly")
            else:
                tamaño_entry.set('')
                tamaño_entry.configure(state="disabled")

        # Vincular eventos para actualizar los Combobox
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
                    messagebox.showinfo("Éxito", f"Material {material_actual} registrado correctamente.")
                    material_window.destroy()
                else:
                    messagebox.showerror("Error", f"No hay suficiente stock de {material_actual}. Stock disponible: {cantidades[indice]}")
            else:
                messagebox.showerror("Error", f"No se encontró el material {material_actual} con tipo {tipo_material_actual} y tamaño {tamaño_material_actual}.")

        tk.Button(material_window, text="Agregar Material", command=agregar_material).grid(row=5, column=0, columnspan=2, pady=10)        
   
    # Función para buscar un material y validar stock
    def buscar_material_para_producto(articulos, cantidades, precios_uni, cantidad_necesaria, material_actual):
        try:
            indice = articulos.index(material_actual)
            return True, indice  # Material encontrado
        except ValueError:
            return False, -1  # Material no encontrado
        
    # Mostrar el título
    frame_titulo = tk.Frame(frame_contenido, bg="#a0b9f0")
    frame_titulo.pack(side=tk.TOP, fill=tk.X, pady=15)

    # Formulario para crear el producto
    form_frame = tk.Frame(frame_contenido, bg="#a0b9f0", padx=20, pady=20)
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

    # Campos para ingresar la información del producto
    tk.Label(form_frame, text="Código del producto:", bg="#a0b9f0", anchor="w").grid(row=0, column=0, sticky="w", pady=1)
    codigo_entry = tk.Entry(form_frame, width=30)
    codigo_entry.grid(row=1, column=0, pady=5)

    # tk.Label(form_frame, text="Nombre del producto:", bg="#8e98f5").grid(row=1, column=0, sticky="e")
    # nombre_entry = tk.Entry(form_frame, width=30)
    # nombre_entry.grid(row=1, column=1, pady=5)

    tk.Label(form_frame, text="Tipo (pulsera/collar/aretes/llavero):", bg="#a0b9f0").grid(row=2, column=0, sticky="w", pady=1)
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
        tiempo_fabricacion = float(tiempo_entry.get())
        cantidad_creada = int(cantidad_creada_entry.get())

    # Botones
    tk.Button(
        form_frame,
        text="Ingresar Materiales",
        command=lambda: [
            obtener_valores(),
            ingresar_materiales()
        ],
        bg="#75EC57"
    ).grid(row=12, column=0, pady=5)

    tk.Button(
        form_frame,
        text="Registrar Producto",
        command=registrar_producto,
        bg="#4283fa"
    ).grid(row=12, column=1, pady=5)


def calcular_costo_producto(materiales_usados):
    costo_total = 0.0
    for material in materiales_usados:
        costo_unitario = obtener_costo_unitario_material(material["codigo"])
        costo_total += material["cantidad"] * costo_unitario
    return round(costo_total, 2)

