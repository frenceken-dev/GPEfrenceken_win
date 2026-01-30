# info_tienda.py

import tkinter as tk
from tkinter import ttk, messagebox
from db import guardar_info_tienda, actualizar_datos_tienda, datos_registrados_tienda
from recursos import crear_boton


def info_tienda(root, mostrar_menu_principal, imagen_tk, imagen_panel_tk):
    # Limpiar el frame de cualquier contenido
    for widget in root.winfo_children():
        widget.destroy()
        
    # Crear frame_contenido (para formularios)
    frame_contenido = tk.Frame(root, bg="#a0b9f0", width=600, height=800)
    frame_contenido.pack(expand=True, fill=tk.BOTH, side=tk.RIGHT)
    
    # Frame para el título
    frame_titulo = tk.Frame(frame_contenido, bg="#a0b9f0")
    frame_titulo.pack(side=tk.TOP, fill=tk.X, pady=15)
    
    frame_imagen = tk.Frame(frame_contenido, bg="#a0b9f0")
    frame_imagen.pack(expand=True)
        
    if imagen_tk:
        tk.Label(frame_imagen, image=imagen_tk, bg="#a0b9f0").pack(pady=20)
    else:
        tk.Label(frame_imagen, text="Ikigai Designs", font=("Arial", 24), bg="#a0b9f0").pack(pady=20)
            
    # Frame para los botones (lado izquierdo)
    frame_botones = tk.Frame(root, bg="#2C3E50", width=200, height=800)
    frame_botones.pack(side=tk.LEFT, fill=tk.Y)
    frame_botones.pack_propagate(False)
    
    frame_imagen_panel = tk.Frame(frame_botones, bg="#2C3E50", height=70)
    frame_imagen_panel.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
    
    # Título
    title_label = tk.Label(
        frame_titulo,
        text="Agrega los datos de tu negocio o actualizalos",
        font=("Arial", 16, "bold"),
        bg="#a0b9f0",
        fg="#2C3E50"
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
        comando=lambda: ingresar_datos_tienda(frame_contenido, frame_imagen_panel, imagen_panel_tk, mostrar_menu_principal),
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
        comando=lambda: actualizar_tienda(frame_contenido, mostrar_menu_principal),
        
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
        
        
def ingresar_datos_tienda(frame_contenido, frame_imagen_panel, imagen_panel_tk, mostrar_menu_principal):
    # Limpiar el frame principal
    for widget in frame_contenido.winfo_children():
        widget.destroy()

    # Frame principal
    frame = tk.Frame(frame_contenido, bg="#a0b9f0", width=600, height=800)
    frame.pack(fill=tk.BOTH, expand=True)
        
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
        
    frame_titulo = tk.Frame(control_frame, bg="#a0b9f0")
    frame_titulo.pack(side=tk.TOP, fill=tk.X, pady=15)
    
    # Frame central para centrar el contenido
    center_frame = tk.Frame(control_frame, bg="#a0b9f0")
    center_frame.pack(expand=True)
    
    # Título
    title_label = tk.Label(
        frame_titulo,
        text="Ingresa los datos de la Tienda ",
        font=("Arial", 16, "bold"),
        bg="#a0b9f0",
        fg="#2C3E50"
        )
    title_label.pack(pady=15)
    
    # Campos para gestionar usuarios
    tk.Label(center_frame, text="Nombre de la Tienda:", bg="#a0b9f0").grid(row=0, column=0, sticky="e", pady=5)
    nombre_tienda_entry = tk.Entry(center_frame, width=30)
    nombre_tienda_entry.grid(row=0, column=1, pady=5)

    tk.Label(center_frame, text="Dirección:", bg="#a0b9f0").grid(row=1, column=0, sticky="e", pady=5)
    direccion_entry = tk.Entry(center_frame, width=30)
    direccion_entry.grid(row=1, column=1, pady=5)

    tk.Label(center_frame, text="ID Fiscal:", bg="#a0b9f0").grid(row=2, column=0, sticky="e", pady=5)
    id_fiscal_entry = tk.Entry(center_frame, width=30)
    id_fiscal_entry.grid(row=2, column=1, pady=5)
    
    tk.Label(center_frame, text="Telefono:", bg="#a0b9f0").grid(row=3, column=0, sticky="e", pady=5)
    telefono_entry = tk.Entry(center_frame, width=30)
    telefono_entry.grid(row=3, column=1, pady=5)
    
    tk.Label(center_frame, text="Email:", bg="#a0b9f0").grid(row=4, column=0, sticky="e", pady=5)
    correo_entry = tk.Entry(center_frame, width=30)
    correo_entry.grid(row=4, column=1, pady=5)

    # Función para agregar un nuevo usuario
    def agregar_tienda_db():
        tienda = nombre_tienda_entry.get()
        direccion = direccion_entry.get()
        id_fiscal = id_fiscal_entry.get()
        telefono = telefono_entry.get()
        correo = correo_entry.get()

        if tienda and direccion and id_fiscal and telefono and correo:
            guardar_info_tienda(tienda, direccion, id_fiscal, telefono, correo)
            messagebox.showinfo("Éxito", "Usuario agregado correctamente.")
            mostrar_menu_principal()
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")

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
            ).grid(row=5, column=0, columnspan=2, pady=10)


def actualizar_tienda(frame_contenido, mostrar_menu_principal):
    lista_actualización = []
    # Limpiar el frame principal
    for widget in frame_contenido.winfo_children():
        widget.destroy()

    # Frame principal
    frame = tk.Frame(frame_contenido, bg="#a0b9f0", width=600, height=800)
    frame.pack(fill=tk.BOTH, expand=True)
    
    # Frame para los controles
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
        text="Actualiza los datos de la Tienda ",
        font=("Arial", 16, "bold"),
        bg="#a0b9f0",
        fg="#2C3E50"
        )
    title_label.pack(pady=15)
    
    # Campos para gestionar usuarios
    tk.Label(center_frame, text=" Actualizar Dirección:", bg="#a0b9f0").grid(row=0, column=0, sticky="e", pady=5)
    actualiza_direccion_entry = tk.Entry(center_frame, width=30)
    actualiza_direccion_entry.grid(row=0, column=1, pady=5)

    tk.Label(center_frame, text="Actualizar Telefono:", bg="#a0b9f0").grid(row=1, column=0, sticky="e", pady=5)
    actualiza_telefono_entry = tk.Entry(center_frame, width=30)
    actualiza_telefono_entry.grid(row=1, column=1, pady=5)

    tk.Label(center_frame, text="Actualizar Email:", bg="#a0b9f0").grid(row=2, column=0, sticky="e", pady=5)
    actualiza_correo_entry = tk.Entry(center_frame, width=30)
    actualiza_correo_entry.grid(row=2, column=1, pady=5)
    
    # Función para agregar un nuevo usuario
    def actualiza_tienda_db():
        direccion_actualizar = actualiza_direccion_entry.get()
        telefono_actualizar = actualiza_telefono_entry.get()
        correo_actualizar = actualiza_correo_entry.get()

        # Recuperación de datos (dirección, telefono, email)
        datos_actuales = datos_registrados_tienda()
        print(datos_actuales)

        if datos_actuales:
            # Obtener la primera tupla de la lista
            datos = datos_actuales[0]
            id_tienda = datos[0]

            # Actualizar solo los campos que no están vacíos
            direccion = datos[1] if not direccion_actualizar else direccion_actualizar
            telefono = datos[2] if not telefono_actualizar else telefono_actualizar
            email = datos[3] if not correo_actualizar else correo_actualizar

            # Llamar a la función para actualizar los datos en la base de datos
            actualizar_datos_tienda(direccion, telefono, email, id_tienda)

            messagebox.showinfo("Éxito", "Datos actualizados correctamente.")
            mostrar_menu_principal()
        else:
            messagebox.showerror("Error", "No se encontraron datos para actualizar.")

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
            ).grid(row=3, column=0, columnspan=2, pady=10)
