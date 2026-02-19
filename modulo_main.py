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
from db import obtener_nombres_usuarios, verificar_stock_bajo
from gestion_usuarios import gestion_usuarios, actualizar_clave
from costos_ganancias import abrir_modulo_costos_ganancias
from crea_factura_nota_entrega import VentanaVentas
from eliminar_datos import eliminar_datos
from info_tienda import info_tienda
from recursos import LOGO_PATH, IMAGEN_BUSQUEDA_PATH, crear_boton, configurar_toplevel, redimensionar_imagen
from alerta_stock import VentanaConfigurarUmbrales
#from productos import usuario_actual
from databasemanager import DataBaseManager


db_connect = DataBaseManager()
class PantallaPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Inventario")
        
        # Configuración de ventana
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = int(screen_width * 1)
        window_height = int(screen_height * 1)
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.configure(bg="#a0b9f0")
        self.root.bind("<Escape>", lambda e: self.root.geometry("800x600"))
        self.root.bind("<F1>", lambda e: self.root.geometry(f"{window_width}x{window_height}+{x}+{y}"))

        # Cargar imágenes base
        self.imagen_tk_login = redimensionar_imagen(LOGO_PATH, 250, 250)
        self.imagen_tk = redimensionar_imagen(LOGO_PATH, 300, 300)
        self.imagen_panel_tk = redimensionar_imagen(LOGO_PATH, 60, 60)
        self.imagen_buscar_tk = redimensionar_imagen(IMAGEN_BUSQUEDA_PATH, 200, 200)

        # Mostrar pantalla de login
        self.pantalla_login()
        
        # Vincular ajuste dinámico de imágenes
        #self.root.bind("<Configure>", self.ajustar_imagenes)

    def ajustar_imagenes(self, event=None):
        """Ajusta dinámicamente las imágenes sin reconstruir la interfaz."""
        try:
            ancho = self.root.winfo_width()
            alto = self.root.winfo_height()
            nuevo_ancho = int(ancho * 0.25)
            nuevo_alto = int(alto * 0.25)
            self.imagen_tk_login = redimensionar_imagen(LOGO_PATH, nuevo_ancho, nuevo_alto)
        except Exception as e:
            print(f"⚠️ Error al ajustar imágenes: {e}")


    def pantalla_login(self):
        """Pantalla de inicio de sesión."""

        for widget in self.root.winfo_children():
            widget.destroy()

        control_frame = tk.Frame(self.root, bg="#a0b9f0", padx=20, pady=50)
        control_frame.pack(fill=tk.BOTH, expand=True)

        if self.imagen_tk_login:
            tk.Label(control_frame, image=self.imagen_tk_login, bg="#a0b9f0").pack(pady=2)
        else:
            tk.Label(control_frame, text="Ikigai Designs", font=("Arial", 24), bg="#a0b9f0").pack(pady=5)

        login_frame = tk.Frame(self.root, bg="#a0b9f0", padx=20, pady=60)
        login_frame.place(relx=0.5, rely=0.55, anchor=tk.CENTER)

        tk.Label(login_frame, text="Nombre de Usuario:", bg="#a0b9f0").grid(row=0, column=0, sticky="w", pady=5)
        usuarios = obtener_nombres_usuarios()
        usuario_combobox = ttk.Combobox(login_frame, values=usuarios, width=20)
        usuario_combobox.grid(row=0, column=1, pady=5)

        tk.Label(login_frame, text="Contraseña:", bg="#a0b9f0").grid(row=1, column=0, sticky="w", pady=5)
        contrasena_entry = tk.Entry(login_frame, width=22, show="*")
        contrasena_entry.grid(row=1, column=1, pady=5)
        
        def recupera_clave():
            self.usuario = usuario_combobox.get()
            
            pregunta, mensaje = db_connect.recuperar_pregunta_seguridad(self.usuario)
            if pregunta is False:
                messagebox.showinfo("Información", mensaje)
                return 
            
            clave_olvidada = tk.Toplevel(login_frame)
            configurar_toplevel(clave_olvidada,
                                titulo="Recuperar Clave",
                                ancho_min=350,
                                alto_min=200,
                                color_fondo="#101113")
            
            frame_clave_olvidada = tk.Frame(clave_olvidada, bg="#101113", padx=10, pady=10)
            frame_clave_olvidada.pack()
            
            preguntar = tk.Label(frame_clave_olvidada, text=pregunta, bg="#101113", fg="#ffffff", padx=5, pady=5)
            preguntar.grid(row=0, column=0, padx=5, pady=10)
            
            tk.Label(frame_clave_olvidada, text="Ingresa tu respuesta:", bg="#101113", fg="#ffffff").grid(row=1, column=0, padx=5, pady=10)
            respuesta_entry = tk.Entry(frame_clave_olvidada, width=22)
            respuesta_entry.grid(row=2, column=0, padx=5, pady=5)
            
            def mediador(frame, usuario, respuesta):
                respuesta_seguridad, mensaje = db_connect.recuperar_clave(usuario, respuesta)
                
                if respuesta_seguridad:
                    for widget in frame.winfo_children():
                        widget.destroy()
                    actualizar_clave(frame_clave_olvidada, usuario)
                else:
                    messagebox.showerror("⚠️ Erro", mensaje)
                    
            crear_boton(frame_clave_olvidada, 
                    texto="Enviar respuesta",
                    ancho=20,
                    alto=30,
                    color_fondo="#4B82F0",                
                    color_texto="white",
                    font=("Arial", 11, "bold"),
                    #bd=0,
                    #relief=tk.FLAT,
                    hover_color="#2ECC71",
                    #activeforeground="black",
                    comando=lambda : mediador(frame_clave_olvidada, self.usuario, respuesta_entry.get()),
                    ).grid(row=3, column=0, columnspan=2, pady=10, sticky="")
            
            
        def validar_login():
            try:
                self.usuario = usuario_combobox.get()
                self.contraseña = contrasena_entry.get()
                es_valido, self.rol, mensaje = db_connect.validar_clave(self.usuario, self.contraseña)
                print(f"El ROL es: {self.rol}")
                # Enviar el usuario actual a producto para guardar borrador de creación de producto
                
            except tk.TclError:
                print("⚠️ El combobox ya no existe. No se puede leer el usuario.")
                return
            if es_valido:
                print(f"{mensaje}")
                self.mostrar_menu_principal()
            else:
                messagebox.showerror("⚠️ Error", "Nombre de usuario o contraseña incorrectos.")
            
        crear_boton(login_frame, 
                    texto="Iniciar Sesión",
                    ancho=30,
                    alto=30,
                    color_fondo="#4B82F0",                
                    color_texto="white",
                    font=("Arial", 11, "bold"),
                    #bd=0,
                    #relief=tk.FLAT,
                    hover_color="#2ECC71",
                    #activeforeground="black",
                    comando=validar_login,
                    ).grid(row=2, column=0, columnspan=2, pady=10, sticky="")
        
        crear_boton(login_frame, 
                    texto="Olvide mi contraseña",
                    ancho=20,
                    alto=20,
                    color_fondo="#a0b9f0",                
                    color_texto="#666363",
                    font=("Arial", 9, "bold"),
                    #bd=0,
                    #relief=tk.FLAT,
                    hover_color="#101113",
                    #activeforeground="black",
                    comando=recupera_clave,
                    ).grid(row=3, column=0, columnspan=2, pady=10, sticky="")
        
        
        self.root.bind("<Return>", lambda event: validar_login())

        
    # Alertas de Stock
    def mostrar_alertas_stock_bajo(self):
        alertas = verificar_stock_bajo()
        if not alertas:
            messagebox.showinfo("Información", "No hay advertencias de stock bajo.")
            return

        # Crear un Toplevel para mostrar las alertas
        toplevel = tk.Toplevel(self.root)
        # Configurar el Toplevel (título, tamaño mínimo, centrado, etc.)
        configurar_toplevel(
            toplevel,
            titulo="Advertencia de stock bajo ⚠️",
            ancho_min=600,
            alto_min=600
        )

        # Frame para el contenido del Toplevel
        frame_contenido = tk.Frame(toplevel, bg="#a0b9f0", padx=20, pady=20)
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
        frame_alertas = tk.Frame(frame_contenido, bg="#a0b9f0")
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
                    fg="#101113",
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
                    fg="#101113",
                    justify=tk.LEFT,
                    pady=5
                )
                alerta_label.pack(fill=tk.X, padx=10, pady=5)

        # Botón para cerrar el Toplevel
        crear_boton(
            frame_contenido,
            texto="Cerrar",
            color_fondo="#FF5733",
            fg="white",
            font=("Arial", 10, "bold"),
            #bd=0,
            #relief=tk.FLAT,
            hover_color="#FB9773",
            comando=toplevel.destroy,
        ).pack(pady=10)
            
    
    def salir_programa(self):
        db_connect.close()
        self.root.quit()
        
        
    def on_closing(self):
        if messagebox.askokcancel("Salir", "¿Deseas salir del programa?"):
            self.salir_programa()  # Reutilizar la función salir_programa
            
            
    def mostrar_menu_principal(self):
        self.root.unbind("<Return>")

        # Limpiar ventana
        for widget in self.root.winfo_children():
            widget.destroy()
        # Verificar bajo stock de Materiales y Productos  
        alertas = verificar_stock_bajo()
        
        # Se modifica el título con el usuario y su rol
        self.root.title(f"Sistema de Inventario - usuario: {self.usuario}-{self.rol}")
        
        # Frame para los botones (lado izquierdo)
        frame_botones = tk.Frame(self.root, bg="#2C3E50", width=200, height=800, bd=3, borderwidth=3, relief="solid")
        frame_botones.pack(side=tk.LEFT, fill=tk.Y)
        frame_botones.pack_propagate(False)
        
        # Frame del Titulo
        frame_titulo = tk.Frame(root, bg="#a0b9f0")
        frame_titulo.pack(side=tk.TOP, fill=tk.X, pady=15)
        
        # Botón de advertencia de stock bajo (solo si hay alertas)
        if alertas:
            crear_boton(
                self.root,
                texto="⚠️ Advertencia de Stock",
                color_texto="#0D0C0C",
                ancho=190,
                alto=30,
                color_fondo="#FF5733",  # Color llamativo para advertencia
                fg="white",
                font=("Arial", 11, "bold"),
                #bd=0,
                #relief=tk.FLAT,
                hover_color="#FF8C61",
                #activeforeground="white",
                comando=self.mostrar_alertas_stock_bajo,
        
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
            crear_boton(
                frame_botones,
                texto="Gestión de Inventario",
                ancho=30,
                alto=30,
                color_fondo="#EE7605",
                color_texto="white",
                font=("Arial", 11, "bold"),
                hover_color="#2ECC71",
                #activeforeground="white",
                comando=lambda: menu_gestion_inventario(self.root, self.mostrar_menu_principal, self.imagen_panel_tk, self.rol, self.imagen_tk, self.usuario),
            ).pack(pady=10)
            crear_boton(
                frame_botones,
                texto="Ventas",
                ancho=30,
                alto=30,
                color_fondo="#DBD944",                
                color_texto="white",
                font=("Arial", 11, "bold"),
                #bd=0,
                #relief=tk.FLAT,
                hover_color="#2ECC71",
                #activeforeground="black",
                comando=lambda: VentanaVentas(self.root, self.usuario, self.mostrar_menu_principal),
            ).pack(pady=10)
            crear_boton(
                frame_botones,
                texto="Costos y Ganancias",
                ancho=30,
                alto=30, 
                color_fondo="#0FA2CF",
                color_texto="white",
                font=("Arial", 11, "bold"),
                #bd=0,
                #relief=tk.FLAT,
                hover_color="#2ECC71",
                #activeforeground="white",
                comando=lambda: abrir_modulo_costos_ganancias(self.root, self.mostrar_menu_principal, self.imagen_panel_tk, self.rol, self.imagen_tk),
            ).pack(pady=10)
            crear_boton(
                frame_botones,
                texto="Buscar Artículo", 
                ancho=30,
                alto=30,
                color_fondo="#F0B34B",                
                color_texto="white",
                font=("Arial", 11, "bold"),
                #bd=0,
                #relief=tk.FLAT,
                hover_color="#2ECC71",
                #activeforeground="black",
                comando=lambda: busqueda_articulos(self.root, self.mostrar_menu_principal, self.imagen_panel_tk, self.imagen_buscar_tk, self.rol),
                
            ).pack(pady=10)
            crear_boton(
                frame_botones,
                texto="Salir", 
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
                comando=self.on_closing
                
            ).pack(pady=100)
        
        if self.rol == "administrador":
            # Crear usuario.
            crear_boton(
                frame_botones,
                texto="Crear un usuario", 
                ancho=30,
                alto=30,
                color_fondo="#2E8418",                
                color_texto="white",
                font=("Arial", 11, "bold"),
                #bd=0,
                #relief=tk.FLAT,
                hover_color="#2ECC71",
                #activeforeground="black",
                #bg=0,
                comando=lambda: gestion_usuarios(self.root, self.mostrar_menu_principal, self.imagen_panel_tk),
                
            ).pack(pady=10)
            # Agregar la información de la tienda.
            crear_boton(
                frame_botones,
                texto="Tu Tienda", 
                ancho=30,
                alto=30,
                color_fondo="#00285C",                
                color_texto="white",
                font=("Arial", 11, "bold"),
                #bd=0,
                #relief=tk.FLAT,
                hover_color="#2ECC71",
                #activeforeground="black",
                #bg=0,
                comando=lambda: info_tienda(self.root, self.mostrar_menu_principal, self.imagen_tk, self.imagen_panel_tk),
                
            ).pack(pady=10)
            
            crear_boton(
                frame_botones,
                texto="Crear alertar de Stock", 
                ancho=30,
                alto=30,
                color_fondo="#FF0A68",
                font=("Arial", 11, "bold"),
                #bd=0,
                #relief=tk.FLAT,
                hover_color="#2ECC71",
                #activeforeground="black",
                #bg=0,
                comando=lambda: VentanaConfigurarUmbrales(self.root, self.mostrar_menu_principal),
                
            ).pack(pady=10)
            
            # Eliminar datos
            crear_boton(
                frame_botones,
                texto="Eliminar dato", 
                ancho=30,
                alto=30,
                color_fondo="#FA2E2E",                
                color_texto="white",
                font=("Arial", 11, "bold"),
                #bd=0,
                #relief=tk.FLAT,
                hover_color="#2ECC71",
                #activeforeground="black",
                #bg=0,
                comando=lambda: eliminar_datos(self.root, self.mostrar_menu_principal, self.imagen_tk, self.imagen_panel_tk),
            
            ).pack(pady=10)

        frame_imagen = tk.Frame(self.root, bg="#a0b9f0")
        frame_imagen.pack(expand=True)
        
        if self.imagen_tk:
            tk.Label(frame_imagen, image=self.imagen_tk, bg="#a0b9f0").pack(pady=20)
        else:
            tk.Label(frame_imagen, text="Ikigai Designs", font=("Arial", 24), bg="#a0b9f0").pack(pady=20)
        
        # Asociar la función on_closing al evento de cierre de la ventana
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
# Inicializador de la App.
if __name__ == "__main__":
    root = tk.Tk()
    app = PantallaPrincipal(root)
    root.mainloop()


# # -*- mode: python ; coding: utf-8 -*-
# import sys
# import os
# from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# # Detectar si se ejecuta en macOS
# is_mac = sys.platform == "darwin"

# # Rutas de recursos (asegura inclusión de imágenes y base de datos)
# datas = [
#     ('ikigai_inventario.db', '.'),
#     ('Img/busqueda/*', 'Img/busqueda'),
#     ('Img/logo/*', 'Img/logo'),
# ]

# # Incluir datos adicionales de Pillow (PIL)
# datas += collect_data_files('PIL', include_py_files=True)

# # Incluir todos los submódulos de tkinter y PIL
# hiddenimports = collect_submodules('tkinter') + collect_submodules('PIL')

# a = Analysis(
#     ['modulo_main.py'],
#     pathex=['.'],
#     binaries=[],
#     datas=datas,
#     hiddenimports=hiddenimports + [
#         'sqlite3',
#         'ctypes',
#         'multiprocessing',
#         'queue',
#         'os',
#         'shutil',
#         'datetime',
#         'time',
#         'pickle',
#         'json',
#         'csv',
#     ],
#     hookspath=[],
#     hooksconfig={},
#     runtime_hooks=[],
#     excludes=[],
#     noarchive=False,
#     optimize=0,
# )

# pyz = PYZ(a.pure)

# # Define el icono según el sistema operativo
# icon_path = os.path.abspath('iniciar.icns' if is_mac else 'iniciar.ico')

# exe = EXE(
#     pyz,
#     a.scripts,
#     a.binaries,
#     a.datas,
#     [],
#     name='Gestion_frenceken',
#     debug=False,
#     bootloader_ignore_signals=False,
#     strip=False,
#     upx=False,
#     upx_exclude=[],
#     runtime_tmpdir=None,
#     console=False,
#     icon=icon_path,
#     osx_bundle=True,
#     bundle_identifier='com.frenceken.gestion',
#     )
    