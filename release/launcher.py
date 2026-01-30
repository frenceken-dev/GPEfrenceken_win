import os
import subprocess
import traceback

def leer_version(ruta_version):
    if not os.path.exists(ruta_version):
        return "0.0.0"
    with open(ruta_version, "r") as f:
        return f.read().strip()

def comparar_versiones(v_local, v_nueva):
    return tuple(map(int, v_nueva.split("."))) > tuple(map(int, v_local.split(".")))

def lanzar_programa():
    try:
        ruta_actual = os.path.dirname(os.path.abspath(__file__))
        ruta_version_local = os.path.join(ruta_actual, "version.txt")
        ruta_version_nueva = os.path.join(ruta_actual, "version_nueva.txt")
        ruta_app = os.path.expanduser("~/Documents/GPEfrenceken/dist/Gestion_FrencKen")

        v_local = leer_version(ruta_version_local)
        v_nueva = leer_version(ruta_version_nueva)

        log_path = os.path.join(ruta_actual, "launcher_log.txt")
        with open(log_path, "w") as log:
            log.write(f"Versión instalada: {v_local}\n")
            log.write(f"Versión disponible: {v_nueva}\n")
            log.write(f"Ruta de ejecución: {ruta_app}\n")

            if comparar_versiones(v_local, v_nueva):
                log.write("Nueva versión disponible.\n")
            else:
                log.write("El programa está actualizado.\n")

            if os.path.exists(ruta_app):
                log.write("Iniciando la aplicación...\n")
                try:
                    subprocess.Popen([ruta_app])
                    log.write("Ejecutado correctamente.\n")
                except Exception as e:
                    log.write(f"Error al ejecutar: {e}\n")
            else:
                log.write(f"No se encontró el ejecutable en: {ruta_app}\n")

    except Exception as e:
        with open("launcher_fatal_error.txt", "w") as f:
            f.write(traceback.format_exc())

if __name__ == "__main__":
    lanzar_programa()
