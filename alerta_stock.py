# alerta_stock.py
import tkinter as tk
from tkinter import ttk, messagebox
#from db import configurar_umbral_alerta #cargar_items, 
from recursos import crear_boton, configurar_toplevel, centrar_ventana_toplevel
from databasemanager import DataBaseManager


class VentanaConfigurarUmbrales:
    def __init__(self, root, volver_menu):
        self.db_connect = DataBaseManager()
        # Crear ventana secundaria centrada y ajustada
        self.root = tk.Toplevel(root)
        configurar_toplevel(self.root, titulo="Configurar Umbrales de Alerta", ancho_min=410, alto_min=290)
        
        # 🎨 Frame principal para el contenido
        frame_contenido = tk.Frame(self.root, bg="#101113", padx=20, pady=20)
        frame_contenido.pack(fill=tk.BOTH, expand=True)

        # 🔹 Tipo
        tk.Label(frame_contenido, text="Tipo:", background="#101113", fg="#ffffff").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.tipo_var = tk.StringVar()
        self.combobox_tipo = ttk.Combobox(frame_contenido, textvariable=self.tipo_var, values=['material', 'producto'], state="readonly", width=35)
        self.combobox_tipo.grid(row=0, column=1, padx=5, pady=10)

        # 🔹 Item
        tk.Label(frame_contenido, text="Item:", background="#101113", fg="#ffffff").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        # Frame para Listbox + Scrollbars
        self.frame_lista = tk.Frame(frame_contenido, bg="#101113")
        self.frame_lista.grid(row=1, column=1, padx=5, pady=10, sticky="nsew")

        # Scroll Vertical
        self.scroll_y = tk.Scrollbar(self.frame_lista, orient="vertical")
        self.scroll_y.pack(side="right", fill="y")

        # Scroll Horizontal
        self.scroll_x = tk.Scrollbar(self.frame_lista, orient="horizontal")
        self.scroll_x.pack(side="bottom", fill="x")

        # Listbox
        self.listbox_item = tk.Listbox(
            self.frame_lista,
            width=30,
            height=3,
            xscrollcommand=self.scroll_x.set,
            yscrollcommand=self.scroll_y.set,
            exportselection=False
        )

        self.listbox_item.pack(side="left", fill="both", expand=True)

        # Asociar scrollbars
        self.scroll_y.config(command=self.listbox_item.yview)
        self.scroll_x.config(command=self.listbox_item.xview)

        # 🔹 Umbral
        tk.Label(frame_contenido, text="Umbral:", background="#101113", fg="#ffffff").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.entry_umbral = ttk.Entry(frame_contenido, width=10)
        self.entry_umbral.grid(row=2, column=1, padx=5, pady=10, sticky="w")

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
        
        # Limpiar Listbox
        self.listbox_item.delete(0, tk.END)

        items_carados = self.db_connect.cargar_items(tipo)
        if tipo == "material":

            for item in items_carados:
                texto = (
                    f"{item[0]} | {item[1]} | "
                    f"{item[2]} | {item[3]} | "
                    f"{item[4]} | Cant:{item[5]}"
                )

                self.listbox_item.insert(tk.END, texto)

        elif tipo == "producto":

            for item in items_carados:
                texto = (
                    f"{item[0]} | {item[1]} | "
                    f"{item[2]} | Cant:{item[3]}"
                )

                self.listbox_item.insert(tk.END, texto)
        
    def guardar_umbral(self, volver_menu):
        tipo = self.tipo_var.get()
        seleccion = self.listbox_item.curselection()

        if not seleccion:
            messagebox.showerror(
                "⚠️ Error",
                "Debe seleccionar un item."
            )
            return
        #print(f"LA SELECCION ES:{seleccion}")
        item_str = self.listbox_item.get(seleccion[0])
        #print(f"LA DATA EN 0 ES:{item_str}")
        umbral = self.entry_umbral.get()

        if not tipo or not item_str or not umbral:
            messagebox.showerror("⚠️ Error", "Todos los campos son obligatorios.")
            return

        try:
            id_item = int(item_str.split(" | ")[0])
            umbral = int(umbral)
        except ValueError:
            messagebox.showerror("⚠️ Error", "ID de item o umbral no válido.")
            return

        self.db_connect.configurar_umbral_alerta(tipo, id_item, umbral)
        messagebox.showinfo("Éxito", "Umbral de alerta configurado correctamente.")
        volver_menu()
