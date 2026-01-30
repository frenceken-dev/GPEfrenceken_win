# registrar_nuevo_proveedor.py

from db import insertar_proveedor, obtener_id_proveedor_por_nombre
from menus import ingresar_inventario
import tkinter as tk
from tkinter import messagebox

def nuevo_proveedor(frame_contenido, volver_menu):
    # Limpiar ventana
    for widget in frame_contenido.winfo_children():
        widget.destroy()
            
    # Formulario para agregar materiales
    form_frame = tk.Frame(frame_contenido, bg="#a0b9f0", padx=20, pady=20)
    form_frame.place(relx=0.5, rely=0.1, anchor=tk.N)
    
    frame_titulo = tk.Frame(frame_contenido, bg="#a0b9f0")
    frame_titulo.pack(side=tk.TOP, fill=tk.X, pady=15)
    
    # Título
    title_label = tk.Label(
        frame_titulo,
        text="Registrar Nuevo Proveedor",
        font=("Arial", 16, "bold"),
        bg="#a0b9f0",
        fg="#2C3E50"
    )
    title_label.pack(pady=15)

    # Campos para materiales
    tk.Label(form_frame, text="Nombre Proveedor:", bg="#a0b9f0").grid(row=0, column=0, sticky="e")
    nombre_entry = tk.Entry(form_frame, width=30)
    nombre_entry.grid(row=0, column=1, pady=5)

    tk.Label(form_frame, text="Contacto web:", bg="#a0b9f0").grid(row=1, column=0, sticky="e")
    contacto_entry = tk.Entry(form_frame, width=30)
    contacto_entry.grid(row=1, column=1, pady=5)

    tk.Label(form_frame, text="Telefono:", bg="#a0b9f0").grid(row=2, column=0, sticky="e")
    telefono_entry = tk.Entry(form_frame, width=30)
    telefono_entry.grid(row=2, column=1, pady=5)

    tk.Label(form_frame, text="Email:", bg="#a0b9f0").grid(row=3, column=0, sticky="e")
    email_entry = tk.Entry(form_frame, width=30)
    email_entry.grid(row=3, column=1, pady=5)
    
    tk.Label(form_frame, text="Dirección:", bg="#a0b9f0").grid(row=3, column=0, sticky="e")
    direccion_entry = tk.Entry(form_frame, width=30)
    direccion_entry.grid(row=3, column=1, pady=5)

    def guardar_y_comprobar():
        # 1. Primero, inserta el proveedor
        insertar_proveedor(
            nombre_entry.get(),
            contacto_entry.get(),
            telefono_entry.get(),
            email_entry.get(),
            direccion_entry.get(),
        )
        # 2. Luego, comprueba si se guardó
        comprobacion_registro(nombre_entry.get(), frame_contenido, volver_menu)

    # Botón modificado para usar la función intermedia
    tk.Button(
        form_frame,
        text="Guardar Proveedor",
        command=lambda: guardar_y_comprobar(),  # Aquí llamas a la función intermedia
        bg="#4283fa"
    ).grid(row=4, column=0, columnspan=2, pady=10)
    

def comprobacion_registro(nombre, frame_contenido, volver_menu):
    # Realizar la comprobacion el base de datos
    proveedor = obtener_id_proveedor_por_nombre(nombre)
    if proveedor is not None:
        messagebox.showinfo("Guardado", "El proveedor se guardo correctamente.")
        ingresar_inventario(frame_contenido, volver_menu)
    else:
        messagebox.showinfo("Error", "El proveedor no se guardo...Error")
        ingresar_inventario(frame_contenido, volver_menu)
    