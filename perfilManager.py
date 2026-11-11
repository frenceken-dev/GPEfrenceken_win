# perfilManager.py
# Módulo para la personalización de branding del NEGOCIO (Fase 7).

# perfilManager.py
# Módulo para la personalización de branding del NEGOCIO (Fase 7).

import os
import shutil
import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from recursos import crear_boton, redimensionar_imagen, configurar_toplevel, carpeta_logo_negocio
from databasemanager import DataBaseManager

db_connect = DataBaseManager()

# Valores default (los mismos que usa hoy todo el programa).
DEFAULTS = {"fondo": "#a0b9f0", "fuente": "#272525",
            "fondo_menu": "#2C3E50", "fondo_img": "#a0b9f0"}


class perfilUsuario:
    """Configura la apariencia (colores y logo) del negocio actual."""

    def __init__(self, root, nombre_negocio):
        self.root = root
        self.nombre_negocio = nombre_negocio

        # Estado en memoria, inicializado con lo guardado en la BD.
        branding = db_connect.obtener_branding()
        self.color_pantalla = branding["color_fondo"] or DEFAULTS["fondo"]
        self.color_letra = branding["color_fuente"] or DEFAULTS["fuente"]
        self.color_menu = branding["color_menu"] or DEFAULTS["fondo_menu"]
        self.logo_archivo = branding["logo_archivo"]  # None si nunca se ha subido

        self.interfaz_configuracion()

    # ==================== CONSTRUCCIÓN DE LA INTERFAZ ====================

    def interfaz_configuracion(self):
        self.ventana = tk.Toplevel(self.root)
        configurar_toplevel(self.ventana, titulo="Apariencia del Negocio",
                            ancho_min=760, alto_min=470, color_fondo="#34495e")

        # ---- Título ----
        tk.Label(self.ventana, text=f"🎨  Apariencia de {self.nombre_negocio}",
                font=("Arial", 15, "bold"), bg="#34495e", fg="#ecf0f1"
                ).pack(fill="x", padx=15, pady=(12, 6))

        # ---- Cuerpo: vista previa (izq) + controles (der) ----
        cuerpo = tk.Frame(self.ventana, bg="#34495e")
        cuerpo.pack(fill="both", expand=True, padx=15, pady=5)

        # ----- Vista previa -----
        prev = tk.LabelFrame(cuerpo, text="  Vista previa  ", bg="#34495e",
                            fg="#ecf0f1", font=("Arial", 10, "bold"))
        prev.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # Área de contenido (fondo principal)
        self.prev_contenido = tk.Frame(prev, bg=self.color_pantalla)
        self.prev_contenido.pack(fill="both", expand=True, padx=8, pady=8)

        # Logo (o texto) dentro de la vista previa
        self.prev_logo_label = tk.Label(self.prev_contenido,
                                        text=self.nombre_negocio,
                                        font=("Arial", 13, "bold"),
                                        bg=self.color_pantalla,
                                        fg=self.color_letra)
        self.prev_logo_label.pack(pady=10)

        # Etiqueta simulada de "contenido"
        tk.Label(self.prev_contenido, text="Tu inventario se verá aquí",
                font=("Arial", 10), bg=self.color_pantalla,
                fg=self.color_letra).pack(expand=True)

        # Mini-menú lateral sobre el contenido
        self.prev_menu = tk.Frame(self.prev_contenido, bg=self.color_menu,
                                width=110)
        self.prev_menu.place(x=8, rely=0.12, relheight=0.76, width=110)
        for texto in ["Menú", "Botones", "Aquí"]:
            tk.Label(self.prev_menu, text="● " + texto, bg=self.color_menu,
                    fg="#ecf0f1", font=("Arial", 9), anchor="w"
                    ).pack(fill="x", padx=8, pady=8)

        # ----- Controles -----
        controles = tk.Frame(cuerpo, bg="#34495e")
        controles.pack(side="left", fill="both", expand=True)

        self._crear_control_color(
            controles, "Fondo principal", "fondo", self.color_pantalla)
        self._crear_control_color(
            controles, "Menú lateral", "fondo_menu", self.color_menu)
        self._crear_control_color(
            controles, "Fuente (texto)", "fuente", self.color_letra)

        # ----- Logo -----
        marco_logo = tk.LabelFrame(controles, text="  Logo del negocio  ",
                                    bg="#34495e", fg="#ecf0f1",
                                    font=("Arial", 10, "bold"))
        marco_logo.pack(fill="x", pady=(8, 0))

        fila_logo = tk.Frame(marco_logo, bg="#34495e")
        fila_logo.pack(fill="x", padx=8, pady=8)

        crear_boton(fila_logo, texto="Seleccionar imagen", ancho=16, alto=20,
                    color_fondo="#2980b9", color_texto="white",
                    hover_color="#1f6391",
                    comando=self.cambiar_logo).pack(side="left", padx=(0, 8))

        self.label_estado_logo = tk.Label(
            fila_logo, text="Sin logo propio" if not self.logo_archivo else "Logo cargado ✔",
            bg="#34495e", fg="#bdc3c7", font=("Arial", 9))
        self.label_estado_logo.pack(side="left")

        # Mostrar logo guardado si existe
        logo_guardado = os.path.join(carpeta_logo_negocio(self.nombre_negocio), "logo.png")
        if os.path.exists(logo_guardado):
            self._mostrar_logo(logo_guardado)

        # ----- Botones finales -----
        fila_botones = tk.Frame(self.ventana, bg="#34495e")
        fila_botones.pack(fill="x", padx=15, pady=(6, 12))

        crear_boton(fila_botones, texto="Restaurar default", ancho=16, alto=22,
                    color_fondo="#7f8c8d", color_texto="white",
                    hover_color="#616a6b",
                    comando=self.restaurar_default).pack(side="left")

        crear_boton(fila_botones, texto="💾  Guardar configuración",
                    ancho=22, alto=22, color_fondo="#27ae60", color_texto="white",
                    hover_color="#1e8449",
                    comando=self.guardar).pack(side="right")

    def _crear_control_color(self, padre, titulo, llave, color_actual):
        """Crea una fila: título + muestra de color + botón 'Cambiar'."""
        marco = tk.LabelFrame(padre, text=f"  {titulo}  ", bg="#34495e",
                            fg="#ecf0f1", font=("Arial", 10, "bold"))
        marco.pack(fill="x", pady=5)

        fila = tk.Frame(marco, bg="#34495e")
        fila.pack(fill="x", padx=8, pady=8)

        # Muestra grande del color actual
        muestra = tk.Frame(fila, bg=color_actual, width=120, height=30,
                        relief="groove", bd=2)
        muestra.pack(side="left", padx=(0, 8))
        muestra.pack_propagate(False)

        crear_boton(fila, texto="Cambiar", ancho=12, alto=20,
                    color_fondo="#34495e", color_texto="#ecf0f1",
                    hover_color="#46637f",
                    comando=lambda: self.seleccionar_color(llave, muestra)
                    ).pack(side="left")

        # Guardar referencia de la muestra para actualizarla
        setattr(self, f"muestra_{llave}", muestra)

    # ==================== ACCIONES ====================

    def seleccionar_color(self, llave, muestra):
        color = colorchooser.askcolor(title=f"Color de {llave}")
        if not color or not color[1]:
            return  # usuario canceló

        hex_color = color[1]
        if llave == "fondo":
            self.color_pantalla = hex_color
        elif llave == "fuente":
            self.color_letra = hex_color
        elif llave == "fondo_menu":
            self.color_menu = hex_color

        muestra.config(bg=hex_color)
        self._actualizar_preview()

    def cambiar_logo(self):
        ruta = filedialog.askopenfilename(
            title="Seleccionar logo",
            filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.gif *.bmp *.ico")]
        )
        if not ruta:
            return

        carpeta = carpeta_logo_negocio(self.nombre_negocio)
        destino = os.path.join(carpeta, "logo.png")
        try:
            # Conversión real a PNG (soporta jpg, bmp, gif, ico, etc.)
            from PIL import Image
            imagen = Image.open(ruta).convert("RGBA")
            imagen.save(destino, "PNG")
        except ImportError:
            # Sin PIL: copia directa (así funciona hoy)
            shutil.copy(ruta, destino)
        except Exception as e:
            messagebox.showerror("⚠️ Error", f"No se pudo guardar el logo: {e}")
            return

        self.logo_archivo = "logo.png"
        self.label_estado_logo.config(text="Logo cargado ✔")
        self._mostrar_logo(destino)
        self._actualizar_preview()

    def _mostrar_logo(self, ruta):
        imagen = redimensionar_imagen(ruta, 90, 90)
        if imagen is None:
            return
        self.imagen_actual = imagen  # mantener referencia para que Tk no la borre
        self.prev_logo_label.config(image=imagen, text="")
        self.prev_logo_label.image = imagen

    def restaurar_default(self):
        """Vuelve a los colores default (aún sin guardar; presiona Guardar para aplicar)."""
        self.color_pantalla = DEFAULTS["fondo"]
        self.color_menu = DEFAULTS["fondo_menu"]
        self.color_letra = DEFAULTS["fuente"]
        self.muestra_fondo.config(bg=self.color_pantalla)
        self.muestra_fondo_menu.config(bg=self.color_menu)
        self.muestra_fuente.config(bg=self.color_letra)
        self._actualizar_preview()

    def _actualizar_preview(self):
        """Refleja en la vista previa los colores elegidos al instante."""
        self.prev_contenido.config(bg=self.color_pantalla)
        self.prev_menu.config(bg=self.color_menu)
        self.prev_logo_label.config(bg=self.color_pantalla, fg=self.color_letra)
        for w in self.prev_contenido.winfo_children():
            if isinstance(w, tk.Label) and w is not self.prev_logo_label:
                w.config(bg=self.color_pantalla, fg=self.color_letra)
        for w in self.prev_menu.winfo_children():
            if isinstance(w, tk.Label):
                w.config(bg=self.color_menu)

    def guardar(self):
        guardado = db_connect.guardar_branding(
            self.color_pantalla,
            self.color_menu,
            self.color_letra,
            self.logo_archivo
        )
        if guardado:
            messagebox.showinfo(
                "Guardado",
                "Apariencia guardada.\nVuelve a entrar al negocio para verla aplicada."
            )
            self.ventana.destroy()
        else:
            messagebox.showerror("⚠️ Error", "No se pudo guardar la apariencia.")