# Proyecto Para Firma Ikigai
# Modulo-main
# Modulo Número: 1
# Pantalla Inicial
import sys
import os
import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
from PIL import Image, ImageTk
from menus import menu_gestion_inventario
from busqueda import busqueda_articulos
#from db import verificar_stock_bajo # obtener_nombres_usuarios, 
from gestion_usuarios import gestion_usuarios, actualizar_clave
#from costos_ganancias import abrir_modulo_costos_ganancias
from costos_ganancias import CostosGananciasApp
from crea_factura_nota_entrega import VentanaVentas
from eliminar_datos import eliminar_datos
from info_tienda import info_tienda
from recursos import (LOGO_PATH, 
                    IMAGEN_BUSQUEDA_PATH, 
                    crear_boton, 
                    configurar_toplevel, 
                    ruta_logo_negocio, 
                    redimensionar_imagen, 
                    DB_ACTUAL, 
                    DB_PATH, 
                    LOGO_ACTUAL,
                    crear_encabezado)
from alerta_stock import VentanaConfigurarUmbrales
#from productos import usuario_actual
from databasemanager import DataBaseManager
from perfilManager import perfilUsuario
from perfiles_negocio import cargar_perfiles, crear_perfil, eliminar_perfil


db_connect = DataBaseManager()

class PantallaPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Inventario y Ventas")
        
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
        #self.imagen_tk_login = redimensionar_imagen(self.branding["logo"], 250, 250)
        #self.imagen_tk = redimensionar_imagen(self.branding["logo"], 300, 300)
        #self.imagen_panel_tk = redimensionar_imagen(LOGO_PATH, 60, 60)
        #self.imagen_panel_tk = redimensionar_imagen(self.branding["logo"], 60, 60)  # original 110 110
        #self.imagen_buscar_tk = redimensionar_imagen(IMAGEN_BUSQUEDA_PATH, 200, 200)

        # Mostrar pantalla de login
        self.modo_negocio = None
        self.pantalla_seleccion_perfil()
        #self.pantalla_login()
        
        
        # Vincular ajuste dinámico de imágenes
        #self.root.bind("<Configure>", self.ajustar_imagenes)

    # def ajustar_imagenes(self, event=None):
    #     """Ajusta dinámicamente las imágenes sin reconstruir la interfaz."""
    #     try:
    #         ancho = self.root.winfo_width()
    #         alto = self.root.winfo_height()
    #         nuevo_ancho = int(ancho * 0.25)
    #         nuevo_alto = int(alto * 0.25)
    #         self.imagen_tk_login = redimensionar_imagen(LOGO_PATH, nuevo_ancho, nuevo_alto)
    #     except Exception as e:
    #         pass
            #print(f"⚠️ Error al ajustar imágenes: {e}")
    
    
    def pantalla_seleccion_perfil(self):
        """Pantalla inicial: elegir el negocio (perfil) con el que se trabajará."""

        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root, bg="#a0b9f0", padx=30, pady=40)
        frame.place(relx=0.50, rely=0.50, anchor="center", width=400)# pack(fill=tk.BOTH, expand=True)
        
        nombre_app = tk.Label(self.root, text="GPEfrenceken-App", bg="#a0b9f0", font=("Arial", 40, "bold"), fg="#2C3E50")
        nombre_app.place(relx=0.50, rely=0.25, anchor="center", width=500)

        # # Cargar imágenes base
        # self.imagen_tk_login = redimensionar_imagen(self.branding["logo"], 250, 250)
                
        # if self.imagen_tk_login:
        #     tk.Label(frame, image=self.imagen_tk_login, bg="#a0b9f0").pack(pady=5)
        # tk.Label(frame, text="¿Con qué negocio deseas trabajar?",
        #         font=("Arial", 16, "bold"), bg="#a0b9f0", fg="#2C3E50").pack(pady=15)

        perfiles = cargar_perfiles()
        
        # # --- DIAGNÓSTICO TEMPORAL ---
        # from recursos import PERFILES_PATH
        # print(f"Buscando perfiles en: {PERFILES_PATH}")
        # print(f"¿Existe el archivo?: {os.path.exists(PERFILES_PATH)}")
        # print(f"Perfiles cargados: {perfiles}")
        # # ---------------------------
        
        self.perfil_elegido = tk.StringVar()
        listado = [p["nombre"] for p in perfiles]

        tk.Label(frame, text="Selecciona tu Negocio:", bg="#a0b9f0", font=("Arial", 18, "bold"), fg="#2C3E50").pack(pady=5)
        combo_perfil = ttk.Combobox(frame, textvariable=self.perfil_elegido,
                                    values=listado, state="readonly", width=28, font=("Arial", 12))
        combo_perfil.pack(pady=5)
        if listado:
            combo_perfil.current(0)

        def continuar():
            for p in cargar_perfiles():
                if p["nombre"] == self.perfil_elegido.get():
                    DB_ACTUAL["ruta"] = p["db"]
                    # Asegurar que el nombre del negocio sea texto plano, no StringVar.
                    nombre_negocio_elegido = self.perfil_elegido.get() if hasattr(self.perfil_elegido, "get") else self.perfil_elegido
                    # Buscar la entrada completa en perfiles.json:
                    perfiles = cargar_perfiles()
                    perfil_actual = next(
                        (p for p in perfiles if p["nombre"] == nombre_negocio_elegido or p["db"] == nombre_negocio_elegido),
                        None
                    )

                    if perfil_actual:
                        self.nombre_negocio_actual = perfil_actual["nombre"]      # "FrencekenAutoParts
                        # --- Cargar branding del negocio --- 
                        LOGO_ACTUAL["ruta"] = ruta_logo_negocio(self.nombre_negocio_actual)  # puede ser None
                        
                    # # --- Cargar branding del negocio (Fase 7) ---
                    # LOGO_ACTUAL["ruta"] = ruta_logo_negocio(self.perfil_elegido)
                    
                    branding = db_connect.obtener_branding()
                    # --- Branding consolidado del negocio (Fase 7) ---
                    branding = db_connect.obtener_branding()
                    self.branding = {
                        "fondo":   branding["color_fondo"] or "#a0b9f0",
                        "menu":    branding["color_menu"]  or "#2C3E50",
                        "fuente":  branding["color_fuente"] or "#272525",
                        "logo":    LOGO_ACTUAL["ruta"],
                    }
                    break
            else:
                messagebox.showerror("⚠️ Error", "Selecciona un negocio o crea uno nuevo.")
                return
            db_connect.close()          # cerrar conexión previa si existía
            self.pantalla_login()

        def nuevo_negocio():
            nombre = simpledialog.askstring("Nuevo Negocio",
                "Nombre del negocio:", parent=self.root)
            if not nombre:
                return

            perfil = crear_perfil(nombre)
            DB_ACTUAL["ruta"] = perfil["db"]
            db_connect.close()

            # --- Formulario de inicialización: admin + modo de negocio ---
            from keygen_user import validar_clave_segura

            ventana_init = tk.Toplevel(self.root)
            configurar_toplevel(ventana_init, titulo=f"Inicializar: {perfil['nombre']}",
                            ancho_min=380, alto_min=420, color_fondo="#a0b9f0")
            form = tk.Frame(ventana_init, bg="#a0b9f0", padx=15, pady=10)
            form.pack(fill=tk.BOTH, expand=True)

            tk.Label(form, text="Usuario administrador:", bg="#a0b9f0").grid(row=0, column=0, sticky="e", pady=4)
            usuario_entry = tk.Entry(form, width=25)
            usuario_entry.grid(row=0, column=1, pady=4)

            tk.Label(form, text="Clave:", bg="#a0b9f0").grid(row=1, column=0, sticky="e", pady=4)
            clave_entry = tk.Entry(form, width=25, show="*")
            clave_entry.grid(row=1, column=1, pady=4)

            tk.Label(form, text="Confirmar clave:", bg="#a0b9f0").grid(row=2, column=0, sticky="e", pady=4)
            clave2_entry = tk.Entry(form, width=25, show="*")
            clave2_entry.grid(row=2, column=1, pady=4)

            tk.Label(form, text="Pregunta de seguridad:", bg="#a0b9f0").grid(row=3, column=0, sticky="e", pady=4)
            pregunta_entry = tk.Entry(form, width=25)
            pregunta_entry.grid(row=3, column=1, pady=4)

            tk.Label(form, text="Respuesta de seguridad:", bg="#a0b9f0").grid(row=4, column=0, sticky="e", pady=4)
            respuesta_entry = tk.Entry(form, width=25)
            respuesta_entry.grid(row=4, column=1, pady=4)

            tk.Label(form, text="Tipo de negocio:", bg="#a0b9f0").grid(row=5, column=0, sticky="e", pady=4)
            modo_var = tk.StringVar(value="fabricante")
            modo_combo = ttk.Combobox(form, textvariable=modo_var,
                                    values=["fabricante", "vendedor"],
                                    state="readonly", width=23)
            modo_combo.grid(row=5, column=1, pady=4)

            def registrar():
                usuario = usuario_entry.get().strip()
                clave = clave_entry.get()
                clave2 = clave2_entry.get()

                if not usuario or not clave:
                    messagebox.showerror("⚠️ Error", "Usuario y clave son obligatorios.", parent=ventana_init)
                    return
                if clave != clave2:
                    messagebox.showerror("⚠️ Error", "Las claves no coinciden.", parent=ventana_init)
                    return

                clave_valida, mensaje_clave = validar_clave_segura(clave)
                if not clave_valida:
                    return  # validar_clave_segura ya muestra el error detallado

                exito, mensaje = db_connect.inicializar_negocio(
                    perfil["nombre"],
                    modo_var.get(),
                    usuario, clave,
                    pregunta_entry.get().strip(),
                    respuesta_entry.get().strip().lower()
                )
                if exito:
                    messagebox.showinfo("✅ Éxito", mensaje, parent=ventana_init)
                    ventana_init.destroy()
                    self.pantalla_login()
                else:
                    messagebox.showerror("⚠️ Error", mensaje, parent=ventana_init)

            crear_boton(form, texto="Crear Administrador", ancho=25, alto=30,
                        color_fondo="#1B8420", color_texto="white",
                        font=("Arial", 11, "bold"), hover_color="#2ECC71",
                        comando=registrar).grid(row=6, column=0, columnspan=2, pady=15)

        def eliminar_negocio():
            nombre = self.perfil_elegido.get()
            if not nombre:
                messagebox.showerror("⚠️ Error", "Selecciona un negocio de la lista.")
                return

            # Doble confirmación: es una acción destructiva (aunque reversible)
            confirmar = messagebox.askyesno(
                "Eliminar Negocio",
                f"¿Eliminar el negocio '{nombre}'?\n\n"
                "Ya no aparecerá en la lista y no podrá usarse desde el programa."
            )
            if not confirmar:
                return
            confirmar2 = messagebox.askyesno(
                "Confirmar una vez más",
                f"¿Estás TOTALMENTE seguro de eliminar '{nombre}'?\n\n"
                "La base de datos NO se destruye: quedará en 'db/descartados/' "
                "y podría restaurarse manualmente si te arrepientes."
            )
            if not confirmar2:
                return

            # Si la BD activa apunta a ese negocio, cerrar la conexión antes de mover el archivo
            from recursos import DB_ACTUAL
            for p in cargar_perfiles():
                if p["nombre"] == nombre and DB_ACTUAL["ruta"] == p["db"]:
                    db_connect.close()
                    break

            exito, mensaje = eliminar_perfil(nombre)   # a_papelera=True por defecto
            if exito:
                messagebox.showinfo("✅ Eliminado", mensaje)
            else:
                messagebox.showerror("⚠️ Error", mensaje)

            # Recargar la pantalla para refrescar el combobox
            self.pantalla_seleccion_perfil()
            
        tk.Button(frame, text="Continuar", font=("Arial", 12, "bold"),
                bg="#4B82F0", fg="white", command=continuar).pack(pady=15, ipadx=20)
        tk.Button(frame, text="Crear nuevo negocio", font=("Arial", 11),
                bg="#1B8420", fg="white", command=nuevo_negocio).pack(pady=5, ipadx=10)
        tk.Button(frame, text="Eliminar negocio", font=("Arial", 11),
                bg="#913131", fg="white", command=eliminar_negocio).pack(pady=10, ipadx=10)
        crear_boton(
                frame,
                texto="Salir del programa", 
                ancho=20,
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
                
            ).pack(pady=50)


    def pantalla_login(self):
        """Pantalla de inicio de sesión."""

        for widget in self.root.winfo_children():
            widget.destroy()

        control_frame = tk.Frame(self.root, bg="#a0b9f0", padx=20, pady=50)
        control_frame.pack(fill=tk.BOTH, expand=True)

        # Cargar imágenes base
        # self.imagen_tk_login = redimensionar_imagen(self.branding["logo"], 250, 250)
        
        # if self.imagen_tk_login:
        #     tk.Label(control_frame, image=self.imagen_tk_login, bg="#a0b9f0").pack(pady=2)
        # else:
        #     tk.Label(control_frame, text="Ikigai Designs", font=("Arial", 24), bg="#a0b9f0").pack(pady=5)
        crear_encabezado(control_frame, self.branding, self.nombre_negocio_actual,
                tamano=250, fuente=("Arial", 24, "bold"))

        login_frame = tk.Frame(self.root, bg="#a0b9f0", padx=20, pady=60)
        login_frame.place(relx=0.5, rely=0.55, anchor=tk.CENTER)

        tk.Label(login_frame, text="Nombre de Usuario:", bg="#a0b9f0").grid(row=0, column=0, sticky="w", pady=5)
        self.usuarios = db_connect.obtener_nombres_usuarios()
        usuario_combobox = ttk.Combobox(login_frame, values=self.usuarios, width=20)
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
                    actualizar_clave(frame_clave_olvidada, usuario, self.branding["fuente"])
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
            es_valido = None
            try:
                self.usuario = usuario_combobox.get()
                self.contraseña = contrasena_entry.get()
                
                if self.usuario in self.usuarios:
                    es_valido, self.rol, mensaje = db_connect.validar_clave(self.usuario, self.contraseña)
                
            except tk.TclError:
                #print("⚠️ El combobox ya no existe. No se puede leer el usuario.")
                return
            
            if es_valido:
                #print(f"{mensaje}")
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
                    relieve="raised",
                    border_width=3,
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
                    relieve="raised",
                    #bd=0,
                    border_width=3,
                    hover_color="#101113",
                    #activeforeground="black",
                    comando=recupera_clave,
                    ).grid(row=3, column=0, columnspan=2, pady=10, sticky="")
        
        
        self.root.bind("<Return>", lambda event: validar_login())

        
    # Alertas de Stock
    def mostrar_alertas_stock_bajo(self):
        alertas = db_connect.verificar_stock_bajo()
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
        frame_contenido = tk.Frame(toplevel, bg=self.branding["fondo"], padx=20, pady=20)
        frame_contenido.pack(fill=tk.BOTH, expand=True)

        # Título
        title_label = tk.Label(
            frame_contenido,
            text="Stock Bajo",
            font=("Arial", 14, "bold"),
            bg="#FF5733",
            fg="#ff0000"
        )
        title_label.pack(pady=10)

        # Frame para las alertas
        frame_alertas = tk.Frame(frame_contenido, bg="#a0b9f0")
        frame_alertas.pack(fill=tk.BOTH, expand=True)

        # Scrollbar para las alertas
        canvas = tk.Canvas(frame_alertas, bg="#101113")
        scrollbar = tk.Scrollbar(frame_alertas, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#101113")

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
                        f"Material:\nCódigo: {alerta['codigo']}\n"
                        f"Nombre: {alerta['nombre']}\n"
                        f"Tipo: {alerta['tipo_material']}\n"
                        f"Tamaño: {alerta['tamaño']}\n"
                        f"Color: {alerta['color']}\n"
                        f"Cantidad: {alerta['cantidad']}\n"
                        f"- - - - - - - - - - - - - - - - - - - - - - "
                    ),
                    font=("Arial", 10),
                    bg="#101113",
                    fg="#fa8e00",
                    justify=tk.LEFT,
                    pady=5
                )
                alerta_label.pack(fill=tk.X, padx=5, pady=5)

            elif alerta['tipo'] == 'producto':
                alerta_label = tk.Label(
                    scrollable_frame,
                    text=(
                        f"Producto:\nCódigo {alerta['codigo']}\n"
                        f"Tipo: {alerta['tipo_producto']}\n"
                        f"Cantidad: {alerta['cantidad']}\n"
                        f"- - - - - - - - - - - - - - - - - - - - - - "
                    ),
                    font=("Arial", 10),
                    bg="#101113",
                    fg="#1100ff",
                    justify=tk.LEFT,
                    pady=5
                )
                alerta_label.pack(fill=tk.X, padx=10, pady=5)

        # Botón para cerrar el Toplevel
        crear_boton(
            frame_contenido,
            texto="Cerrar",
            ancho=30,
            alto=30,
            color_fondo="#FF5733",
            #fg="white",
            font=("Arial", 10, "bold"),
            #bd=0,
            #relief=tk.FLAT,
            hover_color="#FB9773",
            comando=toplevel.destroy,
        ).pack(pady=10)
    
    
    def cerrar_sesion(self):
        if messagebox.askokcancel("Finalizar Sesión", "¿Deseas salir de la Sesión?"):
            self.pantalla_seleccion_perfil()
    
    
    def salir_programa(self):
        db_connect.close()
        self.root.quit()
        
        
    def on_closing(self):
        if messagebox.askokcancel("Salir", "¿Deseas salir del programa?"):
            self.salir_programa()  # Reutilizar la función salir_programa
    
    
    def mostrar_menu_principal(self, frame_principal=None):
        self.root.unbind("<Return>")

        if frame_principal is None:
            # Modo clásico: limpiar la ventana completa y crear el frame contenedor.
            for widget in self.root.winfo_children():
                widget.destroy()
            frame_principal = tk.Frame(self.root, bg=self.branding["fondo"],
                                        
                                        borderwidth=3, relief="solid")
            frame_principal.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            
        else:
            # Modo negocio: solo limpiar lo que haya DENTRO del frame, no el frame.
            for widget in frame_principal.winfo_children():
                widget.destroy()
                
        # Verificar bajo stock de Materiales y Productos  
        alertas = db_connect.verificar_stock_bajo()
        
        # Cargar el modo de negocio de la tienda (fabricante / vendedor)
        # Si aún no hay datos registrados, por defecto es 'fabricante'.
        self.modo_negocio = db_connect.obtener_modo_negocio()
        
        # Se modifica el título con el usuario y su rol
        self.root.title(f"Sistema de Inventario - usuario: {self.usuario}-{self.rol}")
        
        # Frame para los botones (lado izquierdo)
        frame_botones = tk.Frame(frame_principal, bg=self.branding["menu"], width=200, height=800, bd=3, borderwidth=3, relief="solid") # frame del Menu conf Perfil
        frame_botones.pack(side=tk.LEFT, fill=tk.Y)
        frame_botones.pack_propagate(False)
        
        # Frame del Titulo
        frame_titulo = tk.Frame(frame_principal, bg=self.branding["fondo"]) # Aplica conf perfil
        frame_titulo.pack(side=tk.TOP, fill=tk.X, pady=15)
        
        # Botón de advertencia de stock bajo (solo si hay alertas)
        if alertas:
            crear_boton(
                frame_principal,
                texto="⚠️ Advertencia de Stock",
                color_texto="#0D0C0C",
                ancho=30,
                alto=30,
                color_fondo="#FF5733",  # Color llamativo para advertencia
                #fg="white",
                font=("Arial", 11, "bold"),
                #bd=0,
                #relief=tk.FLAT,
                hover_color="#FF8C61",
                #activeforeground="white",
                comando=self.mostrar_alertas_stock_bajo,
        
            ).pack(pady=10)
            
        # Cargar imágenes base
        #self.imagen_tk = redimensionar_imagen(self.branding["logo"], 300, 300)
        self.imagen_buscar_tk = redimensionar_imagen(IMAGEN_BUSQUEDA_PATH, 200, 200)
        #self.imagen_panel_tk = redimensionar_imagen(self.branding["logo"], 60, 60)  # original 110 110
        
        # cargar logo de tienda
        # if self.imagen_tk:
        #     tk.Label(frame_principal, image=self.imagen_tk, bg=self.branding["fondo"]).pack(pady=20)
        # else:
        #     tk.Label(frame_principal, text="Ikigai Designs", font=("Arial", 24), bg=self.branding["fondo"]).pack(pady=20)
        crear_encabezado(frame_principal, self.branding, self.nombre_negocio_actual,
                tamano=300, fuente=("Arial", 20, "bold"))
        
        # Título
        title_label = tk.Label(
            frame_titulo,
            text="Sistema para la Gestión de Negocios",
            font=("Arial", 16, "bold"),
            bg=self.branding["fondo"],  #"#a0b9f0",
            fg=self.branding["fuente"] #"#2C3E50"
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
                comando=lambda: menu_gestion_inventario(frame_principal, self.mostrar_menu_principal, self.rol, self.usuario, self.branding, self.nombre_negocio_actual, self.modo_negocio),
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
                comando=lambda: VentanaVentas(frame_principal, self.usuario, self.mostrar_menu_principal, self.branding, self.nombre_negocio_actual)
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
                comando=lambda: CostosGananciasApp(frame_principal, self.mostrar_menu_principal, self.rol, self.branding, self.nombre_negocio_actual)
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
                comando=lambda: busqueda_articulos(frame_principal, self.mostrar_menu_principal,  self.branding, self.nombre_negocio_actual, self.imagen_buscar_tk, self.rol),
                
            ).pack(pady=10)
            # crear_boton(
            #     frame_botones,
            #     texto="Confg Usuario", 
            #     ancho=30,
            #     alto=30,
            #     color_fondo="#319139",                
            #     color_texto="white",
            #     font=("Arial", 11, "bold"),
            #     #bd=0,
            #     #relief=tk.FLAT,
            #     hover_color="#222423",
            #     #activeforeground="black",
            #     #bg=0,
            #     comando=lambda: self.conf_usuario.interfaz_configuracion()
                
            # ).pack(pady=10)
            crear_boton(
                frame_botones,
                texto="Cerrar Sesión", 
                ancho=30,
                alto=30,
                color_fondo="#BD5703",                
                color_texto="white",
                font=("Arial", 11, "bold"),
                #bd=0,
                #relief=tk.FLAT,
                hover_color="#222423",
                #activeforeground="black",
                #bg=0,
                comando=self.cerrar_sesion
                
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
                comando=lambda: gestion_usuarios(frame_principal, self.mostrar_menu_principal, self.branding, self.nombre_negocio_actual),
                
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
                comando=lambda: info_tienda(frame_principal, self.mostrar_menu_principal, self.branding, self.nombre_negocio_actual),
                
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
                comando=lambda: VentanaConfigurarUmbrales(frame_principal, self.mostrar_menu_principal),
                
            ).pack(pady=10)
            crear_boton(
                frame_botones,  # el frame donde tengas los botones del menú
                texto="Apariencia del Negocio",
                ancho=160, alto=30,
                color_fondo="#8A2BE2",
                color_texto="white",
                font=("Arial", 11, "bold"),
                hover_color="#6A1FB1",
                comando=lambda: perfilUsuario(frame_principal, self.nombre_negocio_actual)
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
                comando=lambda: eliminar_datos(frame_principal, self.mostrar_menu_principal, self.branding, self.nombre_negocio_actual),
            
            ).pack(pady=10)
            
            crear_boton(
                frame_botones,
                texto="Salir del programa", 
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
                
            ).pack(pady=10)
        
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
    