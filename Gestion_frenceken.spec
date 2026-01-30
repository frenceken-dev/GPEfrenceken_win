# -*- mode: python ; coding: utf-8 -*-
block_cipher = None

# Configuración para Windows
a = Analysis(
    ['modulo_main.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('ikigai_inventario.db', '.'),
        ('Img/busqueda/*', 'Img/busqueda'),
        ('Img/logo/*', 'Img/logo')
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.simpledialog',
        'tkinter.messagebox',
        'sqlite3',
        'ctypes',
        'PIL',
        'multiprocessing',
        'queue',
        'os',
        'shutil',
        'datetime',
        'time',
        'pickle',
        'json',
        'csv',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

