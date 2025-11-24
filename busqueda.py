# modulo_busqueda.py

import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from db import buscar_en_bd, obtener_materiales, encontrar_notas_entrega, encontrar_facturas, actualizar_en_bd
from recursos import LOGO_PATH
from inventario import convertir_a_float


def busqueda_articulos(root, volver_menu, imagen_panel_tk, imagen_buscar_tk, usuario_actual):
    # Limpiar el frame de contenido
    for widget in root.winfo_children():
        widget.destroy()

    # panel izquierdo
    frame_menu = tk.Frame(root, bg="#2C3E50", width=200, height=800)
    frame_menu.pack(side=tk.LEFT, fill=tk.Y)
    frame_menu.pack_propagate(False)
    
    # Frame para imagen del panel izquierdo
    frame_imagen_panel = tk.Frame(frame_menu, bg="#2C3E50", height=70)
    frame_imagen_panel.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
    
    # Crear frame_contenido (para formularios)
    frame_contenido = tk.Frame(root, bg="#a0b9f0", width=600, height=800)
    frame_contenido.pack(expand=True, fill=tk.BOTH, side=tk.RIGHT)
    
    frame_titulo = tk.Frame(frame_contenido, bg="#a0b9f0")
    frame_titulo.pack(side=tk.TOP, fill=tk.X, pady=15)
    
    # frame para Imagen buscar del panel derecho 
    frame_imagen = tk.Frame(frame_contenido, bg="#a0b9f0")
    frame_imagen.pack(expand=True)
    
    # Imagen del Logo para el panel izquierdo
    if imagen_panel_tk:
        label_imagen = tk.Label(frame_imagen_panel, image=imagen_panel_tk, bg="#2C3E50")
        label_imagen.pack(side=tk.LEFT, padx=70)
    else:
        label_texto = tk.Label(frame_imagen_panel, text="Ikigai", font=("Arial", 10), bg="#2C3E50")
        label_texto.pack(side=tk.LEFT, padx=30)

    # Título
    title_label = tk.Label(
        frame_titulo,
        text="Módulo de Busqueda",
        font=("Arial", 16, "bold"),
        bg="#a0b9f0",
        fg="#2C3E50"
    )
    title_label.pack(pady=15)
    
    # Imagen buscar para el panel derecho
    if imagen_buscar_tk:
        tk.Label(frame_imagen, image=imagen_buscar_tk, bg="#a0b9f0").pack(pady=20)
    else:
        tk.Label(frame_imagen, text="Ikigai Designs", font=("Arial", 24), bg="#a0b9f0").pack(pady=20)

    # Crear un frame para el formulario de búsqueda
    form_frame = tk.Frame(frame_contenido, bg="#a0b9f0", padx=20, pady=20)
    form_frame.place(relx=0.5, rely=0.1, anchor=tk.N)

    #tk.Label(frame_contenido, text="Buscador de Artículos", width=30, font=16, bg="#6876f5").place(relx=0.5, rely=0.03, anchor=tk.CENTER)

    # Campo para seleccionar el tipo de búsqueda
    tk.Label(form_frame, text="Buscar por:", bg="#8e98f5").grid(row=0, column=0, sticky="e")
    tipo_busqueda = ttk.Combobox(form_frame, values=["Todos los Materiales", "Proveedor", "Factura Proveedor", "Notas de Entregas" ,"Código", "Material", "Todos los Productos", "Producto", "Facturas Ventas"], width=28)
    tipo_busqueda.grid(row=0, column=1, pady=5)

    # Campo para ingresar el valor de búsqueda
    tk.Label(form_frame, text="Valor de búsqueda:", bg="#8e98f5").grid(row=1, column=0, sticky="e")
    valor_busqueda_entry = tk.Entry(form_frame, width=30)
    valor_busqueda_entry.grid(row=1, column=1, pady=5)
    
    # Función para realizar la búsqueda
    def realizar_busqueda():
        tipo = tipo_busqueda.get()
        valor = valor_busqueda_entry.get()
        if not tipo:#or not valor:
            messagebox.showerror("Error", "Debe seleccionar un tipo de búsqueda")# y proporcionar un valor.")
            return

        resultados = buscar_en_bd(tipo, valor)
        mostrar_resultados(resultados, tipo, root, usuario_actual, volver_menu)
        
        

    # Botón para realizar la búsqueda
    tk.Button(
        form_frame,
        text="Buscar",
        command=realizar_busqueda,
        bg="#75EC57"
    ).grid(row=2, column=0, columnspan=2, pady=10)

    # Botón para volver al menú
    tk.Button(
        frame_menu,
        text="Volver al Menú",
        command=volver_menu,
        width=18,
        bg="#913131"
    ).pack(side=tk.LEFT, padx=30, pady=40)


# Muestra la busqueda realizada.
def mostrar_resultados(resultados, tipo_busqueda, root, usuario_actual, volver_menu):
    if not resultados:
        messagebox.showinfo("Resultado", "No se encontraron resultados.")
        return
    
    resultados_window = tk.Toplevel()
    resultados_window.title("Resultados de la Búsqueda")
    
    frame_datos= tk.Frame(resultados_window, pady="5")
    frame_datos.pack(fill=tk.BOTH, expand=True)
    
    if tipo_busqueda in ["Proveedor", "Factura Proveedor", "Código", "Material"]:
        # Crear un Treeview para mostrar los resultados de materiales/facturas/proveedores
        tree = ttk.Treeview(frame_datos, columns=("Proveedor", "Factura N°", "Fecha", "Código", "Nombre", "Tipo", "Tamaño", "Color", "Stock", "Costo", "Costo Unit."), show="headings")

        # Configurar las columnas
        tree.heading("Proveedor", text="Prov.")
        tree.heading("Factura N°", text="Fact.N°")
        tree.heading("Fecha", text="Fecha")
        tree.heading("Código", text="Cod.")
        tree.heading("Nombre", text="Art.")
        tree.heading("Tipo", text="Tipo.")
        tree.heading("Tamaño", text="Tamaño.")
        tree.heading("Color", text="Color.")
        tree.heading("Stock", text="Cant.")
        tree.heading("Costo", text="C.Total")
        tree.heading("Costo Unit.", text="C.Uni")

        # Ajustar el ancho de las columnas
        tree.column("Proveedor", width=100)
        tree.column("Factura N°", width=80)
        tree.column("Fecha", width=80)
        tree.column("Código", width=50)
        tree.column("Nombre", width=100)
        tree.column("Tipo", width=60)
        tree.column("Tamaño", width=60)
        tree.column("Color", width=60)
        tree.column("Stock", width=60)
        tree.column("Costo", width=60)
        tree.column("Costo Unit.", width=60)

        # Insertar los resultados en el Treeview
        for resultado in resultados:
            tree.insert("", tk.END, values=resultado)
        
    elif tipo_busqueda == "Producto":
        # Crear un Treeview para mostrar los resultados de productos (Se elimino el campo Nombre)
        tree = ttk.Treeview(frame_datos, columns=("Código", "Tipo", "Costo Venta", "Precio Venta", "Materiales Usados", "Tiempo Fabricación", "Cantidad", "Fecha R", "Descripción"), show="headings")

        # Configurar las columnas
        tree.heading("Código", text="Cod.")
        tree.heading("Tipo", text="Tipo")
        tree.heading("Costo Venta", text="Costo")
        tree.heading("Precio Venta", text="P.Venta")
        tree.heading("Materiales Usados", text="Mat.Usados")
        tree.heading("Cantidad", text="Cant.")
        tree.heading("Tiempo Fabricación", text="T.Fab")
        tree.heading("Fecha R", text="Fecha.R")
        tree.heading("Descripción", text="Descripción")

        # Ajustar el ancho de las columnas
        tree.column("Código", width=100)
        tree.column("Tipo", width=80)
        tree.column("Costo Venta", width=80)
        tree.column("Precio Venta", width=50)
        tree.column("Materiales Usados", width=300)
        tree.column("Cantidad", width=50)
        tree.column("Tiempo Fabricación", width=100)
        tree.column("Fecha R", width=80)
        tree.column("Descripción", width=300)

        # Insertar los resultados en el Treeview
        for resultado in resultados:
            tree.insert("", tk.END, values=resultado)
            
    elif tipo_busqueda == "Todos los Materiales":
        tree = ttk.Treeview(frame_datos, columns=("Código", "Nombre", "Tipo", "Tamaño", "Color", "Stock", "Costo", "Costo Unit."), show="headings")

        # Configurar las columnas
        tree.heading("Código", text="Cod.")
        tree.heading("Nombre", text="Nombre")
        tree.heading("Tipo", text="Tipo")
        tree.heading("Tamaño", text="Tamaño")
        tree.heading("Color", text="Color")
        tree.heading("Stock", text="Cant.")
        tree.heading("Costo", text="P.Vent")
        tree.heading("Costo Unit.", text="P.Uni.")

        # Ajustar el ancho de las columnas
        tree.column("Código", width=70)
        tree.column("Nombre", width=65)
        tree.column("Tipo", width=80)
        tree.column("Tamaño", width=80)
        tree.column("Color", width=70)
        tree.column("Stock", width=70)
        tree.column("Costo", width=65)
        tree.column("Costo Unit.", width=65)

        # Insertar los resultados en el Treeview
        for resultado in resultados:
            tree.insert("", tk.END, values=resultado)
            
    elif tipo_busqueda == "Todos los Productos":
        # Crear un Treeview para mostrar los resultados de productos (Se elimino el campo Nombre)
        tree = ttk.Treeview(frame_datos, columns=("Código", "Tipo", "Costo Venta", "Precio Venta", "Materiales Usados", "Tiempo Fabricación", "Cantidad", "Fecha R", "Descripción"), show="headings")

        # Configurar las columnas
        tree.heading("Código", text="Cod.")
        tree.heading("Tipo", text="Tipo")
        tree.heading("Costo Venta", text="C.Venta")
        tree.heading("Precio Venta", text="P.Venta")
        tree.heading("Materiales Usados", text="Mat.Usados")
        tree.heading("Cantidad", text="Cant.")
        tree.heading("Tiempo Fabricación", text="T.Fab")
        tree.heading("Fecha R", text="Fecha.R")
        tree.heading("Descripción", text="Descripción")

        # Ajustar el ancho de las columnas
        tree.column("Código", width=70)
        tree.column("Tipo", width=70)
        tree.column("Costo Venta", width=60)
        tree.column("Precio Venta", width=60)
        tree.column("Materiales Usados", width=300)
        tree.column("Cantidad", width=50)
        tree.column("Tiempo Fabricación", width=70)
        tree.column("Fecha R", width=70)
        tree.column("Descripción", width=300)

        # Insertar los resultados en el Treeview
        for resultado in resultados:
            tree.insert("", tk.END, values=resultado)
            
    # Busqueda de notas de entregas
    elif tipo_busqueda == "Notas de Entregas":
        from crea_factura_nota_entrega import imprimir_nota_entrega, convertir_nota_a_factura
        
        # Crear un Treeview para mostrar las notas de entrega
        tree = ttk.Treeview(frame_datos, columns=("ID", "Fecha", "Cliente", "Total", "Estado"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Fecha", text="Fecha")
        tree.heading("Cliente", text="Cliente")
        tree.heading("Total", text="Total")
        tree.heading("Estado", text="Estado")
        tree.pack(fill=tk.BOTH, expand=True)
        
        # Función para cargar las notas de entrega
        def cargar_notas():
            
            for item in tree.get_children():
                tree.delete(item)
            notas_entrega = encontrar_notas_entrega()
            
            for row in notas_entrega:
                tree.insert("", tk.END, values=row)

        # Botón para cargar las notas de entrega
        tk.Button(frame_datos, 
                text="Cargar Notas de Entrega", 
                command=cargar_notas).pack(side="left", padx=5, pady=5)

        # Función para convertir a factura
        def convertir_a_factura_seleccionada():
            try:
                selected_item = tree.selection()
                if not selected_item:
                    messagebox.showerror("Error", "Selecciona una nota de entrega.")
                    return
                id_nota_entrega = tree.item(selected_item)["values"][0]
                estado = tree.item(selected_item)["values"][4]
                if estado == "Facturado":
                    messagebox.showerror("Error", "Esta nota de entrega ya ha sido facturada.")
                    return
                print("El id_nota_entrega es: ", id_nota_entrega)
                convertir_nota_a_factura(id_nota_entrega)
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error: {e}")

        # Botón para convertir a factura
        tk.Button(frame_datos, text="Facturar", command=convertir_a_factura_seleccionada).pack(side="left", padx=5, pady=5)

        # Función para imprimir la nota de entrega seleccionada
        def imprimir_nota_seleccionada():
            try:
                selected_item = tree.selection()
                if not selected_item:
                    messagebox.showerror("Error", "Selecciona una nota de entrega.")
                    return
                id_nota_entrega = tree.item(selected_item)["values"][0]
                imprimir_nota_entrega(id_nota_entrega, es_copia=True)  # Ajuste Para intentar que solo sea una copia.
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error: {e}")

        # Botón para imprimir la nota de entrega
        tk.Button(frame_datos, 
                text="Imprimir Nota de Entrega", 
                command=imprimir_nota_seleccionada).pack(side="left", padx=5, pady=5)
        
    
    elif tipo_busqueda == "Facturas Ventas":
        from crea_factura_nota_entrega import imprimir_factura
        print("Llamando a encontrar factura desde busqueda")

        tree = ttk.Treeview(frame_datos, columns=("N° Factura", "Fecha", "Cliente", "Subtotal", "Descuento", "Impuesto", "Total"), show="headings")
        tree.heading("N° Factura", text="Factura N°")
        tree.heading("Fecha", text="Fecha")
        tree.heading("Cliente", text="Cliente")
        tree.heading("Subtotal", text="Subtotal")
        tree.heading("Descuento", text="Descuento")
        tree.heading("Impuesto", text="Impuesto")
        tree.heading("Total", text="Total")
        tree.pack(fill=tk.BOTH, expand=True)

        def cargar_facturas():
            for item in tree.get_children():
                tree.delete(item)
            facturas = encontrar_facturas()
            for row in facturas:
                tree.insert("", tk.END, values=row)

        tk.Button(frame_datos, 
                text="Cargar Facturas", 
                command=cargar_facturas).pack(side="left", padx=5, pady=5)

        # Botón para imprimir una factura seleccionada
        def imprimir_factura_seleccionada():
            try:
                selected_item = tree.selection()
                if not selected_item:
                    messagebox.showerror("Error", "Selecciona una factura para imprimir.")
                    return
                id_factura = tree.item(selected_item)["values"][0]
                imprimir_factura(id_factura, es_copia=True)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo imprimir la factura: {e}")

        tk.Button(frame_datos, 
                text="Imprimir Factura", 
                command=imprimir_factura_seleccionada).pack(side="left", padx=5, pady=5)

    
    # Agregar un Scrollbar
    scrollbar = ttk.Scrollbar(frame_datos, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    

    def editar_item():
        # Obtener el ítem seleccionado en el Treeview
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Selecciona un ítem para editar.")
            return

        # Obtener los valores del ítem seleccionado
        valores = tree.item(selected_item)["values"]

        # Crear una ventana para editar el ítem
        ventana_editar = tk.Toplevel()
        ventana_editar.title("Editar Ítem")

        # Variables para almacenar los nuevos valores
        nuevos_valores = {}
        entries = {}

        # Crear un frame para los campos de edición
        frame_edicion = tk.Frame(ventana_editar, padx=10, pady=10)
        frame_edicion.pack()

        # Crear campos de edición según el tipo de búsqueda
        if tipo_busqueda =="Proveedor":
            campos = ["Proveedor"]
            campo_indice = {"Proveedor": 0}
            
        elif tipo_busqueda == "Factura Proveedor":
            campos = ["Factura N°",  "Fecha"]
            campo_indice = {
                "Factura N°": 1,
                "Fecha": 2,
            }
        elif tipo_busqueda == "Código":
            campos = ["Código"]
            campo_indice = {"Código": 3}
            
        elif tipo_busqueda == "Material":
            campos = ["Nombre", "Tipo", "Tamaño", "Color", "Stock", "Costo", "Costo Unit."]
            campo_indice = {"Nombre": 4,
                            "Tipo": 5,
                            "Tamaño": 6,
                            "Color": 7,
                            "Stock": 8,
                            "Costo": 9,
                            "Costo Unit.": 10}
        
        elif tipo_busqueda == "Todos los Materiales":
            campos = ["Código", "Nombre", "Tipo", "Tamaño", "Color", "Stock", "Costo", "Costo Unit."]
            campo_indice = {"Código": 0,
                            "Nombre": 1,
                            "Tipo": 2,
                            "Tamaño": 3,
                            "Color": 4,
                            "Stock": 5,
                            "Costo": 6,
                            "Costo Unit.": 7}
            
        elif tipo_busqueda in ["Producto", "Todos los Productos"]:
            campos = ["Código", "Tipo", "Costo Venta", "Precio Venta", "Materiales Usados", "Tiempo Fabricación", "Cantidad", "Fecha R", "Descripción"]
            campo_indice = {"Código": 0,
                            "Tipo": 1,
                            "Costo Venta": 2,
                            "Precio Venta": 3,
                            "Materiales Usados": 4,
                            "Tiempo Fabricación": 5,
                            "Cantidad": 6,
                            "Fecha R": 7,
                            "Descripción": 8}
            
        else:
            messagebox.showerror("Error", "Tipo de búsqueda no soportado para edición.")
            return
    
    
        # Crear etiquetas y campos de entrada para cada campo
        for i, campo in enumerate(campos):
            tk.Label(frame_edicion, text=campo).grid(row=i, column=0, sticky="e")
            entry = tk.Entry(frame_edicion)
            entry.grid(row=i, column=1)
            entry.insert(0, valores[campo_indice[campo]])
            entries[campo] = entry

        # Función para actualizar los datos en la base de datos y el Treeview
        def actualizar_datos():
            # Obtener los nuevos valores de los campos de entrada
            for campo in campos:
                nuevos_valores[campo] = entries[campo].get()

            # Crear una copia de los valores originales del Treeview
            nuevos_valores_tree = list(valores)  # Copia de los valores originales del Treeview

            # Actualizar solo los campos editados en la lista del Treeview
            for campo in campos:
                nuevos_valores_tree[campo_indice[campo]] = nuevos_valores[campo]  # Actualizar en la posición correcta

            print("DATOS QUE SE ENVIAN A DB: ", nuevos_valores_tree)
            # Para reajustar el precio unitario si el precio total cambia
            if "Costo" in nuevos_valores and "Stock" in nuevos_valores:
                try:
                    precio_total = convertir_a_float(nuevos_valores["Costo"])
                    cantidad = convertir_a_float(nuevos_valores["Stock"])
                    nuevo_precio_unitario = precio_total / cantidad
                    nuevos_valores["Costo Unit."] = f"{nuevo_precio_unitario:.2f}"
                    print("Resultado del nuevo Costo Unitario: ", nuevo_precio_unitario)
                    print("El Costo Unitario Actualizado es: ", nuevos_valores["Costo Unit."])
                    
                    # Actualizar el precio unitario en la lista del Treeview
                    if "Costo Unit." in campo_indice:  # Verificar si "Costo Unit." está en campo_indice
                        idx = campo_indice["Costo Unit."]  # Usar el índice correcto de campo_indice
                        nuevos_valores_tree[idx] = nuevos_valores["Costo Unit."]
                except ValueError:
                    messagebox.showerror("Error", "El precio o la cantidad no son valores numéricos válidos.")
                    
            # Llamar a la función para actualizar la base de datos
            actualizar_en_bd(tipo_busqueda, valores[0], nuevos_valores, valores)
            # Actualizar el Treeview con los nuevos valores (incluyendo los no editados)
            tree.item(selected_item, values=nuevos_valores_tree)
            # Cerrar la ventana de edición
            ventana_editar.destroy()

        # Botón para guardar los cambios
        tk.Button(ventana_editar, text="Guardar", command=actualizar_datos).pack(pady=10)


    # Función para imprimir los resultados
    def imprimir_resultados():
        # Obtener las columnas del Treeview
        columnas = [tree.heading(col)["text"] for col in tree["columns"]]

        # Obtener los datos del Treeview
        datos = []
        for item in tree.get_children():
            valores = tree.item(item, "values")
            datos.append(list(valores))

        # Determinar el título según el tipo de búsqueda
        titulo = f"Resultados de Búsqueda: {tipo_busqueda}"

        # Generar el PDF
        from impresora import ImpresorPDF
        logo_path = LOGO_PATH  # Asegúrate de que esta ruta sea correcta
        col_widths = [100, 100, 100, 100, 100, 100, 100, 100, 100]  # Ajusta según tus necesidades

        ImpresorPDF.generar_pdf(
            titulo=titulo,
            datos=datos,
            columnas=columnas,
            nombre_archivo=f"resultados_{tipo_busqueda.replace(' ', '_').lower()}",
            #col_widths=col_widths,
            logo_path=logo_path
        )


    # Botón para imprimir
    boton_imprimir = tk.Button(
        resultados_window,
        text="Imprimir",
        command=imprimir_resultados
    )
    boton_imprimir.pack(side=tk.LEFT, padx=5, pady=5)
    
    # Dar acceso si es admin
    if usuario_actual == "admin":
        # Botón para editar
        boton_editar = tk.Button(
            resultados_window,
            text="Editar",
            command=editar_item
        )
        boton_editar.pack(side=tk.LEFT, padx=5, pady=5)

    # Empaquetar los widgets
    tree.pack(fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
