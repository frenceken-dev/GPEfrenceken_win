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

pyz = PYZ(a.pure)

# Configuración del ejecutable para Windows
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Gestion_frenceken',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    icon='iniciar.ico',  # Cambié la extensión de .icns a .ico (formato de icono para Windows)
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    name='Gestion_frenceken',
)

