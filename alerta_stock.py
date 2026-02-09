# alerta_stock.py
import tkinter as tk
from tkinter import ttk, messagebox
from db import cargar_items, configurar_umbral_alerta
from recursos import crear_boton, configurar_toplevel, centrar_ventana_toplevel


class VentanaConfigurarUmbrales:
    def __init__(self, root, volver_menu):
        # Crear ventana secundaria centrada y ajustada
        self.root = tk.Toplevel(root)
        configurar_toplevel(self.root, titulo="Configurar Umbrales de Alerta", ancho_min=400, alto_min=250)
        
        # 🎨 Frame principal para el contenido
        frame_contenido = tk.Frame(self.root, bg="#101113", padx=20, pady=20)
        frame_contenido.pack(fill=tk.BOTH, expand=True)

        # 🔹 Tipo
        tk.Label(frame_contenido, text="Tipo:", background="#101113", fg="#ffffff").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.tipo_var = tk.StringVar()
        self.combobox_tipo = ttk.Combobox(frame_contenido, textvariable=self.tipo_var, values=['material', 'producto'], state="readonly")
        self.combobox_tipo.grid(row=0, column=1, padx=10, pady=10)

        # 🔹 Item
        tk.Label(frame_contenido, text="Item:", background="#101113", fg="#ffffff").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.combobox_item = ttk.Combobox(frame_contenido, state="readonly")
        self.combobox_item.grid(row=1, column=1, padx=10, pady=10)

        # 🔹 Umbral
        tk.Label(frame_contenido, text="Umbral:", background="#101113", fg="#ffffff").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.entry_umbral = ttk.Entry(frame_contenido)
        self.entry_umbral.grid(row=2, column=1, padx=10, pady=10)

        # 🔹 Botón Guardar
        crear_boton(frame_contenido, 
                    texto="Guardar",
                    color_texto="#ffffff",
                    ancho=30,
                    alto=30,
                    color_fondo="#FF5733",  # Color llamativo para advertencia
                    #fg="white",
                    font=("Arial", 11, "bold"),
                    #bd=0,
                    #relief=tk.FLAT,
                    hover_color="#FF8C61",
                    #activeforeground="white",
                    comando=lambda: self.guardar_umbral(volver_menu)).grid(row=3, column=0, columnspan=2, pady=20)

        # Evento de cambio de tipo
        self.combobox_tipo.bind("<<ComboboxSelected>>", self.cargar_los_items)

        # 🔹 Ajustar centrado de columnas
        frame_contenido.grid_columnconfigure(0, weight=1)
        frame_contenido.grid_columnconfigure(1, weight=1)


    def cargar_los_items(self, event):
        tipo = self.tipo_var.get()
        self.combobox_item['values'] = []

        items_carados = cargar_items(tipo)
        self.combobox_item['values'] = [f"{item[0]} - {item[1]}" for item in items_carados]
        
    def guardar_umbral(self, volver_menu):
        tipo = self.tipo_var.get()
        item_str = self.combobox_item.get()
        umbral = self.entry_umbral.get()

        if not tipo or not item_str or not umbral:
            messagebox.showerror("⚠️ Error", "Todos los campos son obligatorios.")
            return

        try:
            id_item = int(item_str.split(" - ")[0])
            umbral = int(umbral)
        except ValueError:
            messagebox.showerror("⚠️ Error", "ID de item o umbral no válido.")
            return

        configurar_umbral_alerta(tipo, id_item, umbral)
        messagebox.showinfo("Éxito", "Umbral de alerta configurado correctamente.")
        volver_menu()
