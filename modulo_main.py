# Proyecto Para Firma Ikigai
# Modulo-main
# Modulo Número: 1
# Pantalla Inicial
import sys
import os
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
from menus import menu_gestion_inventario
from busqueda import busqueda_articulos
from db import validar_credenciales, obtener_nombres_usuarios, verificar_stock_bajo
from gestion_usuarios import gestion_usuarios
from costos_ganancias import abrir_modulo_costos_ganancias
from crea_factura_nota_entrega import VentanaVentas
from eliminar_datos import eliminar_datos
from info_tienda import info_tienda
from recursos import LOGO_PATH, IMAGEN_BUSQUEDA_PATH
from alerta_stock import VentanaConfigurarUmbrales


class PantallaPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Inventario  ")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = 800
        window_height = 600
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{screen_width}x{screen_height}+{x}+{y}")
        self.root.configure(bg="#a0b9f0")
    
        # Cargar logo
        try:
            self.logo_path = LOGO_PATH
            self.imagen = Image.open(self.logo_path)
            self.imagen_resize = self.imagen.resize((300, 300), Image.LANCZOS)
            self.imagen_tk = ImageTk.PhotoImage(self.imagen_resize)
        except Exception as e:
            print(f"Error al cargar la imagen: {e}")
            self.imagen_tk = tk.Label(self.root, text="Ikigai Designs", font=("Arial", 24), bg="#f0f0f0").pack(pady=20)
            
        # Cargar logo para redimencionar a 50px
        try:
            self.imagen_panel = Image.open(self.logo_path)
            self.imagen_panel_resize = self.imagen_panel.resize((60, 60), Image.LANCZOS)
            self.imagen_panel_tk = ImageTk.PhotoImage(self.imagen_panel_resize)
        except Exception as e:
            print(f"Error al cargar la imagen: {e}")
            self.imagen_panel_tk = tk.Label(self.root, text="Ikigai Designs", font=("Arial", 24), bg="#f0f0f0").pack(pady=20)
            
        # Cargar imagen de busqueda a 200px
        try:
            self.img_busqueda = IMAGEN_BUSQUEDA_PATH
            self.imagen_buscar = Image.open(self.img_busqueda)
            self.imagen_buscar_resize = self.imagen_buscar.resize((200, 200), Image.LANCZOS)
            self.imagen_buscar_tk = ImageTk.PhotoImage(self.imagen_buscar_resize)
        except Exception as e:
            print(f"Error al cargar la imagen: {e}")
            
        # Se llama a la pantalla de login
        self.pantalla_login()
        
                
    # Pantal para el inicio de sesión
    def pantalla_login(self):
        # Limpiar pantalla
        for widget in self.root.winfo_children():
            widget.destroy()
            
        try:
            # Redimensión de la Imagen de la pantalla login
            self.imagen = Image.open(self.logo_path)
            ancho_original, alto_original = self.imagen.size
            proporcion = min(300 / ancho_original, 300 / alto_original)
            nuevo_ancho = int(ancho_original * proporcion)
            nuevo_alto = int(alto_original * proporcion)
            self.imagen_resize = self.imagen.resize((nuevo_ancho, nuevo_alto), Image.LANCZOS)
            self.imagen_tk_login = ImageTk.PhotoImage(self.imagen_resize)
        except Exception as e:
            print(f"Error al cargar la imagen: {e}")
            self.imagen_tk = tk.Label(self.root, text="Ikigai Designs", font=("Arial", 24), bg="#f0f0f0").pack(pady=20)
                
        control_frame = tk.Frame(self.root, bg="#a0b9f0", padx=20, pady=50)
        control_frame.pack(fill=tk.BOTH, expand=True)
            
        frame_titulo = tk.Frame(control_frame, bg="#a0b9f0")
        frame_titulo.pack(side=tk.TOP, fill=tk.X)
        
        # Título
        if self.imagen_tk:
            tk.Label(control_frame, image=self.imagen_tk_login, bg="#a0b9f0").pack(pady=2)
        else:
            tk.Label(control_frame, text="Ikigai Designs", font=("Arial", 24), bg="#a0b9f0").pack(pady=5)
                
        # Crear un frame para el login
        login_frame = tk.Frame(self.root, bg="#a0b9f0", padx=20, pady=60)
        login_frame.place(relx=0.5, rely=0.55, anchor=tk.CENTER)

        # # Campos para el login
        tk.Label(login_frame, text="Nombre de Usuario:", bg="#a0b9f0").grid(row=0, column=0, sticky="e", pady=5)
        # usuario_entry = tk.Entry(login_frame, width=30)
        # usuario_entry.grid(row=0, column=1, pady=5)
        
        usuarios = obtener_nombres_usuarios()

        usuario_combobox = ttk.Combobox(login_frame, values=usuarios, width=30)
        usuario_combobox.grid(row=0, column=1, pady=5)

        tk.Label(login_frame, text="Contraseña:", bg="#a0b9f0").grid(row=1, column=0, sticky="e", pady=5)
        contrasena_entry = tk.Entry(login_frame, width=30, show="*")
        contrasena_entry.grid(row=1, column=1, pady=5)

        # Función para validar el login
        def validar_login():
            self.usuario = usuario_combobox.get()
            self.contraseña = contrasena_entry.get()

            # Se guarda el valor true y el rol
            self.verificado, self.rol = validar_credenciales(self.usuario, self.contraseña)
            
            # Si existe abre el menu.
            if self.verificado is True:
                self.mostrar_menu_principal()
                print(f"El usuario es: {self.usuario}\nEl Rol es: {self.rol}")
            else:
                messagebox.showerror("Error", "Nombre de usuario o contraseña incorrectos.")

        # Botón para iniciar sesión
        tk.Button(login_frame, text="Iniciar Sesión", command=validar_login, bg="#8e98f5").grid(row=2, column=0, columnspan=2, pady=10)  
        
        # Vincular tecla Enter con el bóton Iniciar Sesión
        self.root.bind("<Return>", lambda event: validar_login())
        
    # Alertas de Stock
    def mostrar_alertas_stock_bajo(self):
        alertas = verificar_stock_bajo()
        if not alertas:
            messagebox.showinfo("Información", "No hay advertencias de stock bajo.")
            return

        # Crear un Toplevel para mostrar las alertas
        toplevel = tk.Toplevel(self.root)
        toplevel.title("Advertencias de Stock Bajo")
        toplevel.geometry("500x400")
        toplevel.resizable(False, False)

        # Frame para el contenido del Toplevel
        frame_contenido = tk.Frame(toplevel, bg="#f0f0f0", padx=20, pady=20)
        frame_contenido.pack(fill=tk.BOTH, expand=True)

        # Título
        title_label = tk.Label(
            frame_contenido,
            text="Advertencias de Stock Bajo",
            font=("Arial", 14, "bold"),
            bg="#f0f0f0",
            fg="#FF5733"
        )
        title_label.pack(pady=10)

        # Frame para las alertas
        frame_alertas = tk.Frame(frame_contenido, bg="#f0f0f0")
        frame_alertas.pack(fill=tk.BOTH, expand=True)

        # Scrollbar para las alertas
        canvas = tk.Canvas(frame_alertas, bg="#f0f0f0")
        scrollbar = tk.Scrollbar(frame_alertas, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#f0f0f0")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Mostrar las alertas en el frame scrollable
        for alerta in alertas:
            if alerta['tipo'] == 'material':
                alerta_label = tk.Label(
                    scrollable_frame,
                    text=(
                        f"Material: {alerta['nombre']}\n"
                        f"Tipo: {alerta['tipo_material']}\n"
                        f"Tamaño: {alerta['tamano']}\n"
                        f"Color: {alerta['color']}\n"
                        f"Cantidad: {alerta['cantidad']}\n"
                    ),
                    font=("Arial", 10),
                    bg="#f0f0f0",
                    fg="#333333",
                    justify=tk.LEFT,
                    pady=5
                )
                alerta_label.pack(fill=tk.X, padx=10, pady=5)

            elif alerta['tipo'] == 'producto':
                alerta_label = tk.Label(
                    scrollable_frame,
                    text=(
                        f"Producto: Código {alerta['codigo']}\n"
                        f"Tipo: {alerta['tipo_producto']}\n"
                        f"Cantidad: {alerta['cantidad']}\n"
                    ),
                    font=("Arial", 10),
                    bg="#f0f0f0",
                    fg="#333333",
                    justify=tk.LEFT,
                    pady=5
                )
                alerta_label.pack(fill=tk.X, padx=10, pady=5)

        # Botón para cerrar el Toplevel
        tk.Button(
            frame_contenido,
            text="Cerrar",
            bg="#FF5733",
            fg="white",
            font=("Arial", 10, "bold"),
            bd=0,
            relief=tk.FLAT,
            activebackground="#FF8C61",
            command=toplevel.destroy,
            width=10
        ).pack(pady=10)
            
     
    def mostrar_menu_principal(self):
        # Limpiar ventana
        for widget in self.root.winfo_children():
            widget.destroy()
        # Verificar bajo stock de Materiales y Productos  
        alertas = verificar_stock_bajo()
        
        # Se modifica el título con el usuario y su rol
        self.root.title(f" usuario: {self.usuario}-{self.rol}")
        
        # Frame para los botones (lado izquierdo)
        frame_botones = tk.Frame(self.root, bg="#2C3E50", width=200, height=800, bd=3, borderwidth=3, relief="solid")
        frame_botones.pack(side=tk.LEFT, fill=tk.Y)
        frame_botones.pack_propagate(False)
        
        # Frame del Titulo
        frame_titulo = tk.Frame(root, bg="#a0b9f0")
        frame_titulo.pack(side=tk.TOP, fill=tk.X, pady=15)
        
        # Botón de advertencia de stock bajo (solo si hay alertas)
        if alertas:
            tk.Button(
                self.root,
                text="⚠️ Advertencia de Stock",
                bg="#FF5733",  # Color llamativo para advertencia
                fg="white",
                font=("Arial", 11, "bold"),
                bd=0,
                relief=tk.FLAT,
                activebackground="#FF8C61",
                activeforeground="white",
                command=self.mostrar_alertas_stock_bajo,
                width=18, borderwidth=2
            ).pack(pady=10)
        
        # Título
        title_label = tk.Label(
            frame_titulo,
            text="Sistema para la Gestión de Negocios",
            font=("Arial", 16, "bold"),
            bg="#a0b9f0",
            fg="#2C3E50"
        )
        title_label.pack(pady=15)
        
        # Botones del menú principal
        #tk.Label(self.root, text=rol, font=("Arial", 14), bg="#a0b9f0").pack(pady=10)
        if self.rol == "administrador" or self.rol == "usuario":
            tk.Button(
                frame_botones,
                text="Gestión de Inventario",
                bg="#EE7605",
                fg="white",
                font=("Arial", 11, "bold"),
                bd=0,
                relief=tk.FLAT,
                activebackground="#2ECC71",
                activeforeground="white",
                command=lambda: menu_gestion_inventario(self.root, self.mostrar_menu_principal, self.imagen_panel_tk, self.rol, self.imagen_tk),
                width=18, borderwidth=2
            ).pack(pady=10)
            tk.Button(
                frame_botones,
                text="Ventas", 
                bg="#DBD944",                
                fg="white",
                font=("Arial", 11, "bold"),
                bd=0,
                relief=tk.FLAT,
                activebackground="#2ECC71",
                activeforeground="white",
                command=lambda: VentanaVentas(self.root, self.usuario, self.mostrar_menu_principal),
                width=18, borderwidth=2
            ).pack(pady=10)
            tk.Button(
                frame_botones,
                text="Costos y Ganancias", 
                bg="#0FA2CF",
                fg="white",
                font=("Arial", 11, "bold"),
                bd=0,
                relief=tk.FLAT,
                activebackground="#2ECC71",
                activeforeground="white",
                command=lambda: abrir_modulo_costos_ganancias(self.root, self.mostrar_menu_principal, self.imagen_panel_tk, self.rol, self.imagen_tk),
                width=18, borderwidth=2
            ).pack(pady=10)
            tk.Button(
                frame_botones,
                text="Buscar Artículo", 
                bg="#F7AF45",
                fg="white",
                font=("Arial", 11, "bold"),
                bd=0,
                relief=tk.FLAT,
                activebackground="#2ECC71",
                activeforeground="white",
                command=lambda: busqueda_articulos(self.root, self.mostrar_menu_principal, self.imagen_panel_tk, self.imagen_buscar_tk, self.usuario),
                width=18, borderwidth=2
            ).pack(pady=10)
            tk.Button(
                frame_botones,
                text="Salir", 
                bg="#913131",
                fg="white",
                font=("Arial", 11, "bold"),
                bd=0,
                relief=tk.FLAT,
                activebackground="#222423",
                activeforeground="white",
                command=self.root.quit,
                width=18, borderwidth=2
            ).pack(pady=100)
        
        if self.rol == "administrador":
            # Crear usuario.
            tk.Button(
                frame_botones,
                text="Crear un usuario", 
                bg="#75EC57",
                fg="white",
                font=("Arial", 11, "bold"),
                bd=0,
                relief=tk.FLAT,
                activebackground="#2ECC71",
                activeforeground="white",
                command=lambda: gestion_usuarios(self.root, self.mostrar_menu_principal, self.imagen_panel_tk),
                width=18, borderwidth=2
            ).pack(pady=10)
            # Agregar la información de la tienda.
            tk.Button(
                frame_botones,
                text="Tu Tienda", 
                bg="#00285C",
                fg="white",
                font=("Arial", 11, "bold"),
                bd=0,
                relief=tk.FLAT,
                activebackground="#2ECC71",
                activeforeground="white",
                command=lambda: info_tienda(self.root, self.mostrar_menu_principal, self.imagen_tk, self.imagen_panel_tk),
                width=18, borderwidth=2
            ).pack(pady=10)
            
            tk.Button(
                frame_botones,
                text="Crear alertar de Stock", 
                bg="#FF0A68",
                fg="white",
                font=("Arial", 11, "bold"),
                bd=0,
                relief=tk.FLAT,
                activebackground="#2ECC71",
                activeforeground="white",
                command=lambda: VentanaConfigurarUmbrales(self.root, self.mostrar_menu_principal),
                width=18, borderwidth=2
            ).pack(pady=10)
            
            # Eliminar datos
            tk.Button(
                frame_botones,
                text="Eliminar dato", 
                bg="#FA2E2E",
                fg="white",
                font=("Arial", 11, "bold"),
                bd=0,
                relief=tk.FLAT,
                activebackground="#2ECC71",
                activeforeground="white",
                command=lambda: eliminar_datos(self.root, self.mostrar_menu_principal, self.imagen_tk, self.imagen_panel_tk),
                width=18, borderwidth=2
            ).pack(pady=10)

        frame_imagen = tk.Frame(self.root, bg="#a0b9f0")
        frame_imagen.pack(expand=True)
        
        if self.imagen_tk:
            tk.Label(frame_imagen, image=self.imagen_tk, bg="#a0b9f0").pack(pady=20)
        else:
            tk.Label(frame_imagen, text="Ikigai Designs", font=("Arial", 24), bg="#a0b9f0").pack(pady=20)
        

# Inicializador de la App.
if __name__ == "__main__":
    root = tk.Tk()
    app = PantallaPrincipal(root)
    root.mainloop()