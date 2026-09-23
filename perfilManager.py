# Modulo para la personalización de sesión de un usuario.
import tkinter as tk
from tkinter import messagebox, ttk, colorchooser, filedialog
import subprocess, os, shutil
from pathlib import Path
from recursos import crear_boton, redimensionar_imagen, DOWLOAD_LOGO, configurar_toplevel
from databasemanager import DataBaseManager

db_connect = DataBaseManager()
class perfilUsuario():
    """Maneja la configuración de la sesión del usuario"""
    
    def __init__(self, root, usuario_actual):
        self.usuario = usuario_actual
        self.root = root
        #self.root.title("Configuración del Perfil")
        self.color_fondo_default = {"fondo": "#a0b9f0", "fuente": "#ffffff", "fondo_menu": "#2C3E50", "fondo_img": "#94a7ac"}
        self.color_pantalla = ""
        self.color_menu = ""
        self.color_letra = ""
        self.logotipo = "Frenceken-dev"
        self.ruta = None 
        self.conf_aplicada = [{"fondo_pantalla": None},
                                {"fondo_letra": None},
                                {"fondo_menu": None},
                                {"imag_fondo": None} ]
        self.guardar_config = []   
        self.interfaz_configuracion()        
        
    def cargar_configuracion(self):
        """Cargar la configuración"""
        pass
    
    
    def interfaz_configuracion(self):
        """Usuario configura su perfil"""
        
        # Tamaño fijo.
        frame_fijo = tk.Toplevel(self.root)  
        configurar_toplevel(frame_fijo, titulo="Configurar Perfíl", ancho_min=700, alto_min=500, color_fondo="#a0b9f0")
        
        #frame_fijo.pack(fill="both", expand=True, padx=5, pady=5)
        #frame_fijo.propagate(False)
        
        frame_config = tk.Frame(frame_fijo, bg="#a0b9f0")
        frame_config.columnconfigure(0, weight=1)
        frame_config.columnconfigure(1, weight=1)
        frame_config.rowconfigure(0, weight=1)
        frame_config.rowconfigure(1, weight=1)
        frame_config.pack(fill="both", expand=True)
        
        frame_fuente = tk.LabelFrame(frame_config, text="Tipo de letra")
        # Expande solo el frame de muestra del color.
        frame_fuente.rowconfigure(1, weight=1)
        frame_fuente.columnconfigure(1, weight=1)
        frame_fuente.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        frame_color_fondo = tk.LabelFrame(frame_config, text="Color de fondo")
        # Expande solo el frame de muestra del color.
        frame_color_fondo.rowconfigure(1, weight=1)
        frame_color_fondo.columnconfigure(1, weight=1)
        frame_color_fondo.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
        
        frame_color_fondo_menu = tk.LabelFrame(frame_config, text="Color de fondo del Menu")
        # Expande solo el frame de muestra del color.
        frame_color_fondo_menu.rowconfigure(1, weight=1)
        frame_color_fondo_menu.columnconfigure(1, weight=1)
        frame_color_fondo_menu.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        
        frame_logo = tk.LabelFrame(frame_config, text="Logo de la Tienda")
        # Expande solo el frame de muestra del color.
        frame_logo.rowconfigure(1, weight=1)
        frame_logo.columnconfigure(1, weight=1)
        frame_logo.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        
        
        # Cambiel Color de la fuente.
        boton_fuente_color = crear_boton(frame_fuente, texto="Color de la Fuente:",
                                        ancho=18,
                                        alto=15,
                                        comando=lambda:self.seleccionar_color("fuente"))
        boton_fuente_color.grid(row=0, column=0, padx=10, pady=15, sticky="nsew")
        label_fuente = tk.Label(frame_fuente
                                , text="Color de la Fuente:")
        label_fuente.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.frame_fuente_seleccionado = tk.Frame(frame_fuente, width=150, height=75, bg=self.color_fondo_default["fuente"])
        self.frame_fuente_seleccionado.grid(row=1, column=1, padx=15, pady=15, sticky="nsew")
        
        # Cambiar Color del Fondo Principal.
        boton_fondo_color = crear_boton(frame_color_fondo, texto="Color Fondo principal",
                                        ancho=18,
                                        alto=15,
                                        comando=lambda:self.seleccionar_color("fondo"))
        boton_fondo_color.grid(row=0, column=0, padx=10, pady=15, sticky="nsew")
        label_fondo = tk.Label(frame_fuente, text="Color del Fondo:")
        label_fondo.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.frame_fondo_seleccionado = tk.Frame(frame_color_fondo, width=150, height=75, bg=self.color_fondo_default["fondo"])
        self.frame_fondo_seleccionado.grid(row=1, column=1, padx=15, pady=15, sticky="nsew")

        # Cambiar Color del Fondo del Menu..
        boton_fondo_color = crear_boton(frame_color_fondo_menu, texto="Color Fondo Menu",
                                        ancho=18,
                                        alto=15,
                                        comando=lambda:self.seleccionar_color("fondo_menu"))
        boton_fondo_color.grid(row=0, column=0, padx=10, pady=15, sticky="nsew")
        label_fondo = tk.Label(frame_color_fondo_menu, text="Color del Fondo:")
        label_fondo.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.frame_fondo_seleccionado_menu = tk.Frame(frame_color_fondo_menu, width=150, height=75, bg=self.color_fondo_default["fondo_menu"])
        self.frame_fondo_seleccionado_menu.grid(row=1, column=1, padx=15, pady=15, sticky="nsew")
        
        # Cambiar Imagen
        boton_fondo_color = crear_boton(frame_logo, texto="Seleccionar Imágen",
                                        ancho=18,
                                        alto=15,
                                        comando=self.cambiar_logo)
        boton_fondo_color.grid(row=0, column=0, padx=10, pady=15, sticky="nsew")
        logo_fondo = tk.Label(frame_logo, text="Logo:")
        logo_fondo.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.frame_logo_im = tk.Frame(frame_logo, width=150, height=75, bg=self.color_fondo_default["fondo_img"])
        self.frame_logo_im.grid(row=1, column=1, padx=15, pady=15, sticky="nsew") 
        
        bton_filtar_guardar = crear_boton(frame_fijo,
            texto="Guardar configuración",
            ancho=20,
            alto=30,
            comando=self.filtrar_config         
            )
        bton_filtar_guardar.pack(side="bottom", pady=10, expand=False)
        
        
    def seleccionar_color(self, llave):
        """Aqui se elige el color del fondo"""
        #print(f"La Llave es: {llave}")
        dato = llave
        select_fondo = colorchooser.askcolor(title="Seleccionar Fondo")
        if select_fondo:
            if dato == "fondo":
                if dato in self.color_fondo_default:
                    #print(f"La Llave es: {llave} dentro del fondo")
                    self.color_fondo_default["fondo"] = select_fondo
                    # print(f"El color de fondo es: {self.color_fondo_default}")
                    formatos = self.color_fondo_default["fondo"]
                    color_exadecimal = formatos[1]
                    # print(f"Los formatos son: {formatos}")
                    self.frame_fondo_seleccionado.config(bg=color_exadecimal)
                    self.color_pantalla = select_fondo[1]
                    self.guardar_configuracion(1)
                    
            elif dato == "fuente":   
                if dato in self.color_fondo_default:
                    #print(f"La Llave es: {llave}, dentro de la fuente")
                    self.color_fondo_default["fuente"] = select_fondo
                    formatos = self.color_fondo_default["fuente"]
                    color_exadecimal = formatos[1]
                    self.frame_fuente_seleccionado.config(bg=color_exadecimal)
                    self.color_letra = select_fondo[1]
                    self.guardar_configuracion(2)
                    
            elif dato == "fondo_menu":   
                if dato in self.color_fondo_default:
                    #print(f"La Llave es: {llave}, dentro de la fuente")
                    self.color_fondo_default["fuente"] = select_fondo
                    formatos = self.color_fondo_default["fuente"]
                    color_exadecimal = formatos[1]
                    self.frame_fondo_seleccionado_menu.config(bg=color_exadecimal)
                    self.color_menu = select_fondo[1]
                    self.guardar_configuracion(3)
                    
    
    def cambiar_logo(self):
        """Seleciona una nueva imagen para el logo"""
        
        self.ruta = filedialog.askopenfilename(initialdir=DOWLOAD_LOGO)
        if not self.ruta:  # Si el usuario cancela, no hacer nada
            return

        # Redimensionar y guardar referencia
        self.imagen_actual = redimensionar_imagen(self.ruta, 150, 150)
        
        # Si el Label ya existe, actualizar su imagen
        if hasattr(self, 'label_logo'):
            os.makedirs("Img/logo_usuario", exist_ok=True)
            self.label_logo.config(image=self.imagen_actual)
            
        else:
            # Crear el Label la primera vez
            os.makedirs("Img/logo_usuario", exist_ok=True)
            self.label_logo = tk.Label(self.frame_logo_im, image=self.imagen_actual, bg=self.color_fondo_default["fondo_img"])
            self.label_logo.pack(fill="x", expand=True)
        
        ruta_carpeta = Path("Img/logo_usuario")
        
        if ruta_carpeta:
            # Borrar todo lo que haya dentro
            for archivo in ruta_carpeta.iterdir():
                if archivo.is_file():
                    archivo.unlink()
                    
            shutil.copy(self.ruta, ruta_carpeta)
            self.guardar_configuracion(4)
        else:
            print("No se existe la ruta")
            
        
    def guardar_configuracion(self, numero):
        """Envia la configuracion a la DB"""
        
        match numero:
            case 1:
                print(f"El fondo Pantalla es: {self.color_pantalla}")
                self.conf_aplicada[0]["fondo_pantalla"] = self.color_pantalla
                self.guardar_config.append(self.conf_aplicada[0])
            case 2:
                print(f"El fondo Letra es: {self.color_letra}")
                self.conf_aplicada[1]["fondo_letra"] = self.color_letra
                self.guardar_config.append(self.conf_aplicada[1])
            case 3:
                print(f"El fondo Menu es: {self.color_menu}")
                self.conf_aplicada[2]["fondo_menu"] = self.color_menu
                self.guardar_config.append(self.conf_aplicada[2])
            case _:
                print(f"La Imágen seleccionada es: {self.ruta}")
                self.conf_aplicada[3]["imag_fondo"]  = self.ruta
                self.guardar_config.append(self.conf_aplicada[3])
            
        print(f"Las configuraciones elegidas son: {self.conf_aplicada}")
        print(f"Las configuraciones elegidas son: {type(self.conf_aplicada)}")
        
        
                
        print(f"la config es: {self.guardar_config} datos guardados: {len(self.guardar_config)}")
    
    def filtrar_config(self):
        """Comprobar la configuaraciones del usuario y dejar default las no editadas."""
        #print(f"Dentro de Filtrado")
        print(f"La inf dentro de la variable conf_aplicada es: {self.conf_aplicada}")
        
        if self.conf_aplicada[0]["fondo_pantalla"] == None:
            pant_principal = self.color_fondo_default["fondo"]
        else:
            pant_principal = self.conf_aplicada[0]["fondo_pantalla"] #"#a0b9f0"
        #print(f"Color de pantalla principal: {pant_principal}")
        
        if self.conf_aplicada[1]["fondo_letra"] == None:
            fuente = self.color_fondo_default["fuente"]    
        else:
            fuente = self.conf_aplicada[1]["fondo_letra"]
        #print(f"Color de fuente: {fuente}")
        
        if self.conf_aplicada[2]["fondo_menu"] == None:
            pantalla_m =  self.conf_aplicada[2]["fondo_menu"]  
        else:
            pantalla_m = self.color_fondo_default["fondo_menu"]
        #print(f"Color de pantalla menu: {pantalla_m}")
        
        logo = self.conf_aplicada[3] #if self.conf_aplicada[3] == None else self.color_fondo_default["fondo_img"]
        #print(f"Logo: {logo}")
        
        logo_ruta = logo["imag_fondo"]
        if logo_ruta:
            logo_ruta_relativa_plit = logo_ruta.split("/")
            #print(f"logo_ruta {logo_ruta_relativa_plit}")
            logo_ruta_relativa = logo_ruta_relativa_plit[-1]
        else:
            logo_ruta_relativa = self.color_fondo_default["fondo_img"]
        

        # print(f"""CONFIGURACIÖN FINAL
        #     Pantalla Principal : {pant_principal}\n
        #     Color de la fuente: {fuente}\n
        #     Pantalla Menú: {pantalla_m}\n
        #     Logo: {logo_ruta_relativa}""") 

        configuracion_usuario = [pant_principal, pantalla_m, fuente, logo_ruta_relativa]
        #print(f"la configuración final es: {configuracion_usuario}")
        guardado = db_connect.configuracion_usuario(configuracion_usuario, self.usuario)
        print(guardado)
    
if __name__ == "__main__":
    root = tk.Tk()
    probar = perfilUsuario(root, "Ron")
    root.mainloop()