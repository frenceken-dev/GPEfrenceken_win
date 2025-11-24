# gestion_usuario.py
import tkinter as tk
from tkinter import ttk, messagebox
from db import insertar_usuario, buscar_usuarios, actualizar_usuario, eliminar_usuario_bd

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

    tk.Label(center_frame, text="Contraseña:", bg="#a0b9f0").grid(row=1, column=0, sticky="e", pady=5)
    nueva_contrasena_entry = tk.Entry(center_frame, width=30, show="*")
    nueva_contrasena_entry.grid(row=1, column=1, pady=5)

    tk.Label(center_frame, text="Rol:", bg="#a0b9f0").grid(row=2, column=0, sticky="e", pady=5)
    rol_combobox = ttk.Combobox(center_frame, values=["administrador", "usuario", "invitado"], width=28)
    rol_combobox.grid(row=2, column=1, pady=5)

    # Función para agregar un nuevo usuario
    def agregar_usuario():
        usuario = nuevo_usuario_entry.get()
        clave = nueva_contrasena_entry.get()
        rol = rol_combobox.get()

        if usuario and clave and rol:
            insertar_usuario(usuario, clave, rol)
            messagebox.showinfo("Éxito", "Usuario agregado correctamente.")
            mostrar_menu_principal
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")

    # Botón para agregar usuario
    tk.Button(center_frame, text="Agregar Usuario", command=agregar_usuario, bg="#8e98f5").grid(row=3, column=0, columnspan=2, pady=10)

    tk.Button(
        frame_menu,
        text="Buscar usuario",
        bg="#3777EE",
        fg="white",
        font=("Arial", 11, "bold"),
        bd=0,
        relief=tk.FLAT,
        activebackground="#2ECC71",
        activeforeground="white",
        command=lambda: formulario_buscar_usuario(root, mostrar_menu_principal, imagen_panel_tk),
        width=18
    ).pack(pady=80)
    
    tk.Button(
        frame_menu,
        text="Volver al Menú",
        bg="#913131",
        fg="white",
        font=("Arial", 11, "bold"),
        bd=0,
        relief=tk.FLAT,
        activebackground="#2ECC71",
        activeforeground="white",
    command=mostrar_menu_principal,
        width=18
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
    tk.Button(center_frame, 
            text="Buscar", 
            command=realizar_busqueda, 
            bg="#8e98f5",
            fg="white",
            font=("Arial", 11, "bold"),
            bd=0,
            relief=tk.FLAT,
            activebackground="#2ECC71",
            activeforeground="white",
            ).grid(row=1, column=0, columnspan=2, pady=10)

    # Botón para volver al menú
    tk.Button(
        frame_menu,
        text="Volver al Menú",
        bg="#913131",
        fg="white",
        font=("Arial", 11, "bold"),
        bd=0,
        relief=tk.FLAT,
        activebackground="#2ECC71",
        activeforeground="white",
        command=lambda: gestion_usuarios(root, volver_menu, imagen_panel_tk),
        width=18,
        
    ).pack(side=tk.LEFT, padx=30, pady=40)

# Mostrar los resultados de la busqueda.  
def mostrar_resultados_usuarios(resultados, root, volver_menu):
    if not resultados:
        messagebox.showinfo("Resultado", "No se encontraron usuarios.")
        return

    resultados_window = tk.Toplevel()
    resultados_window.title("Resultados de Usuarios")

    # Crear un Treeview para mostrar los resultados
    tree = ttk.Treeview(resultados_window, columns=("ID", "Nombre de Usuario", "Rol"), show="headings")

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
    tk.Button(resultados_window, 
            text="Editar Usuario", 
            command=editar_usuario, 
            bg="#8e98f5",
            fg="white",
            font=("Arial", 11, "bold"),
            bd=0,
            relief=tk.FLAT,
            activebackground="#2f367c",
            activeforeground="white",
            ).pack(pady=5)
    
    tk.Button(resultados_window, 
            text="Eliminar Usuario", 
            command=eliminar_usuario, 
            bg="#913131",
            fg="white",
            font=("Arial", 11, "bold"),
            bd=0,
            relief=tk.FLAT,
            activebackground="#2ECC71",
            activeforeground="white",
            ).pack(pady=5)
    
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
    tk.Button(form_frame,
            text="Actualizar", 
            command=actualizar, 
            bg="#2f367c",
            fg="white",
            font=("Arial", 11, "bold"),
            bd=0,
            relief=tk.FLAT,
            activebackground="#2ECC71",
            activeforeground="white",
            ).grid(row=3, column=0, columnspan=2, pady=10)

    # Botón para volver al menú
    tk.Button(frame_botones, 
            text="Volver al Menú", 
            command=volver_menu, 
            bg="#913131",
            fg="white",
            font=("Arial", 11, "bold"),
            bd=0,
            relief=tk.FLAT,
            activebackground="#2ECC71",
            activeforeground="white",
            ).pack(side=tk.LEFT, padx=30, pady=40)
