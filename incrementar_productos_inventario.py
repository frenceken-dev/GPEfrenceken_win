import tkinter as tk
from tkinter import ttk, messagebox
from db import obtener_productos, incrementar_stock_producto
from recursos import LOGO_PATH, crear_boton

class VentanaIncrementarStock:
    def __init__(self, root, imagen_panel_tk, volver_menu):
        for widget in root.winfo_children():
            widget.destroy()

        self.root = root
        
        # Crear frame_contenido (para formularios)
        self.frame_contenido = tk.Frame(self.root, bg="#a0b9f0", width=600, height=800)
        self.frame_contenido.place(relx=0.5, rely=0.3, anchor=tk.N)

        # Panel izquierdo
        frame_menu = tk.Frame(self.root, bg="#2C3E50", width=200, height=800, bd=3, relief="solid")
        frame_menu.pack(side=tk.LEFT, fill=tk.Y)
        frame_menu.pack_propagate(False)
            
        frame_imagen_panel = tk.Frame(frame_menu, bg="#2C3E50", height=70)
        frame_imagen_panel.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

        # Imagen del Logo para el panel izquierdo
        if imagen_panel_tk:
            label_imagen = tk.Label(frame_imagen_panel, image=imagen_panel_tk, bg="#2C3E50")
            label_imagen.pack(side=tk.LEFT, padx=70)
        else:
            label_texto = tk.Label(frame_imagen_panel, text="Ikigai", font=("Arial", 10), bg="#2C3E50")
            label_texto.pack(side=tk.LEFT, padx=70)

        # Frame inferior dentro del menú lateral
        frame_inferior = tk.Frame(frame_menu, bg="#2C3E50")
        frame_inferior.pack(side="bottom", fill="x", pady=20)  # <- este pady sí separa del borde inferior

        self.frame_titulo = tk.Frame(self.root, bg="#a0b9f0")
        self.frame_titulo.place(relx=0.5, rely=0.02, anchor=tk.N)
        
        # Título
        self.title_label = tk.Label(
            self.frame_titulo,
            text="Incrementar Stock de Producto",
            font=("Arial", 16, "bold"),
            bg="#a0b9f0",
            fg="#2C3E50"
        )
        self.title_label.pack(pady=15)
        
        self.label_producto = tk.Label(self.frame_contenido, text="Seleccione el producto:", bg="#a0b9f0")
        self.label_producto.grid(row=0, column=0, padx=10, pady=10)

        self.combobox_productos = ttk.Combobox(self.frame_contenido, state="readonly")
        self.combobox_productos.grid(row=0, column=1, padx=10, pady=10)

        self.label_cantidad = tk.Label(self.frame_contenido, text="Cantidad a incrementar:", bg="#a0b9f0")
        self.label_cantidad.grid(row=1, column=0, padx=10, pady=10)

        self.entry_cantidad = ttk.Entry(self.frame_contenido)
        self.entry_cantidad.grid(row=1, column=1, padx=10, pady=10)

        self.boton_incrementar = crear_boton(self.frame_contenido, 
                texto="Incrementar Stock", 
                ancho=30,
                alto=30,
                color_fondo="#4373C7",                
                color_texto="white",
                font=("Arial", 11, "bold"),
                #bd=0,
                #relief=tk.FLAT,
                hover_color="#2ECC71",
                #activeforeground="black",
                #bg=0,
                comando=self.incrementar_stock)
        self.boton_incrementar.grid(row=2, column=0, columnspan=2, pady=10)

        # Botón para volver
        self.back_button = crear_boton(
            frame_inferior,
            texto="Volver",
            ancho=130,
            alto=30,
            color_fondo="#913131",                
            color_texto="white",
            font=("Arial", 11, "bold"),
            #bd=0,
            #relief=tk.FLAT,
            hover_color="#222423",
            #activeforeground="black",
            #bg=0,
            comando=volver_menu 
        )
        self.back_button.pack(side="bottom", padx=30, pady=30)

        self.cargar_productos()

    def cargar_productos(self):
        productos = obtener_productos()
        self.combobox_productos['values'] = [f"{producto[0]} - {producto[1]}" for producto in productos]

    def incrementar_stock(self):
        producto_seleccionado = self.combobox_productos.get()
        cantidad = self.entry_cantidad.get()

        if not producto_seleccionado:
            messagebox.showerror("Error", "Debe seleccionar un producto.")
            return

        if not cantidad or not cantidad.isdigit() or int(cantidad) <= 0:
            messagebox.showerror("Error", "Debe ingresar una cantidad válida.")
            return

        id_producto = int(producto_seleccionado.split(" - ")[0])
        cantidad = int(cantidad)

        incrementar_stock_producto(id_producto, cantidad)