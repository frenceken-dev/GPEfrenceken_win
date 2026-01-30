# Gestion_frenceken.spec
# Build configuration for macOS app bundle with PyInstaller

from PyInstaller.utils.hooks import collect_submodules
from PyInstaller.building.build_main import Analysis, PYZ, EXE, BUNDLE
import os

project_name = "GPEfrenceken"
main_script = "modulo_main.py"
icon_path = "inic.icns"

datas = [
    ('ikigai_inventario.db', '.'),
    ('Img/logo/logo_ikigai.png', 'Img/logo/'),
    ('Img/busqueda/img-busqueda.png', 'Img/busqueda/'),
    ('inic.icns', '.'),
]

hiddenimports = []
hiddenimports += collect_submodules('tkinter')
hiddenimports += collect_submodules('reportlab')
hiddenimports += collect_submodules('PIL')
hiddenimports += collect_submodules('sqlite3')

a = Analysis(
    [main_script],
    pathex=[os.getcwd()],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=['tests', 'unittest'],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name=project_name,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon=icon_path
)

app = BUNDLE(
    exe,
    name=f"{project_name}.app",
    icon=icon_path,
    bundle_identifier="com.frenc.ken.gestion"
)
