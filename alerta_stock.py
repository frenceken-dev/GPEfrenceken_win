# alerta_stock.py
import tkinter as tk
from tkinter import ttk, messagebox
from db import cargar_items, configurar_umbral_alerta

class VentanaConfigurarUmbrales:
    def __init__(self, root, volver_menu):
        self.root = tk.Toplevel(root)
        self.root.title("Configurar Umbrales de Alerta")

        self.label_tipo = ttk.Label(self.root, text="Tipo:")
        self.label_tipo.grid(row=0, column=0, padx=10, pady=10)

        self.tipo_var = tk.StringVar()
        self.combobox_tipo = ttk.Combobox(self.root, textvariable=self.tipo_var, values=['material', 'producto'], state="readonly")
        self.combobox_tipo.grid(row=0, column=1, padx=10, pady=10)

        self.label_item = ttk.Label(self.root, text="Item:")
        self.label_item.grid(row=1, column=0, padx=10, pady=10)

        self.combobox_item = ttk.Combobox(self.root, state="readonly")
        self.combobox_item.grid(row=1, column=1, padx=10, pady=10)

        self.label_umbral = ttk.Label(self.root, text="Umbral:")
        self.label_umbral.grid(row=2, column=0, padx=10, pady=10)

        self.entry_umbral = ttk.Entry(self.root)
        self.entry_umbral.grid(row=2, column=1, padx=10, pady=10)

        self.boton_guardar = ttk.Button(self.root, text="Guardar", command=lambda : self.guardar_umbral(volver_menu))
        self.boton_guardar.grid(row=3, column=0, columnspan=2, pady=10)

        self.combobox_tipo.bind("<<ComboboxSelected>>", self.cargar_los_items)

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
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
            id_item = int(item_str.split(" - ")[0])
            umbral = int(umbral)
        except ValueError:
            messagebox.showerror("Error", "ID de item o umbral no válido.")
            return

        configurar_umbral_alerta(tipo, id_item, umbral)
        messagebox.showinfo("Éxito", "Umbral de alerta configurado correctamente.")
        volver_menu()