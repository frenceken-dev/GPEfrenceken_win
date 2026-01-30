# gestion_usuario.py
import tkinter as tk
from tkinter import ttk, messagebox
from db import registrar_usuario, buscar_usuarios, actualizar_usuario, eliminar_usuario_bd, restablecer_clave
from recursos import crear_boton, configurar_toplevel
from keygen_user import validar_clave_segura


def gestion_usuarios(root, mostrar_menu_principal, imagen_panel_tk):#, rol):
    # Limpiar el frame principal
    for widget in root.winfo_children():
        widget.destroy()

    # Frame principal
    frame = tk.Frame(root, bg="#a0b9f0", width=600, height=800)
    frame.pack(fill=tk.BOTH, expand=True)

    # Panel izquierdo (menú lateral)
    frame_menu = tk.Frame(frame, bg="#2C3E50", width=200, height=800)
    frame_menu.pack(side=tk.LEFT, fill=tk.Y)
    frame_menu.pack_propagate(False)
    
    # Frame para imagen del panel izquierdo
    frame_imagen_panel = tk.Frame(frame_menu, bg="#2C3E50", height=70)
    frame_imagen_panel.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
    
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
        text="Crear un nuevo Usuario",
        font=("Arial", 16, "bold"),
        bg="#a0b9f0",
        fg="#2C3E50"
    )
    title_label.pack(pady=15)
    
    # Campos para gestionar usuarios
    tk.Label(center_frame, text="Nombre de Usuario:", bg="#a0b9f0").grid(row=0, column=0, sticky="e", pady=5)
    nuevo_usuario_entry = tk.Entry(center_frame, width=30)
    nuevo_usuario_entry.grid(row=0, column=1, pady=5)
    
    tk.Label(center_frame, text="Pregunta de seguridad:", bg="#a0b9f0").grid(row=1, column=0, sticky="e", pady=5)
    pregunta_seguridad_entry = tk.Entry(center_frame, width=30)
    pregunta_seguridad_entry.grid(row=1, column=1, pady=5)
    
    tk.Label(center_frame, text="Respuesta a pregunta de seguridad:", bg="#a0b9f0").grid(row=2, column=0, sticky="e", pady=5)
    respuesta_seguridad_entry = tk.Entry(center_frame, width=30)
    respuesta_seguridad_entry.grid(row=2, column=1, pady=5)

    tk.Label(center_frame, text="Contraseña:", bg="#a0b9f0").grid(row=3, column=0, sticky="e", pady=5)
    nueva_contrasena_entry = tk.Entry(center_frame, width=30, show="*")
    nueva_contrasena_entry.grid(row=3, column=1, pady=5)

    tk.Label(center_frame, text="Rol:", bg="#a0b9f0").grid(row=4, column=0, sticky="e", pady=5)
    rol_combobox = ttk.Combobox(center_frame, values=["administrador", "usuario", "invitado"], width=28)
    rol_combobox.grid(row=4, column=1, pady=5)

    # Función para agregar un nuevo usuario
    def agregar_usuario():
        usuario = nuevo_usuario_entry.get()
        pregunta_seguridad = pregunta_seguridad_entry.get()
        respuesta_seguridad = respuesta_seguridad_entry.get()
        clave = nueva_contrasena_entry.get()
        rol = rol_combobox.get()

        if usuario and pregunta_seguridad and respuesta_seguridad and clave and rol:
            clave_valida, mensaje = validar_clave_segura(clave)
            print(f"{mensaje}")
            if clave_valida:                
                registrar_usuario(usuario, clave,  rol, pregunta_seguridad, respuesta_seguridad.lower())
                messagebox.showinfo("Éxito", "Usuario agregado correctamente.")
                mostrar_menu_principal
            else:
                print(f"Hubo un problema al intentar guardar el usuario")
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")

    # Botón para agregar usuario
    crear_boton(center_frame, 
        texto="Agregar Usuario",
        ancho=30,
        alto=30,
        color_fondo="#8e98f5",                
        color_texto="white",
        font=("Arial", 11, "bold"),
        #bd=0,
        #relief=tk.FLAT,
        hover_color="#2ECC71",
        #activeforeground="black",
        #bg=0, 
        comando=agregar_usuario, 
        ).grid(row=5, column=0, columnspan=2, pady=10)

    crear_boton(frame_menu,
        texto="Buscar usuario",
        ancho=30,
        alto=30,
        color_fondo="#3777EE",                
        color_texto="white",
        font=("Arial", 11, "bold"),
        #bd=0,
        #relief=tk.FLAT,
        hover_color="#2ECC71",
        #activeforeground="black",
        #bg=0,
        comando=lambda: formulario_buscar_usuario(root, mostrar_menu_principal, imagen_panel_tk),
        #width=18
    ).pack(pady=80)
    
    crear_boton(
        frame_menu,
        texto="Volver al Menú",
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
        #width=18
    ).pack(side=tk.LEFT, padx=30, pady=40)

# Formulario para la busqueda de usuario.
def formulario_buscar_usuario(root, volver_menu, imagen_panel_tk):
    # Limpiar el frame principal
    for widget in root.winfo_children():
        widget.destroy()
# Frame principal
    frame = tk.Frame(root, bg="#a0b9f0", width=600, height=800)
    frame.pack(fill=tk.BOTH, expand=True)

    # Panel izquierdo (menú lateral)
    frame_menu = tk.Frame(frame, bg="#2C3E50", width=200, height=800)
    frame_menu.pack(side=tk.LEFT, fill=tk.Y)
    frame_menu.pack_propagate(False)
    
    # Frame para imagen del panel izquierdo
    frame_imagen_panel = tk.Frame(frame_menu, bg="#2C3E50", height=70)
    frame_imagen_panel.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
    
    # Imagen del Logo para el panel izquierdo
    if imagen_panel_tk:
        label_imagen = tk.Label(frame_imagen_panel, image=imagen_panel_tk, bg="#2C3E50")
        label_imagen.pack(side=tk.LEFT, padx=70)
    else:
        label_texto = tk.Label(frame_imagen_panel, text="Ikigai Designs", font=("Arial", 10), bg="#2C3E50")
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
        text="Crear un nuevo Usuario",
        font=("Arial", 16, "bold"),
        bg="#a0b9f0",
        fg="#2C3E50"
    )
    title_label.pack(pady=15)

    # Campo para ingresar el valor de búsqueda
    tk.Label(center_frame, text="Buscar usuario:", bg="#a0b9f0").grid(row=0, column=0, sticky="e", pady=5)
    valor_busqueda_entry = tk.Entry(center_frame, width=30)
    valor_busqueda_entry.grid(row=0, column=1, pady=5)

    # Función para realizar la búsqueda
    def realizar_busqueda():
        valor = valor_busqueda_entry.get()
        resultados = buscar_usuarios(valor)
        mostrar_resultados_usuarios(resultados, root, volver_menu)

    # Botón para realizar la búsqueda
    crear_boton(center_frame, 
        texto="Buscar", 
        ancho=30,
        alto=30,
        color_fondo="#8e98f5",                
        color_texto="white",
        font=("Arial", 11, "bold"),
        #bd=0,
        #relief=tk.FLAT,
        hover_color="#2ECC71",
        #activeforeground="black",
        #bg=0,
        comando=realizar_busqueda, 
        ).grid(row=1, column=0, columnspan=2, pady=10)

    # Botón para volver al menú
    crear_boton(frame_menu,
        texto="Volver al Menú",
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
        comando=lambda: gestion_usuarios(root, volver_menu, imagen_panel_tk),
        
    ).pack(side=tk.LEFT, padx=30, pady=40)

# Mostrar los resultados de la busqueda.  
def mostrar_resultados_usuarios(resultados, root, volver_menu):
    if not resultados:
        messagebox.showinfo("Resultado", "No se encontraron usuarios.")
        return

    resultados_window = tk.Toplevel()
    configurar_toplevel(resultados_window, titulo="Resultados de Usuarios", ancho_min=500, alto_min=300, color_fondo="#101113")

    style = ttk.Style()
    style.configure("mystyle.Treeview", background="#101113",  # Fondo oscuro
        fieldbackground="#101113",  # Fondo de las celdas
        foreground="#ffffff"  # Color del texto (blanco)
    )
    # Crear un Treeview para mostrar los resultados
    tree = ttk.Treeview(resultados_window, columns=("ID", "Nombre de Usuario", "Rol"),
                        show="headings",
                        style="mystyle.Treeview")

    # Configurar las columnas
    tree.heading("ID", text="ID")
    tree.heading("Nombre de Usuario", text="Nombre de Usuario")
    tree.heading("Rol", text="Rol")

    # Ajustar el ancho de las columnas
    tree.column("ID", width=50)
    tree.column("Nombre de Usuario", width=150)
    tree.column("Rol", width=100)

    # Insertar los resultados en el Treeview
    for resultado in resultados:
        tree.insert("", tk.END, values=resultado)

    # Crear un Scrollbar y asociarlo al Treeview
    scrollbar = ttk.Scrollbar(resultados_window, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    # Empaquetar los widgets
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Botón para editar usuario
    def editar_usuario():
        selected_item = tree.selection()
        if selected_item:
            item = tree.item(selected_item)
            usuario = item['values']
            formulario_editar_usuario(root, volver_menu, usuario[0], usuario[1], usuario[2])
        else:
            messagebox.showerror("Error", "Selecciona un usuario para editar.")

    # Botón para eliminar usuario
    def eliminar_usuario():
        selected_item = tree.selection()
        if selected_item:
            item = tree.item(selected_item)
            usuario_id = item['values'][0]
            confirmar = messagebox.askyesno("Confirmar", "¿Estás seguro de que deseas eliminar este usuario?")
            if confirmar:
                eliminar_usuario_bd(usuario_id)
                messagebox.showinfo("Éxito", "Usuario eliminado correctamente.")
                resultados_window.destroy()
                formulario_buscar_usuario(root, volver_menu)
        else:
            messagebox.showerror("Error", "Selecciona un usuario para eliminar.")

    # Botones para editar y eliminar
    crear_boton(resultados_window, 
            texto="Editar Usuario",
            ancho=30,
            alto=30,
            color_fondo="#8e98f5",                
            color_texto="white",
            font=("Arial", 11, "bold"),
            #bd=0,
            #relief=tk.FLAT,
            hover_color="#2ECC71",
            #activeforeground="black",
            #bg=0, 
            comando=editar_usuario, 
            ).pack(side="bottom", pady=5)
    
    crear_boton(resultados_window, 
            texto="Eliminar Usuario", 
            ancho=30,
            alto=30,
            color_fondo="#913131",                
            color_texto="white",
            font=("Arial", 11, "bold"),
            #bd=0,
            #relief=tk.FLAT,
            hover_color="#2ECC71",
            #activeforeground="black",
            #bg=0,
            comando=eliminar_usuario, 
            
            ).pack(side="bottom", pady=5)
    
# Editar datos de usuario.
def formulario_editar_usuario(root, volver_menu, id_usuario, nombre_usuario, rol):
    # Limpiar el frame principal
    for widget in root.winfo_children():
        widget.destroy()

    # Crear un frame para el formulario de edición
    form_frame = tk.Frame(root, bg="#a0b9f0", padx=20, pady=20)
    form_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    # Frame para los botones (lado izquierdo)
    frame_botones = tk.Frame(root, bg="#2C3E50", width=200, height=800, bd=3, borderwidth=3, relief="solid")
    frame_botones.pack(side=tk.LEFT, fill=tk.Y)
    frame_botones.pack_propagate(False)

    # Campos para editar el usuario
    tk.Label(form_frame, text="Nombre de Usuario:", bg="#a0b9f0").grid(row=0, column=0, sticky="e", pady=5)
    usuario_entry = tk.Entry(form_frame, width=30)
    usuario_entry.grid(row=0, column=1, pady=5)
    usuario_entry.insert(0, nombre_usuario)

    tk.Label(form_frame, text="Rol:", bg="#a0b9f0").grid(row=1, column=0, sticky="e", pady=5)
    rol_combobox = ttk.Combobox(form_frame, values=["administrador", "usuario", "invitado"], width=28)
    rol_combobox.grid(row=1, column=1, pady=5)
    rol_combobox.set(rol)

    tk.Label(form_frame, text="Contraseña (dejar vacío para no cambiar):", bg="#a0b9f0").grid(row=2, column=0, sticky="e", pady=5)
    contrasena_entry = tk.Entry(form_frame, width=30, show="*")
    contrasena_entry.grid(row=2, column=1, pady=5)

    # Función para actualizar el usuario
    def actualizar():
        nuevo_usuario = usuario_entry.get()
        nuevo_rol = rol_combobox.get()
        nueva_contrasena = contrasena_entry.get()

        if nuevo_usuario and nuevo_rol:
            actualizar_usuario(id_usuario, nuevo_usuario, nuevo_rol, nueva_contrasena if nueva_contrasena else None)
            messagebox.showinfo("Éxito", "Usuario actualizado correctamente.")
            volver_menu()
        else:
            messagebox.showerror("Error", "El nombre de usuario y el rol son obligatorios.")

    # Botón para actualizar el usuario
    crear_boton(form_frame,
            texto="Actualizar", 
            ancho=30,
            alto=30,
            color_fondo="#2f367c",                
            color_texto="white",
            font=("Arial", 11, "bold"),
            #bd=0,
            #relief=tk.FLAT,
            hover_color="#2ECC71",
            #activeforeground="black",
            #bg=0,
            comando=actualizar, 
            ).grid(row=3, column=0, columnspan=2, pady=10)

    # Botón para volver al menú
    crear_boton(frame_botones, 
            texto="Volver al Menú",
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
            comando=volver_menu, 
            ).pack(side=tk.LEFT, padx=30, pady=40)

# Se actualiza la clave olvidada
def actualizar_clave(frame, usuario):  # viene de frame_clave_olvidada
    # Limpiar el frame principal
    def cerrar_toplevels(frame):
        for ventana in frame.winfo_children():
            if isinstance(ventana, tk.Toplevel):
                ventana.destroy()
    
    def validar_guardar_clave(frame, usuario, clave_1_entry, clave_2_entry):        
        clave1 = clave_1_entry.get().strip()
        clave2 = clave_2_entry.get().strip()
        
        if clave1 and clave2:
            if clave2 == clave1:
                nueva_clave = validar_clave_segura(clave1)
                if nueva_clave:
                    guardar_nueva_clave(frame, usuario, clave1)
            else:
                messagebox.showerror("Error", "Las claves deben ser iguales en ambos campos.")
        else:
            messagebox.showerror("Error", "Por favor, completa ambos campos.")
    
    def guardar_nueva_clave(frame, usuario, nueva_clave):
        
        if nueva_clave:
            recuperada, mensaje = restablecer_clave(usuario, nueva_clave)
            
            if recuperada:
                messagebox.showinfo("Proceso exitoso", mensaje)
                cerrar_toplevels(frame)
            else:
                messagebox.showerror("ERROR", "UPPS Algo salío mal, intenta mas tarde.")
        else:
            messagebox.showerror("Error", "No se pudo guardar la clave, contacte al servicio técnico")
            return
        
        
    ventana_actualizar = tk.Toplevel(frame)
    configurar_toplevel(ventana_actualizar, titulo="Crea una nueva Clave", ancho_min=240, alto_min=250, color_fondo="#101113")
    
    tk.Label(ventana_actualizar, text="Introduce la nueva contraseña", bg="#101113", fg="#ffffff").grid(row=0, column=0, padx=15, pady=10)
    clave_1_entry = tk.Entry(ventana_actualizar, width=25, show="*")
    clave_1_entry.grid(row=1, column=0, padx=15, pady=10)
    
    tk.Label(ventana_actualizar, text="Confirma la nueva contraseña", bg="#101113", fg="#ffffff").grid(row=2, column=0, padx=15, pady=10)
    clave_2_entry = tk.Entry(ventana_actualizar, width=25, show="*")
    clave_2_entry.grid(row=3, column=0, padx=15, pady=10)
    
    crear_boton(ventana_actualizar, 
        texto="Guardar",
        ancho=20,
        alto=20,
        color_fondo="#4B82F0",                
        color_texto="white",
        font=("Arial", 10, "bold"),
        #bd=0,
        #relief=tk.FLAT,
        hover_color="#2ECC71",
        #activeforeground="black",
        comando=lambda : validar_guardar_clave(frame, usuario, clave_1_entry, clave_2_entry),
        ).grid(row=4, column=0, columnspan=2, padx=15, pady=10, sticky="")
        