# inventario.py

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, simpledialog
from db import (
    obtener_nombres_proveedores, 
    insertar_factura, insertar_material, 
    obtener_id_proveedor_por_nombre, 
    obtener_id_factura_por_numero, 
    obtener_id_material_por_codigo, 
    insertar_detalle_factura,
    codigo_existe
)
from recursos import crear_boton, configurar_toplevel, LOGO_PATH, redimensionar_imagen


# Variables globales para almacenar datos temporales
materiales_temporales = []  # Lista para almacenar los materiales antes de guardar
datos_factura = {
    "proveedor": "",
    "numero_factura": "",
    "fecha": ""
}

def ingresar_inventario(root, imagen_panel_tk, volver_menu):
    # Limpiar el frame de contenido
    for widget in root.winfo_children():
        widget.destroy()

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

    frame_titulo = tk.Frame(frame, bg="#a0b9f0")
    frame_titulo.pack(side=tk.TOP, fill=tk.X, pady=15)

    # Formulario para ingresar factura
    form_frame = tk.Frame(frame, bg="#a0b9f0", padx=20, pady=20)
    form_frame.place(relx=0.5, rely=0.1, anchor=tk.N)

    # Título
    title_label = tk.Label(
        frame_titulo,
        text="Aumento de inventario por facturas",
        font=("Arial", 16, "bold"),
        bg="#a0b9f0",
        fg="#2C3E50"
    )
    title_label.pack(pady=15)

    # Campos de la factura
    tk.Label(form_frame, text="Proveedor:", bg="#a0b9f0").grid(row=0, column=0, sticky="e") # ajustar entry mostrar lista
    proveedor_entry = tk.Entry(form_frame, width=30)
    proveedor_entry.grid(row=0, column=1, pady=5)
    
    # Obtener nombres de proveedores desde BD
    nombres_proveedores = obtener_nombres_proveedores(proveedor_entry.get())
    
    # Crear el Combox
    proveedor_combobox = ttk.Combobox(form_frame, values=nombres_proveedores, width=28)
    proveedor_combobox.grid(row=0, column=1, pady=5)
    
    # Funcion para actualizar las funciones del combobox según lo que se escriba.
    def actualizar_opciones(event):
        texto = proveedor_combobox.get()
        proveedores_filtrados = obtener_nombres_proveedores(texto)
        proveedor_combobox['values'] = proveedores_filtrados
        
    # Vincular la funcion al evento de escritura.
    proveedor_combobox.bind('<KeyRelease>', actualizar_opciones)    
    
    # Ingreso Número de fectura
    tk.Label(form_frame, text="Número de Factura:", bg="#a0b9f0").grid(row=1, column=0, sticky="e")
    factura_entry = tk.Entry(form_frame, width=30)
    factura_entry.grid(row=1, column=1, pady=5)

    # Fecha de ingreso al sistema
    tk.Label(form_frame, text="Fecha (DD/MM/AAAA):", bg="#a0b9f0").grid(row=2, column=0, sticky="e")
    fecha_entry = tk.Entry(form_frame, width=30)
    fecha_entry.grid(row=2, column=1, pady=5)
    
    # Botones (inicialmente deshabilitados)
    btn_agregar_material = crear_boton(
        form_frame,
        texto="Agregar Material",
        ancho=30,
        alto=30,
        color_fondo="#073EAD",
        color_texto="white",
        font=("Arial", 11, "bold"),
        #bd=0,
        #relief=tk.FLAT,
        hover_color="#2ECC71",
        #activeforeground="black",
        comando=lambda: agregar_material_temporal(frame)
    )
    btn_agregar_material.grid(row=3, column=0, pady=20)
    btn_agregar_material.set_state("disabled")  # ← Aquí sí, ya con método real


    btn_mostrar_datos = crear_boton(
        form_frame,
        texto="Mostrar Datos Ingresados",
        ancho=30,
        alto=30,
        color_fondo="#324f98",                
        color_texto="white",
        font=("Arial", 11, "bold"),
        #bd=0,
        #relief=tk.FLAT,
        hover_color="#2ECC71",
        #activeforeground="black",
        comando=lambda: [
            datos_factura.update({
                "proveedor": proveedor_combobox.get(),
                "numero_factura": factura_entry.get(),
                "fecha": fecha_entry.get()
            }),
            mostrar_datos_ingresados()
        ],
        state=tk.DISABLED
    )
    btn_mostrar_datos.grid(row=3, column=1, pady=20)

    btn_guardar_factura = crear_boton(
        form_frame,
        texto="Guardar Factura",
        ancho=30,
        alto=30,
        color_fondo="#4283fa",                
        color_texto="white",
        font=("Arial", 11, "bold"),
        #bd=0,
        #relief=tk.FLAT,
        hover_color="#2ECC71",
        #activeforeground="black",
        comando=lambda: [
            datos_factura.update({
                "proveedor": proveedor_combobox.get(),
                "numero_factura": factura_entry.get(),
                "fecha": fecha_entry.get()
            }),
            guardar_factura_y_materiales(frame)
        ],
        state=tk.DISABLED
    )
    btn_guardar_factura.grid(row=4, column=0, columnspan=2, pady=20)

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

    # Función para validar campos al cambiar su contenido
    def on_campo_cambiado(*args):
        actualizar_estado_botones(
            proveedor_combobox.get(),
            factura_entry.get(),
            fecha_entry.get(),
            btn_agregar_material,
            btn_mostrar_datos,
            btn_guardar_factura
        )

    # Vincular la función a los cambios en los campos
    proveedor_combobox.bind("<<ComboboxSelected>>", lambda _: on_campo_cambiado())
    proveedor_combobox.bind("<KeyRelease>", lambda _: on_campo_cambiado())
    factura_entry.bind("<KeyRelease>", lambda _: on_campo_cambiado())
    fecha_entry.bind("<KeyRelease>", lambda _: on_campo_cambiado())

    
    # Función para validar campos obligatorios
    def agregar_material_temporal(frame_contenido, ):
        # Crear una ventana emergente para ingresar los datos del material
        material_window = tk.Toplevel(frame_contenido)
        configurar_toplevel(material_window, titulo="Agregar Material", ancho_min=300, alto_min=330, color_fondo="#101113")
        #material_window.configure(bg="#a0b9f0")

        # Campos para el material
        tk.Label(material_window, text="Código:", bg="#101113", fg="#ffffff").grid(row=0, column=0, padx=10, pady=5)
        codigo_entry = tk.Entry(material_window)
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

        
        # Comprobar que el codigo no este en la lista temporal
        def existe_codigo_lista_temporales(codigo):
            for material in materiales_temporales:
                if codigo == material["codigo"]:
                    return True
                else:
                    return False
                
                
        # Función para guardar el material temporalmente
        def guardar_material():
            
            codigo = codigo_entry.get()
            #existe_codigo = codigo_existe(codigo_entry.get())
            precio = convertir_a_float(precio_entry.get())
            cantidad = convertir_a_float(stock_entry.get())
            costo_unitario = precio / cantidad
            
            codigo_db = codigo_existe(codigo)
            # Verificar si el código ya existe
            if codigo_db or existe_codigo_lista_temporales(codigo):
                messagebox.showerror("⚠️ Error", "El Código ya existe. Por favor, usa un código único.")
                material_window.lift()  # Traer la ventana al frente
                material_window.focus_force()  # Forzar el foco en la ventana
                return  # No cerrar la ventana

            # Validar que cantidad y precio sean números
            try:
                cantidad_float = float(cantidad)
                precio_float = float(precio)
            except ValueError:
                messagebox.showerror("⚠️ Error", "La cantidad y el precio deben ser números válidos.")
                return  # No cerrar la ventana            
            
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
            materiales_temporales.append(material)
            messagebox.showinfo("Éxito", "Material agregado temporalmente.")
            material_window.destroy()

        # Botón para guardar el material
        boton_guardar_material = crear_boton(
        material_window,
        texto="Guardar Material",
        ancho=30,
        alto=30,
        color_fondo="#4283fa",                
        color_texto="white",
        font=("Arial", 11, "bold"),
        #bd=0,
        #relief=tk.FLAT,
        hover_color="#2ECC71",
        #activeforeground="black",
        comando=guardar_material
    )
        boton_guardar_material.grid(row=7, column=0, columnspan=2, padx=15, pady=10)


def validar_campos_obligatorios(proveedor, num_factura, fecha):
    return proveedor.strip() != "" and num_factura.strip() != "" and fecha.strip() != ""


# Función para actualizar el estado de los botones
# def actualizar_estado_botones(proveedor, num_factura, fecha, btn_agregar_material, btn_mostrar_datos, btn_guardar_factura):
    
#     if validar_campos_obligatorios(proveedor, num_factura, fecha):
#         btn_agregar_material.config(state=tk.NORMAL)
#         btn_mostrar_datos.config(state=tk.NORMAL)
#         btn_guardar_factura.config(state=tk.NORMAL)
#     else:
#         btn_agregar_material.config(state=tk.DISABLED)
#         btn_mostrar_datos.config(state=tk.DISABLED)
#         btn_guardar_factura.config(state=tk.DISABLED)

def actualizar_estado_botones(proveedor, num_factura, fecha, btn_agregar_material, btn_mostrar_datos, btn_guardar_factura):
    estado_activo = validar_campos_obligatorios(proveedor, num_factura, fecha)

    botones = [btn_agregar_material, btn_mostrar_datos, btn_guardar_factura]

    for boton in botones:
        # Verificamos si el botón tiene método set_state (botón macOS)
        if hasattr(boton, "set_state"):
            boton.set_state("normal" if estado_activo else "disabled")
        else:
            boton.config(state=tk.NORMAL if estado_activo else tk.DISABLED)


def limpiar_campos(frame_contenido):
    # Limpiar los campos de la factura
    for widget in frame_contenido.winfo_children():
        if isinstance(widget, tk.Frame):
            for child in widget.winfo_children():
                if isinstance(child, tk.Entry):
                    child.delete(0, tk.END)
                elif isinstance(child, ttk.Combobox):
                    child.set('')


def guardar_factura_y_materiales(frame_contenido):
    # Validar que los datos de la factura estén completos
    if not datos_factura["proveedor"] or not datos_factura["numero_factura"] or not datos_factura["fecha"]:
        messagebox.showerror("⚠️ Error", "Faltan datos de la factura (proveedor, número o fecha).")
        return

    # Validar que haya al menos un material ingresado
    if not materiales_temporales:
        messagebox.showerror("⚠️ Error", "No se han ingresado materiales.")
        return
    
    try:
        # 1. Guardar la factura en la base de datos
        insertar_factura(
            datos_factura["numero_factura"],
            datos_factura["fecha"],
            datos_factura["proveedor"]
        )

        # 2. Obtener el id_proveedor para guardar los materiales
        id_proveedor = obtener_id_proveedor_por_nombre(datos_factura["proveedor"])
        print("Este es el id del proveedor: ",id_proveedor)
        
        # 3. Obtener el id_factura recién ingresado
        id_factura = obtener_id_factura_por_numero(datos_factura["numero_factura"])
        print("Este es el id de la factura: ", id_factura)
        # 3. Guardar los materiales Base da datos
        for material in materiales_temporales:
            try:
                material["costo_unitario"] = round(material["costo_unitario"], 2)
            except:
                print(f"⚠️ Error: El valor {material['costo_unitario']} no es un número válido.")
                material["costo_unitario"]
                
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

            # Obtener el id_material recién ingresado
            id_material = obtener_id_material_por_codigo(material["codigo"])
            print(f" Este es el id del material: {id_material}")
            # Verificar que id_material no sea None
            if id_material is not None:
                # Insertar en Detalle_Factura
                print("Dentro del if para insertar_detalle_factura")
                insertar_detalle_factura(id_factura, id_material, material["stock"], material["precio"], material["costo_unitario"])
            else:
                messagebox.showinfo("No encontrado", f"No se encontró el material con código {material['codigo']}")
        
        # Mostrar mensaje de éxito
        messagebox.showinfo("Éxito", "Factura y materiales guardados correctamente.")
        
        # Limpiar las entradas.
        limpiar_campos(frame_contenido)
        
        # Limpiar la lista temporal
        materiales_temporales.clear()        

    except Exception as e:
        messagebox.showerror("⚠️ Error", f"No se pudo guardar: {e}")
        
        
# Esta función cambia la coma por el punto si el usuario usa coma.
def convertir_a_float(valor_str):
    try:
        valor_str = str(valor_str).replace(",", ".")
        return float(valor_str)
    except ValueError:
        print(f"⚠️ Error: '{valor_str}' no es un número válido.")
        return None
        
total_actual = []
def mostrar_datos_ingresados():
    global materiales_temporales
    
    if not materiales_temporales:
        messagebox.showwarning("Advertencia", "No hay materiales ingresados.")
        return

    ventana_datos = tk.Toplevel()
    configurar_toplevel(ventana_datos, titulo="Datos Ingresados", ancho_min=800, alto_min=500)
    
    frame_principal = ttk.Frame(ventana_datos, padding="10")
    frame_principal.pack(fill=tk.BOTH, expand=True)

    # Crear Treeview
    tree = ttk.Treeview(frame_principal, columns=("Código", "Nombre", "Tipo", "Tamaño", "Color", "Cantidad", "Precio", "Precio Unitario"), show="headings")

    # Configurar encabezados
    tree.heading("Código", text="Código")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Tipo", text="Tipo")
    tree.heading("Tamaño", text="Tamaño")
    tree.heading("Color", text="Color")
    tree.heading("Cantidad", text="Cantidad")
    tree.heading("Precio", text="Precio")
    tree.heading("Precio Unitario", text="Precio Unitario")

    # Configurar columnas
    tree.column("Código", width=80, anchor=tk.CENTER)
    tree.column("Nombre", width=100, anchor=tk.CENTER)
    tree.column("Tipo", width=80, anchor=tk.CENTER)
    tree.column("Tamaño", width=80, anchor=tk.CENTER)
    tree.column("Color", width=80, anchor=tk.CENTER)
    tree.column("Cantidad", width=80, anchor=tk.CENTER)
    tree.column("Precio", width=80, anchor=tk.CENTER)
    tree.column("Precio Unitario", width=100, anchor=tk.CENTER)

    tree.pack(fill=tk.BOTH, expand=True)

    # Función para cargar datos en el Treeview
    def cargar_datos():
        for item in tree.get_children():
            tree.delete(item)
        
        id_proveedor = obtener_id_proveedor_por_nombre(datos_factura["proveedor"])

        for material in materiales_temporales:
            precio = convertir_a_float(material["precio"])
            cantidad = convertir_a_float(material["stock"])
            precio_uni = precio / cantidad if precio is not None and cantidad is not None and cantidad != 0 else 0
            total_actual.append(precio) # Calcular el total para mostrar en pantalla.
            
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
        # Configura el Frame para mostrar el total actual
        frame_total.config(text=f"{sum(total_actual):.2f}", font=("Arial", 12, "bold"))
        
    # Función para editar una celda
    def editar_celda(event):
        region = tree.identify_region(event.x, event.y)
        if region == "cell":
            columna = tree.identify_column(event.x)
            fila = tree.identify_row(event.y)

            if fila and columna:
                columna_idx = int(columna[1:]) - 1  # Obtener índice de columna
                columna_nombre = tree["columns"][columna_idx]

                item = tree.selection()[0]
                valores = tree.item(item, "values")

                # Crear una entrada para editar el valor
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

    # Vincular el evento de doble clic para editar
    tree.bind("<Double-1>", editar_celda)

    # Función para guardar los cambios
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
                "costo_unitario": convertir_a_float(precio) / convertir_a_float(cantidad) if convertir_a_float(cantidad) != 0 else 0
            }
                
            # Actualizar materiales_temporales
            for i, mat in enumerate(materiales_temporales):
                if mat["codigo"] == codigo:
                    materiales_temporales[i] = material
                    print(i)
                    # Actualizar el precio en total_actual usando el mismo índice
                    if i < len(total_actual):
                        
                        print(total_actual[i])
                        total_actual[i] = convertir_a_float(precio)
                    break

        # Actualizar el label del total
        frame_total.config(text=f"{sum(total_actual):.2f}", font=("Arial", 12, "bold"))
        #messagebox.showinfo("Éxito", "Los cambios se han guardado correctamente.")

    def eliminar_dato():
        item = tree.selection()
        if not item:
            messagebox.showwarning("Advertencia", "Selecciona un ítem para eliminar.")
            return

        item_id = item[0]
        valores = tree.item(item_id, "values")
        codigo_a_eliminar = valores[0]

        # 1. Eliminar del Treeview
        tree.delete(item_id)

        # 2. Eliminar de materiales_temporales
        for i, material in enumerate(materiales_temporales):
            if material["codigo"] == codigo_a_eliminar:
                materiales_temporales.pop(i)
                break

        # 3. Eliminar del total_actual
        for i, material in enumerate(total_actual):
            # total_actual está alineado con materiales_temporales
            # pero como ya sacamos un índice arriba, aquí queda más fácil:
            total_actual.pop(i)
            break

        # 4. Actualizar total en pantalla
        frame_total.config(text=f"{sum(total_actual):.2f}")

    # Función para cerrar la ventana
    def cerrar_ventana():
        ventana_datos.destroy()
        total_actual.clear()
    
    # Vincular el evento de cierre de la ventana (con la "X")
    def on_closing():
        total_actual.clear()  # Limpiar la lista al cerrar con la "X"
        ventana_datos.destroy()

    ventana_datos.protocol("WM_DELETE_WINDOW", on_closing)  # Asociar el evento de cierre

    # Botones
    frame_botones = tk.Frame(ventana_datos)
    frame_botones.pack(fill=tk.X, padx=10, pady=10)
    
    frame_total = tk.Label(frame_botones)
    frame_total.pack(side=tk.RIGHT, padx=30)
    
    frame_label_total = tk.Label(frame_botones, text="Total Factura: ")
    frame_label_total.pack(side=tk.RIGHT, padx=7)

    boton_guardar = crear_boton(
        frame_botones,
        texto="Guardar Factura",
        ancho=30,
        alto=30,
        color_fondo="#4283fa",                
        color_texto="white",
        font=("Arial", 11, "bold"),
        #bd=0,
        #relief=tk.FLAT,
        hover_color="#2ECC71",
        #activeforeground="black",
        comando=guardar_cambios
    )

    boton_guardar.pack(side=tk.LEFT, padx=5)

    boton_eliminar = crear_boton(
        frame_botones,
        texto="Eliminar",
        ancho=30,
        alto=30,
        color_fondo="#4283fa",                
        color_texto="white",
        font=("Arial", 11, "bold"),
        #bd=0,
        #relief=tk.FLAT,
        hover_color="#2ECC71",
        #activeforeground="black",
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
        #bd=0,
        #relief=tk.FLAT,
        hover_color="#222423",
        #activeforeground="black",
        #bg=0,
        comando=cerrar_ventana 
    )
    boton_cerrar.pack(side=tk.LEFT, padx=5)

    cargar_datos()
