# recursos.py

import sys
import os
import platform
import tkinter as tk

def resource_path(relative_path):
    """ Obtiene la ruta absoluta al recurso, funciona para dev y para PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Rutas de imágenes
DB_PATH = resource_path('ikigai_inventario.db')
LOGO_PATH = resource_path("Img/logo/logo_ikigai.png")
IMAGEN_BUSQUEDA_PATH = resource_path('Img/busqueda/img-busqueda.png')


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
    border_color = border_color or "#333333"
    border_width = border_width or 2
    font = font or ("Arial", 10, "bold")
    cursor = cursor or "hand2"

    # Colores interactivos
    hover_color_local = hover_color or "#333333"
    focus_color_local = focus_color  # ← solo si se pasa, si no queda None
    focus_width = focus_width if focus_width is not None else 2

    sistema = platform.system()

    # --- macOS o modo redondeado ---
    if sistema == "Darwin" or modo == "redondeado":
        cont = tk.Frame(parent, bg=parent.cget("bg"), highlightthickness=0)
        canvas = tk.Canvas(
            cont,
            width=ancho,
            height=alto,
            bg=parent.cget("bg"),
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
                canvas.itemconfig(boton_shape, fill="#333333")
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


def configurar_toplevel(ventana, titulo="Ventana", ancho_min=400, alto_min=300):
    """
    Configura un Toplevel sin afectar la ventana principal ni heredar su geometría.
    """
    ventana.title(titulo)

    # Asegura que el fondo sea blanco o neutro (evita heredar el del root)
    ventana.configure(bg="#f0f0f0")

    # Quita cualquier modo fullscreen heredado del root
    try:
        ventana.attributes('-fullscreen', False)
    except Exception:
        pass

    ventana.resizable(False, False)
    ventana.grab_set()
    ventana.update_idletasks()  # Calcula el tamaño real

    ancho = max(ventana.winfo_reqwidth(), ancho_min)
    alto = max(ventana.winfo_reqheight(), alto_min)
    x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana.winfo_screenheight() // 2) - (alto // 2)

    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

