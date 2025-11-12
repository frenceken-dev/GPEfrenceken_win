# modulo_db.py
# modulo_db.py
"""Modulo Base de Datos de las Películas"""
import os
import sqlite3
import subprocess
from datetime import datetime
from zoneinfo import ZoneInfo
import pytz
from tkinter import messagebox, Toplevel
from recursos import DB_PATH

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, DB_PATH) # agregado ayer

# database
def init_db():
    pass
    

# Registrar un nuevo Proveedor.
def insertar_proveedor(nombre, contacto, telefono, email, direccion):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Proveedores (nombre, contacto, telefono, email, direccion)
        VALUES (?, ?, ?, ?, ?)
    ''', (nombre, contacto, telefono, email, direccion))
    conn.commit()
    conn.close()
    

# Obtener todos los Proveedores .
def obtener_proveedores():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT nombre FROM Proveedores')
    proveedores = cursor.fetchall()
    conn.close()
    return proveedores


# Obtener ID del proveedor por su nombre. 
def obtener_id_proveedor_por_nombre(nombre_proveedor):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id_proveedor FROM Proveedores
        WHERE nombre = ?
    ''', (nombre_proveedor,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else None


# Obtener ID de la Factura por su numero. 
def obtener_id_factura_por_numero(numero_factura):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id_factura FROM Facturas
        WHERE numero_factura = ?
    ''', (numero_factura,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else None


# Obtener ID del material por su código.
def obtener_id_material_por_codigo(codigo):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT id_material FROM Materiales WHERE codigo = ?', (codigo,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else None


# Obtener ID del nuevo producto por su código.
def obtener_id_producto_por_codigo(codigo):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT id_producto FROM Productos WHERE codigo = ?', (codigo,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else None


# Ingresar los Items de las facturas.
def insertar_material(codigo, nombre, tipo, tamaño, color, stock, precio, costo_unitario, id_proveedor):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
    # Obtener el id_proveedor usando el nombre
        #id_proveedor = obtener_id_proveedor_por_nombre(nombre)
        
        cursor.execute('''
            INSERT INTO Materiales (codigo, nombre, tipo, tamaño, color, stock, precio, costo_unitario, id_proveedor)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (codigo, nombre, tipo, tamaño, color, stock, precio, costo_unitario, id_proveedor))
        conn.commit()
    except Exception as e:
        conn.rollback()
    finally:
        conn.close()
        

# Ingresar datos Basicos de la factura para el ingreso de Items.
def insertar_factura(numero_factura, fecha, nombre_proveedor):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Obtener el id_proveedor usando el nombre
    id_proveedor = obtener_id_proveedor_por_nombre(nombre_proveedor)

    # Si el proveedor no existe, crear uno nuevo
    if id_proveedor is None:
        # Aquí podrías pedir más detalles del proveedor, pero por simplicidad, solo usamos el nombre
        cursor.execute('''
            INSERT INTO Proveedores (nombre)
            VALUES (?)
        ''', (nombre_proveedor,))
        conn.commit()
        id_proveedor = cursor.lastrowid  # Obtener el id del proveedor recién insertado

    fecha_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO Facturas (numero_factura, fecha, fecha_registro, id_proveedor)
        VALUES (?, ?, ?, ?)
    ''', (numero_factura, fecha, fecha_registro, id_proveedor))
    conn.commit()
    conn.close()
    

#  Insertar los detalles de una factura.
def insertar_detalle_factura(id_factura, id_material, stock,  precio, costo_unitario):
    print("id: ", id_factura)
    print("id-materia: ", id_material)
    print("stock: ", stock)
    print("Precio: ", precio)
    print("Costo Uni.: ", costo_unitario)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Detalle_Factura (id_factura, id_material, stock, precio, costo_unitario)
        VALUES (?, ?, ?, ?, ?)
    ''', (id_factura, id_material, stock, precio, costo_unitario))
    conn.commit()
    conn.close()
    
    
# Se registra un nuevo producto creado por Ikigai GmbH.
def insertar_producto(codigo, nombre, tipo, costo_producto, precio_venta, materiales_usados, tiempo_fabricacion, cantidad, descripcion):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    fecha_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO Productos (codigo, nombre, tipo, costo_producto, precio_venta, materiales_usados, tiempo_fabricacion, cantidad, fecha_registro, descripcion)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (codigo, nombre, tipo, costo_producto, precio_venta, ", ".join(materiales_usados), tiempo_fabricacion, cantidad, fecha_registro, descripcion)) 
    conn.commit()
    conn.close()
    

# Obtener los materiales empleados en un producto creado.
def insertar_detalle_producto(id_producto, id_material, cantidad, tipo, tamaño):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Detalle_Producto
        (id_producto, id_material, cantidad, tipo_material, tamaño_material)
        VALUES (?, ?, ?, ?, ?)
    ''', (id_producto, id_material, cantidad, tipo, tamaño))
    conn.commit()
    conn.close()
    
    
# Obtener Materiales para creacion de producto.
def obtener_materiales():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Materiales')
    materiales = cursor.fetchall()
    conn.close()
    return materiales


# Obtener el nombre del material por el código
def obtener_nombre_material_por_codigo(codigo_material):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT nombre FROM Materiales WHERE codigo = ?', (codigo_material,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else "Desconocido"


# Obtener código del materia por su nombre
def obtener_codigo_material_por_nombre(nombre_material):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT codigo FROM Materiales WHERE nombre = ?', (nombre_material,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else None


# Materales por nombre, tipo, tamaño para crear producto nuevo.
def obtener_codigo_material_por_nombre_color_tipo_tamaño(nombre, color, tipo, tamaño):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT codigo
        FROM Materiales
        WHERE nombre = ? AND color = ? AND tipo = ? AND tamaño = ?
    ''', (nombre, color, tipo, tamaño))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else None


# Obtener el costo Unitario del material
def obtener_costo_unitario_material(codigo_material):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT costo_unitario FROM Materiales WHERE codigo = ?', (codigo_material,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else 0.0


# Función para verificar si el código ya existe en la base de datos
def codigo_existe(codigo):
    # Aquí debes implementar la consulta a tu base de datos
    # Ejemplo con SQLite:
    import sqlite3
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT codigo FROM materiales WHERE codigo=?", (codigo,))
    existe = cursor.fetchone() is not None
    conn.close()
    return existe


# Función para actualizar el stock de un material en la base de datos
def actualizar_stock_material(codigo, cantidad):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE Materiales
        SET stock = stock - ?
        WHERE codigo = ?
    ''', (cantidad, codigo))
    conn.commit()
    conn.close()
    

# Obtener los productos ya creados.
def obtener_productos():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Productos')
    productos = cursor.fetchall()
    conn.close()
    return productos


# Seleccionar el color del material por nombre
def obtener_color_por_material(nombre_material):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT DISTINCT color
        FROM Materiales
        WHERE nombre = ? 
    ''', (nombre_material,))
    resultados = cursor.fetchall()
    conn.close()
    return [resultado[0] for resultado in resultados]


# Seleccionar el tipo del material por nombre
def obtener_tipos_por_material_y_color(nombre_material, color_material):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT DISTINCT tipo
        FROM Materiales
        WHERE nombre = ? AND color = ? 
    ''', (nombre_material, color_material))
    resultados = cursor.fetchall()
    conn.close()
    return [resultado[0] for resultado in resultados]


# Obtener tipo y tamaño de un material.
def obtener_tamaños_por_material_color_tipo(nombre_material, color_material, tipo_material):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT DISTINCT tamaño
        FROM Materiales
        WHERE nombre = ? AND color = ? AND tipo = ?
    ''', (nombre_material, color_material, tipo_material))
    resultados = cursor.fetchall()
    conn.close()
    return [resultado[0] for resultado in resultados]


# Datos seleccionados para el calculo de precio de venta
def obtener_productos_para_costoventa():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''SELECT id_producto, codigo, costo_producto FROM Productos''')
    _3_productos = cursor.fetchall()
    conn.close()
    return _3_productos


# Datos para actualizar el historial de ganancias.
def obtener_productos_para_acthistorial():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''SELECT id_producto, codigo, costo_producto, precio_venta FROM Productos''')
    productos_h = cursor.fetchall()
    conn.close()
    return productos_h


# Guardar en Historial_Ganancias
def guardar_historial(id_producto, mes_año, ganancia, margen):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
            INSERT INTO Historial_Ganancias
            (id_producto, mes, ganancia_total, margen_promedio)
            VALUES (?, ?, ?, ?)
            """,
            (id_producto, mes_año, ganancia, margen)
                )
    conn.commit()
    conn.close()


def registrar_historial_costo(id_producto, costo_anterior, costo_nuevo, es_por_lote, unidades=None, motivo=None):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO Historial_Costos
        (id_producto, fecha, costo_anterior, costo_nuevo, es_por_lote, unidades, motivo)
        VALUES (?, DATE('now'), ?, ?, ?, ?, ?)
        """,
        (id_producto, costo_anterior, costo_nuevo, es_por_lote, unidades, motivo)
    )
    conn.commit()
    conn.close()

# Mostrar el historial de costos por producto.
def mostrar_historial_costos_por_producto(codigo_producto):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT h.fecha, h.costo_anterior, h.costo_nuevo, h.es_por_lote, h.unidades, h.motivo
        FROM Historial_Costos h
        JOIN Productos p ON h.id_producto = p.id_producto
        WHERE p.codigo = ?
        ORDER BY h.fecha DESC
        """,
        (codigo_producto,)
        )
    historial_producto = cursor.fetchall()
    conn.commit()
    conn.close()
    return historial_producto

    
# Mostrar el historial de costos de todos los productos..
def mostrar_historial_costos_general():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
            """
            SELECT p.codigo, h.fecha, h.costo_anterior, h.costo_nuevo, h.es_por_lote, h.unidades, h.motivo
            FROM Historial_Costos h
            JOIN Productos p ON h.id_producto = p.id_producto
            ORDER BY h.fecha DESC
            """
        )
    historial_general = cursor.fetchall()
    conn.commit()
    conn.close()
    return historial_general


# Mostrar Historial de ganacias.
def mostrar_historial_ganancias_producto(codigo_producto):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
            """
            SELECT h.mes, h.ganancia_total, h.margen_promedio
            FROM Historial_Ganancias h
            JOIN Productos p ON h.id_producto = p.id_producto
            WHERE p.codigo = ?
            ORDER BY h.mes DESC
            """,
            (codigo_producto,)
        )
    historial = cursor.fetchall()
    conn.commit()
    conn.close()
    return historial


# Mostrar historial de ganancias mensual general.
def mostrar_historial_general_mensual(mes_str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT p.codigo, h.ganancia_total, h.margen_promedio
        FROM Historial_Ganancias h
        JOIN Productos p ON h.id_producto = p.id_producto
        WHERE h.mes = ?
        ORDER BY p.codigo
        """,
        (mes_str,)
    )

    historial = cursor.fetchall()
    conn.commit()
    conn.close()
    return historial


# Obtener una lista de nombres de proveedores.
def obtener_nombres_proveedores(texto):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT nombre FROM Proveedores WHERE nombre LIKE ?', (f'%{texto}%',))
    proveedores = [row[0] for row in cursor.fetchall()]
    conn.close()
    return proveedores


# Obtener los datos para el módulo de búsqueda.
def buscar_en_bd(tipo_busqueda, valor_busqueda):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    if tipo_busqueda == "Todos los Materiales":
       cursor.execute('SELECT codigo, nombre, tipo, tamaño, color, stock, precio, costo_unitario FROM Materiales')
    
    elif tipo_busqueda == "Proveedor":
        cursor.execute('''
            SELECT Proveedores.nombre, Facturas.numero_factura, Facturas.fecha, Materiales.codigo, Materiales.nombre, Materiales.stock, materiales.precio, materiales.costo_unitario
            FROM Proveedores
            JOIN Facturas ON Proveedores.id_proveedor = Facturas.id_proveedor
            JOIN Detalle_Factura ON Facturas.id_factura = Detalle_Factura.id_factura
            JOIN Materiales ON Detalle_Factura.id_material = Materiales.id_material
            WHERE Proveedores.nombre LIKE ?
        ''', (f"%{valor_busqueda}%",))

    elif tipo_busqueda == "Factura Proveedor":
        cursor.execute('''
            SELECT Proveedores.nombre, Facturas.numero_factura, Facturas.fecha, Materiales.codigo, Materiales.nombre, Materiales.stock, materiales.precio, materiales.costo_unitario
            FROM Facturas
            JOIN Proveedores ON Facturas.id_proveedor = Proveedores.id_proveedor
            JOIN Detalle_Factura ON Facturas.id_factura = Detalle_Factura.id_factura
            JOIN Materiales ON Detalle_Factura.id_material = Materiales.id_material
            WHERE Facturas.numero_factura LIKE ?
        ''', (f"%{valor_busqueda}%",))
    
    elif tipo_busqueda == "Facturas Ventas":
        print("El tipo de busqueda es FActuras Ventas") # aqui llega
        cursor.execute("""
            SELECT 
                Ventas.id_venta AS NumeroFactura,
                Clientes.nombre AS Cliente,
                Ventas.fecha,
                Ventas.subtotal,
                Ventas.descuento,
                Ventas.impuesto,
                Ventas.total
            FROM Ventas
            JOIN Clientes ON Ventas.id_cliente = Clientes.id_cliente
            WHERE Ventas.tipo_documento = 'factura'
            ORDER BY Ventas.fecha DESC;
        """)
        
        
    elif tipo_busqueda == "Notas de Entregas":
        cursor.execute('''
            SELECT Proveedores.nombre, Facturas.numero_factura, Facturas.fecha, Materiales.codigo, Materiales.nombre, Materiales.stock, materiales.precio, materiales.costo_unitario
            FROM Facturas
            JOIN Proveedores ON Facturas.id_proveedor = Proveedores.id_proveedor
            JOIN Detalle_Factura ON Facturas.id_factura = Detalle_Factura.id_factura
            JOIN Materiales ON Detalle_Factura.id_material = Materiales.id_material
            WHERE Facturas.numero_factura LIKE ?
        ''', (f"%{valor_busqueda}%",))

    elif tipo_busqueda == "Código":
        cursor.execute('''
            SELECT Proveedores.nombre, Facturas.numero_factura, Facturas.fecha, Materiales.codigo, Materiales.nombre, Materiales.stock, materiales.precio, materiales.costo_unitario
            FROM Materiales
            JOIN Detalle_Factura ON Materiales.id_material = Detalle_Factura.id_material
            JOIN Facturas ON Detalle_Factura.id_factura = Facturas.id_factura
            JOIN Proveedores ON Facturas.id_proveedor = Proveedores.id_proveedor
            WHERE Materiales.codigo LIKE ?
        ''', (f"%{valor_busqueda}%",))

    elif tipo_busqueda == "Material":
        cursor.execute('''
            SELECT p.nombre, f.numero_factura, f.fecha, m.codigo, m.nombre, m.stock, m.precio, m.costo_unitario
            FROM Materiales m
            JOIN Detalle_Factura df ON m.id_material = df.id_material
            JOIN Facturas f ON df.id_factura = f.id_factura
            JOIN Proveedores p ON f.id_proveedor = p.id_proveedor
            WHERE m.nombre LIKE ?
        ''', (f"%{valor_busqueda}%",))

    elif tipo_busqueda == "Producto":
        cursor.execute('''
            SELECT p.codigo, p.tipo, p.costo_producto, p.precio_venta, p.materiales_usados, p.tiempo_fabricacion, p.cantidad, p.fecha_registro, p.descripcion
            FROM Productos p
            WHERE p.codigo LIKE ? OR p.nombre LIKE ?
        ''', (f"%{valor_busqueda}%", f"%{valor_busqueda}%"))
        
    elif tipo_busqueda == "Todos los Productos":
       cursor.execute('SELECT codigo, tipo, costo_producto, precio_venta, materiales_usados, tiempo_fabricacion, cantidad, fecha_registro, descripcion FROM Productos')


    resultados = cursor.fetchall()
    print(resultados)
    conn.close()
    
    return resultados

# def buscar_en_bd(tipo_busqueda, valor_busqueda):
#     # Aseguramos que la ruta a la base sea absoluta y válida
#     db_absoluta = os.path.abspath(db_path)

#     if not os.path.exists(db_absoluta):
#         print(f"⚠️ La base de datos no existe en la ruta: {db_absoluta}")
#         return []

#     conn = sqlite3.connect(db_absoluta)
#     cursor = conn.cursor()

#     # Limpiamos el valor de búsqueda
#     valor_busqueda = (valor_busqueda or "").strip()
#     if not valor_busqueda:
#         valor_busqueda = "%"

#     print(f"🔍 Tipo de búsqueda: {tipo_busqueda}")
#     print(f"🧩 Valor de búsqueda: {valor_busqueda}")

#     try:
#         if tipo_busqueda == "Todos los Materiales":
#             cursor.execute('''
#                 SELECT codigo, nombre, tipo, tamaño, color, stock, precio, costo_unitario
#                 FROM Materiales
#             ''')

#         elif tipo_busqueda == "Proveedor":
#             cursor.execute('''
#                 SELECT p.nombre, f.numero_factura, f.fecha,
#                        m.codigo, m.nombre, m.stock, m.precio, m.costo_unitario
#                 FROM Proveedores p
#                 LEFT JOIN Facturas f ON p.id_proveedor = f.id_proveedor
#                 LEFT JOIN OUTER Detalle_Factura df ON f.id_factura = df.id_factura
#                 LEFT JOIN Materiales m ON df.id_material = m.id_material
#                 WHERE p.nombre LIKE ?
#             ''', (f"%{valor_busqueda}%",))

#         elif tipo_busqueda == "Factura":
#             cursor.execute('''
#                 SELECT p.nombre, f.numero_factura, f.fecha,
#                        m.codigo, m.nombre, m.stock, m.precio, m.costo_unitario
#                 FROM Facturas f
#                 LEFT JOIN Proveedores p ON f.id_proveedor = p.id_proveedor
#                 LEFT JOIN Detalle_Factura df ON f.id_factura = df.id_factura
#                 LEFT JOIN Materiales m ON df.id_material = m.id_material
#                 WHERE f.numero_factura LIKE ?
#             ''', (f"%{valor_busqueda}%",))

#         elif tipo_busqueda == "Notas de Entregas":
#             cursor.execute('''
#                 SELECT p.nombre, f.numero_factura, f.fecha,
#                        m.codigo, m.nombre, m.stock, m.precio, m.costo_unitario
#                 FROM Facturas f
#                 LEFT JOIN Proveedores p ON f.id_proveedor = p.id_proveedor
#                 LEFT JOIN Detalle_Factura df ON f.id_factura = df.id_factura
#                 LEFT JOIN Materiales m ON df.id_material = m.id_material
#                 WHERE f.numero_factura LIKE ?
#             ''', (f"%{valor_busqueda}%",))

#         elif tipo_busqueda == "Código":
#             cursor.execute('''
#                 SELECT p.nombre, f.numero_factura, f.fecha,
#                        m.codigo, m.nombre, m.stock, m.precio, m.costo_unitario
#                 FROM Materiales m
#                 LEFT JOIN Detalle_Factura df ON m.id_material = df.id_material
#                 LEFT JOIN Facturas f ON df.id_factura = f.id_factura
#                 LEFT JOIN Proveedores p ON f.id_proveedor = p.id_proveedor
#                 WHERE m.codigo LIKE ?
#             ''', (f"%{valor_busqueda}%",))

#         elif tipo_busqueda == "Material":
#             cursor.execute('''
#                 SELECT p.nombre, f.numero_factura, f.fecha,
#                        m.codigo, m.nombre, m.stock, m.precio, m.costo_unitario
#                 FROM Materiales m
#                 LEFT JOIN Detalle_Factura df ON m.id_material = df.id_material
#                 LEFT JOIN Facturas f ON df.id_factura = f.id_factura
#                 LEFT JOIN Proveedores p ON f.id_proveedor = p.id_proveedor
#                 WHERE m.nombre LIKE ?
#             ''', (f"%{valor_busqueda}%",))

#         elif tipo_busqueda == "Producto":
#             cursor.execute('''
#                 SELECT p.codigo, p.tipo, p.costo_producto, p.precio_venta,
#                        p.materiales_usados, p.tiempo_fabricacion,
#                        p.cantidad, p.fecha_registro, p.descripcion
#                 FROM Productos p
#                 WHERE p.codigo LIKE ? OR p.nombre LIKE ?
#             ''', (f"%{valor_busqueda}%", f"%{valor_busqueda}%"))

#         elif tipo_busqueda == "Todos los Productos":
#             cursor.execute('''
#                 SELECT codigo, tipo, costo_producto, precio_venta,
#                        materiales_usados, tiempo_fabricacion,
#                        cantidad, fecha_registro, descripcion
#                 FROM Productos
#             ''')

#         else:
#             print(f"⚠️ Tipo de búsqueda desconocido: {tipo_busqueda}")
#             conn.close()
#             return []

#         resultados = cursor.fetchall()
#         print(f"📦 Resultados encontrados: {len(resultados)}")
#         if len(resultados) == 0:
#             print("⚠️ No se encontraron resultados con ese criterio.")
#         else:
#             for fila in resultados:
#                 print("   ➜", fila)

#         conn.close()
#         return resultados

#     except sqlite3.Error as e:
#         print(f"❌ Error al ejecutar la consulta: {e}")
#         conn.close()
#         return []


# Busca las notas de entrega para mostrar en la busqueda.
def encontrar_notas_entrega():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""SELECT ne.id_nota_entrega, ne.fecha, c.nombre, ne.total, ne.estado
        FROM NotasEntrega ne
        JOIN Clientes c ON ne.id_cliente = c.id_cliente""")
    notas_entregas = cursor.fetchall()
    conn.close()
    return notas_entregas

def encontrar_facturas():
    print("Buscado factura...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            v.id_venta, 
            v.fecha, 
            c.nombre, 
            v.subtotal, 
            v.descuento, 
            v.impuesto, 
            v.total
        FROM Ventas v
        JOIN Clientes c ON v.id_cliente = c.id_cliente
        WHERE v.tipo_documento = 'factura'
        ORDER BY v.fecha DESC
    """)
    facturas = cursor.fetchall()
    conn.close()
    print("Resultados de la Busqueda en encontrar_factura: ", facturas)
    return facturas

    
def verificar_datos():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Facturas  
    cursor.execute('SELECT * FROM Facturas')
    facturas = cursor.fetchall()
    for factura in facturas:
        print(factura)

    # Materiales
    cursor.execute('SELECT * FROM Materiales')
    materiales = cursor.fetchall()
    for material in materiales:
        print(material)

    # Detalle_Factura
    cursor.execute('SELECT * FROM Detalle_Factura')
    detalle_factura = cursor.fetchall()
    for detalle in detalle_factura:
        print(detalle)

    # Productos
    cursor.execute('SELECT * FROM Productos')
    productos = cursor.fetchall()
    for producto in productos:
        print(producto)

    # Detalle_Producto
    cursor.execute('SELECT * FROM Detalle_Producto')
    detalle_producto = cursor.fetchall()
    for detalle in detalle_producto:
        print(detalle)

    conn.close()
    
    
def agregar_campo_():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Agregar el campo 'descripcion' a la tabla Productos
    cursor.execute('''
        ALTER TABLE Detalle_Factura
        ADD COLUMN Precio TEXT
    ''')

    conn.commit()
    conn.close()
    
    
def verificar_campo_en_bd():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Verificar la estructura de la tabla Productos
    cursor.execute("PRAGMA table_info(Proveedores)")
    columnas = cursor.fetchall()
    for columna in columnas:
        print(columna)

    conn.close()
    
# Crear nuevo usuario.
def insertar_usuario(usuario, clave, rol):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Usuarios (nombre_usuario, clave, rol) VALUES (?, ?, ?)', (usuario, clave, rol))
    conn.commit()
    conn.close()


# Validar entrada de un usuario.
def validar_credenciales(usuario, contrasena):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT clave, rol FROM Usuarios WHERE nombre_usuario = ?', (usuario,))
    resultado = cursor.fetchone()
    conn.close()

    if resultado and resultado[0] == contrasena:
        return True, resultado[1]  # Retorna True y el rol del usuario
    else:
        return False, None

# Buscar usuarios en la base de datos.
def buscar_usuarios(texto_busqueda):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id_usuario, nombre_usuario, rol
        FROM Usuarios
        WHERE nombre_usuario LIKE ?
    ''', (f"%{texto_busqueda}%",))
    resultados = cursor.fetchall()
    conn.close()
    return resultados


# Actualizar datos de Usuarios.
def actualizar_usuario(id_usuario, nombre_usuario, rol, contrasena=None):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    if contrasena:
        cursor.execute('''
            UPDATE Usuarios
            SET nombre_usuario = ?, rol = ?, contraseña = ?
            WHERE id_usuario = ?
        ''', (nombre_usuario, rol, contrasena, id_usuario))
    else:
        cursor.execute('''
            UPDATE Usuarios
            SET nombre_usuario = ?, rol = ?
            WHERE id_usuario = ?
        ''', (nombre_usuario, rol, id_usuario))

    conn.commit()
    conn.close()


# Obtener los usuarios del sistema.
def obtener_nombres_usuarios():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT nombre_usuario FROM Usuarios')
    resultados = cursor.fetchall()
    conn.close()
    return [resultado[0] for resultado in resultados]


# Eliminar a usuarios de la base de datos por nombre.
def eliminar_usuario_bd_nombre(nombre_usuario):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Usuarios WHERE nombre_usuario = ?', (nombre_usuario,))
    conn.commit()
    conn.close()


# Eliminar a usuarios de la base de datos por ID.
def eliminar_usuario_bd(id_usuario):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Usuarios WHERE id_usuario = ?', (id_usuario,))
    conn.commit()
    conn.close()


# Calcular el costo de un producto.
def calcular_costo_produccion(id_producto):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Obtener materiales usados en el producto
    cursor.execute('''
        SELECT m.costo_unitario, dp.cantidad
        FROM detalle_producto dp
        JOIN Materiales m ON dp.id_material = m.id_material
        WHERE dp.id_producto = ?
    ''', (id_producto,))
    materiales = cursor.fetchall()

    # Sumar el costo total
    costo_total = sum(material[0] * material[1] for material in materiales)

    conn.close()
    return costo_total


def actualizar_costo_producto(nuevo_costo, id_producto): # Acualizar aqui los datos
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
            "UPDATE Productos SET costo_producto = ? WHERE id_producto = ?",
            (nuevo_costo, id_producto))
    conn.commit()
    conn.close()


# Actualizar los costos de producción.
def datos_costo_d_producto_actualizar(codigo_producto):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id_producto, costo_producto, precio_venta FROM Productos WHERE codigo = ?",
            (codigo_producto,))
    producto = cursor.fetchone()

    if not producto:
        messagebox.showerror("Error", f"No se encontró el producto seleccionado con código {codigo_producto}")
    return producto


# Actualizar el precio_venta en la base de datos
def actualizar_precio_venta(precio, id_producto):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Productos SET precio_venta = ? WHERE id_producto = ?",
            (precio, id_producto)
        )
        conn.commit()
        conn.close()
        

# Modulo de simulacion de precios.
def simular_escenario(id_producto, nuevo_precio=None, nuevo_costo=None, nuevo_margen=None):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Obtener datos actuales
    cursor.execute('SELECT costo_produccion, precio_venta FROM Producto WHERE id_producto = ?', (id_producto,))
    costo_actual, precio_actual = cursor.fetchone()

    # Aplicar cambios simulados
    costo_simulado = nuevo_costo if nuevo_costo is not None else costo_actual
    precio_simulado = nuevo_precio if nuevo_precio is not None else precio_actual
    if nuevo_margen is not None:
        precio_simulado = costo_simulado * (1 + nuevo_margen/100)

    # Calcular ganancia simulada
    ganancia_simulada = (precio_simulado - costo_simulado)
    margen_simulado = (ganancia_simulada / costo_simulado) * 100

    conn.close()
    return {
        "costo_simulado": costo_simulado,
        "precio_simulado": precio_simulado,
        "ganancia_simulada": ganancia_simulada,
        "margen_simulado": margen_simulado
    }


def incrementar_stock_producto(id_producto, cantidad):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Verificar que el producto exista
        cursor.execute("SELECT cantidad FROM Productos WHERE id_producto = ?", (id_producto,))
        resultado = cursor.fetchone()

        if not resultado:
            messagebox.showerror("Error", "Producto no encontrado en la base de datos.")
            return False

        stock_actual = resultado[0]
        nuevo_stock = stock_actual + cantidad

        # Actualizar el stock en la base de datos
        cursor.execute("UPDATE Productos SET cantidad = ? WHERE id_producto = ?", (nuevo_stock, id_producto))
        conn.commit()
        messagebox.showinfo("Éxito", f"Stock del producto actualizado. Nuevo stock: {nuevo_stock}")
        return True

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo actualizar el stock: {e}")
        conn.rollback()
        return False

    finally:
        conn.close()


# Verificar cantidad de producto para la venta.
def verificar_stock_suficiente(id_producto, cantidad_solicitada):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT cantidad FROM Productos WHERE id_producto = ?", (id_producto,))
    resultado = cursor.fetchone()
    conn.close()

    if not resultado:
        return False, 0, "Producto no encontrado en la base de datos."

    stock_actual = resultado[0]

    if stock_actual <= 0:
        return False, stock_actual, "No hay stock disponible para este producto."
    elif stock_actual < cantidad_solicitada:
        return False, stock_actual, f"No hay suficiente stock. Stock disponible: {stock_actual}"
    else:
        return True, stock_actual, "Stock suficiente."


# Verificar cantidad de producto para la venta.
# def verificar_stock_suficiente(id_producto, cantidad_solicitada):
#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()
#     cursor.execute("SELECT cantidad FROM Productos WHERE id_producto = ?", (id_producto,))
#     stock_actual = cursor.fetchone()[0]
#     conn.commit()
#     conn.close()
#     return stock_actual >= cantidad_solicitada


# Restar la venta de un producto en la base de datos.
def actualizar_stock_después_venta(id_producto, cantidad_vendida):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Restar la cantidad vendida del stock actual
    cursor.execute("""
        UPDATE Productos
        SET cantidad = cantidad - ?
        WHERE id_producto = ?
    """, (cantidad_vendida, id_producto))
    conn.commit()
    conn.close()
    

# Agregar nuevo Cliente.
def nuevo_cliente(nombre, direccion, casa_num, zona_postal, identificacion_fiscal, email, telefono):
    conn = sqlite3.connect("ikigai_inventario.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Clientes (nombre, direccion, casa_num, zona_postal, identificacion_fiscal, email, telefono)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (nombre, direccion, casa_num, zona_postal, identificacion_fiscal, email, telefono))
    conn.commit()
    conn.close()


# Cargar los clientes para factura.
def cargador_clientes():
    conn = sqlite3.connect("ikigai_inventario.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id_cliente, nombre FROM Clientes")
    clientes = cursor.fetchall()
    conn.commit()
    conn.close()
    return clientes


# Cargar productos disponibles para factura.
def cargador_productos():
    conn = sqlite3.connect("ikigai_inventario.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id_producto, codigo, tipo, precio_venta, cantidad FROM Productos WHERE cantidad > 0")
    productos = cursor.fetchall()
    conn.commit()
    conn.close()
    return productos


# Validar stock del producto.
def validar_stock_del_producto(id_producto):
    conn = sqlite3.connect("ikigai_inventario.db")
    cursor = conn.cursor()
    cursor.execute("SELECT cantidad FROM Productos WHERE id_producto = ?", (id_producto,))
    stock_actual = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return stock_actual


# Obtener detalle del producto para venta.
def detalle_producto_venta(id_producto):
    conn = sqlite3.connect("ikigai_inventario.db")
    cursor = conn.cursor()
    cursor.execute("SELECT codigo, precio_venta FROM Productos WHERE id_producto = ?", (id_producto,))
    nombre, precio_unitario = cursor.fetchone()
    conn.commit()
    conn.close()
    return nombre, precio_unitario


# Insertar la venta en la base de datos "FACTURA"
def guarda_venta_bd(id_venta, id_cliente, fecha_actual, tipo_documento, subtotal, descuento, impuesto, total):
    
    #fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    conn = sqlite3.connect("ikigai_inventario.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Ventas (id_venta, id_cliente, fecha, tipo_documento, subtotal, descuento, impuesto, total)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (id_venta, id_cliente, fecha_actual, tipo_documento, subtotal, descuento, impuesto, total))
    id_venta = cursor.lastrowid
    conn.commit()
    conn.close()
    return id_venta


# Insertar datos en detalle factura.
def agregar_detalle_venta(id_venta, id_producto, cantidad, precio_unitario, subtotal):
    conn = sqlite3.connect("ikigai_inventario.db")
    cursor = conn.cursor()
    cursor.execute("""
            INSERT INTO Detalle_Venta (id_venta, id_producto, cantidad, precio_unitario, subtotal)
            VALUES (?, ?, ?, ?, ?)
        """, (id_venta, id_producto, cantidad, precio_unitario, subtotal,))
    conn.commit()
    conn.close()
    

def guardar_nota_entrega(id_cliente, fecha, subtotal, descuento, impuesto, total):
    conn = sqlite3.connect("ikigai_inventario.db")
    cursor = conn.cursor()
    cursor.execute("""
            INSERT INTO NotasEntrega (id_cliente, fecha, subtotal, descuento, impuesto, total)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (id_cliente, fecha, subtotal, descuento, impuesto, total))
    id_nota_entrega = cursor.lastrowid  # Obtener el ID de la nota de entrega generada
    conn.commit()
    conn.close()
    return id_nota_entrega


def agregar_detalle_nota_entrega(nota_entrega, id_producto, cantidad, precio_unitario, subtotal):
    conn = sqlite3.connect("ikigai_inventario.db")
    cursor = conn.cursor()
    cursor.execute("""
            INSERT INTO DetalleNotaEntrega (id_nota_entrega, id_producto, cantidad, precio_unitario, subtotal)
            VALUES (?, ?, ?, ?, ?)
        """, (nota_entrega, id_producto, cantidad, precio_unitario, subtotal))
    conn.commit()
    conn.close()
    

# Actualiza el stock del producto vendido.
def actualizar_stock_producto_venta(cantidad, id_producto):
    conn = sqlite3.connect("ikigai_inventario.db")
    cursor = conn.cursor()
    cursor.execute("""
            UPDATE Productos
            SET cantidad = cantidad - ?
            WHERE id_producto = ?
        """, (cantidad, id_producto))
    conn.commit()
    conn.close()
 
# Consulta el historial de costos en la base de datos
def datos_imprimir_historial_costo(): 
    conn = sqlite3.connect("ikigai_inventario.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.nombre, hc.fecha, hc.costo_anterior, hc.costo_nuevo, hc.motivo
        FROM Historial_Costos hc
        JOIN Productos p ON hc.id_producto = p.id_producto
    """)
    historial = cursor.fetchall()
    conn.close()
    return historial
   
   
# Consulta el historial de Ganancias en la base de datos
def datos_imprimir_historial_ganancia():
    conn = sqlite3.connect("ikigai_inventario.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.nombre, hg.mes, hg.ganancia_total, hg.margen_promedio
        FROM Historial_Ganancias hg
        JOIN Productos p ON hg.id_producto = p.id_producto
    """)
    historial = cursor.fetchall()
    conn.close()
    return historial


# Eliminar Proveedores de la base de datos
def eliminar_proveedor_bd(nombre_proveedor):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Proveedores WHERE nombre = ?', (nombre_proveedor,))
    conn.commit()
    conn.close()
    
# Eliminar materiales de la base de datos
def eliminar_material_bd(nombre_material):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Materiales WHERE nombre = ?', (nombre_material,))
    conn.commit()
    conn.close()
    
    
# Eliminar Productos.
def eliminar_producto_bd(codigo_producto):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Productos WHERE codigo = ?', (codigo_producto,))
    conn.commit()
    conn.close()
    
# Obtener los lotes 
def obtener_lotes():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id_lote, fecha_creacion, descripcion, cantidad_unidades FROM Lotes")
    lotes = cursor.fetchall()
    conn.close()
    return lotes

# Registrar el nuevo lote
def registrar_producto_en_lote(id_lote, id_producto, unidades_lote):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Lote_Productos (id_lote, id_producto, cantidad_asignada) VALUES (?, ?, ?)",
        (id_lote, id_producto, unidades_lote)
    )
    conn.commit()
    conn.close()
    
# Obtener lotes y sus productos.
def obtener_lotes_con_productos():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            l.id_lote,
            l.descripcion,
            l.cantidad_unidades,
            GROUP_CONCAT(p.codigo || ' (' || lp.cantidad_asignada || ')', ', ') as productos
        FROM Lotes l
        LEFT JOIN Lote_Productos lp ON l.id_lote = lp.id_lote
        LEFT JOIN Productos p ON lp.id_producto = p.id_producto
        GROUP BY l.id_lote
    """)
    lotes = cursor.fetchall()
    conn.close()
    return lotes


def obtener_costo_actual_lote(id_lote):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT costo_lote FROM Lotes WHERE id_lote = ?", (id_lote,))
    costo_actual = cursor.fetchone()
    conn.close()
    return costo_actual[0] if costo_actual else 0.0


def guardar_info_tienda(tienda, direccion, id_fiscal, telefono, correo):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Tienda (nombre, direccion, identificacion_fiscal, telefono, email) VALUES (?, ?, ?, ?, ?)",
                   (tienda, direccion, id_fiscal, telefono, correo))
    conn.commit()
    conn.close()
    

def datos_registrados_tienda():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id_tienda, direccion, telefono, email FROM Tienda WHERE id_tienda = 1")
    datos_tienda = cursor.fetchall()
    conn.close()
    return datos_tienda


def actualizar_datos_tienda(direccion, telefono, correo, id_tienda):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""UPDATE Tienda SET direccion = ?, telefono = ?,email = ? WHERE id_tienda = ?""", (direccion, telefono, correo, id_tienda ))
    conn.commit()
    conn.close()    


def obtener_estado_nota_entrega(id_nota_entrega):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT estado FROM NotasEntrega WHERE id_nota_entrega = ?", (id_nota_entrega,))
    estado = cursor.fetchone()
    conn.close()

    if estado:
        return estado[0]
    else:
        return None
    

def obtener_datos_nota_entrega(id_nota_entrega):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id_cliente, fecha, subtotal, descuento, impuesto, total
        FROM NotasEntrega
        WHERE id_nota_entrega = ?
    """, (id_nota_entrega,))
    nota_data = cursor.fetchone()
    conn.close()
    return nota_data

def obtener_ultimo_numero_factura():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT ultimo_numero_factura FROM Configuracion WHERE id_configuracion = 1")
    ultimo_numero = cursor.fetchone()[0]
    conn.close()
    return ultimo_numero

def actualizar_ultimo_numero_factura(nuevo_numero):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("UPDATE Configuracion SET ultimo_numero_factura = ? WHERE id_configuracion = 1", (nuevo_numero,))
    conn.commit()
    conn.close()

def insertar_factura_venta(id_venta, id_cliente, fecha, subtotal, descuento, impuesto, total):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Ventas (id_venta, id_cliente, fecha, tipo_documento, subtotal, descuento, impuesto, total)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (id_venta, id_cliente, fecha, "Factura", subtotal, descuento, impuesto, total))
    conn.commit()
    conn.close()

def obtener_detalles_nota_entrega(id_nota_entrega):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id_producto, cantidad, precio_unitario, subtotal FROM DetalleNotaEntrega WHERE id_nota_entrega = ?", (id_nota_entrega,))
    detalles = cursor.fetchall()
    conn.close()
    return detalles

def insertar_detalle_venta(id_venta, id_producto, cantidad, precio_unitario, subtotal_detalle):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Detalle_Venta (id_venta, id_producto, cantidad, precio_unitario, subtotal)
        VALUES (?, ?, ?, ?, ?)
    """, (id_venta, id_producto, cantidad, precio_unitario, subtotal_detalle))
    conn.commit()
    conn.close()

def actualizar_estado_nota_entrega(id_nota_entrega, estado):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE NotasEntrega
        SET estado = ?
        WHERE id_nota_entrega = ?
    """, (estado, id_nota_entrega))
    conn.commit()
    conn.close()
    

# Datos de la Venta.
def datos_de_la_venta(id_venta):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
            SELECT
                v.id_venta,
                v.fecha,
                c.nombre,
                c.direccion,
                c.casa_num,
                c.zona_postal,
                c.identificacion_fiscal,
                c.email,
                c.telefono,
                v.total,
                v.tipo_documento,
                t.nombre AS tienda_nombre,
                t.direccion AS tienda_direccion,
                t.identificacion_fiscal AS tienda_identificacion_fiscal,
                v.descuento,
                v.subtotal,
                v.impuesto
            FROM
                Ventas v
            JOIN
                Clientes c ON v.id_cliente = c.id_cliente
            CROSS JOIN
                Tienda t
            WHERE
                v.id_venta = ?
        """, (id_venta,))

    venta_data = cursor.fetchone()
    conn.close()
    return venta_data


# Detalles de la venta
def detalle_de_la_venta(id_venta):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.codigo, dv.cantidad, dv.precio_unitario, dv.subtotal
        FROM Detalle_Venta dv
        JOIN Productos p ON dv.id_producto = p.id_producto
        WHERE dv.id_venta = ?
    """, (id_venta,))
    detalles = cursor.fetchall()
    conn.close()
    return detalles


# Datos de la nota de entrega.
def datos_nota_entrega(id_nota_entrega):
    conn = sqlite3.connect("ikigai_inventario.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            ne.id_nota_entrega,
            ne.fecha,
            c.nombre,
            c.direccion,
            c.casa_num,
            c.zona_postal,
            c.identificacion_fiscal,
            c.email,
            c.telefono,
            ne.total,
            ne.subtotal,
            ne.descuento,
            ne.impuesto,
            t.nombre AS tienda_nombre,
            t.direccion AS tienda_direccion,
            t.identificacion_fiscal AS tienda_identificacion_fiscal
        FROM
            NotasEntrega ne
        JOIN
            Clientes c ON ne.id_cliente = c.id_cliente
        CROSS JOIN
            Tienda t
        WHERE
            ne.id_nota_entrega = ?
    """, (id_nota_entrega,))
    nota_data = cursor.fetchone()
    conn.close()
    return nota_data


# Detalles de la nota de entrega.
def detalle_nota_entrega(id_nota_entrega):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.codigo, dne.cantidad, dne.precio_unitario, dne.subtotal
        FROM DetalleNotaEntrega dne
        JOIN Productos p ON dne.id_producto = p.id_producto
        WHERE dne.id_nota_entrega = ?
    """, (id_nota_entrega,))

    detalles = cursor.fetchall()
    conn.close()
    return detalles

# insertar lote en la base de datos
def insertar_lote(descripcion, unidades, costo_lote):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Lotes (fecha_creacion, descripcion, cantidad_unidades, costo_lote) VALUES (?, ?, ?, ?)",
        (datetime.now().strftime("%Y-%m-%d"), descripcion, unidades, costo_lote)
    )
    id_lote = cursor.lastrowid  # Obtener el ID del lote recién creado
    conn.commit()
    conn.close()
    return id_lote


# Insertar en la tabla lote_productos
def insertar_lote_productos(id_lote, id_producto, cantidad):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Lote_Productos (id_lote, id_producto, cantidad_asignada) VALUES (?, ?, ?)",
        (id_lote, id_producto, cantidad)
    )
    conn.commit()
    conn.close()
    

# Actualizar el costo del lote.
def actualizar_costo_lote(nuevo_costo, id_lote):
    conn = sqlite3.connect(db_path)
    conn = sqlite3.connect('ikigai_inventario.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE Lotes SET costo_lote = ? WHERE id_lote = ?", (nuevo_costo, id_lote))
    conn.commit()
    conn.close()


# Obtener el costo anterior del lote
def costo_anterior_lote(id_lote):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT costo_lote FROM Lotes WHERE id_lote = ?", (id_lote,))
    anterior_costo = cursor.fetchone()[0]
    conn.close()
    return anterior_costo


# Actualizar el precio de venta del lote en la base de datos
def actualiza_precio_venta_lote(nuevo_precio, id_lote):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("UPDATE Lotes SET precio_venta_lote = ? WHERE id_lote = ?", (nuevo_precio, id_lote))
    conn.commit()
    conn.close()


# Obtener el ultimo número de factura y crear el siguiente úmero de factura.
def siguiente_numero_factura():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT ultimo_numero_factura FROM Configuracion WHERE id_configuracion = 1")
    ultimo_numero = cursor.fetchone()[0]
    nuevo_numero = ultimo_numero + 1
    cursor.execute("UPDATE Configuracion SET ultimo_numero_factura = ? WHERE id_configuracion = 1", (nuevo_numero,))
    id_venta = nuevo_numero
    conn.commit()
    conn.close()
    return id_venta


# Obtener los umbrales configurados.
def obtener_umbrales_alertas():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT tipo, id_item, umbral FROM UmbralesAlerta")
    umbrales = cursor.fetchall()
    conn.close()
    return umbrales


#  Crear advetencias de stock para materiles y productos
def cargar_items(tipo):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    if tipo == 'material':
        cursor.execute("SELECT id_material, nombre FROM Materiales")
    elif tipo == 'producto':
        cursor.execute("SELECT id_producto, codigo FROM Productos")
    items = cursor.fetchall()
    conn.close()
    return items


# Configurar el umbral para las alertas.
def configurar_umbral_alerta(tipo, id_item, umbral):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Verificar si ya existe un umbral para este item
    cursor.execute("SELECT id_umbral FROM UmbralesAlerta WHERE tipo = ? AND id_item = ?", (tipo, id_item))
    umbral_existente = cursor.fetchone()

    if umbral_existente:
        # Actualizar el umbral existente
        cursor.execute("UPDATE UmbralesAlerta SET umbral = ? WHERE id_umbral = ?", (umbral, umbral_existente[0]))
    else:
        # Insertar un nuevo umbral
        cursor.execute("INSERT INTO UmbralesAlerta (tipo, id_item, umbral) VALUES (?, ?, ?)", (tipo, id_item, umbral))

    conn.commit()
    conn.close()


def verificar_stock_bajo():
    umbrales = obtener_umbrales_alertas()
    alertas = []

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for tipo, id_item, umbral in umbrales:
        if tipo == 'material':
            cursor.execute("SELECT nombre, tipo, tamaño, color, stock FROM Materiales WHERE id_material = ?", (id_item,))
        elif tipo == 'producto':
            cursor.execute("SELECT codigo, tipo, cantidad FROM Productos WHERE id_producto = ?", (id_item,))

        item = cursor.fetchone()
        if item:
            cantidad_actual = item[-1]  # La cantidad es el último elemento de la tupla
            if cantidad_actual <= umbral:
                if tipo == 'material':
                    nombre, tipo_material, tamaño, color, cantidad = item
                    alertas.append({
                        'tipo': tipo,
                        'nombre': nombre,
                        'tipo_material': tipo_material,
                        'tamaño': tamaño,
                        'color': color,
                        'cantidad': cantidad
                    })
                elif tipo == 'producto':
                    codigo, tipo_producto, cantidad = item
                    alertas.append({
                        'tipo': tipo,
                        'codigo': codigo,
                        'tipo_producto': tipo_producto,
                        'cantidad': cantidad
                    })

    conn.close()
    return alertas

    
# Borrado total de la base de datos
def limpiar_base_datos():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Desactivar las restricciones de claves foráneas
    cursor.execute("PRAGMA foreign_keys = OFF;")

    # Eliminar datos de las tablas en el orden correcto
    # Primero, elimina datos de tablas que tienen claves foráneas
    cursor.execute("DELETE FROM Detalle_Venta;")
    cursor.execute("DELETE FROM Ventas;")
    cursor.execute("DELETE FROM DetalleNotaEntrega;")
    cursor.execute("DELETE FROM NotasEntrega;")
    cursor.execute("DELETE FROM Clientes;")
    cursor.execute("DELETE FROM Productos;")
    cursor.execute("DELETE FROM Detalle_Producto;")
    cursor.execute("DELETE FROM Historial_Costos;")
    cursor.execute("DELETE FROM Historial_Ganancias;")
    cursor.execute("DELETE FROM Materiales;")
    cursor.execute("DELETE FROM Proveedores;")
    # Añade aquí más tablas según sea necesario

    # Volver a activar las restricciones de claves foráneas
    cursor.execute("PRAGMA foreign_keys = ON;")

    conn.commit()
    conn.close()
    print("borrado")


if __name__ == "__main__":
    init_db()
    #verificar_campo_en_bd()
    #agregar_campo_()
    #verificar_datos()
    #limpiar_base_datos()
    #buscar_en_bd("Proveedores", "ronald")