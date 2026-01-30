from setuptools import setup
import os

APP = ['modulo_main.py']

DATA_FILES = [
    ('Img/logo', ['Img/logo/logo_ikigai.png']),
    ('Img/busqueda', ['Img/busqueda/img-busqueda.png']),
    ('', ['ini.icns']),
]

HIDDEN_IMPORTS = [
    'tkinter',
    'tkinter.ttk',
    'tkinter.filedialog',
    'tkinter.messagebox',
    'tkinter.simpledialog',
    'PIL',
    'PIL._imagingtk',
    'PIL.ImageTk',
    'reportlab',
    'sqlite3',
    'tkcalendar',
    'babel',
    'pytz',
]

OPTIONS = {
    'argv_emulation': False,
    'iconfile': 'ini.icns',
    'includes': HIDDEN_IMPORTS,
    'packages': ['PIL', 'reportlab', 'tkcalendar', 'babel', 'pytz'],
    'strip': False,
    'compressed': False,
    'optimize': 0,
    'plist': {
        'CFBundleName': 'GPEfrenceken',
        'CFBundleDisplayName': 'GPEfrenceken',
        'CFBundleIdentifier': 'com.frenc.ken.gestion',
        'CFBundleVersion': '1.0.0',
        'NSHighResolutionCapable': True,
        'LSUIElement': False,
    },
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    package_dir={'jaraco': 'fake_modules/jaraco'},  # <- apuntamos al stub vacío
)


# """
# setup.py — Plantilla base funcional para py2app en macOS

# 💡 Recomendado:
# - Ejecutar dentro de un entorno virtual limpio (venv)
# - Instalar py2app con: pip install py2app
# - Construir con: python setup.py py2app -A  (modo alias)
#                  python setup.py py2app     (build final)
# """

# from setuptools import setup

# APP = ['modulo_main.py']  # Tu archivo principal
# APP_NAME = 'GPEfrenceken'
# DATA_FILES = [
#     ('', ['ikigai_inventario.db']),
#     ('Img/logo', ['Img/logo/logo_ikigai.png']),
#     ('Img/busqueda', ['Img/busqueda/img-busqueda.png']),
#     ('', ['ini.icns']),
# ]  # Si tienes archivos externos (iconos, db, etc.)
# OPTIONS = {
#     'argv_emulation': True,  # Permite que los argumentos funcionen en macOS
#     'packages': [
#         'jaraco.text',        # Evita el error de importación
#         'jaraco.functools',
#         'jaraco.context',
#     ],
#     'includes': [
#         'os', 'sys', 'pkg_resources', 'json', 'tkinter'
#     ],
#     'excludes': [
#         'PyQt5', 'matplotlib', 'pandas', 'pygame', 'lxml'
#     ],
#     'plist': {
#         'CFBundleName': APP_NAME,
#         'CFBundleDisplayName': APP_NAME,
#         'CFBundleIdentifier': 'com.gpefrenceken.launcher',
#         'CFBundleVersion': '1.0.0',
#         'CFBundleShortVersionString': '1.0.0',
#         'LSMinimumSystemVersion': '10.13.0',
#         'NSHighResolutionCapable': True,
#         'NSPrincipalClass': 'NSApplication'
#     },
#     'iconfile': 'ini.icns',  # Opcional: cambia si tienes tu ícono
#     'resources': ['openssl.ca'],  # Evita errores SSL (opcional)
#     'strip': False,  # Evita que py2app elimine binarios necesarios
#     'semi_standalone': True,  # Permite usar módulos del sistema
# }

# setup(
#     app=APP,
#     name=APP_NAME,
#     data_files=DATA_FILES,
#     options={'py2app': OPTIONS},
#     setup_requires=['py2app'],
# )
