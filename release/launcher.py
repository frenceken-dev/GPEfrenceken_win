import os
import requests
import subprocess
import shutil

# Configuración
GITHUB_REPO = "https://raw.githubusercontent.com/frenceken-dev/GPEfrenceken_win/master/"
VERSION_URL = GITHUB_REPO + "version.txt"
EXE_URL = GITHUB_REPO + "releases/programa_principal.exe"
LOCAL_EXE = "programa_principal.exe"
LOCAL_VERSION_FILE = "version.txt"

def get_latest_version():
    try:
        response = requests.get(VERSION_URL)
        return response.text.strip()
    except:
        return None

def download_latest_exe():
    try:
        response = requests.get(EXE_URL, stream=True)
        with open(LOCAL_EXE, 'wb') as f:
            f.write(response.content)
        return True
    except:
        return False

def run_program():
    if os.path.exists(LOCAL_EXE):
        subprocess.Popen([LOCAL_EXE])

def main():
    latest_version = get_latest_version()
    if latest_version:
        print(f"Versión más reciente: {latest_version}")
        # Aquí podrías comparar con la versión local si la tienes guardada
        if download_latest_exe():
            print("Descarga completada. Ejecutando...")
            run_program()
        else:
            print("Error al descargar la actualización.")
    else:
        print("No se pudo verificar la versión.")

if __name__ == "__main__":
    main()
