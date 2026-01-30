# eliminar_datos.py
import tkinter as tk
from tkinter import messagebox, ttk
from db import obtener_proveedores, eliminar_proveedor_bd, obtener_materiales, eliminar_material_bd, obtener_productos, eliminar_producto_bd
from db import obtener_nombres_usuarios, eliminar_usuario_bd_nombre
from PIL import Image, ImageTk


# Menu de selección para la eliminación
def eliminar_datos(root, volver_menu, imagen_tk, imagen_panel_tk):
# Limpiar el frame de cualquier contenido
    for widget in root.winfo_children():
        widget.destroy()         

    # Crear frame_contenido (para formularios)
    frame_contenido = tk.Frame(root, bg="#a0b9f0", width=600, height=800)
    frame_contenido.pack(expand=True, fill=tk.BOTH, side=tk.RIGHT)
    
    # Frame para los botones (lado izquierdo)
    frame_botones = tk.Frame(root, bg="#2C3E50", width=200, height=800)
    frame_botones.pack(side=tk.LEFT, fill=tk.Y)
    frame_botones.pack_propagate(False)
    
    # Frame para el título
    frame_titulo = tk.Frame(frame_contenido, bg="#a0b9f0")
    frame_titulo.pack(side=tk.TOP, fill=tk.X, pady=15)
    
    frame_imagen = tk.Frame(frame_contenido, bg="#a0b9f0")
    frame_imagen.pack(expand=True)
        
    if imagen_tk:
        tk.Label(frame_imagen, image=imagen_tk, bg="#a0b9f0").pack(pady=20)
    else:
        tk.Label(frame_imagen, text="Ikigai Designs", font=("Arial", 24), bg="#a0b9f0").pack(pady=20)
    
    # Título
    title_label = tk.Label(
        frame_titulo,
        text="Eliminar Datos",
        font=("Arial", 16, "bold"),
        bg="#a0b9f0",
        fg="#2C3E50"
    )
    title_label.pack(pady=15)
    
    # Eliminar Proveedores 
    tk.Button(frame_botones, 
            text="Eliminar Proveedor", 
            bg="#eb4747",
            fg="white",
            font=("Arial", 11, "bold"),
            bd=0,
            relief=tk.FLAT,
            activebackground="#2ECC71",
            activeforeground="white",
            command=lambda: eliminar_proveedor(root, volver_menu, imagen_tk, imagen_panel_tk),
            width=20,
            ).pack(pady=15)
    
    # Eliminar Materiales
    tk.Button(frame_botones, 
            text="Eliminar Material", 
            bg="#eb4747",
            fg="white",
            font=("Arial", 11, "bold"),
            bd=0,
            relief=tk.FLAT,
            activebackground="#2ECC71",
            activeforeground="white",
            command=lambda: eliminar_material(root, volver_menu, imagen_tk, imagen_panel_tk), 
            width=20
            ).pack(pady=15)
    
    # Eliminar Productos
    tk.Button(frame_botones, 
            text="Eliminar Producto",
            bg="#eb4747",
            fg="white",
            font=("Arial", 11, "bold"),
            bd=0,
            relief=tk.FLAT,
            activebackground="#2ECC71",
            activeforeground="white",
            command=lambda: eliminar_producto(root, volver_menu, imagen_tk, imagen_panel_tk), 
            width=20, 
            ).pack(pady=15)
    
    # Eliminar Usuarios del sistema.
    tk.Button(frame_botones, 
            text="Eliminar Usuario", 
            bg="#eb4747",
            fg="white",
            font=("Arial", 11, "bold"),
            bd=0,
            relief=tk.FLAT,
            activebackground="#2ECC71",
            activeforeground="white",
            command=lambda: eliminar_usuario(root, volver_menu, imagen_tk, imagen_panel_tk), 
            width=20
            ).pack(pady=15)
    
    # Regresar al menu aprincipal
    tk.Button(frame_botones, 
            text="Volver al Menú",
            bg="#913131",
            fg="white",
            font=("Arial", 11, "bold"),
            bd=0,
            relief=tk.FLAT,
            activebackground="#2ECC71",
            activeforeground="white",
            command=volver_menu, 
            width=20, 
            ).pack(side=tk.LEFT, padx=30, pady=40)
    
    
# Código para eliminar proveedores.
def eliminar_proveedor(root, volver_menu, imagen_tk, imagen_panel_tk):
    # Limpiar el frame principal
    for widget in root.winfo_children():
        widget.destroy()
    
    # Frame para los botones (lado izquierdo)
    frame_botones = tk.Frame(root, bg="#2C3E50", width=200, height=800)
    frame_botones.pack(side=tk.LEFT, fill=tk.Y)
    frame_botones.pack_propagate(False)

    # Crear un frame para eliminar proveedor
    eliminar_proveedor_frame = tk.Frame(root, bg="#a0b9f0", padx=20, pady=20)
    eliminar_proveedor_frame.place(relx=0.65, rely=0.5, anchor=tk.CENTER)
    
    frame_imagen_panel = tk.Frame(frame_botones, bg="#2C3E50", height=70)
    frame_imagen_panel.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
    
    if imagen_panel_tk:
        label_imagen = tk.Label(frame_imagen_panel, image=imagen_panel_tk, bg="#2C3E50")
        label_imagen.pack(side=tk.LEFT, padx=50)
    else:
        label_texto = tk.Label(frame_imagen_panel, text="Ikigai", font=("Arial", 10), bg="#2C3E50")
        label_texto.pack(side=tk.LEFT, padx=50)

    tk.Label(eliminar_proveedor_frame, text="Selecciona el proveedor a eliminar:", bg="#a0b9f0", font=("Arial", 12)).pack(pady=10)

    # Obtener los nombres de los proveedores
    proveedores = obtener_proveedores()

    proveedor_combobox = ttk.Combobox(eliminar_proveedor_frame, values=proveedores, width=30)
    proveedor_combobox.pack(pady=5)

    def confirmar_eliminar_proveedor():
        proveedor_seleccionado = proveedor_combobox.get()
        if not proveedor_seleccionado:
            messagebox.showerror("Error", "Debes seleccionar un proveedor.")
            return

        confirmar = messagebox.askyesno("Confirmar", f"¿Estás seguro de que deseas eliminar al proveedor {proveedor_seleccionado}?")
        if confirmar:
            eliminar_proveedor_bd(proveedor_seleccionado)
            messagebox.showinfo("Éxito", f"Proveedor {proveedor_seleccionado} eliminado correctamente.")
            volver_menu()

    tk.Button(eliminar_proveedor_frame, text="Eliminar", command=confirmar_eliminar_proveedor, width=20, bg="#8e98f5", fg="#E60F0F").pack(pady=5)
    tk.Button(frame_botones, text="Volver al Menú", command=lambda: eliminar_datos(root, volver_menu, imagen_tk, imagen_panel_tk), width=18, bg="#913131").pack(side=tk.LEFT, padx=30, pady=40)
   
    
# Código para eliminar Materiales.
def eliminar_material(root, volver_menu, imagen_tk, imagen_panel_tk):
    # Limpiar el frame principal
    for widget in root.winfo_children():
        widget.destroy()

    # Frame para los botones (lado izquierdo)
    frame_botones = tk.Frame(root, bg="#2C3E50", width=200, height=800)
    frame_botones.pack(side=tk.LEFT, fill=tk.Y)
    frame_botones.pack_propagate(False)
    
    # Crear un frame para eliminar material
    eliminar_material_frame = tk.Frame(root, bg="#a0b9f0", padx=20, pady=20)
    eliminar_material_frame.place(relx=0.65, rely=0.5, anchor=tk.CENTER)


    frame_imagen_panel = tk.Frame(frame_botones, bg="#2C3E50", height=70)
    frame_imagen_panel.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
    
    if imagen_panel_tk:
        label_imagen = tk.Label(frame_imagen_panel, image=imagen_panel_tk, bg="#2C3E50")
        label_imagen.pack(side=tk.LEFT, padx=50)
    else:
        label_texto = tk.Label(frame_imagen_panel, text="Ikigai", font=("Arial", 10), bg="#2C3E50")
        label_texto.pack(side=tk.LEFT, padx=50)
    
    
    tk.Label(eliminar_material_frame, text="Selecciona el material a eliminar:", bg="#a0b9f0", font=("Arial", 12)).pack(pady=10)

    # Obtener los nombres de los materiales
    materiales = obtener_materiales()
    nombres_materiales = [material[1:6] for material in materiales]  # quite [2]

    material_combobox = ttk.Combobox(eliminar_material_frame, values=nombres_materiales, width=30)
    material_combobox.pack(pady=5)

    def confirmar_eliminar_material():
        material_seleccionado = material_combobox.get()
        if not material_seleccionado:
            messagebox.showerror("Error", "Debes seleccionar un material.")
            return

        confirmar = messagebox.askyesno("Confirmar", f"¿Estás seguro de que deseas eliminar el material {material_seleccionado}?")
        if confirmar:
            eliminar_material_bd(material_seleccionado)
            messagebox.showinfo("Éxito", f"Material {material_seleccionado} eliminado correctamente.")
            volver_menu()

    tk.Button(eliminar_material_frame, text="Eliminar", command=confirmar_eliminar_material, width=20, bg="#8e98f5", fg="#E60F0F").pack(pady=5)
    tk.Button(frame_botones, text="Volver al Menú", command=lambda: eliminar_datos(root, volver_menu, imagen_tk, imagen_panel_tk), width=18, bg="#913131").pack(side=tk.LEFT, padx=30, pady=40)
    
    
# Código para eliminar Productos.
def eliminar_producto(root, volver_menu, imagen_tk, imagen_panel_tk):
    # Limpiar el frame principal
    for widget in root.winfo_children():
        widget.destroy()

    # Frame para los botones (lado izquierdo)
    frame_botones = tk.Frame(root, bg="#2C3E50", width=200, height=800)
    frame_botones.pack(side=tk.LEFT, fill=tk.Y)
    frame_botones.pack_propagate(False)

    # Crear un frame para eliminar producto
    eliminar_producto_frame = tk.Frame(root, bg="#a0b9f0", padx=20, pady=20)
    eliminar_producto_frame.place(relx=0.65, rely=0.5, anchor=tk.CENTER)
    
    
    frame_imagen_panel = tk.Frame(frame_botones, bg="#2C3E50", height=70)
    frame_imagen_panel.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
    
    if imagen_panel_tk:
        label_imagen = tk.Label(frame_imagen_panel, image=imagen_panel_tk, bg="#2C3E50")
        label_imagen.pack(side=tk.LEFT, padx=50)
    else:
        label_texto = tk.Label(frame_imagen_panel, text="Ikigai", font=("Arial", 10), bg="#2C3E50")
        label_texto.pack(side=tk.LEFT, padx=50)

    tk.Label(eliminar_producto_frame, text="Selecciona el producto a eliminar:", bg="#a0b9f0", font=("Arial", 12)).pack(pady=10)

    # Obtener los nombres de los productos
    productos = obtener_productos()
    nombres_productos = [producto[1] for producto in productos]

    producto_combobox = ttk.Combobox(eliminar_producto_frame, values=nombres_productos, width=30)
    producto_combobox.pack(pady=5)

    def confirmar_eliminar_producto():
        producto_seleccionado = producto_combobox.get()
        if not producto_seleccionado:
            messagebox.showerror("Error", "Debes seleccionar un producto.")
            return

        confirmar = messagebox.askyesno("Confirmar", f"¿Estás seguro de que deseas eliminar el producto {producto_seleccionado}?")
        if confirmar:
            eliminar_producto_bd(producto_seleccionado)
            messagebox.showinfo("Éxito", f"Producto {producto_seleccionado} eliminado correctamente.")
            volver_menu()

    tk.Button(eliminar_producto_frame, text="Eliminar", command=confirmar_eliminar_producto, width=20, bg="#8e98f5", fg="#E60F0F").pack(pady=5)
    tk.Button(frame_botones, text="Volver al Menú", command=lambda: eliminar_datos(root, volver_menu, imagen_tk, imagen_panel_tk), width=18, bg="#913131").pack(side=tk.LEFT, padx=30, pady=40)


# Código para eliminar usuarios del sistema.
def eliminar_usuario(root, volver_menu, imagen_tk, imagen_panel_tk):
    # Limpiar el frame principal
    for widget in root.winfo_children():
        widget.destroy()

    # Frame para los botones (lado izquierdo)
    frame_botones = tk.Frame(root, bg="#2C3E50", width=200, height=800)
    frame_botones.pack(side=tk.LEFT, fill=tk.Y)
    frame_botones.pack_propagate(False)
    
    # Crear un frame para eliminar usuario
    eliminar_usuario_frame = tk.Frame(root, bg="#a0b9f0", padx=20, pady=20)
    eliminar_usuario_frame.place(relx=0.65, rely=0.5, anchor=tk.CENTER)
    
    frame_imagen_panel = tk.Frame(frame_botones, bg="#2C3E50", height=70)
    frame_imagen_panel.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
    
    if imagen_panel_tk:
        label_imagen = tk.Label(frame_imagen_panel, image=imagen_panel_tk, bg="#2C3E50")
        label_imagen.pack(side=tk.LEFT, padx=50)
    else:
        label_texto = tk.Label(frame_imagen_panel, text="Ikigai", font=("Arial", 10), bg="#2C3E50")
        label_texto.pack(side=tk.LEFT, padx=50)

    tk.Label(eliminar_usuario_frame, text="Selecciona el usuario a eliminar:", bg="#a0b9f0", font=("Arial", 12)).pack(pady=10)

    # Obtener los nombres de los usuarios
    usuarios = obtener_nombres_usuarios()

    usuario_combobox = ttk.Combobox(eliminar_usuario_frame, values=usuarios, width=30)
    usuario_combobox.pack(pady=5)

    def confirmar_eliminar_usuario():
        usuario_seleccionado = usuario_combobox.get()
        if not usuario_seleccionado:
            messagebox.showerror("Error", "Debes seleccionar un usuario.")
            return

        confirmar = messagebox.askyesno("Confirmar", f"¿Estás seguro de que deseas eliminar al usuario {usuario_seleccionado}?")
        if confirmar:
            eliminar_usuario_bd_nombre(usuario_seleccionado)
            messagebox.showinfo("Éxito", f"Usuario {usuario_seleccionado} eliminado correctamente.")
            volver_menu()

    tk.Button(eliminar_usuario_frame, text="Eliminar", command=confirmar_eliminar_usuario, width=20, bg="#8e98f5", fg="#E60F0F").pack(pady=5)
    tk.Button(frame_botones, text="Volver al Menú", command=lambda: eliminar_datos(root, volver_menu, imagen_tk, imagen_panel_tk), width=18, bg="#913131").pack(side=tk.LEFT, padx=30, pady=40)
