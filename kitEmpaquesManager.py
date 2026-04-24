import tkinter as tk
from tkinter import messagebox
from databasemanager import DataBaseManager
from recursos import crear_boton
import ast

import tkinter as tk
from tkinter import ttk, messagebox

class kitEmpaques:
    """Maneja la creación de diferentes Kit de empaques usando los materiales de empaques"""

    def __init__(self, root, imagen_panel_tk, volver_menu, usuario):
        self.db_connect = DataBaseManager()
        self.root = root
        self.imagen_panel_tk = imagen_panel_tk
        self.volver_menu = volver_menu
        self.usuario = usuario
        self.colores = {
            "fondo_principal": "#a0b9f0",  # Azul muy claro
            "fondo_menu": "#2C3E50",       # Azul oscuro
            "fondo_frame": "#a0b9f0",      # Azul claro
            "boton_guardar": "#4285F4",    # Azul Google
            "boton_volver": "#d32f2f",     # Rojo
            "texto_oscuro": "#2C3E50",
            "texto_claro": "#ffffff",
        }

    def limpiar_pantalla(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def iniciar_interfaz(self):
        self.limpiar_pantalla()
        self.crear_kit_empaque()

    def crear_kit_empaque(self):
        """Creación de la interfaz gráfica con frame de kits disponibles"""
        self.limpiar_pantalla()

        # Frame principal
        self.emp_frame = tk.Frame(self.root, bg=self.colores["fondo_principal"])
        self.emp_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.95, relheight=0.95)

        # Frame del menú lateral (izquierda)
        self.frame_menu = tk.Frame(
            self.emp_frame,
            bg=self.colores["fondo_menu"],
            width=180,
            bd=0,
            relief="solid"
        )
        self.frame_menu.pack(side=tk.LEFT, fill=tk.Y)
        self.frame_menu.pack_propagate(False)

        # Frame de contenido central (formulario)
        self.frame_contenido = tk.Frame(
            self.emp_frame,
            bg=self.colores["fondo_principal"],
            padx=20,
            pady=20
        )
        self.frame_contenido.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Frame de kits disponibles (derecha)
        self.frame_kits = tk.LabelFrame(
            self.emp_frame,
            text="Kits Disponibles",
            bg=self.colores["fondo_frame"],
            fg=self.colores["texto_oscuro"],
            font=("Arial", 12, "bold"),
            padx=10,
            pady=10,
            bd=2,
            relief="groove"
        )
        self.frame_kits.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        # Logo en el menú lateral
        self.crear_logo_panel()

        # Título en el frame central
        self.frame_titulo = tk.Frame(
            self.frame_contenido,
            bg=self.colores["fondo_principal"]
        )
        self.frame_titulo.pack(side=tk.TOP, fill=tk.X, pady=10)

        self.title_label = tk.Label(
            self.frame_titulo,
            text="Crear/Editar Kit de Empaque",
            font=("Arial", 18, "bold"),
            bg=self.colores["fondo_principal"],
            fg=self.colores["texto_oscuro"]
        )
        self.title_label.pack(pady=10)

        # Frame para los campos de entrada y lista (centrado)
        self.frame_campos = tk.LabelFrame(
            self.frame_contenido,
            text="Nuevo kit de empaque",
            bg=self.colores["fondo_frame"],
            fg=self.colores["texto_oscuro"],
            font=("Arial", 12, "bold"),
            padx=20,
            pady=20,
            bd=2,
            relief="groove"
        )
        self.frame_campos.pack(pady=10, padx=10, fill="both", expand=True)

        # Campo para el código del kit
        tk.Label(
            self.frame_campos,
            text="Código del kit:",
            bg=self.colores["fondo_frame"],
            fg=self.colores["texto_oscuro"],
            font=("Arial", 11)
        ).grid(row=0, column=0, sticky="w", pady=5, padx=10)

        self.codigo_entry = tk.Entry(
            self.frame_campos,
            width=30,
            font=("Arial", 11),
            bd=2,
            relief="groove"
        )
        self.codigo_entry.grid(row=1, column=0, pady=5, padx=10, sticky="ew")

        # Lista de ítems para el kit
        tk.Label(
            self.frame_campos,
            text="Selecciona los ítems:",
            bg=self.colores["fondo_frame"],
            fg=self.colores["texto_oscuro"],
            font=("Arial", 11, "bold")
        ).grid(row=2, column=0, sticky="w", pady=10, padx=10)

        self.frame_lista = tk.Frame(self.frame_campos, bg=self.colores["fondo_frame"])
        self.frame_lista.grid(row=3, column=0, pady=5, padx=10, sticky="nsew")

        self.scrollbar_items = tk.Scrollbar(self.frame_lista)
        self.scrollbar_items.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox_items = tk.Listbox(
            self.frame_lista,
            selectmode=tk.MULTIPLE,
            width=40,
            height=8,
            font=("Arial", 11),
            bd=2,
            relief="groove",
            yscrollcommand=self.scrollbar_items.set
        )
        self.listbox_items.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar_items.config(command=self.listbox_items.yview)

        # Cargar ítems desde la base de datos
        items = self.db_connect.selecion_empaques()
        for item_nombre in items:
            self.listbox_items.insert(tk.END, item_nombre)

        # Botón para guardar/actualizar el kit
        self.boton_guardar_kit = crear_boton(
            self.frame_campos,
            texto="Guardar Kit",
            ancho=30,
            alto=30,
            relieve="raised",
            border_width=3,
            color_fondo=self.colores["boton_guardar"],
            color_texto=self.colores["texto_claro"],
            font=("Arial", 11, "bold"),
            hover_color="#2ECC71",
            comando=lambda: self.crear_kit(self.usuario, self.codigo_entry.get())
        )
        self.boton_guardar_kit.grid(row=4, column=0, pady=20, sticky="nsew")

        # Frame de kits disponibles (derecha)
        tk.Label(
            self.frame_kits,
            text="Selecciona un kit:",
            bg=self.colores["fondo_frame"],
            fg=self.colores["texto_oscuro"],
            font=("Arial", 11, "bold")
        ).pack(pady=5)

        self.frame_lista_kits = tk.Frame(self.frame_kits, bg=self.colores["fondo_frame"])
        self.frame_lista_kits.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.scrollbar_kits = tk.Scrollbar(self.frame_lista_kits)
        self.scrollbar_kits.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox_kits = tk.Listbox(
            self.frame_lista_kits,
            width=25,
            height=15,
            font=("Arial", 11),
            bd=2,
            relief="groove",
            yscrollcommand=self.scrollbar_kits.set
        )
        self.listbox_kits.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar_kits.config(command=self.listbox_kits.yview)

        # Cargar kits desde la base de datos
        self.cargar_kits_disponibles()

        # Botón para editar el kit seleccionado
        self.boton_editar_kit = crear_boton(
            self.frame_kits,
            texto="Editar kit Seleccionado",
            ancho=30,
            alto=30,
            relieve="raised",
            border_width=1,
            color_fondo="#FFC107",
            color_texto=self.colores["texto_oscuro"],
            font=("Arial", 11, "bold"),
            hover_color="#2ECC71",
            comando=lambda: self.cargar_datos_kit()
            )
        # tk.Button(
        #     self.frame_kits,
        #     text="Editar Kit Seleccionado",
        #     width=20,
        #     height=1,
        #     bg="#FFC107",  # Amarillo para destacar
        #     fg=self.colores["texto_oscuro"],
        #     font=("Arial", 11, "bold"),
        #     relief="raised", 
        #     bd=3,
        #     state=tk.DISABLED,
        #     command=lambda: self.cargar_datos_kit()
        # )
        self.boton_editar_kit.pack(pady=10)

        # Asociar evento de selección del kit
        self.listbox_kits.bind('<<ListboxSelect>>', self.habilitar_boton_editar)

        # Botón para volver al menú
        self.boton_cerrar = crear_boton(self.frame_menu,
            texto="Volver",
            ancho=30,
            alto=30,
            relieve="raised",
            color_fondo=self.colores["boton_volver"],
            color_texto=self.colores["texto_claro"],
            font=("Arial", 11, "bold"),
            border_width=1,
            hover_color="#222423",
            comando=self.cerrar_ventana
        )# tk.Button(
        #     self.frame_menu,
        #     text="Volver",
        #     width=15,
        #     height=2,
        #     bg=self.colores["boton_volver"],
        #     fg=self.colores["texto_claro"],
        #     font=("Arial", 11, "bold"),
        #     relief="raised",
        #     bd=3,
        #     command=self.cerrar_ventana
        # )
        self.boton_cerrar.pack(side="bottom", pady=40)

    def cargar_kits_disponibles(self):
        """Carga los kits disponibles en el Listbox"""
        self.listbox_kits.delete(0, tk.END)
        kits = self.db_connect.obtener_kits()  # Asegúrate de implementar este método en DataBaseManager
        for kit in kits:
            self.listbox_kits.insert(tk.END, kit)  # kit[1] es el nombre del kit

    def habilitar_boton_editar(self, event):
        """Habilita el botón de editar si hay un kit seleccionado"""
        seleccion = self.listbox_kits.curselection()
        if seleccion:
            self.boton_editar_kit.config(state=tk.NORMAL)
        else:
            self.boton_editar_kit.config(state=tk.DISABLED)

    def cargar_datos_kit(self):
        """Abre un Toplevel para mostrar y editar los ítems del kit seleccionado"""
        seleccion = self.listbox_kits.curselection()
        if not seleccion:
            return

        # Obtener el nombre del kit seleccionado
        nombre_kit = self.listbox_kits.get(seleccion[0])

        # Obtener los datos del kit desde la base de datos
        kit_data = self.db_connect.obtener_detalles_kit(nombre_kit)
        if not kit_data:
            messagebox.showerror("Error", "No se pudo cargar la información del kit.")
            return

        # Crear el Toplevel
        self.toplevel_kit = tk.Toplevel(self.root)
        self.toplevel_kit.title(f"Editar Kit: {nombre_kit}") #{kit_data['nombre']}")
        self.toplevel_kit.geometry("550x600")
        self.toplevel_kit.resizable(False, False)
        self.toplevel_kit.transient(self.root)
        self.toplevel_kit.grab_set()

        # Frame principal del Toplevel
        frame_principal = tk.Frame(self.toplevel_kit, bg=self.colores["fondo_principal"], padx=20, pady=20)
        frame_principal.pack(fill=tk.BOTH, expand=True)

        # Título
        tk.Label(
            frame_principal,
            text=f"Editando Kit: {kit_data[0]['id_kit']}", # Sin "nombre" solo codigo
            font=("Arial", 14, "bold"),
            bg=self.colores["fondo_principal"],
            fg=self.colores["texto_oscuro"]
        ).pack(pady=10)

        # Campo para el código del kit (solo lectura)
        tk.Label(
            frame_principal,
            text="Código del Kit:",
            bg=self.colores["fondo_principal"],
            fg=self.colores["texto_oscuro"],
            font=("Arial", 11)
        ).pack(anchor="w", pady=5)

        codigo_label = tk.Label(
            frame_principal,
            text=nombre_kit, # kit_data["codigo"], 
            bg=self.colores["fondo_frame"],
            fg=self.colores["texto_oscuro"],
            font=("Arial", 11),
            relief="groove",
            bd=2,
            width=30,
            padx=5,
            pady=5
        )
        codigo_label.pack(fill=tk.X, pady=5)

        # Lista de ítems actuales del kit
        tk.Label(
            frame_principal,
            text="Ítems del Kit:",
            bg=self.colores["fondo_principal"],
            fg=self.colores["texto_oscuro"],
            font=("Arial", 11, "bold")
        ).pack(anchor="w", pady=10)

        # Frame para la lista de ítems disponibles y seleccionados
        frame_listas = tk.Frame(frame_principal, bg=self.colores["fondo_principal"])
        frame_listas.pack(fill=tk.BOTH, expand=True, pady=10)

        # Lista de ítems disponibles
        frame_disponibles = tk.LabelFrame(
            frame_listas,
            text="Ítems Disponibles",
            bg=self.colores["fondo_frame"],
            fg=self.colores["texto_oscuro"],
            font=("Arial", 10, "bold"),
            padx=5,
            pady=5
        )
        frame_disponibles.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        scrollbar_disponibles = tk.Scrollbar(frame_disponibles)
        scrollbar_disponibles.pack(side=tk.RIGHT, fill=tk.Y)

        listbox_disponibles = tk.Listbox(
            frame_disponibles,
            selectmode=tk.MULTIPLE,
            width=25,
            height=10,
            font=("Arial", 11),
            bd=2,
            relief="groove",
            yscrollcommand=scrollbar_disponibles.set
        )
        listbox_disponibles.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_disponibles.config(command=listbox_disponibles.yview)

        # Cargar ítems disponibles
        items_disponibles = self.db_connect.selecion_empaques()
        for item in items_disponibles:
            listbox_disponibles.insert(tk.END, item)

        # Lista de ítems seleccionados en el kit
        frame_seleccionados = tk.LabelFrame(
            frame_listas,
            text="Ítems en el Kit",
            bg=self.colores["fondo_frame"],
            fg=self.colores["texto_oscuro"],
            font=("Arial", 10, "bold"),
            padx=5,
            pady=5
        )
        frame_seleccionados.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)

        scrollbar_seleccionados = tk.Scrollbar(frame_seleccionados)
        scrollbar_seleccionados.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox_seleccionados = tk.Listbox(
            frame_seleccionados,
            selectmode=tk.MULTIPLE,
            width=25,
            height=10,
            font=("Arial", 11),
            bd=2,
            relief="groove",
            yscrollcommand=scrollbar_seleccionados.set
        )
        self.listbox_seleccionados.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_seleccionados.config(command=self.listbox_seleccionados.yview)
        
        # Cargar ítems del kit seleccionado
        kit_data_list = ast.literal_eval(kit_data[0]['items_del_kit'])
        for item in kit_data_list:
            self.listbox_seleccionados.insert(tk.END, item)

        # Botones para mover ítems entre listas
        frame_botones = tk.Frame(frame_listas, bg=self.colores["fondo_principal"])
        frame_botones.pack(pady=10)

        tk.Button(
            frame_botones,
            text=">>",
            width=5,
            command=lambda: self.mover_item(listbox_disponibles, self.listbox_seleccionados)
        ).pack(pady=5)

        tk.Button(
            frame_botones,
            text="<<",
            width=5,
            command=lambda: self.mover_item(self.listbox_seleccionados, listbox_disponibles)
        ).pack(pady=5)

        # Botones para guardar o cancelar
        frame_acciones = tk.Frame(frame_principal, bg=self.colores["fondo_principal"])
        frame_acciones.pack(fill=tk.X, pady=10)

        tk.Button(
            frame_acciones,
            text="Guardar Cambios",
            width=15,
            bg=self.colores["boton_guardar"],
            fg=self.colores["texto_claro"],
            font=("Arial", 11, "bold"),
            command=lambda: self.guardar_cambios_kit(nombre_kit, self.listbox_seleccionados)
        ).pack(side=tk.RIGHT, padx=10)

        tk.Button(
            frame_acciones,
            text="Cancelar",
            width=15,
            bg=self.colores["boton_volver"],
            fg=self.colores["texto_claro"],
            font=("Arial", 11, "bold"),
            command=self.toplevel_kit.destroy
        ).pack(side=tk.RIGHT)

    def mover_item(self, listbox_origen, listbox_destino):
        """Mueve los ítems seleccionados de un Listbox a otro"""
        seleccion = listbox_origen.curselection()
        if not seleccion:
            return

        for index in seleccion[::-1]:  # Recorrer en orden inverso para evitar problemas al eliminar
            item = listbox_origen.get(index)
            listbox_destino.insert(tk.END, item)
            listbox_origen.delete(index)

    def guardar_cambios_kit(self, codigo_kit, listbox_seleccionados):
        """Guarda los cambios realizados en el kit"""
        empaques = [listbox_seleccionados.get(i) for i in range(listbox_seleccionados.size())]

        if not empaques:
            messagebox.showwarning("Advertencia", "El kit debe tener al menos un ítem.")
            return

        kit_costo, mensaje = self.db_connect.actualizar_kit(codigo_kit, empaques, self.usuario)
        messagebox.showinfo("Éxito", f"{mensaje}\nValor: {kit_costo} Euros")
        self.toplevel_kit.destroy()
        self.cargar_kits_disponibles()  # Actualizar la lista de kits

    def crear_logo_panel(self):
        frame_imagen_panel = tk.Frame(
            self.frame_menu,
            bg=self.colores["fondo_menu"],
            height=70
        )
        frame_imagen_panel.pack(side=tk.BOTTOM, fill=tk.X, pady=20)

        if self.imagen_panel_tk:
            label_imagen = tk.Label(
                frame_imagen_panel,
                image=self.imagen_panel_tk,
                bg=self.colores["fondo_menu"]
            )
            label_imagen.pack(side=tk.TOP, pady=10)
        else:
            label_texto = tk.Label(
                frame_imagen_panel,
                text="Ikigai",
                font=("Arial", 12, "bold"),
                bg=self.colores["fondo_menu"],
                fg=self.colores["texto_claro"]
            )
            label_texto.pack(side=tk.TOP, pady=10)

    def crear_kit(self, usuario, codigo_kit):
        seleccion = self.listbox_items.curselection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona al menos un ítem.")
            return

        empaques = [self.listbox_items.get(i) for i in seleccion]
        if codigo_kit:
            kit_costo, mensaje = self.db_connect.guardar_kit(codigo_kit, empaques, usuario)
            messagebox.showinfo("Éxito", f"{mensaje}\nValor: {kit_costo} Euros")
        else:
            messagebox.showwarning("Advertencia", "Ingresa un código para el kit.")

    def cerrar_ventana(self):
        self.emp_frame.destroy()
        self.volver_menu()