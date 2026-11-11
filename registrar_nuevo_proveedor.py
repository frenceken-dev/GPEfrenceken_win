# registrar_nuevo_proveedor.py

#from db import obtener_id_proveedor_por_nombre
#from menus import ingresar_inventario
import tkinter as tk
from tkinter import messagebox
from recursos import crear_boton, crear_encabezado
from databasemanager import DataBaseManager
from inventarioManager import InventarioManager


db_connect = DataBaseManager()
def nuevo_proveedor(root, branding, nombre_negocio_actual, volver_menu, modo_negocio):
    # Limpiar ventana
    for widget in root.winfo_children():
        widget.destroy()

    # Frame principal
    frame = tk.Frame(root, bg=branding["fondo"], width=800, height=600)
    frame.pack(fill=tk.BOTH, expand=True)

    # Panel izquierdo
    frame_menu = tk.Frame(frame, bg=branding["menu"], width=200, height=900, bd=3, relief="solid")
    frame_menu.pack(side=tk.LEFT, fill=tk.Y)
    frame_menu.pack_propagate(False)
        
    frame_imagen_panel = tk.Frame(frame_menu, bg=branding["menu"], height=70)
    frame_imagen_panel.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

    # Imagen del Logo para el panel izquierdo
    crear_encabezado(frame_imagen_panel, branding, nombre_negocio_actual,
                                    tamano=70, fuente=("Arial", 12, "bold"))
    # if imagen_panel_tk: 
    #     label_imagen = tk.Label(frame_imagen_panel, image=imagen_panel_tk, bg="#2C3E50")
    #     label_imagen.pack(side=tk.LEFT, padx=70)
    # else:
    #     label_texto = tk.Label(frame_imagen_panel, text="Ikigai", font=("Arial", 10), bg="#2C3E50")
    #     label_texto.pack(side=tk.LEFT, padx=70)

    # Frame inferior dentro del menú lateral
    frame_inferior = tk.Frame(frame_menu, bg=branding["menu"])
    frame_inferior.pack(side="bottom", fill="x", pady=20)  # <- este pady sí separa del borde inferior
    
    # Formulario para agregar materiales
    form_frame = tk.Frame(frame, bg=branding["fondo"], padx=20, pady=20)
    form_frame.place(relx=0.5, rely=0.1, anchor=tk.N)
    
    frame_titulo = tk.Frame(frame, bg=branding["fondo"])
    frame_titulo.pack(side=tk.TOP, fill=tk.X, pady=15)
    
    # Título
    title_label = tk.Label(
        frame_titulo,
        text="Registrar Nuevo Proveedor",
        font=("Arial", 16, "bold"),
        bg=branding["fondo"], #"#a0b9f0",
        fg=branding["fuente"]  #"#2C3E50"
    )
    title_label.pack(pady=30)

    # Botón para volver
    back_button = crear_boton(
        frame_inferior,
        texto="Volver menú",
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

    # Campos para materiales
    tk.Label(form_frame, text="Nombre Proveedor:", bg=branding["fondo"]).grid(row=0, column=0, sticky="e")
    nombre_entry = tk.Entry(form_frame, width=30)
    nombre_entry.grid(row=0, column=1, pady=15)

    tk.Label(form_frame, text="Contacto web:", bg=branding["fondo"]).grid(row=1, column=0, sticky="e")
    contacto_entry = tk.Entry(form_frame, width=30)
    contacto_entry.grid(row=1, column=1, pady=15)

    tk.Label(form_frame, text="Telefono:", bg=branding["fondo"]).grid(row=2, column=0, sticky="e")
    telefono_entry = tk.Entry(form_frame, width=30)
    telefono_entry.grid(row=2, column=1, pady=15)

    tk.Label(form_frame, text="Email:", bg=branding["fondo"]).grid(row=3, column=0, sticky="e")
    email_entry = tk.Entry(form_frame, width=30)
    email_entry.grid(row=3, column=1, pady=15)
    
    tk.Label(form_frame, text="Dirección:", bg=branding["fondo"]).grid(row=3, column=0, sticky="e")
    direccion_entry = tk.Entry(form_frame, width=30)
    direccion_entry.grid(row=3, column=1, pady=15)

    def guardar_y_comprobar():
        # 1. Primero, inserta el proveedor
        id_nuevo_proveedor = db_connect.insertar_proveedor(
            nombre_entry.get(),
            contacto_entry.get(),
            telefono_entry.get(),
            email_entry.get(),
            direccion_entry.get(),
        )
        #print(f"El ID del nuevo Proveedor es: {id_nuevo_proveedor}")
        # 2. Luego, comprueba si se guardó
        comprobacion_registro(nombre_entry.get(), frame, volver_menu, root, branding, nombre_negocio_actual, modo_negocio)

    # Botón modificado para usar la función intermedia
    crear_boton(
        form_frame,
        texto="Guardar Proveedor",
        ancho=30,
        alto=30,
        color_fondo="#1B8420",                
        color_texto="white",
        font=("Arial", 11, "bold"),
        #bd=0,
        #relief=tk.FLAT,
        hover_color="#2ECC71",
        #activeforeground="black",
        comando=lambda: guardar_y_comprobar(),  # Aquí llamas a la función intermedia
    
    ).grid(row=4, column=0, columnspan=2, pady=10)
    

def comprobacion_registro(nombre, frame_contenido, volver_menu, root, branding, nombre_negocio_actual, modo_negocio):
    inventario_manager = InventarioManager(root, branding, nombre_negocio_actual, volver_menu, modo_negocio)
    
    # Realizar la comprobacion el base de datos
    proveedor = db_connect.obtener_id_proveedor_por_nombre(nombre)
    if proveedor is not None:
        messagebox.showinfo("Guardado", "El proveedor se guardo correctamente.")
        #inventario_manager.iniciar_interfaz()
        volver_menu()
    else:
        messagebox.showinfo("⚠️ Error", "El proveedor no se guardo...Error")
        #inventario_manager.iniciar_interfaz()
        return
    