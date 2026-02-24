# modulo_menus.py

import tkinter as tk
from tkinter import messagebox
from inventario import ingresar_inventario
#from productos import crear_producto
from busqueda import busqueda_articulos #menu_buscar_articulo, formulario_buscar_por_proveedor, formulario_buscar_por_factura, formulario_buscar_por_codigo, formulario_buscar_por_articulo
from registrar_nuevo_proveedor import nuevo_proveedor
from incrementar_productos_inventario import VentanaIncrementarStock
from recursos import crear_boton
from productManager import ProductoManager
from inventarioManager import InventarioManager

# menus.py
def menu_gestion_inventario(root, mostrar_menu_principal, imagen_panel_tk, rol, imagen_tk, usuario):
    crear_producto = ProductoManager(root, imagen_panel_tk, mostrar_menu_principal)
    inventario_manager = InventarioManager(root, imagen_panel_tk, mostrar_menu_principal)
    
    def usuario_actual_main(usuario):
        """Obtiene el usuario actual y su ID."""
        nombre_usuario_creador = usuario
        print(f"EL USUARIO EN LA CLASE PRODUCTO ES: {usuario}")
        if nombre_usuario_creador:
            crear_producto.usuario_actual(nombre_usuario_creador)
    
    usuario_actual_main(usuario)
    
    # Limpiar el frame de cualquier contenido
    for widget in root.winfo_children():
        widget.destroy()

    # Crear frame_contenido (para formularios)
    frame_contenido = tk.Frame(root, bg="#a0b9f0", width=600, height=800)
    frame_contenido.pack(expand=True, fill=tk.BOTH, side=tk.RIGHT)
    
    # Frame para el título
    frame_titulo = tk.Frame(frame_contenido, bg="#a0b9f0")
    frame_titulo.pack(side=tk.TOP, fill=tk.X, pady=15)
    
    # Frame para los botones (lado izquierdo)
    frame_botones = tk.Frame(root, bg="#2C3E50", width=200, height=800)
    frame_botones.pack(side=tk.LEFT, fill=tk.Y)
    frame_botones.pack_propagate(False)        
    
    frame_imagen = tk.Frame(frame_contenido, bg="#a0b9f0")
    frame_imagen.pack(expand=True)
        
    if imagen_tk:
        tk.Label(frame_imagen, image=imagen_tk, bg="#a0b9f0").pack(pady=20)
    else:
        tk.Label(frame_imagen, text="Ikigai Designs", font=("Arial", 24), bg="#a0b9f0").pack(pady=20)
    
    # Botones del submenú nivel administrador.
    if rol == "administrador":
        
        # Título
        title_label = tk.Label(
            frame_titulo,
            text="Gestión de Inventario, Productos y Proveedores",
            font=("Arial", 16, "bold"),
            bg="#a0b9f0",
            fg="#2C3E50"
            )
        title_label.pack(pady=15)
        
        # Agregar metodos de eliminación y creacion de usuarios
        #tk.Label(frame_contenido, text="GESTIÓN DE INVENTARIO", bg="#a0b9f0", font=("Arial", 14)).pack(pady=10)
        crear_boton(
            frame_botones,
            texto="Ingresar a Inventario",
            ancho=160,
            alto=30,
            color_fondo="#B1AE04",                
            color_texto="white",
            font=("Arial", 11, "bold"),
            #bd=0,
            #relief=tk.FLAT,
            hover_color="#2ECC71",
            #activeforeground="black",
            comando=lambda: inventario_manager.iniciar_interfaz(),
        
        ).pack(pady=15)
        crear_boton(
            frame_botones,
            texto="Crear Producto",
            ancho=160,
            alto=30,
            color_fondo="#EB11CE",                
            color_texto="white",
            font=("Arial", 11, "bold"),
            #bd=0,
            #relief=tk.FLAT,
            hover_color="#2ECC71",
            #activeforeground="black",
            comando=lambda: crear_producto.crear_producto()#(root, imagen_panel_tk, lambda: menu_gestion_inventario(root, mostrar_menu_principal, imagen_panel_tk, rol, imagen_tk)),
        
        ).pack(pady=15)
        crear_boton(
            frame_botones,
            texto="Registrar Proveedor",
            ancho=160,
            alto=30,
            color_fondo="#714BE0",                
            color_texto="white",
            font=("Arial", 11, "bold"),
            #bd=0,
            #relief=tk.FLAT,
            hover_color="#2ECC71",
            #activeforeground="black",
            comando=lambda: nuevo_proveedor(root, imagen_panel_tk, lambda: menu_gestion_inventario(root, mostrar_menu_principal, imagen_panel_tk, rol, imagen_tk, usuario)),
            
        ).pack(pady=15)
        crear_boton(
            frame_botones,
            texto="Aumentar stock",
            ancho=160,
            alto=30,
            color_fondo="#0474A0",                
            color_texto="white",
            font=("Arial", 11, "bold"),
            #bd=0,
            #relief=tk.FLAT,
            hover_color="#2ECC71",
            #activeforeground="black",
            comando=lambda: VentanaIncrementarStock(root, imagen_panel_tk, lambda: menu_gestion_inventario(root, mostrar_menu_principal, imagen_panel_tk, rol, imagen_tk, usuario)),
            
        ).pack(pady=15)
        crear_boton(
            frame_botones,
            texto="Menú Principal",
            ancho=140,
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
    
    # Botones del submenú nivel usuario.  PENDIENTE PARA CAMBIOS
    elif rol == "usuario":
        
        # Título
        title_label = tk.Label(
            frame_titulo,
            text="Gestión de Inventario, Productos y Proveedores",
            font=("Arial", 16, "bold"),
            bg="#a0b9f0",
            fg="#2C3E50"
            )
        title_label.pack(pady=15)
        
        #tk.Label(frame_contenido, text="GESTIÓN DE INVENTARIO", bg="#a0b9f0", font=("Arial", 14)).pack(pady=10)
        crear_boton(
            frame_botones,
            texto="Ingresar a Inventario",
            ancho=160,
            alto=30,
            color_fondo="#B1AE04",                
            color_texto="white",
            font=("Arial", 11, "bold"),
            #bd=0,
            #relief=tk.FLAT,
            hover_color="#2ECC71",
            #activeforeground="black",
            comando=lambda: inventario_manager.iniciar_interfaz(),            
        ).pack(pady=15)
        
        crear_boton(
            frame_botones,
            texto="Crear Producto",
            ancho=160,
            alto=30,
            color_fondo="#EB11CE",                
            color_texto="white",
            font=("Arial", 11, "bold"),
            #bd=0,
            #relief=tk.FLAT,
            hover_color="#2ECC71",
            #activeforeground="black",
            comando=lambda: crear_producto.crear_producto()        
        ).pack(pady=15)
        
        crear_boton(
            frame_botones,
            texto="Registrar Proveedor",
            ancho=160,
            alto=30,
            color_fondo="#714BE0",                
            color_texto="white",
            font=("Arial", 11, "bold"),
            #bd=0,
            #relief=tk.FLAT,
            hover_color="#2ECC71",
            #activeforeground="black",
            comando=lambda: nuevo_proveedor(root, imagen_panel_tk, lambda: menu_gestion_inventario(root, mostrar_menu_principal, imagen_panel_tk, rol, imagen_tk, usuario)),
            
        ).pack(pady=15)
        
        crear_boton(
            frame_botones,
            texto="Menú Principal",
            ancho=140,
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
            