# info_tienda.py

import tkinter as tk
from tkinter import ttk, messagebox
from recursos import crear_boton, crear_encabezado
from databasemanager import DataBaseManager

db_conect = DataBaseManager()
id_del_registro = None

def info_tienda(root, mostrar_menu_principal, branding, nombre_negocio):
    # Limpiar el frame de cualquier contenido
    for widget in root.winfo_children():
        widget.destroy()
        
    # Crear frame_contenido (para formularios)
    frame_contenido = tk.Frame(root, bg=branding["fondo"], width=600, height=800)
    frame_contenido.pack(expand=True, fill=tk.BOTH, side=tk.RIGHT)
    
    # Frame para el título
    frame_titulo = tk.Frame(frame_contenido, bg=branding["fondo"])
    frame_titulo.pack(side=tk.TOP, fill=tk.X, pady=15)
    
    frame_imagen = tk.Frame(frame_contenido, bg=branding["fondo"])
    frame_imagen.pack(expand=True)
    
    # Imagen del Logo
    crear_encabezado(frame_imagen, branding, nombre_negocio,
                        tamano=300, fuente=("Arial", 14, "bold"))
    # if imagen_tk:
    #     tk.Label(frame_imagen, image=imagen_tk, bg=branding["fondo"]).pack(pady=20)
    # else:
    #     tk.Label(frame_imagen, text="Ikigai Designs", font=("Arial", 24), bg=branding["fondo"]).pack(pady=20)
            
    # Frame para los botones (lado izquierdo)
    frame_botones = tk.Frame(root, bg=branding["menu"], width=200, height=800)
    frame_botones.pack(side=tk.LEFT, fill=tk.Y)
    frame_botones.pack_propagate(False)
    
    frame_imagen_panel = tk.Frame(frame_botones, bg=branding["menu"], height=70)
    frame_imagen_panel.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
    
    imagen_panel_tk = crear_encabezado(frame_imagen_panel, branding, nombre_negocio,
                                        tamano=70, fuente=("Arial", 12, "bold"))
    
    # Título
    title_label = tk.Label(
        frame_titulo,
        text="Agrega los datos de tu negocio o actualizalos",
        font=("Arial", 16, "bold"),
        bg=branding["fondo"],
        fg=branding["fuente"]
        )
    title_label.pack(pady=15)
    # Agrega los datos del negocio
    crear_boton(frame_botones,
        texto="Ingresar Datos",
        ancho=30,
        alto=30,
        color_fondo="#B1AE04",                
        color_texto="white",
        font=("Arial", 11, "bold"),
        #bd=0,
        #relief=tk.FLAT,
        hover_color="#2ECC71",
        #activeforeground="black",
        #bg=0,
        comando=lambda: ingresar_datos_tienda(frame_contenido, frame_imagen_panel, imagen_panel_tk, mostrar_menu_principal, branding, nombre_negocio),
        #width=18
    ).pack(pady=15)
    # Agrega los datos del negocio
    crear_boton(frame_botones,
        texto="Ver Datos",
        ancho=30,
        alto=30,
        color_fondo="#0E8518",                
        color_texto="white",
        font=("Arial", 11, "bold"),
        #bd=0,
        #relief=tk.FLAT,
        hover_color="#2ECC71",
        #activeforeground="black",
        #bg=0,
        comando=lambda: ver_datos_tienda(frame_contenido, frame_imagen_panel, imagen_panel_tk, mostrar_menu_principal, branding, nombre_negocio),
        #width=18
    ).pack(pady=15)
    # Actualiza los datos del negocio
    crear_boton(
        frame_botones,
        texto="Actualizar Datos",
        ancho=30,
        alto=30,
        color_fondo="#4011EB",                
        color_texto="white",
        font=("Arial", 11, "bold"),
        #bd=0,
        #relief=tk.FLAT,
        hover_color="#2ECC71",
        #activeforeground="black",
        comando=lambda: actualizar_tienda(frame_contenido, mostrar_menu_principal, branding, nombre_negocio),
        
    ).pack(pady=15)
    # Volver al menu Pricipal
    crear_boton(
        frame_botones,
        texto="Menú Principal",
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
        comando=mostrar_menu_principal,
        
    ).pack(side=tk.LEFT, padx=30, pady=40)
        
        
def ingresar_datos_tienda(frame_contenido, frame_imagen_panel, imagen_panel_tk, mostrar_menu_principal, branding, nombre_negocio):
    # Limpiar el frame principal
    for widget in frame_contenido.winfo_children():
        widget.destroy()

    # Frame principal
    frame = tk.Frame(frame_contenido, bg=branding["fondo"], width=600, height=800)
    frame.pack(fill=tk.BOTH, expand=True)
        
    # # Imagen del Logo para el panel izquierdo
    # if imagen_panel_tk:
    #     label_imagen = tk.Label(frame_imagen_panel, image=imagen_panel_tk, bg=branding["menu"])
    #     label_imagen.pack(side=tk.LEFT, padx=70)
    # else:
    #     label_texto = tk.Label(frame_imagen_panel, text="Ikigai", font=("Arial", 10), bg=branding["menu"])
    #     label_texto.pack(side=tk.LEFT, padx=30)
    
    # Frame para los controles
    control_frame = tk.Frame(frame, bg=branding["fondo"], padx=20, pady=10)
    control_frame.pack(fill=tk.BOTH, expand=True)
        
    frame_titulo = tk.Frame(control_frame, bg=branding["fondo"])
    frame_titulo.pack(side=tk.TOP, fill=tk.X, pady=15)
    
    # Frame central para centrar el contenido
    center_frame = tk.Frame(control_frame, bg=branding["fondo"])
    center_frame.pack(expand=True)
    
    # Título
    title_label = tk.Label(
        frame_titulo,
        text="Ingresa los datos de la Tienda ",
        font=("Arial", 16, "bold"),
        bg=branding["fondo"],
        fg=branding["fuente"]
        )
    title_label.pack(pady=15)
    
    # Campos para gestionar usuarios
    tk.Label(center_frame, text="Nombre de la Tienda:", bg=branding["fondo"]).grid(row=0, column=0, sticky="e", pady=5)
    nombre_tienda_entry = tk.Entry(center_frame, width=30)
    nombre_tienda_entry.grid(row=0, column=1, pady=5)

    tk.Label(center_frame, text="Dirección:", bg=branding["fondo"]).grid(row=1, column=0, sticky="e", pady=5)
    direccion_entry = tk.Entry(center_frame, width=30)
    direccion_entry.grid(row=1, column=1, pady=5)

    tk.Label(center_frame, text="ID Fiscal:", bg=branding["fondo"]).grid(row=2, column=0, sticky="e", pady=5)
    id_fiscal_entry = tk.Entry(center_frame, width=30)
    id_fiscal_entry.grid(row=2, column=1, pady=5)
    
    tk.Label(center_frame, text="Telefono:", bg=branding["fondo"]).grid(row=3, column=0, sticky="e", pady=5)
    telefono_entry = tk.Entry(center_frame, width=30)
    telefono_entry.grid(row=3, column=1, pady=5)
    
    tk.Label(center_frame, text="Email:", bg=branding["fondo"]).grid(row=4, column=0, sticky="e", pady=5)
    correo_entry = tk.Entry(center_frame, width=30)
    correo_entry.grid(row=4, column=1, pady=5)
    
    # Modo de negocio: fabricante (como está ahora) o vendedor (solo reventa)
    tk.Label(center_frame, text="Modo de negocio:", bg=branding["fondo"]).grid(row=5, column=0, sticky="e", pady=5)
    modo_negocio_combobox = ttk.Combobox(center_frame, values=["fabricante", "vendedor"], state="readonly", width=28)
    modo_negocio_combobox.grid(row=5, column=1, pady=5)
    modo_negocio_combobox.set("fabricante")  # Valor por defecto: comportamiento actual

    def limpiar_pantalla():
        # Limpiar campos.
        nombre_tienda_entry.delete(0, tk.END)
        direccion_entry.delete(0, tk.END)
        id_fiscal_entry.delete(0, tk.END)
        telefono_entry.delete(0, tk.END)
        correo_entry.delete(0, tk.END)
        
    # Función para agregar un nuevo usuario
    def agregar_tienda_db():
        tienda = nombre_tienda_entry.get()
        direccion = direccion_entry.get()
        id_fiscal = id_fiscal_entry.get()
        telefono = telefono_entry.get()
        correo = correo_entry.get()
        modo_negocio = modo_negocio_combobox.get()

        if tienda and direccion and id_fiscal and telefono and correo and modo_negocio:
            id_del_registro = db_conect.guardar_info_tienda(tienda, direccion, id_fiscal, telefono, correo, modo_negocio)
            
                
            if id_del_registro:
                #db_conect.guardar_modo_negocio(modo_negocio)
                messagebox.showinfo("✅ Éxito", "Usuario agregado correctamente.")
                limpiar_pantalla()
                mostrar_menu_principal()
            else:
                messagebox.showerror("⚠️ Error", f"No se ha podido Registrar los datos de la tienda.")
        else:
            messagebox.showerror("⚠️ Error", "Todos los campos son obligatorios.")

    # Botón para agregar usuario
    crear_boton(center_frame, 
            texto="Guardar datos", 
            ancho=30,
            alto=30,
            color_fondo="#8e98f5",                
            color_texto="white",
            font=("Arial", 11, "bold"),
            #bd=0,
            #relief=tk.FLAT,
            hover_color="#2ECC71",
            #activeforeground="black",
            comando=agregar_tienda_db, 
            ).grid(row=6, column=0, columnspan=2, pady=10)


def ver_datos_tienda(frame_contenido, frame_imagen_panel, imagen_panel_tk, mostrar_menu_principal, branding, nombre_negocio):
    """Muestro los datos legales guardados en db"""
    # Limpiar el frame principal
    for widget in frame_contenido.winfo_children():
        widget.destroy()

    # Frame principal
    frame = tk.Frame(frame_contenido, bg=branding["fondo"], width=600, height=800)
    frame.pack(fill=tk.BOTH, expand=True)
        
    # Imagen del Logo para el panel izquierdo
    # if imagen_panel_tk:
    #     label_imagen = tk.Label(frame_imagen_panel, image=imagen_panel_tk, bg=branding["fuente"])
    #     label_imagen.pack(side=tk.LEFT, padx=70)
    # else:
    #     label_texto = tk.Label(frame_imagen_panel, text="Ikigai", font=("Arial", 10), bg=branding["fuente"])
    #     label_texto.pack(side=tk.LEFT, padx=30)
    
    # Frame para los controles
    control_frame = tk.Frame(frame, bg=branding["fondo"], padx=20, pady=10)
    control_frame.pack(fill=tk.BOTH, expand=True)
        
    frame_titulo = tk.Frame(control_frame, bg=branding["fondo"])
    frame_titulo.pack(side=tk.TOP, fill=tk.X, pady=15)
    
    # Frame central para centrar el contenido
    center_frame = tk.Frame(control_frame, bg=branding["fondo"])
    center_frame.pack(expand=True)
    
    # Título
    title_label = tk.Label(
        frame_titulo,
        text="Datos Legales ",
        font=("Arial", 16, "bold"),
        bg=branding["fondo"],
        fg=branding["fuente"]
        )
    title_label.pack(pady=15)
    
    firma = db_conect.firmas_registradas()
    
    if firma is None:
        messagebox.showinfo("Información", "No hay datos todavía")
        return
    
    # Modo de negocio: fabricante (como está ahora) o vendedor (solo reventa)
    tk.Label(center_frame, text="Seleciona la Firma:", bg=branding["fondo"]).grid(row=0, column=0, sticky="e", pady=5)
    firmas_combobox = ttk.Combobox(center_frame, values=[firmas[0] for firmas in firma], state="readonly", width=28)
    firmas_combobox.grid(row=0, column=1, pady=5)
    
    print(firmas_combobox['values'])
    firma_seleccion = ""
    
    def obtener_firma(event):
        global firma_seleccion
        firma_seleccion = firmas_combobox.get()
        print(firma_seleccion, "Es la firma seleccionada")
            
        print(f"La firma que se ha seleccionado es {firma_seleccion}")
    
        if firma_seleccion:
            datos = db_conect.datos_tienda(firma_seleccion)
            print(f"Los datos que llegan desde db son {datos} y {firma_seleccion}")
            if datos:
                # Campos para gestionar usuarios
                tk.Label(center_frame, text="Nombre:", bg=branding["fondo"]).grid(row=1, column=0, sticky="e", pady=5)
                tk.Label(center_frame, text=datos[0][0], bg=branding["fondo"]).grid(row=1, column=1, sticky="e", pady=5)
                tk.Label(center_frame, text="Dirección:", bg=branding["fondo"]).grid(row=2, column=0, sticky="e", pady=5)
                tk.Label(center_frame, text=datos[0][1], bg=branding["fondo"]).grid(row=2, column=1, sticky="e", pady=5)
                tk.Label(center_frame, text="Id Fiscal:", bg=branding["fondo"]).grid(row=3, column=0, sticky="e", pady=5)
                tk.Label(center_frame, text=datos[0][2], bg=branding["fondo"]).grid(row=3, column=1, sticky="e", pady=5)
                tk.Label(center_frame, text="Telefono:", bg=branding["fondo"]).grid(row=4, column=0, sticky="e", pady=5)
                tk.Label(center_frame, text=datos[0][3], bg=branding["fondo"]).grid(row=4, column=1, sticky="e", pady=5)
                tk.Label(center_frame, text="Email:", bg=branding["fondo"]).grid(row=5, column=0, sticky="e", pady=5)
                tk.Label(center_frame, text=datos[0][4], bg=branding["fondo"]).grid(row=5, column=1, sticky="e", pady=5)
                
                # Botón para agregar usuario
                crear_boton(center_frame, 
                        texto="Salir", 
                        ancho=30,
                        alto=30,
                        color_fondo="#8e98f5",                
                        color_texto="white",
                        font=("Arial", 11, "bold"),
                        #bd=0,
                        #relief=tk.FLAT,
                        hover_color="#2ECC71",
                        #activeforeground="black",
                        comando=lambda: mostrar_menu_principal(), 
                        ).grid(row=6, column=0, columnspan=2, pady=10)
            else:
                #messagebox.showerror("ERROR", "Ha ocurrido un error")
                print(f"No se pudo cargar datos de la firma {firma_seleccion}")
        else:
            print(f"Fallo la seleccion de la firma {firma_seleccion}")
    
    firmas_combobox.bind("<<ComboboxSelected>>", obtener_firma)
        

def actualizar_tienda(frame_contenido, mostrar_menu_principal, branding, nombre_negocio):
    
    lista_actualización = []
    # Limpiar el frame principal
    for widget in frame_contenido.winfo_children():
        widget.destroy()

    # Frame principal
    frame = tk.Frame(frame_contenido, bg=branding["fondo"], width=600, height=800)
    frame.pack(fill=tk.BOTH, expand=True)
    
    # Frame para los controles
    control_frame = tk.Frame(frame, bg=branding["fondo"], padx=20, pady=10)
    control_frame.pack(fill=tk.BOTH, expand=True)
        
    frame_titulo = tk.Frame(control_frame, bg=branding["fondo"])
    frame_titulo.pack(side=tk.TOP, fill=tk.X, pady=15)
    
    # Frame central para centrar el contenido
    center_frame = tk.Frame(control_frame, bg=branding["fondo"])
    center_frame.pack(expand=True)
    
    # Título
    title_label = tk.Label(
        frame_titulo,
        text="Actualiza los datos de la Tienda ",
        font=("Arial", 16, "bold"),
        bg=branding["fondo"],
        fg=branding["fuente"]
        )
    title_label.pack(pady=15)
    
    # Campos para gestionar usuarios
    tk.Label(center_frame, text=" Actualizar Dirección:", bg=branding["fondo"]).grid(row=0, column=0, sticky="e", pady=5)
    actualiza_direccion_entry = tk.Entry(center_frame, width=30)
    actualiza_direccion_entry.grid(row=0, column=1, pady=5)

    tk.Label(center_frame, text="Actualizar Telefono:", bg=branding["fondo"]).grid(row=1, column=0, sticky="e", pady=5)
    actualiza_telefono_entry = tk.Entry(center_frame, width=30)
    actualiza_telefono_entry.grid(row=1, column=1, pady=5)

    tk.Label(center_frame, text="Actualizar Email:", bg=branding["fondo"]).grid(row=2, column=0, sticky="e", pady=5)
    actualiza_correo_entry = tk.Entry(center_frame, width=30)
    actualiza_correo_entry.grid(row=2, column=1, pady=5)
    
    # Modo de negocio: fabricante (como está ahora) o vendedor (solo reventa)
    tk.Label(center_frame, text="Modo de negocio:", bg=branding["fondo"]).grid(row=3, column=0, sticky="e", pady=5)
    modo_negocio_combobox = ttk.Combobox(center_frame, values=["fabricante", "vendedor"], state="readonly", width=28)
    modo_negocio_combobox.grid(row=3, column=1, pady=5)
    
    modo_actual = db_conect.obtener_modo_negocio()
    modo_negocio_combobox.set(modo_actual)
    
    def limpiar_pantalla():
        # Limpiar campos.
        actualiza_direccion_entry.delete(0, tk.END)
        actualiza_telefono_entry.delete(0, tk.END)
        actualiza_correo_entry.delete(0, tk.END)
    
    # Función para agregar un nuevo usuario
    def actualiza_tienda_db():
        
        direccion_actualizar = actualiza_direccion_entry.get()
        telefono_actualizar = actualiza_telefono_entry.get()
        correo_actualizar = actualiza_correo_entry.get()
        modo_actualizar = modo_negocio_combobox.get()
        
        tienda_id =  db_conect.id_tienda(correo_actualizar)
        
        # Recuperación de datos (dirección, telefono, email)
        datos_actuales = db_conect.datos_registrados_tienda(tienda_id)
        #print(datos_actuales)

        if datos_actuales:
            # Obtener la primera tupla de la lista
            datos = datos_actuales[0]
            id_tienda = datos[0]

            # Actualizar solo los campos que no están vacíos
            direccion = datos[2] if not direccion_actualizar else direccion_actualizar
            telefono = datos[4] if not telefono_actualizar else telefono_actualizar
            email = datos[5] if not correo_actualizar else correo_actualizar
            modo = datos[6] if not modo_actualizar else modo_actualizar

            # Llamar a la función para actualizar los datos en la base de datos 
            actualizado = db_conect.actualizar_datos_tienda(direccion, telefono, email, id_tienda)
            #modo_tabajo = db_conect.guardar_modo_negocio(modo_actualizar)
            if actualizado:
                messagebox.showinfo("✅ Éxito", "Datos actualizados correctamente.")
                limpiar_pantalla()
                mostrar_menu_principal()
            else:
                messagebox.showerror("⚠️ Error", "No se han podido actualizar los datos.")
        else:
            messagebox.showerror("⚠️ Error", "No se encontraron datos para actualizar.")

    # Botón para agregar usuario
    crear_boton(center_frame, 
            texto="Actualizar Datos", 
            ancho=30,
            alto=30,
            color_fondo="#8e98f5",                
            color_texto="white",
            font=("Arial", 11, "bold"),
            #bd=0,
            #relief=tk.FLAT,
            hover_color="#2ECC71",
            #activeforeground="black",
            comando=actualiza_tienda_db, 
            ).grid(row=4, column=0, columnspan=2, pady=10)
