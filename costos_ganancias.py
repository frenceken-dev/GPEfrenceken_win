# costos_ganacias.py
import tkinter as tk
from tkinter import ttk, messagebox, Toplevel
from tkcalendar import Calendar 
from inventario import convertir_a_float
from db import (
    obtener_productos_para_acthistorial, 
    guardar_historial, 
    obtener_productos_para_costoventa, 
    mostrar_historial_costos_por_producto, 
    mostrar_historial_costos_general, 
    mostrar_historial_ganancias_producto,
    mostrar_historial_general_mensual, 
    datos_imprimir_historial_costo, 
    datos_imprimir_historial_ganancia,
    calcular_costo_produccion, 
    obtener_productos_para_costoventa, 
    actualizar_precio_venta, 
    datos_costo_d_producto_actualizar, 
    actualizar_costo_producto, 
    registrar_historial_costo,registrar_producto_en_lote, 
    obtener_lotes, 
    obtener_lotes_con_productos, 
    obtener_costo_actual_lote,
    insertar_lote,
    insertar_lote_productos,
    actualizar_costo_lote,
    costo_anterior_lote,
    actualiza_precio_venta_lote,
    )


# Actualizar los costos por unidad
def abrir_actualizar_costo_por_unidad(root, mostrar_menu_principal, imagen_panel_tk, rol, imagen_tk):
    # Limpiar pantalla
    for widget in root.winfo_children():
        widget.destroy()

    # Frame principal
    frame = tk.Frame(root, bg="#a0b9f0", width=800, height=600)
    frame.pack(fill=tk.BOTH, expand=True)

    # Panel izquierdo
    frame_menu = tk.Frame(frame, bg="#2C3E50", width=200, height=800)
    frame_menu.pack(side=tk.LEFT, fill=tk.Y)
    frame_menu.pack_propagate(False)

    # Frame para imagen del panel izquierdo
    frame_imagen_panel = tk.Frame(frame_menu, bg="#2C3E50", height=70)
    frame_imagen_panel.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

    # Imagen del Logo para el panel izquierdo
    if imagen_panel_tk:
        label_imagen = tk.Label(frame_imagen_panel, image=imagen_panel_tk, bg="#2C3E50")
        label_imagen.pack(side=tk.LEFT, padx=70)
    else:
        label_texto = tk.Label(frame_imagen_panel, text="Ikigai", font=("Arial", 10), bg="#2C3E50")
        label_texto.pack(side=tk.LEFT, padx=30)

    # Frame para los controles (centrado)
    control_frame = tk.Frame(frame, bg="#a0b9f0", padx=20, pady=10)
    control_frame.pack(fill=tk.BOTH, expand=True)

    frame_titulo = tk.Frame(control_frame, bg="#a0b9f0")
    frame_titulo.pack(side=tk.TOP, fill=tk.X, pady=15)

    # Frame central para centrar el contenido
    center_frame = tk.Frame(control_frame, bg="#a0b9f0")
    center_frame.pack(expand=True)

    # Título
    title_label = tk.Label(
        frame_titulo,
        text="Actualizar Costo por Unidad",
        font=("Arial", 16, "bold"),
        bg="#a0b9f0",
        fg="#2C3E50",
        anchor=tk.CENTER
    )
    title_label.pack(expand=True)

    # Dropdown para seleccionar producto
    product_label = tk.Label(
        center_frame,
        text="Selecciona el producto:",
        bg="#a0b9f0",
        fg="#2C3E50",
        font=("Arial", 11)
    )
    product_label.pack(anchor=tk.W, pady=(0, 5))

    productos = obtener_productos_para_costoventa()
    
    # Verificar si la lista de productos está vacía
    if not productos:
        tk.Label(center_frame, text="Actualmente no hay productos registrados.", font=("Arial", 12)).pack(pady=20)
        messagebox.showwarning("Advertencia", "No hay datos que mostrar en este momento")
        tk.Button(center_frame, text="Volver al Menú", command=abrir_modulo_costos_ganancias(root, mostrar_menu_principal, imagen_panel_tk, rol, imagen_tk), font=("Arial", 10)).pack(pady=10)
        return
    
    producto_vars = [f"{prod[1]} (Costo actual: €{prod[2]:.2f})" for prod in productos]
    producto_var = tk.StringVar()
    producto_var.set("Seleccione un producto")
    producto_dropdown = tk.OptionMenu(center_frame, producto_var, *producto_vars)
    producto_dropdown.config(
        bg="#FFFFFF",
        fg="#2C3E50",
        font=("Arial", 10),
        bd=2,
        relief=tk.GROOVE,
        width=40
    )
    producto_dropdown.pack(anchor=tk.W, pady=(0, 15))

    # Label y Entry para el nuevo costo
    nuevo_costo_label = tk.Label(
        center_frame,
        text="Nuevo costo de producción:",
        bg="#a0b9f0",
        fg="#2C3E50",
        font=("Arial", 11)
    )
    nuevo_costo_label.pack(anchor=tk.W, pady=(0, 5))
    nuevo_costo_entry = tk.Entry(center_frame, bd=2, relief=tk.GROOVE, font=("Arial", 10))
    nuevo_costo_entry.pack(anchor=tk.W, pady=(0, 15))

    # Checkbutton para recalcular precio de venta
    recalcular_precio_var = tk.IntVar()
    recalcular_precio_check = tk.Checkbutton(
        center_frame,
        text="Recalcular precio de venta",
        variable=recalcular_precio_var,
        bg="#a0b9f0",
        fg="#2C3E50",
        font=("Arial", 11),
        selectcolor="#a0b9f0",
        command=lambda: toggle_recalculo_frame(recalcular_precio_var.get())
    )
    recalcular_precio_check.pack(anchor=tk.W, pady=(0, 15))

    # Frame para método y parámetro (oculto inicialmente)
    recalculo_frame = tk.Frame(center_frame, bg="#a0b9f0")

    # Dropdown para seleccionar método de recálculo
    metodo_label = tk.Label(
        recalculo_frame,
        text="Selecciona el método:",
        bg="#a0b9f0",
        fg="#2C3E50",
        font=("Arial", 11)
    )
    metodo_label.pack(anchor=tk.W, pady=(0, 5))

    metodo_var = tk.StringVar()
    metodo_dropdown = tk.OptionMenu(recalculo_frame, metodo_var, "factor", "margen", "formula")
    metodo_dropdown.config(
        bg="#FFFFFF",
        fg="#2C3E50",
        font=("Arial", 10),
        bd=2,
        relief=tk.GROOVE,
        width=20
    )
    metodo_dropdown.pack(anchor=tk.W, pady=(0, 10))

    # Label y Entry para el parámetro
    parametro_label = tk.Label(
        recalculo_frame,
        text="Parámetro:",
        bg="#a0b9f0",
        fg="#2C3E50",
        font=("Arial", 11)
    )
    parametro_label.pack(anchor=tk.W, pady=(0, 5))

    parametro_entry = tk.Entry(recalculo_frame, bd=2, relief=tk.GROOVE, font=("Arial", 10))
    parametro_entry.pack(anchor=tk.W, pady=(0, 10))

    # Label dinámico para el parámetro
    tipo_parametro_label = tk.Label(
        recalculo_frame,
        text="",
        bg="#a0b9f0",
        fg="#3498DB",
        font=("Arial", 10, "italic")
    )
    tipo_parametro_label.pack(anchor=tk.W, pady=(0, 10))

    def toggle_recalculo_frame(visible):
        if visible:
            recalculo_frame.pack(anchor=tk.W, pady=(0, 15))
            actualizar_tipo_parametro()
        else:
            recalculo_frame.pack_forget()

    def actualizar_tipo_parametro():
        metodo = metodo_var.get()
        if metodo == "factor":
            tipo_parametro_label.config(text="Ejemplo: 2, 3, 4, 5")
        elif metodo == "margen":
            tipo_parametro_label.config(text="Ejemplo: 50, 100, 150")
        elif metodo == "formula":
            tipo_parametro_label.config(text="Ejemplo: 2, 3, 4, 5")

    metodo_var.trace_add("write", lambda *args: actualizar_tipo_parametro())

    # Función para limpiar campos
    def limpiar_campos():
        producto_var.set("")
        nuevo_costo_entry.delete(0, tk.END)
        recalcular_precio_var.set(0)
        metodo_var.set("factor")
        parametro_entry.delete(0, tk.END)
        tipo_parametro_label.config(text="")

    # Botón para actualizar costo
    update_button = tk.Button(
        center_frame,
        text="Actualizar Costo",
        bg="#3498DB",
        fg="white",
        font=("Arial", 11, "bold"),
        bd=0,
        relief=tk.FLAT,
        activebackground="#2980B9",
        activeforeground="white",
        command=lambda: actualizar_costo_produccion(
            producto_var.get(),
            nuevo_costo_entry.get(),
            recalcular_precio_var.get(),
            metodo_var.get() if recalcular_precio_var.get() else None,
            parametro_entry.get() if recalcular_precio_var.get() else None,
            "unidad",
            None,
            None,
            None
        )
    )
    update_button.pack(pady=20)

    # Botón para volver
    back_button = tk.Button(
        frame_menu,
        text="Volver",
        bg="#E74C3C",
        fg="white",
        font=("Arial", 11, "bold"),
        bd=0,
        relief=tk.FLAT,
        activebackground="#C0392B",
        activeforeground="white",
        command=lambda: abrir_modulo_costos_ganancias(root, mostrar_menu_principal, imagen_panel_tk, rol, imagen_tk),
        width=10
    )
    back_button.pack(side="bottom", padx=30, pady=60)

    # Botón para limpiar pantalla
    clear_button = tk.Button(
        frame_menu,
        text="Limpiar Pantalla",
        bg="#27E0C8",
        fg="white",
        font=("Arial", 11, "bold"),
        bd=0,
        relief=tk.FLAT,
        activebackground="#C0392B",
        activeforeground="white",
        command=lambda: limpiar_campos(),
        width=15
    )
    clear_button.pack(side="bottom", padx=30, pady=60)

# Crear lotes y actualizar los costos por lote
def abrir_actualizar_costo_por_lote(root, mostrar_menu_principal, imagen_panel_tk, rol, imagen_tk):
    # Limpiar pantalla
    for widget in root.winfo_children():
        widget.destroy()

    # Frame principal
    frame = tk.Frame(root, bg="#a0b9f0", width=800, height=600)
    frame.pack(fill=tk.BOTH, expand=True)

    # Panel izquierdo
    frame_menu = tk.Frame(frame, bg="#2C3E50", width=200, height=800)
    frame_menu.pack(side=tk.LEFT, fill=tk.Y)
    frame_menu.pack_propagate(False)

    # Frame para imagen del panel izquierdo
    frame_imagen_panel = tk.Frame(frame_menu, bg="#2C3E50", height=70)
    frame_imagen_panel.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

    # Imagen del Logo para el panel izquierdo
    if imagen_panel_tk:
        label_imagen = tk.Label(frame_imagen_panel, image=imagen_panel_tk, bg="#2C3E50")
        label_imagen.pack(side=tk.LEFT, padx=70)
    else:
        label_texto = tk.Label(frame_imagen_panel, text="Ikigai", font=("Arial", 10), bg="#2C3E50")
        label_texto.pack(side=tk.LEFT, padx=30)

    # Frame para los controles (centrado)
    control_frame = tk.Frame(frame, bg="#a0b9f0", padx=20, pady=10)
    control_frame.pack(fill=tk.BOTH, expand=True)

    frame_titulo = tk.Frame(control_frame, bg="#a0b9f0")
    frame_titulo.pack(side=tk.TOP, fill=tk.X, pady=15)

    # Frame central para centrar el contenido
    center_frame = tk.Frame(control_frame, bg="#a0b9f0")
    center_frame.pack(expand=True)

    # Título
    title_label = tk.Label(
        frame_titulo,
        text="Actualizar Costo por Lote",
        font=("Arial", 16, "bold"),
        bg="#a0b9f0",
        fg="#2C3E50",
        anchor=tk.CENTER
    )
    title_label.pack(expand=True)

    # Botón para crear un nuevo lote
    crear_lote_button = tk.Button(
        center_frame,
        text="Crear Nuevo Lote",
        bg="#27AE60",
        fg="white",
        font=("Arial", 11, "bold"),
        bd=0,
        relief=tk.FLAT,
        activebackground="#2ECC71",
        activeforeground="white",
        command=lambda: abrir_formulario_crear_lote(center_frame)
    )
    crear_lote_button.pack(pady=(0, 15))

    # Dropdown para seleccionar lote
    lote_label = tk.Label(
        center_frame,
        text="Selecciona el lote:",
        bg="#a0b9f0",
        fg="#2C3E50",
        font=("Arial", 11)
    )
    lote_label.pack(anchor=tk.W, pady=(0, 5))

    lotes = obtener_lotes()
    lote_vars = [f"{lote[0]} - {lote[2]}" for lote in lotes]

    if not lote_vars:
        lote_vars = ["No hay lotes disponibles"]

    lote_var = tk.StringVar()
    lote_dropdown = tk.OptionMenu(center_frame, lote_var, *lote_vars, command=lambda lote: mostrar_costo_actual_lote(lote))
    lote_dropdown.config(
        bg="#FFFFFF",
        fg="#2C3E50",
        font=("Arial", 10),
        bd=2,
        relief=tk.GROOVE,
        width=40
    )
    lote_dropdown.pack(anchor=tk.W, pady=(0, 15))
    
    # Etiqueta para mostrar el costo actual del lote
    costo_actual_lote_label = tk.Label(
        center_frame,
        text="Costo actual del lote: ",
        bg="#a0b9f0",
        fg="#2C3E50",
        font=("Arial", 11)
    )
    costo_actual_lote_label.pack(anchor=tk.W, pady=(0, 15))

    def mostrar_costo_actual_lote(lote_str):
        if lote_str and lote_str != "No hay lotes disponibles":
            id_lote = int(lote_str.split(" - ")[0])
            costo_actual = obtener_costo_actual_lote(id_lote)
            costo_actual_lote_label.config(text=f"Costo actual del lote: €{costo_actual:.2f}")
        else:
            costo_actual_lote_label.config(text="Costo actual del lote: ")

    # Campo para ingresar el nuevo costo de producción por lote
    nuevo_costo_lote_label = tk.Label(
        center_frame,
        text="Nuevo costo de producción por lote:",
        bg="#a0b9f0",
        fg="#2C3E50",
        font=("Arial", 11)
    )
    nuevo_costo_lote_label.pack(anchor=tk.W, pady=(0, 5))

    nuevo_costo_lote_entry = tk.Entry(center_frame, bd=2, relief=tk.GROOVE, font=("Arial", 10))
    nuevo_costo_lote_entry.pack(anchor=tk.W, pady=(0, 15))

    # Checkbutton para recalcular precio de venta
    recalcular_precio_var = tk.IntVar()
    recalcular_precio_check = tk.Checkbutton(
        center_frame,
        text="Recalcular precio de venta",
        variable=recalcular_precio_var,
        bg="#a0b9f0",
        fg="#2C3E50",
        font=("Arial", 11),
        selectcolor="#a0b9f0",
        command=lambda: toggle_recalculo_frame(recalcular_precio_var.get())
    )
    recalcular_precio_check.pack(anchor=tk.W, pady=(0, 15))

    # Frame para método y parámetro (oculto inicialmente)
    recalculo_frame = tk.Frame(center_frame, bg="#a0b9f0")

    # Dropdown para seleccionar método de recálculo
    metodo_label = tk.Label(
        recalculo_frame,
        text="Selecciona el método:",
        bg="#a0b9f0",
        fg="#2C3E50",
        font=("Arial", 11)
    )
    metodo_label.pack(anchor=tk.W, pady=(0, 5))

    metodo_var = tk.StringVar()
    metodo_dropdown = tk.OptionMenu(recalculo_frame, metodo_var, "factor", "margen", "formula")
    metodo_dropdown.config(
        bg="#FFFFFF",
        fg="#2C3E50",
        font=("Arial", 10),
        bd=2,
        relief=tk.GROOVE,
        width=20
    )
    metodo_dropdown.pack(anchor=tk.W, pady=(0, 10))

    # Label y Entry para el parámetro
    parametro_label = tk.Label(
        recalculo_frame,
        text="Parámetro:",
        bg="#a0b9f0",
        fg="#2C3E50",
        font=("Arial", 11)
    )
    parametro_label.pack(anchor=tk.W, pady=(0, 5))

    parametro_entry = tk.Entry(recalculo_frame, bd=2, relief=tk.GROOVE, font=("Arial", 10))
    parametro_entry.pack(anchor=tk.W, pady=(0, 10))

    # Label dinámico para el parámetro
    tipo_parametro_label = tk.Label(
        recalculo_frame,
        text="",
        bg="#a0b9f0",
        fg="#3498DB",
        font=("Arial", 10, "italic")
    )
    tipo_parametro_label.pack(anchor=tk.W, pady=(0, 10))

    def toggle_recalculo_frame(visible):
        if visible:
            recalculo_frame.pack(anchor=tk.W, pady=(0, 15))
            actualizar_tipo_parametro()
        else:
            recalculo_frame.pack_forget()

    def actualizar_tipo_parametro():
        metodo = metodo_var.get()
        if metodo == "factor":
            tipo_parametro_label.config(text="Ejemplo: 2, 3, 4, 5")
        elif metodo == "margen":
            tipo_parametro_label.config(text="Ejemplo: 50, 100, 150")
        elif metodo == "formula":
            tipo_parametro_label.config(text="Ejemplo: 2, 3, 4, 5")

    metodo_var.trace_add("write", lambda *args: actualizar_tipo_parametro())

    # Función para limpiar campos
    def limpiar_campos():
        lote_var.set("")
        nuevo_costo_lote_entry.delete(0, tk.END)
        recalcular_precio_var.set(0)
        metodo_var.set("factor")
        parametro_entry.delete(0, tk.END)
        tipo_parametro_label.config(text="")

    # Botón para actualizar costo
    update_button = tk.Button(
        center_frame,
        text="Actualizar Costo",
        bg="#3498DB",
        fg="white",
        font=("Arial", 11, "bold"),
        bd=0,
        relief=tk.FLAT,
        activebackground="#2980B9",
        activeforeground="white",
        command=lambda: actualizar_costo_de_lote(
            nuevo_costo_lote_entry.get(),
            recalcular_precio_var.get(),
            metodo_var.get() if recalcular_precio_var.get() else None,
            parametro_entry.get() if recalcular_precio_var.get() else None,
            "lote",
            lote_var.get(),
        )
    )
    update_button.pack(pady=20)
    
    # Botón para volver
    back_button = tk.Button(
        frame_menu,
        text="Volver",
        bg="#E74C3C",
        fg="white",
        font=("Arial", 11, "bold"),
        bd=0,
        relief=tk.FLAT,
        activebackground="#C0392B",
        activeforeground="white",
        command=lambda: abrir_modulo_costos_ganancias(root, mostrar_menu_principal, imagen_panel_tk, rol, imagen_tk),
        width=10
    )
    back_button.pack(side="bottom", padx=30, pady=60)

     # Botón para limpiar pantalla
    clear_button = tk.Button(
        frame_menu,
        text="Limpiar Pantalla",
        bg="#27E0C8",
        fg="white",
        font=("Arial", 11, "bold"),
        bd=0,
        relief=tk.FLAT,
        activebackground="#C0392B",
        activeforeground="white",
        command=lambda: limpiar_campos(),
        width=15
    )
    clear_button.pack(side="bottom", padx=30, pady=20)
    

def abrir_formulario_crear_lote(parent_frame):
    # Crear una ventana emergente para el formulario de creación de lotes
    lote_window = tk.Toplevel(parent_frame)
    lote_window.title("Crear Nuevo Lote")
    lote_window.geometry("500x450")
    lote_window.transient(parent_frame)
    lote_window.grab_set()

    # Frame para el formulario
    form_frame = tk.Frame(lote_window, bg="#a0b9f0", padx=20, pady=20)
    form_frame.pack(fill=tk.BOTH, expand=True)

    # Campo para la descripción del lote
    descripcion_label = tk.Label(
        form_frame,
        text="Descripción del lote:",
        bg="#a0b9f0",
        fg="#2C3E50",
        font=("Arial", 11)
    )
    descripcion_label.pack(anchor=tk.W, pady=(0, 5))

    descripcion_entry = tk.Entry(form_frame, bd=2, relief=tk.GROOVE, font=("Arial", 10))
    descripcion_entry.pack(anchor=tk.W, fill=tk.X, pady=(0, 15))

    # Campo para la cantidad de unidades del lote
    unidades_label = tk.Label(
        form_frame,
        text="Cantidad de unidades en el lote:",
        bg="#a0b9f0",
        fg="#2C3E50",
        font=("Arial", 11)
    )
    unidades_label.pack(anchor=tk.W, pady=(0, 5))

    unidades_entry = tk.Entry(form_frame, bd=2, relief=tk.GROOVE, font=("Arial", 10))
    unidades_entry.pack(anchor=tk.W, fill=tk.X, pady=(0, 15))

    # Campo para el costo del lote
    costo_lote_label = tk.Label(
        form_frame,
        text="Costo del lote:",
        bg="#a0b9f0",
        fg="#2C3E50",
        font=("Arial", 11)
    )
    costo_lote_label.pack(anchor=tk.W, pady=(0, 5))

    costo_lote_entry = tk.Entry(form_frame, bd=2, relief=tk.GROOVE, font=("Arial", 10))
    costo_lote_entry.pack(anchor=tk.W, fill=tk.X, pady=(0, 15))

    # Label para seleccionar productos
    productos_label = tk.Label(
        form_frame,
        text="Selecciona los productos para este lote:",
        bg="#a0b9f0",
        fg="#2C3E50",
        font=("Arial", 11)
    )
    productos_label.pack(anchor=tk.W, pady=(0, 5))

    # Frame para el Listbox y Scrollbar
    listbox_frame = tk.Frame(form_frame, bg="#a0b9f0")
    listbox_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

    # Listbox para seleccionar productos
    productos_listbox = tk.Listbox(listbox_frame, selectmode=tk.MULTIPLE, height=6, bd=2, relief=tk.GROOVE, font=("Arial", 10))
    productos_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Scrollbar para el Listbox
    scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL)
    scrollbar.config(command=productos_listbox.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    productos_listbox.config(yscrollcommand=scrollbar.set)

    # Obtener y cargar los productos en el Listbox
    productos = obtener_productos_para_costoventa()
    for producto in productos:
        productos_listbox.insert(tk.END, f"{producto[1]} (Costo: €{producto[2]:.2f})")

    # Frame para los campos de cantidad por producto
    cantidades_frame = tk.Frame(form_frame, bg="#a0b9f0")
    cantidades_frame.pack(fill=tk.X, pady=(0, 15))

    # Label y Entry para la cantidad de cada producto seleccionado
    cantidad_label = tk.Label(
        cantidades_frame,
        text="Cantidad por producto:",
        bg="#a0b9f0",
        fg="#2C3E50",
        font=("Arial", 11)
    )
    cantidad_label.pack(side=tk.LEFT, padx=(0, 10))

    cantidad_entry = tk.Entry(cantidades_frame, bd=2, relief=tk.GROOVE, font=("Arial", 10), width=5)
    cantidad_entry.pack(side=tk.LEFT)

    # Botón para guardar el lote
    guardar_button = tk.Button(
        form_frame,
        text="Guardar Lote",
        bg="#27AE60",
        fg="white",
        font=("Arial", 11, "bold"),
        bd=0,
        relief=tk.FLAT,
        activebackground="#2ECC71",
        activeforeground="white",
        command=lambda: guardar_nuevo_lote(
            descripcion_entry.get(),
            unidades_entry.get(),
            [productos_listbox.get(i) for i in productos_listbox.curselection()],
            cantidad_entry.get(),
            costo_lote_entry.get(),
            lote_window
        )
    )
    guardar_button.pack(pady=20)
    
# Guarda el Nuevo lote Creado       
def guardar_nuevo_lote(descripcion, unidades_str, productos_seleccionados, cantidad_str, costo_lote_str, window):
    from datetime import datetime
    import sqlite3
    
    try:
        unidades = int(unidades_str)
        cantidad = int(cantidad_str)
        costo_lote = float(costo_lote_str)

        if unidades <= 0 or cantidad <= 0:
            messagebox.showerror("Error", "La cantidad de unidades y la cantidad por producto deben ser mayores que cero.")
            return

        if not productos_seleccionados:
            messagebox.showerror("Error", "Debes seleccionar al menos un producto.")
            return

        # Insertar el lote en la tabla Lotes
        id_lote = insertar_lote(descripcion, unidades, costo_lote)

        # Insertar los productos en la tabla Lote_Productos
        for producto_str in productos_seleccionados:
            codigo_producto = producto_str.split(" ")[0]
            producto = next((prod for prod in obtener_productos_para_costoventa() if prod[1] == codigo_producto), None)
            if producto:
                id_producto = producto[0]
                # insertar productos en la tabla lote_productos
                insertar_lote_productos(id_lote, id_producto, cantidad)
                
        messagebox.showinfo("Éxito", "El lote se ha creado correctamente.")
        window.destroy()
    except ValueError:
        messagebox.showerror("Error", "Las cantidades y el costo deben ser números válidos.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al guardar el lote: {e}")


# Guarda la actulización del precio de Costo        
def actualizar_costo_de_lote(nuevo_costo_str, recalcular_precio, metodo, parametro_str, tipo_costo, lote_str):
    import sqlite3
    
    try:
        # Validar que el nuevo costo sea un número
        if not nuevo_costo_str:
            messagebox.showerror("Error", "Debes ingresar un nuevo costo.")
            return
        nuevo_costo = convertir_a_float(nuevo_costo_str)

        if tipo_costo == "lote":
            # Validar que se haya seleccionado un lote
            if not lote_str or lote_str == "No hay lotes disponibles":
                messagebox.showerror("Error", "Debes seleccionar un lote.")
                return

            id_lote = int(lote_str.split(" - ")[0])

            # Actualizar el costo del lote en la base de datos
            actualizar_costo_lote(nuevo_costo, id_lote)

            # Obtener el costo anterior del lote
            costo_anterior = costo_anterior_lote(id_lote,)

            # Recalcular el precio de venta si el usuario lo desea
            if recalcular_precio:
                if not metodo or not parametro_str:
                    messagebox.showerror("Error", "Debes seleccionar un método e ingresar un parámetro.")
                    return
                try:
                    parametro = float(parametro_str)
                except ValueError:
                    messagebox.showerror("Error", "El parámetro debe ser un número válido.")
                    return

                # Calcular el nuevo precio según el método
                if metodo == "factor":
                    nuevo_precio = nuevo_costo * parametro
                elif metodo == "margen":
                    nuevo_precio = nuevo_costo * (1 + parametro / 100)
                elif metodo == "formula":
                    nuevo_precio = nuevo_costo + (nuevo_costo * 1) * parametro

                # Actualizar el precio de venta del lote en la base de datos
                actualiza_precio_venta_lote(nuevo_precio, id_lote)

                messagebox.showinfo(
                    "Éxito",
                    f"Costo y precio de venta del lote actualizados:\n"
                    f"Costo anterior: €{costo_anterior:.2f}\n"
                    f"Nuevo costo: €{nuevo_costo:.2f}\n"
                    f"Nuevo precio de venta: €{nuevo_precio:.2f}"
                )
            else:
                messagebox.showinfo(
                    "Éxito",
                    f"Costo del lote actualizado:\n"
                    f"Costo anterior: €{costo_anterior:.2f}\n"
                    f"Nuevo costo: €{nuevo_costo:.2f}"
                )

    except ValueError:
        messagebox.showerror("Error", "El nuevo costo debe ser un número válido.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")


def actualizar_costo_produccion(producto_str, nuevo_costo_str, recalcular_precio, metodo, parametro_str, tipo_costo, unidades_str, lote_str, unidades_lote_str):
    try:
        # Validar que se haya seleccionado un producto
        if not producto_str:
            messagebox.showerror("Error", "Debes seleccionar un producto.")
            return

        # Extraer el código del producto
        codigo_producto = producto_str.split(" ")[0]

        # Validar que el nuevo costo sea un número
        if not nuevo_costo_str:
            messagebox.showerror("Error", "Debes ingresar un nuevo costo.")
            return

        nuevo_costo = convertir_a_float(nuevo_costo_str)

        # Obtener el id_producto y el costo actual
        producto = datos_costo_d_producto_actualizar(codigo_producto)
        if producto is None:
            return

        id_producto, costo_actual, precio_venta_actual = producto

        # Validar unidades si es por lote
        unidades = None
        if tipo_costo == "lote":
            if not unidades_str:
                messagebox.showerror("Error", "Debes ingresar el número de unidades en el lote.")
                return
            try:
                unidades = int(unidades_str)
            except ValueError:
                messagebox.showerror("Error", "El número de unidades debe ser un entero válido.")
                return

        # Validar y registrar el lote
        if lote_str:
            id_lote = int(lote_str.split(" - ")[0])
            if not unidades_lote_str:
                messagebox.showerror("Error", "Debes ingresar el número de unidades del producto en el lote.")
                return
            try:
                unidades_lote = int(unidades_lote_str)
                registrar_producto_en_lote(id_lote, id_producto, unidades_lote)
            except ValueError:
                messagebox.showerror("Error", "El número de unidades del producto en el lote debe ser un entero válido.")
                return

        # Actualizar el costo en la base de datos
        actualizar_costo_producto(nuevo_costo, id_producto)

        # Registrar el cambio en el historial
        registrar_historial_costo(
            id_producto=id_producto,
            costo_anterior=costo_actual,
            costo_nuevo=nuevo_costo,
            es_por_lote=(tipo_costo == "lote"),
            unidades=unidades,
            motivo=f"Actualización manual. Método de recálculo: {metodo}" if recalcular_precio else "Actualización manual"
        )

        # Recalcular el precio de venta si el usuario lo desea
        if recalcular_precio:
            if not metodo or not parametro_str:
                messagebox.showerror("Error", "Debes seleccionar un método e ingresar un parámetro.")
                return
            try:
                parametro = float(parametro_str)
            except ValueError:
                messagebox.showerror("Error", "El parámetro debe ser un número válido.")
                return

            # Calcular el nuevo precio según el método
            if metodo == "factor":
                nuevo_precio = nuevo_costo * parametro
            elif metodo == "margen":
                nuevo_precio = nuevo_costo * (1 + parametro / 100)
            elif metodo == "formula":
                nuevo_precio = nuevo_costo + (nuevo_costo * 1) * parametro

            # Actualizar el precio de venta
            actualizar_precio_venta(nuevo_precio, id_producto)

            messagebox.showinfo(
                "Éxito",
                f"Costo y precio actualizados:\n"
                f"Producto: {codigo_producto}\n"
                f"Costo anterior: €{costo_actual:.2f}\n"
                f"Nuevo costo: €{nuevo_costo:.2f}\n"
                f"Nuevo precio: €{nuevo_precio:.2f}"
            )
        else:
            messagebox.showinfo(
                "Éxito",
                f"Costo de producción actualizado:\n"
                f"Producto: {codigo_producto}\n"
                f"Costo anterior: €{costo_actual:.2f}\n"
                f"Nuevo costo: €{nuevo_costo:.2f}"
            )
    except ValueError:
        messagebox.showerror("Error", "El nuevo costo debe ser un número válido.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")
    


# Variables globales para los botones de impresión
boton_imprimir_costos = None
boton_imprimir_ganancias = None

# Función para actualizar historial de ganancias
def abrir_actualizar_historial(root, mostrar_menu_principal, imagen_panel_tk, rol, imagen_tk):
     # Limpiar pantalla
    for widget in root.winfo_children():
        widget.destroy()

    # Frame principal
    frame = tk.Frame(root, bg="#a0b9f0", width=800, height=600)
    frame.pack(fill=tk.BOTH, expand=True)

    # panel izquierdo
    frame_menu = tk.Frame(frame, bg="#2C3E50", width=200, height=800)
    frame_menu.pack(side=tk.LEFT, fill=tk.Y)
    frame_menu.pack_propagate(False)
    
    # Frame para imagen del panel izquierdo
    frame_imagen_panel = tk.Frame(frame_menu, bg="#2C3E50", height=70)
    frame_imagen_panel.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
    
    # Imagen del Logo para el panel izquierdo
    if imagen_panel_tk:
        label_imagen = tk.Label(frame_imagen_panel, image=imagen_panel_tk, bg="#2C3E50")
        label_imagen.pack(side=tk.LEFT, padx=70)
    else:
        label_texto = tk.Label(frame_imagen_panel, text="Ikigai", font=("Arial", 10), bg="#2C3E50")
        label_texto.pack(side=tk.LEFT, padx=30)
        
    # Frame para los controles
    control_frame = tk.Frame(frame, bg="#a0b9f0", padx=20, pady=10)
    control_frame.pack(fill=tk.BOTH, expand=True)
        
    # Frame para el titulo. 
    frame_titulo = tk.Frame(control_frame, bg="#a0b9f0")
    frame_titulo.pack(side=tk.TOP, fill=tk.X, pady=15)

    # Frame central para centrar el contenido
    center_frame = tk.Frame(control_frame, bg="#a0b9f0")
    center_frame.pack(expand=True)
    
    # Título
    title_label = tk.Label(
        frame_titulo,
        text="Actualizar Historial de Ganancias",
        font=("Arial", 16, "bold"),
        bg="#a0b9f0",
        fg="#2C3E50"
    )
    title_label.pack(pady=15)

    # Label para seleccionar fecha
    fecha_label = tk.Label(
        center_frame,
        text="Selecciona el mes y año:",
        bg="#a0b9f0",
        fg="#2C3E50",
        font=("Arial", 11)
    )
    fecha_label.pack(anchor=tk.W, pady=(0, 10))

    # Frame para el calendario
    cal_frame = tk.Frame(center_frame, bg="#a0b9f0")
    cal_frame.pack(anchor=tk.W, pady=(0, 15))

    # Calendario (para seleccionar día, mes y año)
    cal = Calendar(
        cal_frame,
        selectmode="day",
        year=2025,
        month=10,
        date_pattern="dd/MM/yyyy",
        background="#E0F2F7",
        foreground="#2C3E50",
        headersbackground="#3498DB",
        headersforeground="white",
        selectbackground="#3498DB",
        selectforeground="white",
        normalbackground="#E0F2F7",
        normalforeground="#2C3E50",
        weekendbackground="#E0F2F7",
        weekendforeground="#E74C3C",
        font=("Arial", 10)
    )
    cal.pack()

    # Botón para calcular ganancias
    calculate_button = tk.Button(
        center_frame,
        text="Calcular Ganancias",
        bg="#3498DB",
        fg="white",
        font=("Arial", 11, "bold"),
        bd=0,
        relief=tk.FLAT,
        activebackground="#2980B9",
        activeforeground="white",
        command=lambda:calcular_y_guardar_ganancias(cal.get_date()),
        width=20
    )
    calculate_button.pack(anchor=tk.W, pady=(0, 20))

    # Botón para volver
    back_button = tk.Button(
        frame_menu,
        text="Volver",
        bg="#E74C3C",
        fg="white",
        font=("Arial", 11, "bold"),
        bd=0,
        relief=tk.FLAT,
        activebackground="#C0392B",
        activeforeground="white",
        command=lambda:abrir_modulo_costos_ganancias(root, mostrar_menu_principal, imagen_panel_tk, rol, imagen_tk),
        width=10
    )
    back_button.pack(side="bottom", padx=30, pady=60)

    # Área para mostrar resultados
    resultado_frame = tk.Frame(center_frame, bg="#a0b9f0", padx=20, pady=10)
    resultado_frame.pack(fill=tk.X)

    resultado_text = tk.Text(
        resultado_frame,
        height=10,
        width=60,
        state="disabled",
        bg="#d8dfee",
        fg="#2C3E50",
        font=("Arial", 10),
        bd=2,
        relief=tk.GROOVE,
        padx=10,
        pady=10
    )
    resultado_text.pack()

    def calcular_y_guardar_ganancias(fecha_str):
        try:
            # Convertir la fecha (dd/mm/yyyy) a formato YYYY-MM
            dia, mes, año = fecha_str.split("/")
            mes_año = f"{año}-{mes}"

            # Obtener todos los productos
            productos = obtener_productos_para_acthistorial()

            # Calcular ganancias para cada producto
            ganancias = []
            for producto in productos:
                id_producto, codigo, costo_produccion, precio_venta = producto
                ganancia = precio_venta - costo_produccion
                margen = (ganancia / costo_produccion) * 100 if costo_produccion != 0 else 0

                # Guardar en Historial_Ganancias
                guardar_historial(id_producto, mes_año, ganancia, margen)
                ganancias.append((codigo, ganancia, margen))

            # Mostrar resultados en el Text
            resultado_text.config(state="normal")
            resultado_text.delete(1.0, tk.END)
            resultado_text.insert(tk.END, f"Ganancias para el mes {mes_año}:\n\n")
            resultado_text.insert(tk.END, "Producto\t\tGanancia\tMargen (%)\n")
            resultado_text.insert(tk.END, "-" * 40 + "\n")

            for codigo, ganancia, margen in ganancias:
                resultado_text.insert(tk.END, f"{codigo}\t\t€{ganancia:.2f}\t\t{margen:.1f}%\n")

            resultado_text.config(state="disabled")
            messagebox.showinfo("Éxito", f"Historial de ganancias actualizado para el mes {mes_año}.")

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")
            

# Muestra el historial de costos por productos o todo
def mostrar_historial_costos(root, mostrar_menu_principal, imagen_panel_tk, rol, imagen_tk):
    # Limpiar pantalla
    for widget in root.winfo_children():
        widget.destroy()

    # Frame principal
    frame = tk.Frame(root, bg="#a0b9f0", width=800, height=600)
    frame.pack(fill=tk.BOTH, expand=True)
    
    # panel izquierdo
    frame_menu = tk.Frame(frame, bg="#2C3E50", width=200, height=800)
    frame_menu.pack(side=tk.LEFT, fill=tk.Y)
    frame_menu.pack_propagate(False)
    
    # Frame para imagen del panel izquierdo
    frame_imagen_panel = tk.Frame(frame_menu, bg="#2C3E50", height=70)
    frame_imagen_panel.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
    
    # Imagen del Logo para el panel izquierdo
    if imagen_panel_tk:
        label_imagen = tk.Label(frame_imagen_panel, image=imagen_panel_tk, bg="#2C3E50")
        label_imagen.pack(side=tk.LEFT, padx=70)
    else:
        label_texto = tk.Label(frame_imagen_panel, text="Ikigai", font=("Arial", 10), bg="#2C3E50")
        label_texto.pack(side=tk.LEFT, padx=30)
        
    # Frame para los controles
    control_frame = tk.Frame(frame, bg="#a0b9f0", padx=20, pady=10)
    control_frame.pack(fill=tk.BOTH, expand=True)
        
    # Frame para el titulo. 
    frame_titulo = tk.Frame(control_frame, bg="#a0b9f0")
    frame_titulo.pack(side=tk.TOP, fill=tk.X, pady=15)

    # Frame central para centrar el contenido
    center_frame = tk.Frame(control_frame, bg="#a0b9f0")
    center_frame.pack(expand=True)

    # Título
    title_label = tk.Label(
        frame_titulo,
        text="Historial de Costos",
        font=("Arial", 16, "bold"),
        bg="#a0b9f0",
        fg="#2C3E50"
    )
    title_label.pack(pady=15)

    # Opción para seleccionar un producto específico o ver todos
    opcion_label = tk.Label(
        center_frame,
        text="Selecciona una opción:",
        bg="#a0b9f0",
        fg="#2C3E50",
        font=("Arial", 11)
    )
    opcion_label.pack(anchor=tk.W, pady=(0, 5))

    opcion_var = tk.StringVar()
    opcion_var.set("producto_especifico")
    opcion_dropdown = tk.OptionMenu(center_frame, opcion_var, "producto_especifico", "todos")
    opcion_dropdown.config(
        bg="#FFFFFF",
        fg="#2C3E50",
        font=("Arial", 10),
        bd=2,
        relief=tk.GROOVE,
        width=20
    )
    opcion_dropdown.pack(anchor=tk.W, pady=(0, 15))

    # Dropdown para seleccionar producto (solo visible si se elige "producto_especifico")
    producto_frame = tk.Frame(center_frame, bg="#E0F2F7")

    producto_label = tk.Label(
        producto_frame,
        text="Selecciona el producto:",
        bg="#a0b9f0",
        fg="#2C3E50",
        font=("Arial", 11)
    )
    producto_label.pack(anchor=tk.W, pady=(0, 5))

    productos = obtener_productos_para_costoventa()
    
    # Verificar si la lista de productos está vacía
    if not productos:
        tk.Label(center_frame, text="Actualmente no hay productos registrados.", font=("Arial", 12)).pack(pady=20)
        messagebox.showwarning("Advertencia", "No hay datos que mostrar en este momento")
        tk.Button(center_frame, text="Volver al Menú", command=abrir_modulo_costos_ganancias(root, mostrar_menu_principal, imagen_panel_tk, rol, imagen_tk), font=("Arial", 10)).pack(pady=10)
        return
    
    producto_vars = [f"{prod[1]}" for prod in productos]
    producto_var = tk.StringVar()
    producto_dropdown = tk.OptionMenu(producto_frame, producto_var, *producto_vars)
    producto_dropdown.config(
        bg="#FFFFFF",
        fg="#2C3E50",
        font=("Arial", 10),
        bd=2,
        relief=tk.GROOVE,
        width=40
    )
    producto_dropdown.pack(anchor=tk.W, pady=(0, 15))

    def toggle_producto_frame(*args):
        if opcion_var.get() == "producto_especifico":
            producto_frame.pack(anchor=tk.W, pady=(0, 15))
        else:
            producto_frame.pack_forget()

    opcion_var.trace_add("write", toggle_producto_frame)

    # Botón para mostrar el historial
    show_button = tk.Button(
        center_frame,
        text="Mostrar Historial",
        bg="#3498DB",
        fg="white",
        font=("Arial", 11, "bold"),
        bd=0,
        relief=tk.FLAT,
        activebackground="#2980B9",
        activeforeground="white",
        command=lambda:mostrar_historial(opcion_var.get(), producto_var.get() if opcion_var.get() == "producto_especifico" else None),
        width=20
    )
    show_button.pack(anchor=tk.W, pady=(0, 20))

    # Área para mostrar el historial
    resultado_frame = tk.Frame(center_frame, bg="#E0F2F7", padx=20, pady=10)
    resultado_frame.pack(fill=tk.X)

    historial_text = tk.Text(
        resultado_frame,
        height=15,
        width=80,
        state="disabled",
        bg="#FFFFFF",
        fg="#2C3E50",
        font=("Arial", 10),
        bd=2,
        relief=tk.GROOVE,
        padx=10,
        pady=10
    )
    historial_text.pack()

    # Botón para volver
    back_button = tk.Button(
        frame_menu,
        text="Volver",
        bg="#E74C3C",
        fg="white",
        font=("Arial", 11, "bold"),
        bd=0,
        relief=tk.FLAT,
        activebackground="#C0392B",
        activeforeground="white",
        command=lambda:abrir_modulo_costos_ganancias(root, mostrar_menu_principal, imagen_panel_tk, rol, imagen_tk),
        width=10
    )
    back_button.pack(side="bottom", padx=30, pady=60)
    
    # Limpiar pantalla manualmente.
    clear_button = tk.Button(
        frame_menu,
        text="Limpiar Pantalla",
        bg="#27E0C8",
        fg="white",
        font=("Arial", 11, "bold"),
        bd=0,
        relief=tk.FLAT,
        activebackground="#C0392B",
        activeforeground="white",
        command=lambda:limpiar_campos(),
        width=15
    )
    clear_button.pack(side="bottom", padx=30, pady=20)

    boton_imprimir_costos = None

    def mostrar_historial(opcion, producto_str=None):
        global boton_imprimir_costos

        # Eliminar el botón imprimir si existe
        if boton_imprimir_costos is not None:
            boton_imprimir_costos.destroy()

        historial_text.config(state="normal")
        historial_text.delete(1.0, tk.END)

        if opcion == "producto_especifico":
            historial_text.insert(tk.END, f"Historial de costos para {producto_str}:\n\n")
            historial = mostrar_historial_costos_por_producto(producto_str)
        else:
            historial_text.insert(tk.END, "Historial de costos para TODOS los productos:\n\n")
            historial = mostrar_historial_costos_general()

        # Encabezados
        if opcion == "producto_especifico":
            historial_text.insert(tk.END, "Fecha       | Costo Anterior | Costo Nuevo | Por Lote | Unidades | Motivo\n")
        else:
            historial_text.insert(tk.END, "Producto    | Fecha       | Costo Anterior | Costo Nuevo | Por Lote | Unidades | Motivo\n")

        historial_text.insert(tk.END, "-" * 80 + "\n")

        for row in historial:
            if opcion == "producto_especifico":
                historial_text.insert(tk.END, f"{row[0]} | €{row[1]:.2f}       | €{row[2]:.2f}      | {'Sí' if row[3] else 'No'}   | {row[4] or 'N/A'}     | {row[5] or 'N/A'}\n")
            else:
                historial_text.insert(tk.END, f"{row[0]} | {row[1]} | €{row[2]:.2f}       | €{row[3]:.2f}      | {'Sí' if row[4] else 'No'}   | {row[5] or 'N/A'}     | {row[6] or 'N/A'}\n")

        historial_text.config(state="disabled")

        # Botón para imprimir el historial
        boton_imprimir_costos = tk.Button(
            resultado_frame,
            text="Imprimir Historial de Costos",
            bg="#27AE60",
            fg="white",
            font=("Arial", 11, "bold"),
            bd=0,
            relief=tk.FLAT,
            activebackground="#2ECC71",
            activeforeground="white",
            command=lambda: imprimir_historial_costos(historial, opcion)
        )
        boton_imprimir_costos.pack(side="left", padx=5, pady=5)
    # Función para limpiar campos
    def limpiar_campos():
        producto_var.set("")
        
    
# Muestra el historial de Ganancias por producto o todo 
def mostrar_historial_ganancias(root, mostrar_menu_principal, imagen_panel_tk, rol, imagen_tk):
    # Limpiar pantalla
    for widget in root.winfo_children():
        widget.destroy()

    frame = tk.Frame(root, bg="#a0b9f0", width=800, height=600)
    frame.pack(fill=tk.BOTH, expand=True)

    # panel izquierdo
    frame_menu = tk.Frame(frame, bg="#2C3E50", width=200, height=800)
    frame_menu.pack(side=tk.LEFT, fill=tk.Y)
    frame_menu.pack_propagate(False)
    
    # Frame para imagen del panel izquierdo
    frame_imagen_panel = tk.Frame(frame_menu, bg="#2C3E50", height=70)
    frame_imagen_panel.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
    
    # Imagen del Logo para el panel izquierdo
    if imagen_panel_tk:
        label_imagen = tk.Label(frame_imagen_panel, image=imagen_panel_tk, bg="#2C3E50")
        label_imagen.pack(side=tk.LEFT, padx=70)
    else:
        label_texto = tk.Label(frame_imagen_panel, text="Ikigai", font=("Arial", 10), bg="#2C3E50")
        label_texto.pack(side=tk.LEFT, padx=30)
        
    # Frame para los controles (centrado)
    control_frame = tk.Frame(frame, bg="#a0b9f0", padx=20, pady=10)
    control_frame.pack(fill=tk.BOTH, expand=True)
    
    frame_titulo = tk.Frame(control_frame, bg="#a0b9f0")
    frame_titulo.pack(side=tk.TOP, fill=tk.X, pady=15)

    # Frame central para centrar el contenido
    center_frame = tk.Frame(control_frame, bg="#a0b9f0")
    center_frame.pack(expand=True)
    
    # Título
    title_label = tk.Label(
        frame_titulo,
        text="Historial de Ganancias",
        font=("Arial", 16, "bold"),
        bg="#a0b9f0",
        fg="#2C3E50"
    )
    title_label.pack(pady=15)

    # Opción para seleccionar un producto específico o ver todos por mes
    opcion_label = tk.Label(
        center_frame,
        text="Selecciona una opción:",
        bg="#a0b9f0",
        fg="#2C3E50",
        font=("Arial", 11)
    )
    opcion_label.pack(anchor=tk.W, pady=(0, 5))

    opcion_var = tk.StringVar()
    opcion_var.set("producto_especifico")
    opcion_dropdown = tk.OptionMenu(center_frame, opcion_var, "producto_especifico", "por_mes")
    opcion_dropdown.config(
        bg="#FFFFFF",
        fg="#2C3E50",
        font=("Arial", 10),
        bd=2,
        relief=tk.GROOVE,
        width=20
    )
    opcion_dropdown.pack(anchor=tk.W, pady=(0, 15))

    # Dropdown para seleccionar producto (solo visible si se elige "producto_especifico")
    producto_frame = tk.Frame(center_frame, bg="#a0b9f0")

    producto_label = tk.Label(
        producto_frame,
        text="Selecciona el producto:",
        bg="#a0b9f0",
        fg="#2C3E50",
        font=("Arial", 11)
    )
    producto_label.pack(anchor=tk.W, pady=(0, 5))

    productos = obtener_productos_para_costoventa()
    
    # Verificar si la lista de productos está vacía
    if not productos:
        tk.Label(center_frame, text="Actualmente no hay productos registrados.", font=("Arial", 12)).pack(pady=20)
        messagebox.showwarning("Advertencia", "No hay datos que mostrar en este momento")
        tk.Button(center_frame, text="Volver al Menú", command=abrir_modulo_costos_ganancias(root, mostrar_menu_principal, imagen_panel_tk, rol, imagen_tk), font=("Arial", 10)).pack(pady=10)
        return
    
    producto_vars = [f"{prod[1]}" for prod in productos]
    producto_var = tk.StringVar()
    producto_var.set("producto_especifico")
    producto_dropdown = tk.OptionMenu(producto_frame, producto_var, *producto_vars)
    producto_dropdown.config(
        bg="#FFFFFF",
        fg="#2C3E50",
        font=("Arial", 10),
        bd=2,
        relief=tk.GROOVE,
        width=40
    )
    producto_dropdown.pack(anchor=tk.W, pady=(0, 15))

    # Dropdown para seleccionar mes (solo visible si se elige "por_mes")
    mes_frame = tk.Frame(center_frame, bg="#a0b9f0")

    mes_label = tk.Label(
        mes_frame,
        text="Selecciona el mes (YYYY-MM):",
        bg="#a0b9f0",
        fg="#2C3E50",
        font=("Arial", 11)
    )
    mes_label.pack(anchor=tk.W, pady=(0, 5))

    mes_var = tk.StringVar()
    mes_entry = tk.Entry(mes_frame, bd=2, relief=tk.GROOVE, font=("Arial", 10))
    mes_entry.pack(anchor=tk.W, pady=(0, 15))

    def toggle_frames(*args):
        if opcion_var.get() == "producto_especifico":
            producto_frame.pack(anchor=tk.W, pady=(0, 15))
            mes_frame.pack_forget()
        else:
            producto_frame.pack_forget()
            mes_frame.pack(anchor=tk.W, pady=(0, 15))

    opcion_var.trace_add("write", toggle_frames)

    # Botón para mostrar el historial
    show_button = tk.Button(
        center_frame,
        text="Mostrar Historial",
        bg="#3498DB",
        fg="white",
        font=("Arial", 11, "bold"),
        bd=0,
        relief=tk.FLAT,
        activebackground="#2980B9",
        activeforeground="white",
        command=lambda: mostrar_historial_ganancias_opcion(
            opcion_var.get(),
            producto_var.get() if opcion_var.get() == "producto_especifico" else None,
            mes_entry.get() if opcion_var.get() == "por_mes" else None
        ),
        width=20
    )
    show_button.pack(anchor=tk.W, pady=(0, 20))

    # Área para mostrar el historial
    resultado_frame = tk.Frame(center_frame, bg="#E0F2F7", padx=20, pady=10)
    resultado_frame.pack(fill=tk.X)

    historial_text = tk.Text(
        resultado_frame,
        height=15,
        width=80,
        state="disabled",
        bg="#FFFFFF",
        fg="#2C3E50",
        font=("Arial", 10),
        bd=2,
        relief=tk.GROOVE,
        padx=10,
        pady=10
    )
    historial_text.pack()

    # Botón para volver
    back_button = tk.Button(
        frame_menu,
        text="Volver",
        bg="#E74C3C",
        fg="white",
        font=("Arial", 11, "bold"),
        bd=0,
        relief=tk.FLAT,
        activebackground="#C0392B",
        activeforeground="white",
        command=lambda:abrir_modulo_costos_ganancias(root, mostrar_menu_principal, imagen_panel_tk, rol, imagen_tk),
        width=10
    )
    back_button.pack(side="bottom", padx=30, pady=60)
    
    # Limpiar pantalla manualmente.
    clear_button = tk.Button(
        frame_menu,
        text="Limpiar Pantalla",
        bg="#27E0C8",
        fg="white",
        font=("Arial", 11, "bold"),
        bd=0,
        relief=tk.FLAT,
        activebackground="#C0392B",
        activeforeground="white",
        command=lambda:limpiar_campos(),
        width=15
    )
    clear_button.pack(side="bottom", padx=30, pady=20)

    boton_imprimir_ganancias = None

    def mostrar_historial_ganancias_opcion(opcion, producto_str=None, mes_str=None):
        global boton_imprimir_ganancias

        # Eliminar el botón de impresión anterior si existe
        if boton_imprimir_ganancias is not None:
            boton_imprimir_ganancias.destroy()

        historial_text.config(state="normal")
        historial_text.delete(1.0, tk.END)

        if opcion == "producto_especifico":
            historial_text.insert(tk.END, f"Historial de ganancias para {producto_str}:\n\n")
            historial = mostrar_historial_ganancias_producto(producto_str)
        else:
            if not mes_str:
                messagebox.showerror("Error", "Debes ingresar un mes.")
                historial_text.config(state="disabled")
                return
            historial_text.insert(tk.END, f"Historial de ganancias para el mes {mes_str}:\n\n")
            historial = mostrar_historial_general_mensual(mes_str)

        if not historial:
            messagebox.showerror("Error", "No hay datos en el historial de ganancias.")
            historial_text.config(state="disabled")
            return

        # Encabezados
        if opcion == "producto_especifico":
            historial_text.insert(tk.END, "Mes         | Ganancia Total | Margen Promedio\n")
        else:
            historial_text.insert(tk.END, "Producto    | Ganancia Total | Margen Promedio\n")

        historial_text.insert(tk.END, "-" * 50 + "\n")

        for row in historial:
            if opcion == "producto_especifico":
                historial_text.insert(tk.END, f"{row[0]} | €{row[1]:.2f}         | {row[2]:.1f}%\n")
            else:
                historial_text.insert(tk.END, f"{row[0]} | €{row[1]:.2f}         | {row[2]:.1f}%\n")

        historial_text.config(state="disabled")

        # Botón para imprimir el historial
        boton_imprimir_ganancias = tk.Button(
            resultado_frame,
            text="Imprimir Historial de Ganancias",
            bg="#27AE60",
            fg="white",
            font=("Arial", 11, "bold"),
            bd=0,
            relief=tk.FLAT,
            activebackground="#2ECC71",
            activeforeground="white",
            command=lambda: imprimir_historial_ganancias(historial, opcion, mes_str)
        )
        boton_imprimir_ganancias.pack(side="left", padx=5, pady=5)

    # Función para limpiar campos
    def limpiar_campos():
        producto_var.set("")


def imprimir_historial_costos(historial, tipo):
    if not historial:
        messagebox.showerror("Error", "No hay datos en el historial de costos.")
        return

    # Preparar los datos para el PDF
    datos = []
    for registro in historial:
        if tipo == "producto_especifico":
            fecha, costo_anterior, costo_nuevo, es_por_lote, unidades, motivo = registro
            datos.append([
                str(fecha),                     # Fecha
                f"${float(costo_anterior):.2f}", # Costo anterior
                f"${float(costo_nuevo):.2f}",   # Costo nuevo
                "Sí" if es_por_lote else "No",   # Por lote
                str(unidades or "N/A"),         # Unidades
                str(motivo or "N/A")             # Motivo
            ])
            columnas = ["Fecha", "Costo Anterior", "Costo Nuevo", "Por Lote", "Unidades", "Motivo"]
        else:
            codigo, fecha, costo_anterior, costo_nuevo, es_por_lote, unidades, motivo = registro
            datos.append([
                str(codigo),                     # Código
                str(fecha),                     # Fecha
                f"${float(costo_anterior):.2f}", # Costo anterior
                f"${float(costo_nuevo):.2f}",   # Costo nuevo
                "Sí" if es_por_lote else "No",   # Por lote
                str(unidades or "N/A"),         # Unidades
                str(motivo or "N/A")             # Motivo
            ])
            columnas = ["Código", "Fecha", "Costo Anterior", "Costo Nuevo", "Por Lote", "Unidades", "Motivo"]

    # Generar el PDF
    from impresora import ImpresorPDF
    logo_path = "Img/logo/Logo-ikigai.png"  # Ruta del logo

    ImpresorPDF.generar_pdf(
        titulo=f"Historial de Costos - {'Producto Específico' if tipo == 'producto_especifico' else 'General'}",
        datos=datos,
        columnas=columnas,
        nombre_archivo=f"historial_costos_{tipo}"
    )


def imprimir_historial_ganancias(historial, tipo, mes_str=None):
    if not historial:
        messagebox.showerror("Error", "No hay datos en el historial de ganancias.")
        return

    # Preparar los datos para el PDF
    datos = []
    for registro in historial:
        if tipo == "producto_especifico":
            mes, ganancia_total, margen_promedio = registro
            datos.append([
                str(mes),                     # Mes
                f"${float(ganancia_total):.2f}",  # Ganancia total
                f"{float(margen_promedio):.1f}%"    # Margen promedio
            ])
            columnas = ["Mes", "Ganancia Total", "Margen Promedio"]
        else:
            codigo, ganancia_total, margen_promedio = registro
            datos.append([
                str(codigo),                     # Código
                f"${float(ganancia_total):.2f}",  # Ganancia total
                f"{float(margen_promedio):.1f}%"    # Margen promedio
            ])
            columnas = ["Producto", "Ganancia Total", "Margen Promedio"]

    # Generar el PDF
    from impresora import ImpresorPDF
    logo_path = "Img/logo/logo_ikigai.png"  # Ruta del logo

    ImpresorPDF.generar_pdf(
        titulo=f"Historial de Ganancias - {'Producto Específico' if tipo == 'producto_especifico' else f'Mes {mes_str}'}",
        datos=datos,
        columnas=columnas,
        nombre_archivo=f"historial_ganancias_{tipo}_{mes_str if tipo == 'por_mes' else ''}"
    )




# Inicia el módulo de costos y ganancias
def abrir_modulo_costos_ganancias(root, mostrar_menu_principal, imagen_panel_tk, rol, imagen_tk):
    # Limpiar pantalla
    for widget in root.winfo_children():
        widget.destroy()

    frame_botones_cg = tk.Frame(root, bg="#2C3E50", width=220, height=800, bd=3, relief="solid")
    frame_botones_cg.pack(side=tk.LEFT, fill=tk.Y)
    frame_botones_cg.pack_propagate(False)
    
    # Frame del Titulo
    frame_titulo = tk.Frame(root, bg="#a0b9f0")
    frame_titulo.pack(side=tk.TOP, fill=tk.X, pady=15)
    
    frame_imagen = tk.Frame(root, bg="#a0b9f0")
    frame_imagen.pack(expand=True)
        
    if imagen_tk:
        tk.Label(frame_imagen, image=imagen_tk, bg="#a0b9f0").pack(pady=20)
    else:
        tk.Label(frame_imagen, text="Ikigai Designs", font=("Arial", 24), bg="#a0b9f0").pack(pady=20)

    # Título
    title_label = tk.Label(
        frame_titulo,
        text="Costos y Ganancias",
        font=("Arial", 16, "bold"),
        bg="#a0b9f0",
        fg="#2C3E50"
    )
    title_label.pack(pady=15)

    # #Botón: Calcular costo de producción
    # tk.Button(
    #     frame_botones_cg,
    #     text="Actualizar Costo de Producción",
    #     command=lambda: abrir_actualizar_costo_produccion(root, mostrar_menu_principal, imagen_panel_tk, rol, imagen_tk),
    #     width=21,
    # ).pack(pady=15)

    # # Botón: Calcular precio de venta
    # tk.Button(
    #     frame_botones_cg,
    #     text="Calcular Precio de Venta",
    #     command=lambda: abrir_calcular_precio_venta(root, mostrar_menu_principal, imagen_panel_tk, rol, imagen_tk),
    #     width=21,
    # ).pack(pady=15)


    # Botón para actualizar costo por unidad
    unidad_button = tk.Button(
        frame_botones_cg,
        text="Actualizar Costo de Unidad",
        bg="#3498DB",
        fg="white",
        font=("Arial", 10, "bold"),
        bd=0,
        relief=tk.FLAT,
        activebackground="#2ECC71",
        activeforeground="white",
        command=lambda: abrir_actualizar_costo_por_unidad(root, mostrar_menu_principal, imagen_panel_tk, rol, imagen_tk),
        width=25
    )
    unidad_button.pack(side=tk.TOP, padx=20, pady=10)

    # Botón para actualizar costo por lote
    lote_button = tk.Button(
        frame_botones_cg,
        text="Actualizar Costo de Lote",
        bg="#02AA48",
        fg="white",
        font=("Arial", 10, "bold"),
        bd=0,
        relief=tk.FLAT,
        activebackground="#2ECC71",
        activeforeground="white",
        command=lambda: abrir_actualizar_costo_por_lote(root, mostrar_menu_principal, imagen_panel_tk, rol, imagen_tk),
        width=25
    )
    lote_button.pack(side=tk.TOP, padx=20, pady=10)
    
    # Botón: Actualizar historial de ganancias
    tk.Button(
        frame_botones_cg,
        text="Actualizar Historial de Ganancias",
        bg="#153FB3",
        fg="white",
        font=("Arial", 9, "bold"),
        bd=0,
        relief=tk.FLAT,
        activebackground="#2ECC71",
        activeforeground="white",
        command=lambda: abrir_actualizar_historial(root, mostrar_menu_principal, imagen_panel_tk, rol, imagen_tk),
        width=25,
    ).pack(pady=15)
    
    # Botón: Mostrar historial costos
    tk.Button(
        frame_botones_cg,
        text="Ver historial Costos",
        bg="#AE15B3",
        fg="white",
        font=("Arial", 10, "bold"),
        bd=0,
        relief=tk.FLAT,
        activebackground="#2ECC71",
        activeforeground="white",
        command=lambda: mostrar_historial_costos(root, mostrar_menu_principal, imagen_panel_tk, rol, imagen_tk),
        width=25,
    ).pack(pady=15)
    
    # Botón: Mostrar historial costos
    tk.Button(
        frame_botones_cg,
        text="Ver historial Ganancias",
        bg="#EEDE05",
        fg="white",
        font=("Arial", 10, "bold"),
        bd=0,
        relief=tk.FLAT,
        activebackground="#2ECC71",
        activeforeground="white",
        command=lambda: mostrar_historial_ganancias(root, mostrar_menu_principal, imagen_panel_tk, rol, imagen_tk),
        width=25,
    ).pack(pady=15)
    
    # Botón para volver al menú
    tk.Button(
        frame_botones_cg,
        text="Volver al Menú",
        command=mostrar_menu_principal,
        width=18,
        bg="#913131",
        fg="white",
        font=("Arial", 11, "bold"),
        bd=0,
        relief=tk.FLAT,
        activebackground="#2ECC71",
        activeforeground="white",
    ).pack(side=tk.LEFT, padx=30, pady=40)
