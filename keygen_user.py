# Modulo Generador de Contraseñas para nuevos usuarios.
from tkinter import messagebox
import hashlib
import getpass  # Para ocultar la clave al ingresarla
from db import validar_credenciales

# Base de datos simulada (en un programa real, usa SQLite o un archivo cifrado)
usuarios = {}  # Formato: {usuario: {"hash_clave": "...", "pregunta": "...", "respuesta": "..."}}

def validar_clave_segura(clave):
    """Verifica que la clave cumpla con los requisitos."""
    if len(clave) < 8 or len(clave) > 16:
        messagebox.showerror("⚠️ Error", "La clave debe tener entre 10 y 16 caracteres.")
        return False, "La clave debe tener entre 10 y 16 caracteres."
    
    if not any(c.isupper() for c in clave):
        messagebox.showerror("⚠️Error", "Debe incluir al menos una mayúscula.")
        return False, "Debe incluir al menos una mayúscula."
    
    if not any(c.islower() for c in clave):
        messagebox.showerror("⚠️ Error", "Debe incluir al menos una minúscula.")
        return False, "Debe incluir al menos una minúscula."
    
    if not any(c.isdigit() for c in clave):
        messagebox.showerror("⚠️ Error", "Debe incluir al menos un número.")
        return False, "Debe incluir al menos un número."
    
    if not any(c in "!@#$%^&*,.?=:;'¿¡" for c in clave):
        messagebox.showerror("⚠️ Error", "Debe incluir al menos un carácter especial (!@#$%^&*,.?=:;'¿¡).")
        return False, "Debe incluir al menos un carácter especial (!@#$%^&*,.?=:;'¿¡)."
    
    return True, "Clave válida."

def cifrar_clave(clave):
    """Genera el hash SHA-256 de la clave."""
    return hashlib.sha256(clave.encode()).hexdigest()


def registrar_usuario(usuario, clave, pregunta, respuesta):
    """Registra un usuario con su clave (solo guarda el hash)."""
    hash_clave = cifrar_clave(clave)
    usuarios[usuario] = {
        "hash_clave": hash_clave,
        "pregunta": pregunta,
        "respuesta": respuesta.lower()  # Guardar en minúsculas para evitar errores
    }
    print(f"Usuario '{usuario}' registrado con éxito.")
    print("Clave Hash: ", usuarios[usuario[-1]])
    

def validar_clave(usuario, clave):
    """Valida si la clave ingresada coincide con el hash almacenado."""
    if usuario not in usuarios:
        return False, "Usuario no registrado."
    hash_almacenado = usuarios[usuario]["hash_clave"]
    hash_ingresado = cifrar_clave(clave)
    if hash_ingresado == hash_almacenado:
        return True, "Acceso concedido."
    else:
        return False, "Clave incorrecta."
    

def recuperar_clave(usuario, respuesta):
    if usuario not in usuarios:
        return False, "Usuario no registrado."
    if respuesta.lower() == usuarios[usuario]["respuesta"]:
        # No mostramos la clave, sino que permitimos restablecerla
        nueva_clave = getpass.getpass("Crea tu nueva clave (10-16 caracteres): ")
        valido, mensaje = validar_clave_segura(nueva_clave)
        if valido:
            usuarios[usuario]["hash_clave"] = cifrar_clave(nueva_clave)
            return True, "Clave restablecida con éxito."
        else:
            return False, f"⚠️ Error: {mensaje}"
    else:
        return False, "Respuesta incorrecta."
    

# --- Ejemplo de uso ---
if __name__ == "__main__":
    # print("=== REGISTRO DE USUARIO ===")
    # usuario = input("Ingresa tu nombre de usuario: ")
    # clave = getpass.getpass("Crea tu clave (10-16 caracteres, con mayúsculas, minúsculas, números y !@#$%^&*,.?=:;'¿¡): ")
    # valido, mensaje = validar_clave_segura(clave)
    # if not valido:
    #     print(f"⚠️ Error: {mensaje}")
    # else:
    #     pregunta = input("Ingresa una pregunta de seguridad (ejemplo: '¿Cuál es el nombre de tu primera mascota?'): ")
    #     respuesta = input("Ingresa la respuesta a tu pregunta de seguridad: ")
    #     registrar_usuario(usuario, clave, pregunta, respuesta)

    # # Simular inicio de sesión
    # print("\n=== INICIO DE SESIÓN ===")
    # usuario_login = input("Usuario: ")
    # clave_login = getpass.getpass("Clave: ")
    # acceso, mensaje = validar_clave(usuario_login, clave_login)
    # print(mensaje)

    # # Simular recuperación de clave
    # if not acceso:
    #     print("\n=== RECUPERACIÓN DE CLAVE ===")
    #     usuario_recuperar = input("Usuario: ")
    #     respuesta_recuperar = input(f"Responde: {usuarios[usuario_recuperar]['pregunta']}: ")
    #     recuperado, mensaje = recuperar_clave(usuario_recuperar, respuesta_recuperar)
    #     print(mensaje)

    clave = "Ro123.123"
    hash_clave = cifrar_clave(clave)
    print(hash_clave)