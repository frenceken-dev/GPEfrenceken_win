# costos_ganacias.py
import tkinter as tk
from tkinter import ttk, messagebox, Toplevel
from tkcalendar import Calendar 
# from inventario import convertir_a_float
from db import (
    #registrar_producto_en_lote, 
    #obtener_lotes_con_productos, 
    insertar_lote,
    )
from recursos import crear_boton, configurar_toplevel
from databasemanager import DataBaseManager


class CostosGananciasApp:
    def __init__(self, root, mostrar_menu_principal, imagen_panel_tk, rol, imagen_tk):
        self.root = root
        self.mostrar_menu_principal = mostrar_menu_principal
        self.imagen_panel_tk = imagen_panel_tk
        self.rol = rol
        self.imagen_tk = imagen_tk
        self.db_connect = DataBaseManager()

        # Colores consistentes (igual que en kitEmpaques)
        self.colores = {
            "fondo_principal": "#a0b9f0",  # Azul claro
            "fondo_menu": "#2C3E50",       # Azul oscuro
            "fondo_frame": "#a0b9f0",      # Azul claro
            "boton_guardar": "#4285F4",    # Azul Google
            "boton_volver": "#d32f2f",     # Rojo
            "boton_editar": "#FFC107",    # Amarillo
            "boton_eliminar": "#E74C3C",  # Rojo claro
            "texto_oscuro": "#2C3E50",
            "texto_claro": "#ffffff",
        }

        # Inicializar managers
        self.lote_manager = LoteManager(self.root, self.db_connect, self.colores)
        self.producto_manager = ProductoManager(self.root, self.db_connect, self.colores)
        self.historial_manager = HistorialManager(self.root, self.db_connect, self.colores)

        # Iniciar la interfaz
        self.iniciar_interfaz()

    def limpiar_pantalla(self):
        """Limpia todos los widgets de la ventana principal."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def iniciar_interfaz(self):
        """Inicia la interfaz principal del módulo."""
        self.limpiar_pantalla()
        self.crear_interfaz_principal()

    def crear_interfaz_principal(self):
        """Crea la interfaz principal con menú lateral y área de contenido."""
        
        # Frame del menú lateral (izquierda)
        self.frame_menu = tk.Frame(
            self.root,
            width=200,
            height=800,
            bg=self.colores["fondo_menu"],
            bd=0,
            relief="solid"
        )
        self.frame_menu.pack(side=tk.LEFT, fill=tk.Y)
        self.frame_menu.pack_propagate(False)
        
        # Frame principal (contiene todo)
        self.main_frame = tk.Frame(self.root, width=600, height=800, bg=self.colores["fondo_principal"])
        #self.main_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.95, relheight=0.95)
        self.main_frame.pack(expand=True, fill=tk.BOTH, side=tk.RIGHT)

        # Frame de contenido central
        self.frame_contenido = tk.Frame(
            self.main_frame,
            bg=self.colores["fondo_principal"],
            padx=20,
            pady=20
        )
        self.frame_contenido.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Frame de información adicional (derecha, opcional)
        self.frame_info = tk.LabelFrame(
            self.main_frame,
            text="Información",
            bg=self.colores["fondo_frame"],
            fg=self.colores["texto_oscuro"],
            font=("Arial", 12, "bold"),
            padx=10,
            pady=10,
            bd=2,
            relief="groove"
        )
        self.frame_info.pack(side=tk.RIGHT, fill=tk.Y, padx=3, pady=10)

        # Logo en el menú lateral
        self.crear_logo_panel()

        # Título en el frame central
        self.crear_titulo()

        # Botones del menú lateral
        self.crear_botones_menu()

        # Contenido inicial (vista por defecto)
        self.mostrar_vista_inicial()

    def crear_logo_panel(self):
        """Crea el logo en el panel lateral."""
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

    def crear_titulo(self):
        """Crea el título en el frame de contenido."""
        self.frame_titulo = tk.Frame(
            self.frame_contenido,
            bg=self.colores["fondo_principal"]
        )
        self.frame_titulo.pack(side=tk.TOP, fill=tk.X, pady=10)

        self.title_label = tk.Label(
            self.frame_titulo,
            text="Costos y Ganancias",
            font=("Arial", 18, "bold"),
            bg=self.colores["fondo_principal"],
            fg=self.colores["texto_oscuro"]
        )
        self.title_label.pack(pady=10)

    def crear_botones_menu(self):
        """Crea los botones del menú lateral."""
        botones = [
            ("Act. Costo por Unidad", self.colores["boton_guardar"], self.producto_manager.abrir_actualizar_costo_por_unidad),
            ("Act. Costo por Lote", self.colores["boton_guardar"], self.producto_manager.abrir_actualizar_costo_por_lote),
            ("Actualizar Historial", self.colores["boton_guardar"], self.historial_manager.abrir_actualizar_historial),
            ("Historial de Costos", self.colores["boton_editar"], self.historial_manager.mostrar_historial_costos),
            ("Historial de Ganancias", self.colores["boton_editar"], self.historial_manager.mostrar_historial_ganancias),
            ("Gestionar Lotes", self.colores["boton_editar"], self.lote_manager.mostrar_lotes),
        ]

        for texto, color, comando in botones:
            crear_boton(
                self.frame_menu,
                texto=texto,
                ancho=18,
                alto=2,
                relieve="raised",
                border_width=1,
                color_fondo=color,
                color_texto=self.colores["texto_claro"],
                font=("Arial", 10, "bold"),
                hover_color="#2ECC71",
                comando=lambda cmd=comando: self.cargar_vista(cmd)
            ).pack(pady=5, padx=10)

        # Botón para volver al menú principal
        crear_boton(
            self.frame_menu,
            texto="Menú Principal",
            ancho=18,
            alto=2,
            relieve="raised",
            border_width=1,
            color_fondo=self.colores["boton_volver"],
            color_texto=self.colores["texto_claro"],
            font=("Arial", 10, "bold"),
            hover_color="#222423",
            comando=self.mostrar_menu_principal
        ).pack(side="bottom", pady=20)

    def cargar_vista(self, comando):
        """Carga la vista correspondiente según el botón seleccionado."""
        # Limpiar el frame de contenido
        for widget in self.frame_contenido.winfo_children():
            widget.destroy()

        # # Limpiar el frame de información (opcional)
        # for widget in self.frame_info.winfo_children():
        #     widget.destroy()

        # Llamar al comando con los parámetros necesarios
        comando(
            self.root,
            self.mostrar_menu_principal,
            self.imagen_panel_tk,
            self.rol,
            self.imagen_tk,
            self.frame_contenido,
            #self.frame_info  # Pasamos el frame_info por si se necesita
        )

    def mostrar_vista_inicial(self):
        """Muestra una vista inicial con información general."""
        pass
        # info_frame = tk.Frame(self.frame_contenido, bg=self.colores["fondo_principal"])
        # info_frame.pack(fill=tk.BOTH, expand=True)

        # tk.Label(
        #     info_frame,
        #     text="Módulo para el manejo de Costos y Ganancias",
        #     font=("Arial", 14, "bold"),
        #     bg=self.colores["fondo_principal"],
        #     fg=self.colores["texto_oscuro"]
        # ).pack(pady=20)

        # tk.Label(
        #     info_frame,
        #     text="Selecciona una opción del menú lateral para comenzar.",
        #     font=("Arial", 12),
        #     bg=self.colores["fondo_principal"],
        #     fg=self.colores["texto_oscuro"]
        # ).pack(pady=10)
        
        
class LoteManager:
    def __init__(self, root, db, colores):
        self.root = root
        self.db_connect = db
        self.colores = colores
        self.lotes = self.db_connect.obtener_lotes_con_productos()
        self.productos = self.db_connect.obtener_productos_para_costoventa()
        self.lote_seleccionado = None  # Para almacenar el lote seleccionado

    def mostrar_lotes(self, root, mostrar_menu_principal, imagen_panel_tk, rol, imagen_tk, content_frame): #, info_frame=None):
        """Muestra la interfaz para gestionar lotes: lista de lotes (izquierda) y formulario (derecha)."""
        # Limpiar frames
        for widget in content_frame.winfo_children():
            widget.destroy()
        # if info_frame:
        #     for widget in info_frame.winfo_children():
        #         widget.destroy()

        # --- Frame de contenido (izquierda): Lista de lotes ---
        self.frame_lotes = tk.LabelFrame(
            content_frame,
            text="Lotes Existentes",
            bg=self.colores["fondo_frame"],
            fg=self.colores["texto_oscuro"],
            font=("Arial", 12, "bold"),
            padx=0,
            pady=10,
            bd=2,
            relief="groove"
        )
        self.frame_lotes.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=3, pady=10)

        # Configurar el estilo del Treeview
        style = ttk.Style()
        style.configure("mystyle.Treeview", background="#101113", fieldbackground="#101113", foreground="#ffffff")
        style.configure("mystyle.Treeview.Heading", background="#ffffff", foreground="#101113")
        
        # Treeview para mostrar lotes
        columnas = ("Id", "Código", "Descripción", "Unidades", "Costo", "Precio Venta")
        self.tree_lotes = ttk.Treeview(self.frame_lotes, columns=columnas, show="headings", style="mystyle.Treeview")
        self.tree_lotes.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Configurar columnas
        for col in columnas:
            self.tree_lotes.heading(col, text=col)
            self.tree_lotes.column(col, width=110, anchor=tk.CENTER)

        # Cargar lotes en el Treeview
        self._cargar_lotes_en_treeview()

        # Botón para actualizar la lista
        crear_boton(
            self.frame_lotes,
            texto="Actualizar Lista",
            ancho=20,
            alto=2,
            relieve="raised",
            border_width=1,
            color_fondo="#2ECC71",
            color_texto=self.colores["texto_claro"],
            font=("Arial", 10, "bold"),
            hover_color="#2ECC71",
            comando=self._actualizar_lista_lotes
        ).pack(side=tk.LEFT, padx=5)

        # Asociar evento de selección
        self.tree_lotes.bind("<<TreeviewSelect>>", self._on_lote_seleccionado)

        # --- Frame de información (derecha): Formulario de lote ---
        info_frame = tk.Frame(content_frame, bg=self.colores["fondo_principal"])
        info_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=3, pady=10)
        
        if info_frame:
            self.frame_formulario = tk.LabelFrame(
                info_frame,
                text="Crear/Editar Lote",
                bg=self.colores["fondo_frame"],
                fg=self.colores["texto_oscuro"],
                font=("Arial", 12, "bold"),
                padx=10,
                pady=10,
                bd=2,
                relief="groove"
            )
            self.frame_formulario.pack(fill=tk.BOTH, expand=True, padx=10, pady=3)

            # Campos del formulario
            self._crear_formulario_lote()

        # Botón para crear un nuevo lote (si no hay nada seleccionado)
        crear_boton(
            self.frame_lotes,
            texto="Nuevo Lote",
            ancho=20,
            alto=2,
            relieve="raised",
            border_width=1,
            color_fondo=self.colores["boton_guardar"],
            color_texto=self.colores["texto_claro"],
            font=("Arial", 10, "bold"),
            hover_color="#2ECC71",
            comando=self._limpiar_formulario
        ).pack(side=tk.LEFT, padx=5)
        
        # Botón para eliminar el lote seleccionado
        self.boton_eliminar = crear_boton(
            self.frame_lotes,
            texto="Eliminar Lote",
            ancho=15,
            alto=2,
            relieve="raised",
            border_width=1,
            color_fondo=self.colores["boton_eliminar"],
            color_texto=self.colores["texto_claro"],
            font=("Arial", 10, "bold"),
            hover_color="#E74C3C",
            comando=self._confirmar_eliminar_lote,
            #estado=tk.DISABLED  # Deshabilitado hasta seleccionar un lote
        )
        self.boton_eliminar.config(state=tk.DISABLED)
        self.boton_eliminar.pack(side=tk.LEFT, padx=5)

    def _crear_formulario_lote(self):
        """Crea el formulario para crear/editar un lote con cantidades individuales por producto."""
        # Limpiar el formulario
        for widget in self.frame_formulario.winfo_children():
            widget.destroy()

        # Configurar el grid para que se expanda correctamente
        self.frame_formulario.grid_columnconfigure(0, weight=1)  # Columna 0 se expande
        
        tk.Label(
            self.frame_formulario,
            text="Código del Lote:",
            bg=self.colores["fondo_frame"],
            fg=self.colores["texto_oscuro"],
            font=("Arial", 11)
        ).grid(row=0, column=0, sticky="w", pady=1, padx=10)

        self.codigo_entry = tk.Entry(
            self.frame_formulario,
            width=30,
            font=("Arial", 11),
            bd=2,
            relief="groove"
        )
        self.codigo_entry.grid(row=1, column=0, pady=0, padx=10, sticky="ew")

        # Campo para la descripción
        tk.Label(
            self.frame_formulario,
            text="Descripción:",
            bg=self.colores["fondo_frame"],
            fg=self.colores["texto_oscuro"],
            font=("Arial", 11)
        ).grid(row=2, column=0, sticky="w", pady=1, padx=10)

        self.descripcion_entry = tk.Entry(
            self.frame_formulario,
            width=30,
            font=("Arial", 11),
            bd=2,
            relief="groove"
        )
        self.descripcion_entry.grid(row=3, column=0, pady=0, padx=10, sticky="ew")

        # Campo para unidades (total de unidades en el lote)
        tk.Label(
            self.frame_formulario,
            text="Unidades totales en el lote:",
            bg=self.colores["fondo_frame"],
            fg=self.colores["texto_oscuro"],
            font=("Arial", 11)
        ).grid(row=4, column=0, sticky="w", pady=1, padx=10)

        self.unidades_entry = tk.Entry(
            self.frame_formulario,
            width=30,
            font=("Arial", 11),
            bd=2,
            relief="groove"
        )
        self.unidades_entry.grid(row=5, column=0, pady=0, padx=10, sticky="ew")

        # Campo para costo (solo lectura, se calcula automáticamente)
        tk.Label(
            self.frame_formulario,
            text="Costo del lote (calculado):",
            bg=self.colores["fondo_frame"],
            fg=self.colores["texto_oscuro"],
            font=("Arial", 11)
        ).grid(row=6, column=0, sticky="w", pady=1, padx=10)

        self.costo_entry = tk.Entry(
            self.frame_formulario,
            width=30,
            font=("Arial", 11),
            bd=2,
            relief="groove",
            state="readonly"
        )
        self.costo_entry.grid(row=7, column=0, pady=0, padx=10, sticky="ew")

        # Campo para precio de venta sugerido (opcional)
        tk.Label(
            self.frame_formulario,
            text="Precio de venta sugerido (5x):",
            bg=self.colores["fondo_frame"],
            fg=self.colores["texto_oscuro"],
            font=("Arial", 11)
        ).grid(row=8, column=0, sticky="w", pady=1, padx=10)

        self.precio_venta_entry = tk.Entry(
            self.frame_formulario,
            width=30,
            font=("Arial", 11),
            bd=2,
            relief="groove",
            state="readonly"
        )
        self.precio_venta_entry.grid(row=9, column=0, pady=0, padx=10, sticky="ew")

        # --- Frame para seleccionar productos y sus cantidades ---
        tk.Label(
            self.frame_formulario,
            text="Productos en el lote:",
            bg=self.colores["fondo_frame"],
            fg=self.colores["texto_oscuro"],
            font=("Arial", 11, "bold")
        ).grid(row=10, column=0, sticky="w", pady=2, padx=10)

        # Frame para el Listbox de productos disponibles
        frame_productos = tk.LabelFrame(
            self.frame_formulario,
            text="Productos Disponibles",
            bg=self.colores["fondo_frame"],
            fg=self.colores["texto_oscuro"],
            font=("Arial", 10, "bold"),
            padx=5,
            pady=5,
            bd=2,
            relief="groove"
        )
        frame_productos.grid(row=11, column=0, pady=0, padx=10, sticky="ew")

        # Listbox para productos disponibles
        scrollbar_disponibles = tk.Scrollbar(frame_productos)
        scrollbar_disponibles.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox_disponibles = tk.Listbox(
            frame_productos,
            selectmode=tk.SINGLE,  # Solo un producto a la vez
            height=6,
            width=40,
            font=("Arial", 11),
            bd=2,
            relief="groove",
            yscrollcommand=scrollbar_disponibles.set
        )
        self.listbox_disponibles.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_disponibles.config(command=self.listbox_disponibles.yview)

        # Cargar productos disponibles
        for prod in self.productos:
            self.listbox_disponibles.insert(tk.END, f"{prod[1]} (€{prod[2]:.2f})")

        # Campo para la cantidad del producto seleccionado
        tk.Label(
            self.frame_formulario,
            text="Cantidad:",
            bg=self.colores["fondo_frame"],
            fg=self.colores["texto_oscuro"],
            font=("Arial", 11)
        ).grid(row=12, column=0, sticky="w", pady=3, padx=5)

        # Frame para la cantidad de unidades y el boton de agregar producto.
        self.cantidad_piezas_boton_agregar = tk.Frame(self.frame_formulario, bg=self.colores["fondo_frame"])
        self.cantidad_piezas_boton_agregar.grid(row=13, column=0, sticky="w", pady=0, padx=5)
        
        self.cantidad_entry = tk.Entry(
            self.cantidad_piezas_boton_agregar,
            width=5,
            font=("Arial", 11),
            bd=2,
            relief="groove"
        )
        self.cantidad_entry.pack(side=tk.LEFT, padx=5)
        self.cantidad_entry.insert(0, "1")

        # Botón para agregar el producto seleccionado al lote
        crear_boton(
            self.cantidad_piezas_boton_agregar,
            texto="Agregar Producto",
            ancho=20,
            alto=2,
            relieve="raised",
            border_width=1,
            color_fondo="#3498DB",
            color_texto=self.colores["texto_claro"],
            font=("Arial", 10, "bold"),
            hover_color="#2ECC71",
            comando=self._agregar_producto_al_lote
        ).pack(side=tk.LEFT, padx=15)

        # --- Frame para mostrar los productos del lote con sus cantidades ---
        self.frame_productos_lote = tk.LabelFrame(
            self.frame_formulario,
            text="Productos en el Lote",
            bg=self.colores["fondo_frame"],
            fg=self.colores["texto_oscuro"],
            font=("Arial", 10, "bold"),
            padx=5,
            pady=5,
            bd=2,
            relief="groove"
        )
        self.frame_productos_lote.grid(row=14, column=0, pady=1, padx=5, sticky="ew")

        self.frame_treeview = tk.Frame(self.frame_productos_lote, bg=self.colores["fondo_frame"])
        self.frame_treeview.pack(side=tk.LEFT, fill="both", padx=1, pady=5)
        
        # Treeview para mostrar productos del lote y sus cantidades
        self.tree_productos_lote = ttk.Treeview(
            self.frame_treeview,
            columns=("Producto", "Cantidad", "Costo Unitario", "Costo Total"),
            show="headings",
            height=5  # Limitar la altura para que no ocupe todo el espacio
        )
        self.tree_productos_lote.pack(side=tk.LEFT, expand=True)

        # Configurar columnas del Treeview
        self.tree_productos_lote.heading("Producto", text="Producto")
        self.tree_productos_lote.heading("Cantidad", text="Cant.")
        self.tree_productos_lote.heading("Costo Unitario", text="Costo Unitario")
        self.tree_productos_lote.heading("Costo Total", text="Costo Total")

        self.tree_productos_lote.column("Producto", width=115)
        self.tree_productos_lote.column("Cantidad", width=40)
        self.tree_productos_lote.column("Costo Unitario", width=100)
        self.tree_productos_lote.column("Costo Total", width=90)

        self.frame_botones = tk.Frame(self.frame_productos_lote, bg=self.colores["fondo_frame"])
        self.frame_botones.pack(side=tk.LEFT, fill="y", padx=2, pady=1)

        # --- Frame para los botones (Guardar, Cancelar, Eliminar) ---
        frame_botones = tk.Frame(self.frame_botones, bg=self.colores["fondo_frame"])
        frame_botones.pack()  # Asegurar que esté en la fila 14

        # Configurar el frame_botones para que se expanda
        frame_botones.grid_columnconfigure(0, weight=1)
        frame_botones.grid_columnconfigure(1, weight=1)
        frame_botones.grid_columnconfigure(2, weight=1)

        # Botones
        crear_boton(
            frame_botones,
            texto="Guardar Lote",
            ancho=15,
            alto=2,
            relieve="raised",
            border_width=1,
            color_fondo=self.colores["boton_guardar"],
            color_texto=self.colores["texto_claro"],
            font=("Arial", 10, "bold"),
            hover_color="#2ECC71",
            comando=self._guardar_lote
        ).pack(side=tk.BOTTOM, pady=5)  # Usar grid en lugar de pack

        crear_boton(
            frame_botones,
            texto="Cancelar",
            ancho=15,
            alto=2,
            relieve="raised",
            border_width=1,
            color_fondo=self.colores["boton_volver"],
            color_texto=self.colores["texto_claro"],
            font=("Arial", 10, "bold"),
            hover_color="#222423",
            comando=self._limpiar_formulario
        ).pack(side=tk.BOTTOM, pady=5)  # Usar grid en lugar de pack

        # self.boton_eliminar = crear_boton(
        #     frame_botones,
        #     texto="Eliminar Lote",
        #     ancho=15,
        #     alto=2,
        #     relieve="raised",
        #     border_width=1,
        #     color_fondo=self.colores["boton_eliminar"],
        #     color_texto=self.colores["texto_claro"],
        #     font=("Arial", 10, "bold"),
        #     hover_color="#E74C3C",
        #     comando=self._confirmar_eliminar_lote,
        # )
        # self.boton_eliminar.configure(state=tk.DISABLED)
        # self.boton_eliminar.pack(side=tk.BOTTOM, pady=5)
        
        # Botón para eliminar un producto del lote
        crear_boton(
            self.frame_botones,
            texto="Quitar Producto de lista",
            ancho=50,
            alto=2,
            relieve="raised",
            border_width=1,
            color_fondo="#E74C3C",
            color_texto=self.colores["texto_claro"],
            font=("Arial", 10, "bold"),
            hover_color="#E74C3C",
            comando=self._eliminar_producto_del_lote
        ).pack(side=tk.BOTTOM, padx=5, pady=20)

    def _agregar_producto_al_lote(self):
        """Agrega el producto seleccionado al lote con su cantidad."""
        seleccion = self.listbox_disponibles.curselection()
        if not seleccion:
            messagebox.showerror("⚠️ Error", "Debes seleccionar un producto.")
            return

        try:
            cantidad = int(self.cantidad_entry.get())
            if cantidad <= 0:
                messagebox.showerror("⚠️ Error", "La cantidad debe ser mayor que 0.")
                return
        except ValueError:
            messagebox.showerror("⚠️ Error", "La cantidad debe ser un número válido.")
            return

        # Obtener el producto seleccionado
        prod_str = self.listbox_disponibles.get(seleccion[0])
        codigo_producto = prod_str.split(" ")[0] # Si existe un espacio en el código se generara un error.
        producto = next((p for p in self.productos if p[1] == codigo_producto), None)

        if not producto:
            messagebox.showerror("⚠️ Error", "No se encontró el producto seleccionado.")
            return

        # Verificar si el producto ya está en el lote
        for item in self.tree_productos_lote.get_children():
            valores = self.tree_productos_lote.item(item, "values")
            if valores[0] == prod_str:
                messagebox.showerror("⚠️ Error", "Este producto ya está en el lote. Usa el botón 'Eliminar' para modificarlo.")
                return

        # Agregar el producto al Treeview
        costo_unitario = float(producto[2])
        costo_total = costo_unitario * cantidad

        self.tree_productos_lote.insert(
            "",
            tk.END,
            values=(prod_str, cantidad, f"€{costo_unitario:.2f}", f"€{costo_total:.2f}")
        )

        # Limpiar la selección y el campo de cantidad
        self.listbox_disponibles.selection_clear(seleccion[0])
        self.cantidad_entry.delete(0, tk.END)
        self.cantidad_entry.insert(0, "1")

        # Actualizar el costo total del lote
        self._actualizar_costo_y_precio()

    def _eliminar_producto_del_lote(self):
        """Elimina el producto seleccionado del lote."""
        seleccion = self.tree_productos_lote.selection()
        if not seleccion:
            messagebox.showerror("⚠️ Error", "Debes seleccionar un producto del lote.")
            return

        self.tree_productos_lote.delete(seleccion[0])
        self._actualizar_costo_y_precio()

    def _actualizar_costo_y_precio(self):
        """Actualiza el costo total del lote y el precio de venta sugerido."""
        costo_total = 0.0

        # Sumar el costo de todos los productos en el lote
        for item in self.tree_productos_lote.get_children():
            valores = self.tree_productos_lote.item(item, "values")
            costo_producto = float(valores[3].replace("€", "").replace(",", "."))
            costo_total += costo_producto

        # Actualizar el campo de costo del lote
        self.costo_entry.config(state="normal")
        self.costo_entry.delete(0, tk.END)
        self.costo_entry.insert(0, f"{costo_total:.2f}")
        self.costo_entry.config(state="readonly")

        # Actualizar el precio de venta sugerido (5x el costo)
        precio_venta = costo_total * 5
        self.precio_venta_entry.config(state="normal")
        self.precio_venta_entry.delete(0, tk.END)
        self.precio_venta_entry.insert(0, f"{precio_venta:.2f}")
        self.precio_venta_entry.config(state="readonly")

        # Actualizar el campo de unidades totales (suma de todas las cantidades)
        unidades_totales = 0
        for item in self.tree_productos_lote.get_children():
            valores = self.tree_productos_lote.item(item, "values")
            unidades_totales += int(valores[1])

        self.unidades_entry.delete(0, tk.END)
        self.unidades_entry.insert(0, unidades_totales)
    
    def _on_lote_seleccionado(self, event):
        """Carga los datos del lote seleccionado en el formulario."""
        seleccion = self.tree_lotes.selection()
        print(f"El lote seleccionado es: {seleccion}")###################################################################
        if not seleccion:
            return
        
        lote_id = int(self.tree_lotes.item(seleccion[0], "values")[0])
        self.lote_seleccionado = next((l for l in self.lotes if l[0] == lote_id), None)
        
        if self.lote_seleccionado:
            # Cargar datos en el formulario
            self.codigo_entry.delete(0, tk.END)
            self.codigo_entry.insert(0, self.lote_seleccionado[1])
            self.descripcion_entry.delete(0, tk.END)
            self.descripcion_entry.insert(0, self.lote_seleccionado[2])
            self.unidades_entry.delete(0, tk.END)
            self.unidades_entry.insert(0, self.lote_seleccionado[3])
            self.costo_entry.delete(0, tk.END)
            self.costo_entry.insert(0, self.lote_seleccionado[4])

            # Cargar productos del lote
            self._cargar_productos_del_lote(lote_id)

            # Habilitar botón de eliminar
            self.boton_eliminar.config(state=tk.NORMAL)

    def _cargar_productos_del_lote(self, lote_id):
        """Carga los productos y sus cantidades asociados al lote en el Treeview."""
        # Limpiar el Treeview
        for item in self.tree_productos_lote.get_children():
            self.tree_productos_lote.delete(item)

        # Obtener productos del lote con sus cantidades
        productos_lote = self.db_connect.obtener_productos_del_lote_con_cantidades(lote_id)
        if not productos_lote:
            return
        print(f"Los productos_lote: {productos_lote}")
        # Agregar productos al Treeview
        for prod in productos_lote:
            id_producto, codigo, cantidad = prod
            producto = next((p for p in self.productos if p[0] == id_producto), None)
            if producto:
                costo_unitario = float(producto[2])
                costo_total = costo_unitario * cantidad
                self.tree_productos_lote.insert(
                    "",
                    tk.END,
                    values=(f"{codigo} (€{costo_unitario:.2f})", cantidad, f"€{costo_unitario:.2f}", f"€{costo_total:.2f}")
                )

        # Actualizar el costo total del lote
        self._actualizar_costo_y_precio()

    def _limpiar_formulario(self):
        """Limpia el formulario para crear un nuevo lote."""
        self.lote_seleccionado = None
        self.codigo_entry.delete(0, tk.END)
        self.descripcion_entry.delete(0, tk.END)
        self.unidades_entry.delete(0, tk.END)
        self.costo_entry.config(state="normal")
        self.costo_entry.delete(0, tk.END)
        self.costo_entry.config(state="readonly")
        self.precio_venta_entry.config(state="normal")
        self.precio_venta_entry.delete(0, tk.END)
        self.precio_venta_entry.config(state="readonly")
        self.precio_venta_entry.insert(0, "0.00")
        self.cantidad_entry.delete(0, tk.END)
        self.cantidad_entry.insert(0, "1")

        # Limpiar el Treeview de productos del lote
        for item in self.tree_productos_lote.get_children():
            self.tree_productos_lote.delete(item)

        self.boton_eliminar.config(state=tk.DISABLED)

    def _actualizar_lista_lotes(self):
        """Actualiza la lista de lotes desde la base de datos."""
        self.lotes = self.db_connect.obtener_lotes_con_productos()
        self._cargar_lotes_en_treeview()
        # Desabilitar botón de eliminar
        self.boton_eliminar.config(state=tk.DISABLED)

    def _cargar_lotes_en_treeview(self):
        """Carga los lotes en el Treeview."""
        self.tree_lotes.delete(*self.tree_lotes.get_children())
        for lote in self.lotes:
            lote_id, codigo_lote, descripcion, unidades, costo, precio = lote
            self.tree_lotes.insert(
                "",
                tk.END,
                values=(lote_id, codigo_lote, descripcion, unidades, f"€{costo:.2f}", f"€{precio}")
            )

    def _guardar_lote(self):
        """Guarda el lote con productos y cantidades individuales."""
        try:
            codigo = self.codigo_entry.get()
            descripcion = self.descripcion_entry.get()
            unidades = int(self.unidades_entry.get())
            costo = float(self.costo_entry.get())
            precio_total = float(self.precio_venta_entry.get())
            if unidades <= 0 or costo <= 0:
                messagebox.showerror("⚠️ Error", "Unidades y costo deben ser mayores que 0.")
                return

            # Obtener los productos del lote desde el Treeview
            productos_lote = []
            for item in self.tree_productos_lote.get_children():
                valores = self.tree_productos_lote.item(item, "values")
                prod_str = valores[0]
                cantidad = int(valores[1])
                productos_lote.append((prod_str, cantidad))
            if not productos_lote:
                messagebox.showerror("⚠️ Error", "Debes agregar al menos un producto al lote.")
                return

            if self.lote_seleccionado:
                # Actualizar lote existente
                lote_id = self.lote_seleccionado[0]
                self.db_connect.actualizar_lote(lote_id, codigo, descripcion, unidades, costo, precio_total)

                # Eliminar productos antiguos del lote
                self.db_connect.eliminar_lote_productos(lote_id)

                # Insertar productos en el lote con sus cantidades
                for prod_str, cantidad in productos_lote:
                    codigo_producto = prod_str.split(" ")[0]
                    producto = next(
                        (p for p in self.productos if p[1] == codigo_producto),
                        None
                    )
                    if producto:
                        self.db_connect.registrar_lote_productos(lote_id, producto[0], cantidad)

                messagebox.showinfo("✅ Éxito", "Lote actualizado correctamente.")
            else:
                # Crear nuevo lote
                lote_id = self.db_connect.insertar_lote(codigo, descripcion, unidades, costo, precio_total)
                
                for prod_str, cantidad in productos_lote:
                    codigo_producto = prod_str.split(" ")[0]
                    producto = next(
                        (p for p in self.productos if p[1] == codigo_producto),
                        None
                    )
                    if producto:
                        self.db_connect.registrar_lote_productos(lote_id, producto[0], cantidad)

                        messagebox.showinfo("✅ Éxito", "Lote creado correctamente.")

            # Actualizar la lista y limpiar el formulario
            self._actualizar_lista_lotes()
            self._limpiar_formulario()

        except ValueError:
            messagebox.showerror("⚠️ Error", "Unidades y costo deben ser números válidos.")
        except Exception as e:
            messagebox.showerror("⚠️ Error", f"Ocurrió un error: {e}")
            
    def _calcular_costo_lote(self):
        """Calcula el costo total del lote basado en los productos seleccionados y sus cantidades."""
        try:
            costo_total = 0.0
            productos_seleccionados = [self.productos_listbox.get(i) for i in self.productos_listbox.curselection()]

            if not productos_seleccionados:
                self.costo_entry.delete(0, tk.END)
                self.costo_entry.insert(0, "0.00")
                return 0.0

            cantidad = int(self.cantidad_entry.get()) if self.cantidad_entry.get() else 1

            for prod_str in productos_seleccionados:
                # Extraer el código del producto (ej: "P001 (€5.00)" -> "P001")
                codigo_producto = prod_str.split(" ")[0]

                # Buscar el producto en la lista de productos
                producto = next((p for p in self.productos if p[1] == codigo_producto), None)
                if producto:
                    costo_producto = float(producto[2])  # costo del producto
                    costo_total += costo_producto * cantidad

            # Actualizar el campo de costo del lote
            self.costo_entry.delete(0, tk.END)
            self.costo_entry.insert(0, f"{costo_total:.2f}")

            return costo_total

        except ValueError:
            messagebox.showerror("⚠️ Error", "La cantidad debe ser un número válido.")
            return 0.0
        except Exception as e:
            messagebox.showerror("⚠️ Error", f"Error al calcular el costo del lote: {e}")
            return 0.0

    def _calcular_precio_venta_sugerido(self, costo_total):
        """Calcula el precio de venta sugerido (5x el costo, como mencionaste)."""
        return costo_total * 5  # Margen de 5x (puedes ajustarlo)
        
    def _confirmar_eliminar_lote(self):
        """Confirma la eliminación del lote seleccionado."""
        if not self.lote_seleccionado:
            messagebox.showerror("⚠️ Error", "Debes seleccionar un lote para eliminar.")
            return

        if messagebox.askyesno("Confirmar", f"¿Estás seguro de que deseas eliminar el lote {self.lote_seleccionado[0]}?"):
            self._eliminar_lote(self.lote_seleccionado[0])

    def _eliminar_lote(self, lote_id):
        """Elimina un lote de la base de datos."""
        try:
            confimacion_lote_producto = self.db_connect.eliminar_lote_productos(lote_id)
            confirmacion_lotes = self.db_connect.eliminar_lote(lote_id)
            if self._confirmar_eliminar_lote and confirmacion_lotes:
                messagebox.showinfo("✅ Éxito", f"El lote {lote_id} ha sido eliminado correctamente.")
            self._actualizar_lista_lotes()
            self._limpiar_formulario()
        except Exception as e:
            messagebox.showerror("⚠️ Error", f"No se pudo eliminar el lote: {e}")

        
class ProductoManager:
    def __init__(self, root, db, colores):
        self.root = root
        self.db_connect = db
        self.colores = colores

    def abrir_actualizar_costo_por_unidad(self, root, mostrar_menu_principal, imagen_panel_tk, rol, imagen_tk, content_frame): #, info_frame=None):
        """Abre el formulario para actualizar el costo por unidad de un producto."""
        # Limpiar el frame de contenido
        for widget in content_frame.winfo_children():
            widget.destroy()

        # Frame principal del formulario
        form_frame = tk.LabelFrame(
            content_frame,
            text="Act. Costo por Unidad",
            bg=self.colores["fondo_frame"],
            fg=self.colores["texto_oscuro"],
            font=("Arial", 12, "bold"),
            padx=20,
            pady=20,
            bd=2,
            relief="groove"
        )
        form_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Dropdown para seleccionar producto
        tk.Label(
            form_frame,
            text="Selecciona el producto:",
            bg=self.colores["fondo_frame"],
            fg=self.colores["texto_oscuro"],
            font=("Arial", 11)
        ).grid(row=0, column=0, sticky="w", pady=5, padx=10)

        productos = self.db_connect.obtener_productos_para_costoventa()
        if not productos:
            tk.Label(
                form_frame,
                text="No hay productos registrados.",
                font=("Arial", 12),
                bg=self.colores["fondo_frame"],
                fg=self.colores["texto_oscuro"]
            ).grid(row=1, column=0, pady=20)
            return

        producto_var = [f"{prod[1]} (Costo actual: €{prod[2]:.2f})" for prod in productos]
        producto_dropdown = ttk.Combobox(
            form_frame,
            values=producto_var,
            state="readonly",
            font=("Arial", 10),
            width=30
        )
        producto_dropdown.grid(row=1, column=0, pady=5, padx=10, sticky="ew")

        # Campo para el nuevo costo
        tk.Label(
            form_frame,
            text="Nuevo costo de producción:",
            bg=self.colores["fondo_frame"],
            fg=self.colores["texto_oscuro"],
            font=("Arial", 11)
        ).grid(row=2, column=0, sticky="w", pady=5, padx=10)

        nuevo_costo_entry = tk.Entry(
            form_frame,
            width=30,
            font=("Arial", 11),
            bd=2,
            relief="groove"
        )
        nuevo_costo_entry.grid(row=3, column=0, pady=5, padx=10, sticky="ew")

        # Checkbutton para recalcular precio de venta
        recalcular_precio_var = tk.IntVar()
        recalcular_precio_check = tk.Checkbutton(
            form_frame,
            text="Recalcular precio de venta",
            variable=recalcular_precio_var,
            bg=self.colores["fondo_frame"],
            fg=self.colores["texto_oscuro"],
            font=("Arial", 11),
            selectcolor=self.colores["fondo_frame"],
            command=lambda: self._toggle_recalculo_frame(recalcular_precio_var.get(), form_frame)
        )
        recalcular_precio_check.grid(row=4, column=0, sticky="w", pady=10, padx=10)

        # Frame para método y parámetro (oculto inicialmente)
        self.recalculo_frame = tk.Frame(form_frame, bg=self.colores["fondo_frame"])

        # Dropdown para seleccionar método de recálculo
        tk.Label(
            self.recalculo_frame,
            text="Selecciona el método:",
            bg=self.colores["fondo_frame"],
            fg=self.colores["texto_oscuro"],
            font=("Arial", 11)
        ).grid(row=0, column=0, sticky="w", pady=5, padx=10)

        metodo_var = tk.StringVar()
        metodo_dropdown = tk.OptionMenu(
            self.recalculo_frame,
            metodo_var,
            "factor",
            "margen",
            "formula"
        )
        metodo_dropdown.config(
            bg=self.colores["fondo_frame"],
            fg=self.colores["texto_oscuro"],
            font=("Arial", 10),
            bd=2,
            relief="groove",
            width=20
        )
        metodo_dropdown.grid(row=1, column=0, pady=5, padx=10, sticky="ew")

        # Campo para el parámetro
        tk.Label(
            self.recalculo_frame,
            text="Parámetro:",
            bg=self.colores["fondo_frame"],
            fg=self.colores["texto_oscuro"],
            font=("Arial", 11)
        ).grid(row=2, column=0, sticky="w", pady=5, padx=10)

        parametro_entry = tk.Entry(
            self.recalculo_frame,
            width=30,
            font=("Arial", 11),
            bd=2,
            relief="groove"
        )
        parametro_entry.grid(row=3, column=0, pady=5, padx=10, sticky="ew")

        # Label dinámico para el parámetro
        tipo_parametro_label = tk.Label(
            self.recalculo_frame,
            text="",
            bg=self.colores["fondo_frame"],
            fg="#3498DB",
            font=("Arial", 10, "italic")
        )
        tipo_parametro_label.grid(row=4, column=0, sticky="w", pady=5, padx=10)

        def actualizar_tipo_parametro(*args):
            metodo = metodo_var.get()
            if metodo == "factor":
                tipo_parametro_label.config(text="Ejemplo: 2, 3, 4, 5")
            elif metodo == "margen":
                tipo_parametro_label.config(text="Ejemplo: 50, 100, 150 (porcentaje)")
            elif metodo == "formula":
                tipo_parametro_label.config(text="Ejemplo: 2, 3, 4, 5 (multiplicador)")

        metodo_var.trace_add("write", actualizar_tipo_parametro)

        # Botón para actualizar costo
        crear_boton(
            form_frame,
            texto="Actualizar Costo",
            ancho=20,
            alto=2,
            relieve="raised",
            border_width=1,
            color_fondo=self.colores["boton_guardar"],
            color_texto=self.colores["texto_claro"],
            font=("Arial", 11, "bold"),
            hover_color="#2ECC71",
            comando=lambda: self._actualizar_costo_produccion(
                producto_dropdown.get(),
                nuevo_costo_entry.get(),
                recalcular_precio_var.get(),
                metodo_var.get() if recalcular_precio_var.get() else None,
                parametro_entry.get() if recalcular_precio_var.get() else None,
                "unidad",
                None,
                None,
                None
            )
        ).grid(row=5, column=0, pady=20, sticky="w")


    def _toggle_recalculo_frame(self, visible, parent_frame):
        """Muestra u oculta el frame de recálculo de precio."""
        if visible:
            self.recalculo_frame.grid(row=5, column=0, sticky="ew", pady=(0, 15), padx=10)
        else:
            self.recalculo_frame.grid_forget()

    def _actualizar_costo_produccion(self, producto_str, nuevo_costo_str, recalcular_precio, metodo, parametro_str, tipo_costo, unidades_str, lote_str, unidades_lote_str):
        """Actualiza el costo de producción de un producto."""
        try:
            if not producto_str:
                messagebox.showerror("⚠️ Error", "Debes seleccionar un producto.")
                return

            codigo_producto = producto_str.split(" ")[0]
            if not nuevo_costo_str:
                messagebox.showerror("⚠️ Error", "Debes ingresar un nuevo costo.")
                return

            nuevo_costo = self._convertir_a_float(nuevo_costo_str)
            producto = self.db_connect.datos_costo_d_producto_actualizar(codigo_producto)
            if producto is None:
                return

            id_producto, costo_actual, precio_venta_actual = producto[0]

            unidades = None
            if tipo_costo == "lote":
                if not unidades_str:
                    messagebox.showerror("⚠️ Error", "Debes ingresar el número de unidades en el lote.")
                    return
                try:
                    unidades = int(unidades_str)
                except ValueError:
                    messagebox.showerror("⚠️ Error", "El número de unidades debe ser un entero válido.")
                    return

            if lote_str:
                id_lote = int(lote_str.split(" - ")[0])
                if not unidades_lote_str:
                    messagebox.showerror("⚠️ Error", "Debes ingresar el número de unidades del producto en el lote.")
                    return
                try:
                    unidades_lote = int(unidades_lote_str)
                    self.db_connect.registrar_lote_productos(id_lote, id_producto, unidades_lote)
                except ValueError:
                    messagebox.showerror("⚠️ Error", "El número de unidades del producto en el lote debe ser un entero válido.")
                    return

            costo_nuevo = self.db_connect.actualizar_costo_producto(nuevo_costo, id_producto)
            if costo_nuevo:
                messagebox.showinfo("✅ Éxito", "El nuevo costo del producto se actualizó correctamente.")
            else:
                messagebox.showerror("⚠️ Error", "No se ha podido actualizar el nuevo costo del producto.")
                nuevo_costo = costo_actual

            self.db_connect.registrar_historial_costo(
                id_producto=id_producto,
                costo_anterior=costo_actual,
                costo_nuevo=nuevo_costo,
                es_por_lote=(tipo_costo == "lote"),
                unidades=unidades,
                motivo=f"Actualización manual. Método de recálculo: {metodo}" if recalcular_precio else "Actualización manual"
            )

            if recalcular_precio:
                if not metodo or not parametro_str:
                    messagebox.showerror("⚠️ Error", "Debes seleccionar un método e ingresar un parámetro.")
                    return
                try:
                    parametro = float(parametro_str)
                except ValueError:
                    messagebox.showerror("⚠️ Error", "El parámetro debe ser un número válido.")
                    return

                if metodo == "factor":
                    nuevo_precio = nuevo_costo * parametro
                elif metodo == "margen":
                    nuevo_precio = nuevo_costo * (1 + parametro / 100)
                elif metodo == "formula":
                    nuevo_precio = nuevo_costo + (nuevo_costo * 1) * parametro

                precio_actualizado = self.db_connect.actualizar_precio_venta(nuevo_precio, id_producto)
                if not precio_actualizado:
                    nuevo_precio = costo_actual * 5

                messagebox.showinfo(
                    "✅ Éxito",
                    f"Costo y precio actualizados:\n"
                    f"Producto: {codigo_producto}\n"
                    f"Costo anterior: €{costo_actual:.2f}\n"
                    f"Nuevo costo: €{nuevo_costo:.2f}\n"
                    f"Nuevo precio: €{nuevo_precio:.2f}"
                )
            else:
                messagebox.showinfo(
                    "✅ Éxito",
                    f"Costo de producción actualizado:\n"
                    f"Producto: {codigo_producto}\n"
                    f"Costo anterior: €{costo_actual:.2f}\n"
                    f"Nuevo costo: €{nuevo_costo:.2f}"
                )
        except ValueError:
            messagebox.showerror("⚠️ Error", "El nuevo costo debe ser un número válido.")
        except Exception as e:
            messagebox.showerror("⚠️ Error", f"Ocurrió un error: {e}")

    def _convertir_a_float(self, valor_str):
        """Convierte un string a float, reemplazando comas por puntos."""
        try:
            valor_str = str(valor_str).replace(",", ".")
            return float(valor_str)
        except ValueError:
            messagebox.showerror("⚠️ Error", f"'{valor_str}' no es un número válido.")
            return None

    def abrir_actualizar_costo_por_lote(self, root, mostrar_menu_principal, imagen_panel_tk, rol, imagen_tk, content_frame): #, info_frame=None):
        """Abre el formulario para actualizar el costo por lote."""
        # Limpiar el frame de contenido
        for widget in content_frame.winfo_children():
            widget.destroy()

        # Frame principal del formulario
        form_frame = tk.LabelFrame(
            content_frame,
            text="Act. Costo por Lote",
            bg=self.colores["fondo_frame"],
            fg=self.colores["texto_oscuro"],
            font=("Arial", 12, "bold"),
            padx=20,
            pady=20,
            bd=2,
            relief="groove"
        )
        form_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Botón para crear un nuevo lote
        # crear_boton(
        #     form_frame,
        #     texto="Crear Nuevo Lote",
        #     ancho=20,
        #     alto=2,
        #     relieve="raised",
        #     border_width=1,
        #     color_fondo="#1C4A8F",
        #     color_texto=self.colores["texto_claro"],
        #     font=("Arial", 11, "bold"),
        #     hover_color="#2ECC71",
        #     comando=lambda: LoteManager(self.root, self.db_connect, self.colores)._abrir_formulario_crear_lote(content_frame)
        # ).grid(row=0, column=0, pady=10, sticky="ew")

        # Dropdown para seleccionar lote
        tk.Label(
            form_frame,
            text="Selecciona el lote:",
            bg=self.colores["fondo_frame"],
            fg=self.colores["texto_oscuro"],
            font=("Arial", 11)
        ).grid(row=1, column=0, sticky="w", pady=5, padx=10)

        lotes = self.db_connect.obtener_lotes()
        if lotes:
            lote_vars = [f"{lote[0]} - {lote[2]}" for lote in lotes]
            lote_var = tk.StringVar()
            lote_dropdown = tk.OptionMenu(
                form_frame,
                lote_var,
                *lote_vars,
                command=lambda lote: self._mostrar_costo_actual_lote(lote, form_frame)
            )
            lote_dropdown.config(
                bg=self.colores["fondo_frame"],
                fg=self.colores["texto_oscuro"],
                font=("Arial", 10),
                bd=2,
                relief="groove",
                width=40
            )
            lote_dropdown.grid(row=2, column=0, pady=5, padx=10, sticky="ew")

        # Etiqueta para mostrar el costo actual del lote
        self.costo_actual_lote_label = tk.Label(
            form_frame,
            text="Costo actual del lote: ",
            bg=self.colores["fondo_frame"],
            fg=self.colores["texto_oscuro"],
            font=("Arial", 11)
        )
        self.costo_actual_lote_label.grid(row=3, column=0, sticky="w", pady=5, padx=10)

        # Campo para ingresar el nuevo costo de producción por lote
        tk.Label(
            form_frame,
            text="Nuevo costo de producción por lote:",
            bg=self.colores["fondo_frame"],
            fg=self.colores["texto_oscuro"],
            font=("Arial", 11)
        ).grid(row=4, column=0, sticky="w", pady=5, padx=10)

        nuevo_costo_lote_entry = tk.Entry(
            form_frame,
            width=30,
            font=("Arial", 11),
            bd=2,
            relief="groove"
        )
        nuevo_costo_lote_entry.grid(row=5, column=0, pady=5, padx=10, sticky="ew")

        # Checkbutton para recalcular precio de venta
        recalcular_precio_var = tk.IntVar()
        recalcular_precio_check = tk.Checkbutton(
            form_frame,
            text="Recalcular precio de venta",
            variable=recalcular_precio_var,
            bg=self.colores["fondo_frame"],
            fg=self.colores["texto_oscuro"],
            font=("Arial", 11),
            selectcolor=self.colores["fondo_frame"],
            command=lambda: self._toggle_recalculo_frame_lote(recalcular_precio_var.get(), form_frame)
        )
        recalcular_precio_check.grid(row=6, column=0, sticky="w", pady=10, padx=10)

        # Frame para método y parámetro (oculto inicialmente)
        self.recalculo_frame_lote = tk.Frame(form_frame, bg=self.colores["fondo_frame"])

        # Dropdown para seleccionar método de recálculo
        tk.Label(
            self.recalculo_frame_lote,
            text="Selecciona el método:",
            bg=self.colores["fondo_frame"],
            fg=self.colores["texto_oscuro"],
            font=("Arial", 11)
        ).grid(row=0, column=0, sticky="w", pady=5, padx=10)

        metodo_var = tk.StringVar()
        metodo_dropdown = tk.OptionMenu(
            self.recalculo_frame_lote,
            metodo_var,
            "factor",
            "margen",
            "formula"
        )
        metodo_dropdown.config(
            bg=self.colores["fondo_frame"],
            fg=self.colores["texto_oscuro"],
            font=("Arial", 10),
            bd=2,
            relief="groove",
            width=20
        )
        metodo_dropdown.grid(row=1, column=0, pady=5, padx=10, sticky="ew")

        # Campo para el parámetro
        tk.Label(
            self.recalculo_frame_lote,
            text="Parámetro:",
            bg=self.colores["fondo_frame"],
            fg=self.colores["texto_oscuro"],
            font=("Arial", 11)
        ).grid(row=2, column=0, sticky="w", pady=5, padx=10)

        parametro_entry = tk.Entry(
            self.recalculo_frame_lote,
            width=30,
            font=("Arial", 11),
            bd=2,
            relief="groove"
        )
        parametro_entry.grid(row=3, column=0, pady=5, padx=10, sticky="ew")

        # Label dinámico para el parámetro
        tipo_parametro_label = tk.Label(
            self.recalculo_frame_lote,
            text="",
            bg=self.colores["fondo_frame"],
            fg="#3498DB",
            font=("Arial", 10, "italic")
        )
        tipo_parametro_label.grid(row=4, column=0, sticky="w", pady=5, padx=10)

        def actualizar_tipo_parametro(*args):
            metodo = metodo_var.get()
            if metodo == "factor":
                tipo_parametro_label.config(text="Ejemplo: 2, 3, 4, 5")
            elif metodo == "margen":
                tipo_parametro_label.config(text="Ejemplo: 50, 100, 150 (porcentaje)")
            elif metodo == "formula":
                tipo_parametro_label.config(text="Ejemplo: 2, 3, 4, 5 (multiplicador)")

        metodo_var.trace_add("write", actualizar_tipo_parametro)

        # Botón para actualizar costo
        crear_boton(
            form_frame,
            texto="Actualizar Costo",
            ancho=20,
            alto=2,
            relieve="raised",
            border_width=1,
            color_fondo=self.colores["boton_guardar"],
            color_texto=self.colores["texto_claro"],
            font=("Arial", 11, "bold"),
            hover_color="#2ECC71",
            comando=lambda: self._actualizar_costo_de_lote(
                nuevo_costo_lote_entry.get(),
                recalcular_precio_var.get(),
                metodo_var.get() if recalcular_precio_var.get() else None,
                parametro_entry.get() if recalcular_precio_var.get() else None,
                "lote",
                lote_var.get(),
            )
        ).grid(row=7, column=0, pady=20, sticky="w")


    def _toggle_recalculo_frame_lote(self, visible, parent_frame):
        """Muestra u oculta el frame de recálculo de precio para lotes."""
        if visible:
            self.recalculo_frame_lote.grid(row=7, column=0, sticky="ew", pady=(0, 15), padx=10)
        else:
            self.recalculo_frame_lote.grid_forget()

    def _mostrar_costo_actual_lote(self, lote_str, parent_frame):
        """Muestra el costo actual del lote seleccionado."""
        if lote_str and lote_str != "No hay lotes disponibles":
            id_lote = int(lote_str.split(" - ")[0])
            costo_actual = self.db_connect.obtener_costo_actual_lote(id_lote)
            self.costo_actual_lote_label.config(text=f"Costo actual del lote: €{costo_actual:.2f}")
        else:
            self.costo_actual_lote_label.config(text="Costo actual del lote: ")

    def _actualizar_costo_de_lote(self, nuevo_costo_str, recalcular_precio, metodo, parametro_str, tipo_costo, lote_str):
        """Actualiza el costo de un lote y opcionalmente recalcula el precio de venta."""
        try:
            if not nuevo_costo_str:
                messagebox.showerror("⚠️ Error", "Debes ingresar un nuevo costo.")
                return

            nuevo_costo = self._convertir_a_float(nuevo_costo_str)
            if tipo_costo == "lote":
                if not lote_str or lote_str == "No hay lotes disponibles":
                    messagebox.showerror("⚠️ Error", "Debes seleccionar un lote.")
                    return

                id_lote = int(lote_str.split(" - ")[0])
                costo_anterior = self.db_connect.costo_anterior_lote(id_lote)

                # Actualizar el costo del lote
                self.db_connect.actualizar_costo_lote(nuevo_costo, id_lote)

                if recalcular_precio:
                    if not metodo or not parametro_str:
                        messagebox.showerror("⚠️ Error", "Debes seleccionar un método e ingresar un parámetro.")
                        return
                    try:
                        parametro = float(parametro_str)
                    except ValueError:
                        messagebox.showerror("⚠️ Error", "El parámetro debe ser un número válido.")
                        return

                    # Calcular el nuevo precio según el método
                    if metodo == "factor":
                        nuevo_precio = nuevo_costo * parametro
                    elif metodo == "margen":
                        nuevo_precio = nuevo_costo * (1 + parametro / 100)
                    elif metodo == "formula":
                        nuevo_precio = nuevo_costo + (nuevo_costo * 1) * parametro

                    # Actualizar el precio de venta del lote
                    self.db_connect.actualiza_precio_venta_lote(nuevo_precio, id_lote)

                    messagebox.showinfo(
                        "✅ Éxito",
                        f"Costo y precio de venta del lote actualizados:\n"
                        f"Costo anterior: €{costo_anterior:.2f}\n"
                        f"Nuevo costo: €{nuevo_costo:.2f}\n"
                        f"Nuevo precio de venta: €{nuevo_precio:.2f}"
                    )
                else:
                    messagebox.showinfo(
                        "✅ Éxito",
                        f"Costo del lote actualizado:\n"
                        f"Costo anterior: €{costo_anterior:.2f}\n"
                        f"Nuevo costo: €{nuevo_costo:.2f}"
                    )
        except ValueError:
            messagebox.showerror("⚠️ Error", "El nuevo costo debe ser un número válido.")
        except Exception as e:
            messagebox.showerror("⚠️ Error", f"Ocurrió un error: {e}")
            

class HistorialManager:
    def __init__(self, root, db, colores):
        self.root = root
        self.db_connect = db
        self.colores = colores

    def abrir_actualizar_historial(self, root, mostrar_menu_principal, imagen_panel_tk, rol, imagen_tk, content_frame): #, info_frame=None):
        """Abre el formulario para actualizar el historial de ganancias."""
        # Limpiar el frame de contenido
        for widget in content_frame.winfo_children():
            widget.destroy()

        # Frame principal del formulario
        form_frame = tk.LabelFrame(
            content_frame,
            text="Actualizar Historial de Ganancias",
            bg=self.colores["fondo_frame"],
            fg=self.colores["texto_oscuro"],
            font=("Arial", 12, "bold"),
            padx=20,
            pady=20,
            bd=2,
            relief="groove"
        )
        form_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Label para seleccionar fecha
        tk.Label(
            form_frame,
            text="Selecciona el mes y año:",
            bg=self.colores["fondo_frame"],
            fg=self.colores["texto_oscuro"],
            font=("Arial", 11)
        ).grid(row=0, column=0, sticky="w", pady=5, padx=10)

        # Frame para el calendario
        cal_frame = tk.Frame(form_frame, bg=self.colores["fondo_frame"])
        cal_frame.grid(row=1, column=0, pady=10, padx=10, sticky="ew")

        # Calendario
        cal = Calendar(
            cal_frame,
            selectmode="day",
            year=2026,
            month=5,
            date_pattern="dd/MM/yyyy",
            background="#E0F2F7",
            foreground=self.colores["texto_oscuro"],
            headersbackground="#3498DB",
            headersforeground="white",
            selectbackground="#3498DB",
            selectforeground="white",
            normalbackground="#E0F2F7",
            normalforeground=self.colores["texto_oscuro"],
            weekendbackground="#E0F2F7",
            weekendforeground="#E74C3C",
            font=("Arial", 10)
        )
        cal.pack()

        # Botón para calcular ganancias
        crear_boton(
            form_frame,
            texto="Calcular Ganancias",
            ancho=20,
            alto=2,
            relieve="raised",
            border_width=1,
            color_fondo=self.colores["boton_guardar"],
            color_texto=self.colores["texto_claro"],
            font=("Arial", 11, "bold"),
            hover_color="#2ECC71",
            comando=lambda: self._calcular_y_guardar_ganancias(cal.get_date(), form_frame)
        ).grid(row=2, column=0, pady=20, sticky="ew")

        # Área para mostrar resultados
        resultado_frame = tk.LabelFrame(
            form_frame,
            text="Resultados",
            bg=self.colores["fondo_frame"],
            fg=self.colores["texto_oscuro"],
            font=("Arial", 11, "bold"),
            padx=10,
            pady=10,
            bd=2,
            relief="groove"
        )
        resultado_frame.grid(row=3, column=0, pady=10, padx=10, sticky="ew")

        self.resultado_text = tk.Text(
            resultado_frame,
            height=10,
            width=60,
            state="disabled",
            bg="#d8dfee",
            fg=self.colores["texto_oscuro"],
            font=("Arial", 10),
            bd=2,
            relief="groove",
            padx=10,
            pady=10
        )
        self.resultado_text.pack()
        

    def _calcular_y_guardar_ganancias(self, fecha_str, parent_frame):
        """Calcula y guarda las ganancias para un mes específico."""
        try:
            # Convertir la fecha (dd/mm/yyyy) a formato YYYY-MM
            dia, mes, año = fecha_str.split("/")
            mes_año = f"{año}-{mes}"

            # Obtener todos los productos
            productos = self.db_connect.obtener_productos_para_acthistorial()

            # Calcular ganancias para cada producto
            ganancias = []
            for producto in productos:
                id_producto, codigo, costo_produccion, precio_venta = producto
                ganancia = precio_venta - costo_produccion
                margen = (ganancia / costo_produccion) * 100 if costo_produccion != 0 else 0
                ganancias.append((codigo, ganancia, margen))

            # Guardar en Historial_Ganancias
            for id_producto, codigo, ganancia, margen in [(p[0], p[1], g[1], g[2]) for p, g in zip(productos, ganancias)]:
                self.db_connect.guardar_historial(id_producto, mes_año, ganancia, margen)

            # Mostrar resultados en el Text
            self.resultado_text.config(state="normal")
            self.resultado_text.delete(1.0, tk.END)
            self.resultado_text.insert(tk.END, f"Ganancias para el mes {mes_año}:\n\n")
            self.resultado_text.insert(tk.END, "Producto\t\tGanancia\tMargen (%)\n")
            self.resultado_text.insert(tk.END, "-" * 40 + "\n")

            for codigo, ganancia, margen in ganancias:
                self.resultado_text.insert(tk.END, f"{codigo}\t\t€{ganancia:.2f}\t\t{margen:.1f}%\n")

            self.resultado_text.config(state="disabled")
            messagebox.showinfo("✅ Éxito", f"Historial de ganancias actualizado para el mes {mes_año}.")

        except Exception as e:
            messagebox.showerror("⚠️ Error", f"Ocurrió un error: {e}")

    def mostrar_historial_costos(self, root, mostrar_menu_principal, imagen_panel_tk, rol, imagen_tk, content_frame): #, info_frame=None):
        """Muestra el historial de costos (por producto o general)."""
        # Limpiar el frame de contenido
        for widget in content_frame.winfo_children():
            widget.destroy()

        # Frame principal
        form_frame = tk.LabelFrame(
            content_frame,
            text="Historial de Costos",
            bg=self.colores["fondo_frame"],
            fg=self.colores["texto_oscuro"],
            font=("Arial", 12, "bold"),
            padx=10,
            pady=10,
            bd=2,
            relief="groove"
        )
        form_frame.pack(fill="both", expand=False, padx=10, pady=10)

        # Opción para seleccionar un producto específico o ver todos
        tk.Label(
            form_frame,
            text="Selecciona una opción:",
            bg=self.colores["fondo_frame"],
            fg=self.colores["texto_oscuro"],
            font=("Arial", 11)
        ).grid(row=0, column=0, sticky="w", pady=5, padx=10)

        opcion_var = tk.StringVar()
        opcion_var.set("producto_especifico")
        opcion_dropdown = tk.OptionMenu(
            form_frame,
            opcion_var,
            "producto_especifico",
            "todos los Productos"
        )
        opcion_dropdown.config(
            bg=self.colores["fondo_frame"],
            fg=self.colores["texto_oscuro"],
            font=("Arial", 10),
            bd=2,
            relief="groove",
            width=20
        )
        opcion_dropdown.grid(row=1, column=0, sticky="w", pady=5, padx=10)

        # Dropdown para seleccionar producto (solo visible si se elige "producto_especifico")
        productos = self.db_connect.obtener_productos_para_costoventa()
        if not productos:
            tk.Label(
                form_frame,
                text="Actualmente no hay productos registrados.",
                font=("Arial", 12),
                bg=self.colores["fondo_frame"],
                fg=self.colores["texto_oscuro"]
            ).grid(row=2, column=0, pady=20)
            return

        producto_vars = [f"{prod[1]}" for prod in productos]
        producto_dropdown = ttk.Combobox(
            form_frame,
            values=producto_vars,
            state="readonly",
            font=("Arial", 10),
            width=30
        )
        producto_dropdown.grid(row=2, column=0, pady=5, padx=10, sticky="w")

        # Área para mostrar el historial
        resultado_frame = tk.LabelFrame(
            form_frame,
            text="Historial de Costos",
            bg=self.colores["fondo_frame"],
            fg=self.colores["texto_oscuro"],
            font=("Arial", 11, "bold"),
            padx=10,
            pady=10,
            bd=2,
            relief="groove"
        )
        resultado_frame.grid(row=3, column=0, pady=10, padx=10, sticky="esnw")

        producto_seleccionado_label = tk.Label(
            resultado_frame,
            text="Historial de costos para: (No seleccionado)",
            font=8,
            bg=self.colores["fondo_frame"],
            fg=self.colores["texto_oscuro"]
        )
        producto_seleccionado_label.pack()

        # Treeview para mostrar el historial
        self.tree_historial = ttk.Treeview(
            resultado_frame,
            columns=("Producto", "Fecha", "Costo Anterior", "Costo Nuevo", "Por Lote", "Unidades", "Motivo"),
            show="headings"
        )
        self.tree_historial.column("Producto", width=100)
        self.tree_historial.column("Fecha", width=80)
        self.tree_historial.column("Costo Anterior", width=113)
        self.tree_historial.column("Costo Nuevo", width=108)
        self.tree_historial.column("Por Lote", width=61)
        self.tree_historial.column("Unidades", width=66)
        self.tree_historial.column("Motivo", width=340)
        self.tree_historial.pack(fill="both", expand=False, padx=5, pady=5)

        # Botón para mostrar el historial
        crear_boton(
            form_frame,
            texto="Aceptar",
            ancho=20,
            alto=2,
            relieve="raised",
            border_width=1,
            color_fondo=self.colores["boton_guardar"],
            color_texto=self.colores["texto_claro"],
            font=("Arial", 11, "bold"),
            hover_color="#2ECC71",
            comando=lambda: self._mostrar_historial_costos(
                opcion_var.get(),
                producto_dropdown.get() if opcion_var.get() == "producto_especifico" else None,
                producto_seleccionado_label,
                resultado_frame
            )
        ).grid(row=4, column=0, pady=20, sticky="w")

        # Botón para imprimir el historial
        self.boton_imprimir_costos = None

    def _mostrar_historial_costos(self, opcion, producto_str, producto_seleccionado_label, parent_frame):
        """Muestra el historial de costos según la opción seleccionada."""
        # Eliminar el botón imprimir si existe
        if self.boton_imprimir_costos is not None:
            self.boton_imprimir_costos.destroy()

        # Limpiar el Treeview
        self.tree_historial.delete(*self.tree_historial.get_children())

        if opcion == "producto_especifico":
            producto_seleccionado_label.config(text=f"Historial de costos para: {producto_str}")
            historial = self.db_connect.mostrar_historial_costos_por_producto(producto_str)
        else:
            producto_seleccionado_label.config(text="Historial de costos para TODOS los productos.")
            historial = self.db_connect.mostrar_historial_costos_general()

        # Configurar columnas del Treeview
        for col in ("Producto", "Fecha", "Costo Anterior", "Costo Nuevo", "Por Lote", "Unidades", "Motivo"):
            self.tree_historial.heading(col, text=col)
            # if col in ["Producto", "Fecha", "Motivo"]:
            #     self.tree_historial.column(col, width=80)
            # else:
            #     self.tree_historial.column(col, width=80)

        # Insertar los resultados en el Treeview
        for row in historial:
            self.tree_historial.insert("", tk.END, values=row)

        # Botón para imprimir el historial
        self.boton_imprimir_costos = crear_boton(
            parent_frame,
            texto="Imprimir Historial de Costos",
            ancho=25,
            alto=2,
            relieve="raised",
            border_width=1,
            color_fondo="#299807",
            color_texto=self.colores["texto_claro"],
            font=("Arial", 11, "bold"),
            hover_color="#2ECC71",
            comando=lambda: self._imprimir_historial_costos(historial, opcion)
        )
        self.boton_imprimir_costos.pack(side="left", padx=5, pady=5)

    def _imprimir_historial_costos(self, historial, tipo):
        """Imprime el historial de costos en PDF."""
        if not historial:
            messagebox.showerror("⚠️ Error", "No hay datos en el historial de costos.")
            return

        # Preparar los datos para el PDF
        datos = []
        for registro in historial:
            if tipo == "producto_especifico":
                fecha, costo_anterior, costo_nuevo, es_por_lote, unidades, motivo = registro
                datos.append([
                    str(fecha),
                    f"€{float(costo_anterior):.2f}",
                    f"€{float(costo_nuevo):.2f}",
                    "Sí" if es_por_lote else "No",
                    str(unidades or "N/A"),
                    str(motivo or "N/A")
                ])
                columnas = ["Fecha", "Costo Anterior", "Costo Nuevo", "Por Lote", "Unidades", "Motivo"]
            else:
                codigo, fecha, costo_anterior, costo_nuevo, es_por_lote, unidades, motivo = registro
                datos.append([
                    str(codigo),
                    str(fecha),
                    f"€{float(costo_anterior):.2f}",
                    f"€{float(costo_nuevo):.2f}",
                    "Sí" if es_por_lote else "No",
                    str(unidades or "N/A"),
                    str(motivo or "N/A")
                ])
                columnas = ["Código", "Fecha", "Costo Anterior", "Costo Nuevo", "Por Lote", "Unidades", "Motivo"]

        # Generar el PDF
        from impresora import ImpresorPDF
        logo_path = "Img/logo/Logo-ikigai.png"

        ImpresorPDF.generar_pdf(
            titulo=f"Historial de Costos - {'Producto Específico' if tipo == 'producto_especifico' else 'General'}",
            datos=datos,
            columnas=columnas,
            nombre_archivo=f"historial_costos_{tipo}"
        )

    def mostrar_historial_ganancias(self, root, mostrar_menu_principal, imagen_panel_tk, rol, imagen_tk, content_frame): #, info_frame=None):
        """Muestra el historial de ganancias (por producto o por mes)."""
        # Limpiar el frame de contenido
        for widget in content_frame.winfo_children():
            widget.destroy()

        # Frame principal
        form_frame = tk.LabelFrame(
            content_frame,
            text="Historial de Ganancias",
            bg=self.colores["fondo_frame"],
            fg=self.colores["texto_oscuro"],
            font=("Arial", 12, "bold"),
            padx=20,
            pady=20,
            bd=2,
            relief="groove"
        )
        form_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Opción para seleccionar un producto específico o ver todos por mes
        tk.Label(
            form_frame,
            text="Selecciona una opción:",
            bg=self.colores["fondo_frame"],
            fg=self.colores["texto_oscuro"],
            font=("Arial", 11)
        ).grid(row=0, column=0, sticky="w", pady=5, padx=10)

        opcion_var = tk.StringVar()
        opcion_var.set("producto_especifico")
        opcion_dropdown = tk.OptionMenu(
            form_frame,
            opcion_var,
            "producto_especifico",
            "por_mes"
        )
        opcion_dropdown.config(
            bg=self.colores["fondo_frame"],
            fg=self.colores["texto_oscuro"],
            font=("Arial", 10),
            bd=2,
            relief="groove",
            width=20
        )
        opcion_dropdown.grid(row=1, column=0, sticky="w", pady=5, padx=10)

        # Dropdown para seleccionar producto (solo visible si se elige "producto_especifico")
        producto_frame = tk.Frame(form_frame, bg=self.colores["fondo_frame"])
        tk.Label(
            producto_frame,
            text="Selecciona el producto:",
            bg=self.colores["fondo_frame"],
            fg=self.colores["texto_oscuro"],
            font=("Arial", 11)
        ).pack(anchor=tk.W, pady=(0, 5))

        producto_vars = [f"{prod[1]}" for prod in self.db_connect.obtener_productos_para_costoventa()]
        producto_var = tk.StringVar()
        # Usar ttk.Combobox en lugar de OptionMenu
        producto_combobox = ttk.Combobox(
            producto_frame,
            values=producto_vars,
            state="readonly",  # Solo lectura (no se puede escribir texto libre)
            font=("Arial", 10),
            width=40
        )
        producto_combobox.pack(anchor=tk.W, pady=(0, 15))

        # Dropdown para seleccionar mes (solo visible si se elige "por_mes")
        mes_frame = tk.Frame(form_frame, bg=self.colores["fondo_frame"])
        tk.Label(
            mes_frame,
            text="Selecciona el mes (YYYY-MM):",
            bg=self.colores["fondo_frame"],
            fg=self.colores["texto_oscuro"],
            font=("Arial", 11)
        ).pack(anchor=tk.W, pady=(0, 5))

        mes_var = tk.StringVar()
        mes_entry = tk.Entry(
            mes_frame,
            width=30,
            font=("Arial", 11),
            bd=2,
            relief="groove"
        )
        mes_entry.pack(anchor=tk.W, pady=(0, 15))

        def toggle_frames(*args):
            if opcion_var.get() == "producto_especifico":
                producto_frame.grid(row=2, column=0, sticky="w", pady=(0, 15), padx=10)
                mes_frame.grid_forget()
            else:
                producto_frame.grid_forget()
                mes_frame.grid(row=2, column=0, sticky="w", pady=(0, 15), padx=10)

        opcion_var.trace_add("write", toggle_frames)

        # Botón para mostrar el historial
        crear_boton(
            form_frame,
            texto="Mostrar Historial",
            ancho=20,
            alto=2,
            relieve="raised",
            border_width=1,
            color_fondo=self.colores["boton_guardar"],
            color_texto=self.colores["texto_claro"],
            font=("Arial", 11, "bold"),
            hover_color="#2ECC71",
            comando=lambda: self._mostrar_historial_ganancias_opcion(
                opcion_var.get(),
                producto_combobox.get() if opcion_var.get() == "producto_especifico" else None,
                mes_entry.get() if opcion_var.get() == "por_mes" else None,
                form_frame
            )
        ).grid(row=3, column=0, pady=20, sticky="ew")

        # Área para mostrar el historial
        resultado_frame = tk.LabelFrame(
            form_frame,
            text="Historial de Ganancias",
            bg=self.colores["fondo_frame"],
            fg=self.colores["texto_oscuro"],
            font=("Arial", 11, "bold"),
            padx=10,
            pady=10,
            bd=2,
            relief="groove"
        )
        resultado_frame.grid(row=4, column=0, pady=10, padx=10, sticky="ew")

        self.historial_text = tk.Text(
            resultado_frame,
            height=15,
            width=80,
            state="disabled",
            bg="#FFFFFF",
            fg=self.colores["texto_oscuro"],
            font=("Arial", 10),
            bd=2,
            relief="groove",
            padx=10,
            pady=10
        )
        self.historial_text.pack()
        
        self.boton_imprimir_ganancias = None

    def _mostrar_historial_ganancias_opcion(self, opcion, producto_str, mes_str, parent_frame):
        """Muestra el historial de ganancias según la opción seleccionada."""
        # Eliminar el botón de impresión anterior si existe
        if self.boton_imprimir_ganancias is not None:
            self.boton_imprimir_ganancias.destroy()

        self.historial_text.config(state="normal")
        self.historial_text.delete(1.0, tk.END)

        if opcion == "producto_especifico":
            if not producto_str:
                messagebox.showerror("⚠️ Error", "Debes seleccionar un producto.")
                self.historial_text.config(state="disabled")
                return

            self.historial_text.insert(tk.END, f"Historial de ganancias para {producto_str}:\n\n")
            historial = self.db_connect.mostrar_historial_ganancias_producto(producto_str)
        else:
            if not mes_str:
                messagebox.showerror("⚠️ Error", "Debes ingresar un mes.")
                self.historial_text.config(state="disabled")
                return

            self.historial_text.insert(tk.END, f"Historial de ganancias para el mes {mes_str}:\n\n")
            historial = self.db_connect.mostrar_historial_general_mensual(mes_str)

        if not historial:
            messagebox.showerror("⚠️ Error", "No hay datos en el historial de ganancias.")
            self.historial_text.config(state="disabled")
            return

        # Encabezados
        if opcion == "producto_especifico":
            self.historial_text.insert(tk.END, "Mes         | Ganancia Total | Margen Promedio\n")
        else:
            self.historial_text.insert(tk.END, "Producto    | Ganancia Total | Margen Promedio\n")

        self.historial_text.insert(tk.END, "-" * 50 + "\n")

        for row in historial:
            if opcion == "producto_especifico":
                self.historial_text.insert(tk.END, f"{row[0]} | €{row[1]:.2f}         | {row[2]:.2f}%\n")
            else:
                self.historial_text.insert(tk.END, f"{row[0]} | €{row[1]:.2f}         | {row[2]:.2f}%\n")

        self.historial_text.config(state="disabled")

        # Botón para imprimir el historial
        self.boton_imprimir_ganancias = crear_boton(
            parent_frame,
            texto="Imprimir Historial de Ganancias",
            ancho=20,
            alto=2,
            relieve="raised",
            border_width=1,
            color_fondo="#1C7F36",
            color_texto=self.colores["texto_claro"],
            font=("Arial", 11, "bold"),
            hover_color="#2ECC71",
            comando=lambda: self._imprimir_historial_ganancias(historial, opcion, mes_str)
        )
        self.boton_imprimir_ganancias.grid(row=5, column=0, pady=10, sticky="ew")

    def _imprimir_historial_ganancias(self, historial, tipo, mes_str=None):
        """Imprime el historial de ganancias en PDF."""
        if not historial:
            messagebox.showerror("⚠️ Error", "No hay datos en el historial de ganancias.")
            return

        # Preparar los datos para el PDF
        datos = []
        for registro in historial:
            if tipo == "producto_especifico":
                mes, ganancia_total, margen_promedio = registro
                datos.append([
                    str(mes),
                    f"€{float(ganancia_total):.2f}",
                    f"{float(margen_promedio):.1f}%"
                ])
                columnas = ["Mes", "Ganancia Total", "Margen Promedio"]
            else:
                codigo, ganancia_total, margen_promedio = registro
                datos.append([
                    str(codigo),
                    f"€{float(ganancia_total):.2f}",
                    f"{float(margen_promedio):.1f}%"
                ])
                columnas = ["Producto", "Ganancia Total", "Margen Promedio"]

        # Generar el PDF
        from impresora import ImpresorPDF
        logo_path = "Img/logo/logo_ikigai.png"

        ImpresorPDF.generar_pdf(
            titulo=f"Historial de Ganancias - {'Producto Específico' if tipo == 'producto_especifico' else f'Mes {mes_str}'}",
            datos=datos,
            columnas=columnas,
            nombre_archivo=f"historial_ganancias_{tipo}_{mes_str if tipo == 'por_mes' else ''}"
        )