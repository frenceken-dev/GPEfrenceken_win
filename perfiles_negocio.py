# perfiles_negocio.py
"""Gestión de perfiles de negocio: cada perfil tiene su propia base de datos."""
import os
import json
import sqlite3
from recursos import CARPETA_DATOS, DB_PATH, PERFILES_PATH


def cargar_perfiles():
    """
    Devuelve la lista de perfiles guardados cuyo archivo de BD existe.
    Las entradas 'fantasma' (BD borrada manualmente) se ignoran y se limpian del registro.
    """
    if not os.path.exists(PERFILES_PATH):
        return []
    try:
        with open(PERFILES_PATH, "r", encoding="utf-8") as f:
            perfiles = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        print(f"⚠️ Error leyendo perfiles.json: {e}")
        return []

    # Filtrar entradas cuya BD ya no existe
    validos = [p for p in perfiles if os.path.exists(p.get("db", ""))]

    if len(validos) != len(perfiles):
        # Había fantasmas: limpiar el registro para dejarlo consistente
        print(f"⚠️ Se limpiaron {len(perfiles) - len(validos)} perfil(es) sin base de datos.")
        guardar_perfiles(validos)

    return validos


def guardar_perfiles(perfiles):
    with open(PERFILES_PATH, "w", encoding="utf-8") as f:
        json.dump(perfiles, f, indent=2, ensure_ascii=False)


def clonar_esquema(origen, destino):
    """Copia la estructura (tablas, índices, triggers) de una BD a otra, SIN datos."""
    src = sqlite3.connect(origen)
    dst = sqlite3.connect(destino)
    try:
        for (sql,) in src.execute(
            "SELECT sql FROM sqlite_master WHERE sql IS NOT NULL AND name NOT LIKE 'sqlite_%'"
        ):
            dst.execute(sql)
        dst.commit()
    finally:
        src.close()
        dst.close()


def crear_perfil(nombre, db_plantilla=DB_PATH):
    """
    Crea un nuevo perfil de negocio con su propia BD.
    Clona el esquema de la BD plantilla para que las tablas existan vacías.
    Devuelve el dict del perfil creado.
    """
    os.makedirs(CARPETA_DATOS, exist_ok=True)
    slug = "".join(c if c.isalnum() else "_" for c in nombre.strip().lower())
    ruta_bd = os.path.join(CARPETA_DATOS, f"{slug}.db")
    n = 1
    while os.path.exists(ruta_bd):          # evitar sobrescribir
        n += 1
        ruta_bd = os.path.join(CARPETA_DATOS, f"{slug}_{n}.db")

    if os.path.exists(db_plantilla):
        clonar_esquema(db_plantilla, ruta_bd)
    else:
        sqlite3.connect(ruta_bd).close()   # BD vacía; se creará al inicializar

    perfil = {"nombre": nombre.strip(), "db": ruta_bd}
    perfiles = cargar_perfiles()
    perfiles.append(perfil)
    guardar_perfiles(perfiles)
    return perfil


def eliminar_perfil(nombre, a_papelera=True):
    """
    Elimina un perfil de negocio del registro.
    Por seguridad, NO borra la base de datos: la mueve a db/descartados/.
    Si a_papelera=False, la borra definitivamente (¡usar con mucho cuidado!).

    Args:
        nombre (str): Nombre del negocio tal como aparece en el registro.
        a_papelera (bool): True (recomendado) mueve la BD a descartados.

    Returns:
        Tuple[bool, str]: (exito, mensaje).
    """
    perfiles = cargar_perfiles()
    perfil = next((p for p in perfiles if p["nombre"] == nombre), None)

    if perfil is None:
        return False, f"No se encontró el negocio '{nombre}'."

    ruta_bd = perfil.get("db", "")

    if a_papelera:
        # Mover la BD (y sus archivos auxiliares WAL/SHM si existen) a descartados/
        carpeta_descartados = os.path.join(CARPETA_DATOS, "descartados")
        os.makedirs(carpeta_descartados, exist_ok=True)

        base = os.path.basename(ruta_bd)
        from datetime import datetime
        marca = datetime.now().strftime("%Y%m%d_%H%M%S")
        destino = os.path.join(carpeta_descartados, f"{marca}_{base}")

        try:
            os.replace(ruta_bd, destino)
            # Archivos acompañantes de SQLite (modo WAL), si existieran
            for sufijo in ("-wal", "-shm"):
                origen_aux = ruta_bd + sufijo
                if os.path.exists(origen_aux):
                    os.replace(origen_aux, destino + sufijo)
        except OSError as e:
            return False, f"No se pudo mover la base de datos: {e}"
    else:
        try:
            os.remove(ruta_bd)
            for sufijo in ("-wal", "-shm"):
                origen_aux = ruta_bd + sufijo
                if os.path.exists(origen_aux):
                    os.remove(origen_aux)
        except OSError as e:
            return False, f"No se pudo borrar la base de datos: {e}"

    # Quitar la entrada del registro
    perfiles_restantes = [p for p in perfiles if p["nombre"] != nombre]
    guardar_perfiles(perfiles_restantes)

    if a_papelera:
        return True, (f"Negocio '{nombre}' eliminado del registro.\n"
                    "Su base de datos fue movida a 'db/descartados/' por seguridad.")
    return True, f"Negocio '{nombre}' y su base de datos fueron eliminados definitivamente."