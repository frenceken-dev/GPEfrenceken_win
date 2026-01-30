# recursos.py

import sys
import os
import tkinter as tk
import platform

def resource_path(relative_path: str) -> str:
    """
    Devuelve la ruta absoluta a `relative_path`.
    - Funciona en desarrollo,
    - con PyInstaller (_MEIPASS),
    - con py2app (.app MacOS bundle).
    """
    if hasattr(sys, "_MEIPASS"):  # PyInstaller
        base_path = sys._MEIPASS
    elif getattr(sys, "frozen", False):  # py2app / frozen
        # En py2app, los recursos están en Contents/Resources
        base_path = os.path.join(os.path.dirname(sys.executable), '..', 'Resources')
        base_path = os.path.abspath(base_path)
    else:  # desarrollo
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)


# Rutas de imágenes y base de datos.
DB_PATH = '/home/frenceken/Escritorio/GPEfrencekenApp-Win/GPEfrencekenApp-win/ikigai_inventario.db'
LOGO_PATH = resource_path("Img/logo/logo_ikigai.png")
IMAGEN_BUSQUEDA_PATH = resource_path('Img/busqueda/img-busqueda.png')
ICO_PATH = resource_path('ini.icns')


# --- Función auxiliar para oscurecer colores ---
def _darker(color, factor=0.1):
    """Oscurece un color hexadecimal ligeramente."""
    color = color.lstrip("#")
    r, g, b = tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))
    r = int(r * (1 - factor))
    g = int(g * (1 - factor))
    b = int(b * (1 - factor))
    return f"#{r:02x}{g:02x}{b:02x}"


# --- Función principal para crear botones ---
def crear_boton(
    parent,
    texto=None,
    comando=None,
    color_fondo=None,
    color_texto=None,
    ancho=None,
    alto=None,
    modo=None,  # "plano" o "redondeado"
    radio=None,  # solo aplica si modo="redondeado"
    border_color=None,
    border_width=None,
    font=None,
    cursor=None,
    hover_color=None,   # color al pasar el cursor
    focus_color=None,   # color al recibir foco (solo si se pasa)
    focus_width=None,   # grosor del borde de foco
    **kwargs
):
    """
    Crear un botón adaptable con hover_color y focus_color opcionales.
    Si el usuario no pasa focus_color, el foco queda desactivado visualmente.
    """

    # --- Valores por defecto ---
    texto = texto or ""
    color_fondo = color_fondo or "#4A6CF7"
    color_texto = color_texto or "white"
    ancho = ancho or 150
    alto = alto or 40
    modo = modo or "plano"
    radio = radio or 15
    border_color = border_color or _darker(color_fondo, 0.2)
    border_width = border_width or 2
    font = font or ("Arial", 10, "bold")
    cursor = cursor or "hand2"

    # Colores interactivos
    hover_color_local = hover_color or _darker(color_fondo, 0.15)
    focus_color_local = focus_color  # ← solo si se pasa, si no queda None
    focus_width = focus_width if focus_width is not None else 2

    sistema = platform.system()

    # --- macOS o modo redondeado ---
    if sistema == "Darwin" or modo == "redondeado":
        bg_color = parent.cget("bg") if "bg" in parent.keys() else parent.winfo_toplevel().cget("bg")
        cont = tk.Frame(parent, bg=bg_color, highlightthickness=0)
        canvas = tk.Canvas(
            cont,
            width=ancho,
            height=alto,
            bg=bg_color,
            highlightthickness=0,
            bd=0,
            takefocus=1
        )
        canvas.pack()

        boton_shape = canvas.create_rectangle(
            border_width,
            border_width,
            ancho - border_width,
            alto - border_width,
            outline=border_color,
            width=border_width,
            fill=color_fondo
        )

        text_id = canvas.create_text(
            ancho / 2,
            alto / 2,
            text=texto,
            fill=color_texto,
            font=font
        )

        # Referencia mutable al comando actual
        comando_ref = [comando]
        current_state = ["normal"]  # estado inicial

        # --- Interacciones ---
        def on_enter(e):
            if current_state[0] == "normal":
                canvas.itemconfig(boton_shape, fill=hover_color_local)

        def on_leave(e):
            if current_state[0] == "normal":
                canvas.itemconfig(boton_shape, fill=color_fondo)

        def on_click(e):
            if current_state[0] == "normal" and callable(comando_ref[0]):
                comando_ref[0]()

        # Focus visual opcional
        def on_focus_in(e):
            if focus_color_local:
                canvas.itemconfig(boton_shape, outline=focus_color_local, width=focus_width)

        def on_focus_out(e):
            if focus_color_local:
                canvas.itemconfig(boton_shape, outline=border_color, width=border_width)

        # Enlazar eventos
        for tag in (boton_shape, text_id):
            canvas.tag_bind(tag, "<Enter>", on_enter)
            canvas.tag_bind(tag, "<Leave>", on_leave)
            canvas.tag_bind(tag, "<Button-1>", on_click)

        canvas.bind("<FocusIn>", on_focus_in)
        canvas.bind("<FocusOut>", on_focus_out)

        # --- Métodos dinámicos ---
        def set_text(new_text):
            canvas.itemconfig(text_id, text=new_text)

        def set_command(new_command):
            comando_ref[0] = new_command

        def set_state(new_state):
            current_state[0] = new_state
            if new_state == "disabled":
                canvas.itemconfig(boton_shape, fill=_darker(color_fondo, 0.4))
                canvas.itemconfig(text_id, fill="#aaaaaa")
                canvas.config(cursor="arrow")
            else:
                canvas.itemconfig(boton_shape, fill=color_fondo)
                canvas.itemconfig(text_id, fill=color_texto)
                canvas.config(cursor="hand2")

        def get_state():
            return current_state[0]

        cont.set_text = set_text
        cont.set_command = set_command
        cont.set_state = set_state
        cont.get_state = get_state
        cont.canvas = canvas

        return cont


    # --- Windows / Linux ---
    active_bg = hover_color_local

    boton = tk.Button(
        parent,
        text=texto,
        command=comando,
        bg=color_fondo,
        fg=color_texto,
        activebackground=active_bg,
        activeforeground=color_texto,
        font=font,
        relief="flat",
        borderwidth=0,
        cursor=cursor,
        takefocus=1,
        width=ancho,
        height=int(alto / 20),
        **kwargs
    )

    # --- Métodos dinámicos para Windows/Linux ---
    def set_text(new_text):
        boton.config(text=new_text)

    def set_command(new_command):
        boton.config(command=new_command)

    def set_state(new_state):
        if new_state == "disabled":
            boton.config(state=tk.DISABLED, bg=_darker(color_fondo, 0.4), fg="#aaaaaa")
        else:
            boton.config(state=tk.NORMAL, bg=color_fondo, fg=color_texto)

    def get_state():
        return boton.cget("state")

    boton.set_text = set_text
    boton.set_command = set_command
    boton.set_state = set_state
    boton.get_state = get_state

    # Si el usuario pasa focus_color, aplicamos visualmente el efecto
    if focus_color_local:
        boton.configure(
            highlightthickness=focus_width,
            highlightbackground=color_fondo,
            highlightcolor=focus_color_local
        )

        def _on_focus_in(e):
            boton.configure(highlightbackground=focus_color_local)

        def _on_focus_out(e):
            boton.configure(highlightbackground=color_fondo)

        boton.bind("<FocusIn>", _on_focus_in)
        boton.bind("<FocusOut>", _on_focus_out)
    else:
        boton.configure(highlightthickness=0)

    # Métodos de actualización dinámica también en el botón normal
    boton.set_text = lambda t: boton.config(text=t)
    boton.set_command = lambda c: boton.config(command=c)

    return boton


def configurar_toplevel(ventana, titulo="Ventana", ancho_min=400, alto_min=300, color_fondo="#f0f0f0"):
    """
    Configura un Toplevel sin afectar la ventana principal ni heredar su geometría.
    """
    ventana.title(titulo)

    # Asegura que el fondo sea blanco o neutro (evita heredar el del root)
    ventana.configure(bg=color_fondo)

    # Quita cualquier modo fullscreen heredado del root
    try:
        ventana.attributes('-fullscreen', False)
    except Exception:
        pass

    ventana.resizable(False, False)

    # --- CLAVE 1: hacer modal real ---
    padre = ventana.master            # obtiene root o el contenedor
    ventana.transient(padre)          # el padre siempre queda detrás
    ventana.grab_set()                # bloquea clics fuera del modal
    ventana.lift()                    # trae al frente
    ventana.focus_force()             # enfoca el modal sí o sí

    # --- CLAVE 2: evitar que se vaya atrás en macOS ---
    ventana.attributes("-topmost", True)
    ventana.after(100, lambda: ventana.attributes("-topmost", False))
    # Esto fuerza a macOS a respetar la jerarquía


    ventana.update_idletasks()  # Calcula el tamaño real

    ancho = max(ventana.winfo_reqwidth(), ancho_min)
    alto = max(ventana.winfo_reqheight(), alto_min)
    x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana.winfo_screenheight() // 2) - (alto // 2)

    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")


# Centrar Toplevel
def centrar_ventana_toplevel(ventana, ancho_min=400, alto_min=300):
    """Centra cualquier ventana (Tk o Toplevel) según su contenido."""
    ventana.update_idletasks()
    ancho = max(ventana.winfo_reqwidth(), ancho_min)
    alto = max(ventana.winfo_reqheight(), alto_min)
    x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana.winfo_screenheight() // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")


def redimensionar_imagen(ruta, ancho_max, alto_max):
    from PIL import Image, ImageTk
    """Redimensiona una imagen manteniendo su proporción sin deformarla."""
    try:
        imagen = Image.open(ruta)
        ancho_original, alto_original = imagen.size
        proporcion = min(ancho_max / ancho_original, alto_max / alto_original)
        nuevo_ancho = int(ancho_original * proporcion)
        nuevo_alto = int(alto_original * proporcion)
        imagen_redimensionada = imagen.resize((nuevo_ancho, nuevo_alto), Image.LANCZOS)
        return ImageTk.PhotoImage(imagen_redimensionada)
    except Exception as e:
        print(f"Error al redimensionar {ruta}: {e}")
        return None