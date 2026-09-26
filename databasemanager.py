"Base de datos nueva más organizada y matenible"
import sqlite3
import hashlib
from datetime import datetime
from tkinter import messagebox
from decimal import Decimal, getcontext
import json
import ast
from typing import List, Dict, Optional, Any, Union, Tuple
from recursos import DB_PATH

db_path = DB_PATH

class DataBaseManager():
    
    def __init__(self, db_name: str = db_path):
        """
        Inicializa el manejador de la base de datos.

        Args:
            db_name (str): Nombre del archivo de la base de datos.
        """
    
        self.db_name = db_name
        self.connection = None
        self.in_transaction = False
        
        
    def connect(self) ->None:
        """
        Establece la conexión a la base de datos.
        """
        try:
            self.connection = sqlite3.connect(self.db_name)
            print(f"Conección establecida con exito")
        except sqlite3.Error as e:
            messagebox.showerror(f"Error al conectar a la base de datos: {e}")
            
    
    def begin_transaction(self) -> bool:
        """Inicia una transacción."""
        
        if not self.connection:
            self.connect()
            
        try:
            if not self.in_transaction:
                self.connection.execute("BEGIN TRANSACTION")
                self.in_transaction = True
                #print("Transacción iniciada.")
                return True
            else:
                print("Ya hay una transacción activa.")
                return False
        except sqlite3.Error as e:
            print(f"Error al iniciar transacción: {e}")
            return False
        

    def commit_transaction(self) -> bool:
        """Confirma una transacción."""
        
        if not self.connection:
            self.connect()
            
        try:
            if self.in_transaction:
                self.connection.commit()
                self.in_transaction = False
                print("Transacción confirmada.")
                return True
            else:
                print("No hay una transacción activa para confirmar.")
                return False
        except sqlite3.Error as e:
            print(f"Error al confirmar transacción: {e}")
            return False
        

    def rollback_transaction(self) -> bool:
        """Revierte una transacción."""
        
        if not self.connection:
            self.connect()
            
        try:
            if self.in_transaction:
                self.connection.rollback()
                self.in_transaction = False
                print("Transacción revertida.")
                return True
            else:
                print("No hay una transacción activa para revertir.")
                return False
        except sqlite3.Error as e:
            print(f"Error al revertir transacción: {e}")
            return False
        
                
    def close(self) -> None:
        """
        Cierra la conexión a la base de datos.
        """
        try:
            if self.in_transaction:
                self.rollback_transaction()  # Revertir transacciones pendientes al cerrar
            self.connection.close()
            print("Base de datos cerrada correctamente.")
        except sqlite3.Error as e:
            messagebox.showerror(f"⚠️ Error", "Problemas al cerrar la base de datos: {e}")
            
#######################################################################################################################
################################ SECCIÓN DE SELECCIÓN-INSERCIÓN-ACTUALIZACIÓN-ELIMINACIÓN #############################
#######################################################################################################################

    def select(self, query: str, params: tuple = (), fetch_one: bool = False) -> Union[List[Dict[str, Any]], Dict[str, Any], None]:
        """
        Ejecuta una consulta SELECT y devuelve los resultados.

        Args:
            query (str): Consulta SQL.
            params (tuple): Parámetros para la consulta.
            fetch_one (bool): Si es True, devuelve solo el primer resultado.

        Returns:
            Union[List[Dict[str, Any]], Dict[str, Any], None]: Resultados de la consulta.
        """
        #print(f"Los datos de la consulta son: {params}")  # imprime el usuario
        if not self.connection:
            self.connect()

        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)

            if fetch_one:
                result = cursor.fetchone()
                columns = [column[0] for column in cursor.description]
                return dict(zip(columns, result)) if result else None
            else:
                columns = [column[0] for column in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]

        except sqlite3.Error as e:
            print(f"Error en consulta SELECT: {e}")
            return [] if not fetch_one else None
    
    
    def insert(self, table: str, data: Dict[str, Any]) -> int:
        """
        Inserta un registro en una tabla.

        Args:
            table (str): Nombre de la tabla.
            data (Dict[str, Any]): Diccionario con los campos y valores a insertar.

        Returns:
            int: ID del registro insertado.
        """
        if not self.connection:
            self.connect()

        try:
            columns = ", ".join(data.keys())
            placeholders = ", ".join(["?"] * len(data))
            query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

            cursor = self.connection.cursor()
            cursor.execute(query, tuple(data.values()))
            self.connection.commit()
            return cursor.lastrowid

        except sqlite3.Error as e:
            print(f"Error al insertar en {table}: {e}")
            self.connection.rollback()
            return -1
    
    
    def update(self, table: str, updates: Dict[str, Any], where_condition: str, where_params: tuple = ()) -> bool:
        """
        Actualiza registros en una tabla.

        Args:
            table (str): Nombre de la tabla.
            updates (Dict[str, Any]): Diccionario con los campos y valores a actualizar.
            where_condition (str): Condición WHERE.
            where_params (tuple): Parámetros para la condición WHERE.

        Returns:
            bool: True si la actualización fue exitosa.
        """
        if not self.connection:
            self.connect()
        #print(f"los datos de la actualización son: {table, updates, where_condition, where_params}")
        try:
            set_clause = ", ".join([f"{key} = ?" for key in updates.keys()])
            query = f"UPDATE {table} SET {set_clause} WHERE {where_condition}"

            cursor = self.connection.cursor()
            cursor.execute(query, tuple(updates.values()) + where_params)
            self.connection.commit()
            return True

        except sqlite3.Error as e:
            print(f"Error al actualizar {table}: {e}")
            self.connection.rollback()
            return False
    
    
    def delete(self, table: str, where_condition: str, where_params: tuple = ()) -> bool:
        """
        Elimina registros de una tabla.

        Args:
            table (str): Nombre de la tabla.
            where_condition (str): Condición WHERE.
            where_params (tuple): Parámetros para la condición WHERE.

        Returns:
            bool: True si la eliminación fue exitosa.
        """
        if not self.connection:
            self.connect()

        try:
            query = f"DELETE FROM {table} WHERE {where_condition}"

            cursor = self.connection.cursor()
            cursor.execute(query, where_params)
            self.connection.commit()
            return True

        except sqlite3.Error as e:
            print(f"Error al eliminar de {table}: {e}")
            self.connection.rollback()
            return False

#######################################################################################################################
################################ SECCIÓN DE BUSQUEDAS Y ACTALIZACIÓN DE UNA BUSQUEDA ##################################
#######################################################################################################################
    
    def search(self, tipo_busqueda: str, valor_busqueda: str = None) -> List[Dict[str, Any]]:
        """
        Realiza una búsqueda en la base de datos según el tipo de búsqueda especificado.

        Args:
            tipo_busqueda (str): Tipo de búsqueda a realizar.
            valor_busqueda (str, opcional): Valor a buscar. Por defecto es None.

        Returns:
            List[Dict[str, Any]]: Lista de diccionarios con los resultados de la búsqueda.
        """
        if not self.connection:
            self.connect()

        try:
            cursor = self.connection.cursor()

            if tipo_busqueda == "Todos los Materiales":
                query = '''
                    SELECT codigo, nombre, tipo, tamaño, color, stock, precio, costo_unitario
                    FROM Materiales
                '''

            elif tipo_busqueda == "Proveedor especifico":
                query = '''
                    SELECT Proveedores.nombre, Facturas.numero_factura, Facturas.fecha,
                        Materiales.codigo, Materiales.nombre, Materiales.tipo,
                        Materiales.tamaño, Materiales.color, Materiales.stock,
                        Materiales.precio, Materiales.costo_unitario
                    FROM Proveedores
                    JOIN Facturas ON Proveedores.id_proveedor = Facturas.id_proveedor
                    JOIN Detalle_Factura ON Facturas.id_factura = Detalle_Factura.id_factura
                    JOIN Materiales ON Detalle_Factura.id_material = Materiales.id_material
                    WHERE Proveedores.nombre LIKE ?
                '''
                params = (f"%{valor_busqueda}%",)

            elif tipo_busqueda == "Factura Proveedor":
                query = '''
                    SELECT Proveedores.nombre, Facturas.numero_factura, Facturas.fecha,
                        Materiales.codigo, Materiales.nombre, Materiales.tipo,
                        Materiales.tamaño, Materiales.color, Materiales.stock,
                        Materiales.precio, Materiales.costo_unitario
                    FROM Facturas
                    JOIN Proveedores ON Facturas.id_proveedor = Proveedores.id_proveedor
                    JOIN Detalle_Factura ON Facturas.id_factura = Detalle_Factura.id_factura
                    JOIN Materiales ON Detalle_Factura.id_material = Materiales.id_material
                    WHERE Facturas.numero_factura LIKE ?
                '''
                params = (f"%{valor_busqueda}%",)

            elif tipo_busqueda == "Facturas Ventas":
                query = '''
                    SELECT Ventas.id_venta AS NumeroFactura, Clientes.nombre AS Cliente,
                        Ventas.fecha, Ventas.subtotal, Ventas.descuento,
                        Ventas.impuesto, Ventas.total
                    FROM Ventas
                    JOIN Clientes ON Ventas.id_cliente = Clientes.id_cliente
                    WHERE Ventas.tipo_documento = 'factura'
                    ORDER BY Ventas.fecha DESC
                '''
                params = ()

            elif tipo_busqueda == "Notas de Entregas":
                query = '''
                    SELECT Proveedores.nombre, Facturas.numero_factura, Facturas.fecha,
                        Materiales.codigo, Materiales.nombre, Materiales.stock,
                        Materiales.precio, Materiales.costo_unitario
                    FROM Facturas
                    JOIN Proveedores ON Facturas.id_proveedor = Proveedores.id_proveedor
                    JOIN Detalle_Factura ON Facturas.id_factura = Detalle_Factura.id_factura
                    JOIN Materiales ON Detalle_Factura.id_material = Materiales.id_material
                    WHERE Facturas.numero_factura LIKE ?
                '''
                params = (f"%{valor_busqueda}%",)

            elif tipo_busqueda == "Código especifico":
                query = '''
                    SELECT Proveedores.nombre, Facturas.numero_factura, Facturas.fecha,
                        Materiales.codigo, Materiales.nombre, Materiales.tipo,
                        Materiales.tamaño, Materiales.color, Materiales.stock,
                        Materiales.precio, Materiales.costo_unitario
                    FROM Materiales
                    JOIN Detalle_Factura ON Materiales.id_material = Detalle_Factura.id_material
                    JOIN Facturas ON Detalle_Factura.id_factura = Facturas.id_factura
                    JOIN Proveedores ON Facturas.id_proveedor = Proveedores.id_proveedor
                    WHERE Materiales.codigo LIKE ?
                '''
                params = (f"%{valor_busqueda}%",)

            elif tipo_busqueda == "Material especifico":
                query = '''
                    SELECT p.nombre, f.numero_factura, f.fecha, m.codigo, m.nombre,
                        m.tipo, m.tamaño, m.color, m.stock, m.precio, m.costo_unitario
                    FROM Materiales m
                    JOIN Detalle_Factura df ON m.id_material = df.id_material
                    JOIN Facturas f ON df.id_factura = f.id_factura
                    JOIN Proveedores p ON f.id_proveedor = p.id_proveedor
                    WHERE m.nombre LIKE ?
                '''
                params = (f"%{valor_busqueda}%",)

            elif tipo_busqueda == "Producto especifico":
                query = '''
                    SELECT p.codigo, p.tipo, p.costo_producto, p.precio_venta,
                            p.materiales_usados, p.tiempo_fabricacion, p.cantidad,
                            p.fecha_registro, p.descripcion
                    FROM Productos p
                    WHERE p.codigo LIKE ? OR p.nombre LIKE ?
                '''
                params = (f"%{valor_busqueda}%", f"%{valor_busqueda}%")

            elif tipo_busqueda == "Todos los Productos":
                query = '''
                    SELECT codigo, tipo, costo_producto, precio_venta,
                            materiales_usados, tiempo_fabricacion, cantidad,
                            fecha_registro, descripcion
                    FROM Productos
                '''
                params = ()

            elif tipo_busqueda == "Borradores Nuevos Productos":
                query = '''
                    SELECT nombre_usuario_creador, codigo_producto, tipo_producto,
                            cantidad_producida, fecha_creacion, fecha_finalizacion, estado
                    FROM productos_borrador
                '''
                params = ()
            
            elif tipo_busqueda == "Materiales de Empaque":
                query = '''
                    SELECT codigo_emp, nombre_emp, tamaño_emp,
                            stock_emp, precio_emp, costo_unitario_emp
                    FROM Empaques
                '''
                params = ()

            else:
                raise ValueError(f"Tipo de búsqueda no válido: {tipo_busqueda}")

            cursor.execute(query, params if 'params' in locals() else ())
            resultados = cursor.fetchall()

            # Obtener los nombres de las columnas
            columns = [column[0] for column in cursor.description]
            #print(columns)
            # Convertir los resultados a una lista de diccionarios
            #return [dict(zip(columns, row)) for row in resultados]
            #print(resultados) # duvuelve una lista de diccionarios con los valores
            return resultados

        except sqlite3.Error as e:
            #print(f"Error al realizar la búsqueda: {e}")
            return []
        
    
    def actualizar_en_bd(self, tipo_busqueda: str, nuevos_valores: Dict[str, Any], valores_originales: List[Any]) -> bool:
        """
        Realiza una actualización en la base de datos según el tipo de búsqueda especificado.

        Args:
            tipo_busqueda (str): Tipo de búsqueda a realizar.
            nuevos_valores (Dict[str, Any]): Diccionario con los nuevos valores.
            valores_originales (List[Any]): Lista con los valores originales.

        Returns:
            bool: True si la actualización fue exitosa, False en caso contrario.
        """
        #print(f"Tipo de búsqueda: {tipo_busqueda}")
        #print(f"Nuevos valores: {nuevos_valores}")
        #print(f"Valores originales: {valores_originales}")

        if not self.connection:
            self.connect()

        try:
            # --- Todos los Materiales ---
            if tipo_busqueda == "Todos los Materiales":
                codigo_original = valores_originales[0]  # Usar el código original para el WHERE
                #print(f"Actualizando material con código original: {codigo_original}")

                updates = {
                    "codigo": nuevos_valores.get("Código", valores_originales[0]),
                    "nombre": nuevos_valores.get("Nombre", valores_originales[1]),
                    "tipo": nuevos_valores.get("Tipo", valores_originales[2]),
                    "tamaño": nuevos_valores.get("Tamaño", valores_originales[3]),
                    "color": nuevos_valores.get("Color", valores_originales[4]),
                    "stock": nuevos_valores.get("Stock", valores_originales[5]),
                    "precio": nuevos_valores.get("Costo", valores_originales[6]),
                    "costo_unitario": nuevos_valores.get("Costo Unit.", valores_originales[7])
                }

                resultado = self.update(
                    table="Materiales",
                    updates=updates,
                    where_condition="codigo = ?",
                    where_params=(codigo_original,)
                )

                if resultado:
                    self.connection.commit()
                    #print("Actualización exitosa para 'Todos los Materiales'.")
                    return True
                else:
                    #print("No se actualizó ningún registro para 'Todos los Materiales'.")
                    return False

            # --- Material Específico ---
            elif tipo_busqueda == "Material especifico":
                codigo_original = valores_originales[3]  # Índice correcto para el código original
                #print(f"Actualizando material específico con código original: {codigo_original}")

                updates = {
                    "nombre": nuevos_valores.get("Nombre", valores_originales[4]),
                    "tipo": nuevos_valores.get("Tipo", valores_originales[5]),
                    "tamaño": nuevos_valores.get("Tamaño", valores_originales[7]),
                    "color": nuevos_valores.get("Color", valores_originales[7]),
                    "stock": nuevos_valores.get("Stock", valores_originales[8]),
                    "precio": nuevos_valores.get("Costo", valores_originales[9]),
                    "costo_unitario": nuevos_valores.get("Costo Unit.", valores_originales[10])
                }

                resultado = self.update(
                    table="Materiales",
                    updates=updates,
                    where_condition="codigo = ?",
                    where_params=(codigo_original,)
                )

                if resultado:
                    self.connection.commit()
                    #print("Actualización exitosa para 'Material Específico'.")
                    return True
                else:
                    #print("No se actualizó ningún registro para 'Material Específico'.")
                    return False

            # --- Código Específico ---
            elif tipo_busqueda == "Código especifico":
                codigo_nuevo = nuevos_valores.get("Código", valores_originales[3])
                id_material = self.obtener_codigo_por_id(codigo_nuevo)
                #print(f"ID del material para código {codigo_nuevo}: {id_material}")

                if not id_material:
                    #print("No se encontró el ID del material.")
                    return False

                resultado = self.update(
                    table="Materiales",
                    updates={"codigo": codigo_nuevo},
                    where_condition="id_material = ?",
                    where_params=(id_material,)
                )

                if resultado:
                    self.connection.commit()
                    #print("Actualización exitosa para 'Código Específico'.")
                    return True
                else:
                    #print("No se actualizó ningún registro para 'Código Específico'.")
                    return False

            # --- Proveedor Específico ---
            elif tipo_busqueda == "Proveedor especifico":
                proveedor_nuevo = nuevos_valores.get("Proveedor", valores_originales[0])
                id_proveedor = self.obtener_id_proveedor_por_nombre(proveedor_nuevo)
                #print(f"ID del proveedor para {proveedor_nuevo}: {id_proveedor}")

                if not id_proveedor:
                    #print("No se encontró el ID del proveedor.")
                    return False

                resultado = self.update(
                    table="Proveedores",
                    updates={"nombre": proveedor_nuevo},
                    where_condition="id_proveedor = ?",
                    where_params=(id_proveedor,)
                )

                if resultado:
                    self.connection.commit()
                    #print("Actualización exitosa para 'Proveedor Específico'.")
                    return True
                else:
                    #print("No se actualizó ningún registro para 'Proveedor Específico'.")
                    return False

            # --- Factura Proveedor ---
            elif tipo_busqueda == "Factura Proveedor":
                factura_nueva = nuevos_valores.get("Factura N°", valores_originales[1])
                fecha_nueva = nuevos_valores.get("Fecha", valores_originales[2])
                proveedor_original = valores_originales[0]

                id_proveedor = self.obtener_id_proveedor_por_nombre(proveedor_original)
                #print(f"ID del proveedor para {proveedor_original}: {id_proveedor}")

                if not id_proveedor:
                    #print("No se encontró el ID del proveedor.")
                    return False

                id_factura = self.obtener_id_factura_por_proveedor(id_proveedor, valores_originales[1])
                #print(f"ID de la factura: {id_factura}")

                if not id_factura:
                    #print("No se encontró el ID de la factura.")
                    return False

                resultado = self.update(
                    table="Facturas",
                    updates={"numero_factura": factura_nueva, "fecha": fecha_nueva},
                    where_condition="id_factura = ?",
                    where_params=(id_factura,)
                )

                if resultado:
                    self.connection.commit()
                    #print("Actualización exitosa para 'Factura Proveedor'.")
                    return True
                else:
                    #print("No se actualizó ningún registro para 'Factura Proveedor'.")
                    return False

            # --- Todos los Productos / Producto Específico ---
            elif tipo_busqueda in ["Todos los Productos", "Producto especifico"]:
                codigo_original = valores_originales[0]
                id_producto = self.obtener_id_producto_por_codigo(codigo_original)
                #print(f"ID del producto para código {codigo_original}: {id_producto}")

                if not id_producto:
                    #print("No se encontró el ID del producto.")
                    return False

                updates = {
                    "codigo": nuevos_valores.get("Código", valores_originales[0]),
                    "tipo": nuevos_valores.get("Tipo", valores_originales[1]),
                    "costo_producto": nuevos_valores.get("Costo Venta", valores_originales[2]),
                    "precio_venta": nuevos_valores.get("Precio Venta", valores_originales[3]),
                    "materiales_usados": nuevos_valores.get("Materiales Usados", valores_originales[4]),
                    "tiempo_fabricacion": nuevos_valores.get("Tiempo Fabricación", valores_originales[5]),
                    "cantidad": nuevos_valores.get("Cantidad", valores_originales[6]),
                    "fecha_registro": nuevos_valores.get("Fecha R", valores_originales[7]),
                    "descripcion": nuevos_valores.get("Descripción", valores_originales[8])
                }

                resultado = self.update(
                    table="Productos",
                    updates=updates,
                    where_condition="id_producto = ?",
                    where_params=(id_producto,)
                )

                if resultado:
                    self.connection.commit()
                    #print("Actualización exitosa para 'Productos'.")
                    return True
                else:
                    #print("No se actualizó ningún registro para 'Productos'.")
                    return False

            # --- Material Empaque ---
            elif tipo_busqueda == "Materiales de Empaque":
                codigo_original = valores_originales[0]  # Índice correcto para el código original
                #print(f"Actualizando material específico con código original: {codigo_original}")

                updates = {
                    "codigo_emp": nuevos_valores.get("Codigo", valores_originales[0]),
                    "nombre_emp": nuevos_valores.get("Nombre", valores_originales[1]),
                    "tamaño_emp": nuevos_valores.get("Tamaño", valores_originales[2]),
                    "stock_emp": nuevos_valores.get("Stock", valores_originales[3]),
                    "costo_unitario_emp": nuevos_valores.get("Costo Unit.", valores_originales[4])
                }

                resultado = self.update(
                    table="Empaques",
                    updates=updates,
                    where_condition="codigo_emp = ?",
                    where_params=(codigo_original,)
                )
                
            else:
                raise ValueError(f"Tipo de búsqueda no válido: {tipo_busqueda}")

        except Exception as e:
            #print(f"Error al actualizar la base de datos: {e}")
            self.connection.rollback()
            return False


    def obtener_id_proveedor_por_nombre(self, nombre_proveedor: str) -> Union[int, None]:
        """
        Obtiene el ID de un proveedor por su nombre.

        Args:
            nombre_proveedor (str): Nombre del proveedor.

        Returns:
            Union[int, None]: ID del proveedor o None si no se encuentra.
        """
        query = "SELECT id_proveedor FROM Proveedores WHERE nombre LIKE ?"
        resultado = self.select(query, (f"%{nombre_proveedor}%",), fetch_one=True)
        return resultado.get("id_proveedor") if resultado else None


    def obtener_id_factura_por_proveedor(self, id_proveedor: int, numero_factura: str) -> Union[int, None]:
        """
        Obtiene el ID de una factura por el ID del proveedor y el número de factura.

        Args:
            id_proveedor (int): ID del proveedor.
            numero_factura (str): Número de factura.

        Returns:
            Union[int, None]: ID de la factura o None si no se encuentra.
        """
        query = "SELECT numero_factura FROM Facturas WHERE id_proveedor = ?"
        
        resultado = self.select(query, (id_proveedor, f"%{numero_factura}%"), fetch_one=True)
        return resultado.get("id_factura") if resultado else None


    def obtener_codigo_por_id(self, id_material: int) -> Union[str, None]:
        """
        Obtiene el código de un material por su ID.

        Args:
            id_material (int): ID del material.

        Returns:
            Union[str, None]: Código del material o None si no se encuentra.
        """
        query = "SELECT id_material FROM Materiales WHERE codigo = ?"
        resultado = self.select(query, (id_material,), fetch_one=True)
        return resultado.get("codigo") if resultado else None


    def obtener_id_producto_por_codigo(self, codigo_producto: str) -> Union[int, None]:
        """
        Obtiene el ID de un producto por su código.

        Args:
            codigo_producto (str): Código del producto.

        Returns:
            Union[int, None]: ID del producto o None si no se encuentra.
        """
        #print("EL Código para obtener el id es: ",codigo_producto)
        query = "SELECT id_producto FROM Productos WHERE codigo = ?"
        resultado = self.select(query, (codigo_producto,), fetch_one=True)
        
        return resultado.get("id_producto") if resultado else None


#######################################################################################################################
############################################ SECCIÓN DE GESTIÓN DE USUARIO ############################################
#######################################################################################################################

    def registrar_usuario(self, usuario: str, clave: str, rol: str, pregunta: str, respuesta: str) -> Tuple[bool, str]:
        """
            Registra un nuevo usuario en la base de datos.

            Args:
                usuario (str): Nombre de usuario.
                clave (str): Clave del usuario.
                rol (str): Rol del usuario.
                pregunta (str): Pregunta de seguridad.
                respuesta (str): Respuesta de seguridad.

            Returns:
                Tuple[bool, str]: True y mensaje de éxito si el usuario se registró,
                        False y mensaje de error si el usuario ya existe.
        """
        if not self.connection:
            self.connect()
        
        try:
            # Validar que el usuario no exista
            query = "SELECT nombre_usuario FROM Usuarios WHERE nombre_usuario = ?"
            resultado = self.select(query, (usuario,), fetch_one=True)
            
            if resultado is not None:
                return False, "El usuario ya existe."

            # Cifrar la clave y guardar el hash
            hash_clave = hashlib.sha256(clave.encode()).hexdigest()

            # Insertar el nuevo usuario
            query = '''
                INSERT INTO Usuarios (nombre_usuario, clave, rol, pregunta_seguridad, respuesta_seguridad)
                VALUES (?, ?, ?, ?, ?)
            '''
            user_new = {"nombre_usuario": usuario,
                        "clave": hash_clave,
                        "rol": rol,
                        "pregunta_seguridad": pregunta,
                        "respuesta_seguridad": respuesta.lower()}
            
            user_id = self.insert("Usuarios", user_new)
            
            if user_id == -1:
                return False, "Error al registrar al usuario."
            
            return True, f"El usuario {usuario} se ha registrado exitosamente."
        
        except sqlite3.Error as e:
            #print(f"Error al registrar al usuario {e}")
            return False, f"Error al registrar al usuario {e}"
    
    
    def configuracion_usuario(self, conf_usuario: list[Any], usuario:str) -> bool:
        """
        Configuración de colores y fondo del usuario.

        Args:
            conf_usuario (list[Any]): datos de configuración.
            usuario (str): id del usuario.
        Returns:
            bool: Retorna True si la acción es exitosa o False si no lo es.
        """
        fondo_p = conf_usuario[0]
        fondo_m = conf_usuario[1]
        fondo_f = conf_usuario[2]
        img_fondo = conf_usuario[3]
        
        print(f"""CONFIGURACIÖN FINAL
            Pantalla Principal : {fondo_p}\n
            Color de la fuente: {fondo_m}\n
            Pantalla Menú: {fondo_f}\n
            Logo: {img_fondo}""")
        
        query = "SELECT id_usuario FROM Usuarios WHERE nombre_usuario = ?"
        params = usuario
        print(f"Usuario Actual: {usuario}")
        id_usuario = self.select(query, (params,))
        
        print(f"ID: {id_usuario}")
        actualizaciones = {
            "fondo_letra":fondo_f,
            "fondo_pantalla":fondo_p,
            "fondo_menu":fondo_m,
            "logo":img_fondo
        }
        # actualizado = self.update(
        #     table="Usuarios",
        #     updates=actualizaciones,
        #     where_condition="id_usuario",
        #     where_params=id_usuario
        # )
        return "El resultado ha llegado al Base de Datos."
        
    
    def validar_clave(self, usuario: str, clave: str) -> Tuple[bool, str, str]:
        """
        Valida los datos ingresados por un usuario.

        Args:
            usuario (str): Nombre de usuario.

        Returns:
            Tuple[bool, str, str]: verdadero, rol, mensaje.
        """
        query = """SELECT clave , rol FROM Usuarios WHERE nombre_usuario = ?"""
        resultado = self.select(query, (usuario,))
        
        if resultado is None:
            return False, "Usuario no registrado."
        #print(f"DataBaseManager: {resultado}")
        usuario_data = resultado[0]
        hash_almacenado = usuario_data["clave"]
        hash_ingresado = hashlib.sha256(clave.encode()).hexdigest()
        rol = usuario_data["rol"]
        
        if hash_ingresado == hash_almacenado:
            return True, rol, "Acceso concedido."
        else:
            rol = ""
            return False, rol, "Clave incorrecta."


    def recuperar_pregunta_seguridad(self, usuario: str) -> Tuple[Union[List[Dict[str, Any]], bool]]:
        """
        Recupera la pregunta de seguridad de un usuario.

        Args:
            usuario (str): Nombre de usuario.

        Returns:
            Tuple[Union[List[Dict[str, Any]], bool], str]:
                - Si el usuario existe: (lista con la pregunta de seguridad, mensaje)
                - Si el usuario no existe: (False, mensaje de error)
        """
        
        # Buscar el usuario y su respuesta de seguridad
        query = '''
            SELECT pregunta_seguridad FROM Usuarios
            WHERE nombre_usuario = ?
            '''
        resultado = self.select(query, (usuario,))
        #print(f"La pregunta de seguridad se ve asi: {resultado}")
        pregunta = resultado[0]["pregunta_seguridad"]
        if pregunta is None:
            return False, "Indica tu Usuario"
        
        return pregunta, "Usuario encontrado"
    
    
    def recuperar_clave(self, usuario: str, respuesta: str) -> Tuple[bool, str]:
        """
        Valida la respuesta 
        
        Args:
            usuario (str): Nombre de usuario
            respuesta (str): Respuesta ingresada por el usuario
        
        Return:
            Tuple[bool, str]: 
                - Si es correcto devuelve True y mensaje de exito.
                - si es incorrecto devuelve False y mensaje.
        """
        query = '''
            SELECT respuesta_seguridad FROM Usuarios
            WHERE nombre_usuario = ?
        '''
        #print(f"Los argumentos para la respuesta son: {usuario}, y {respuesta}")
        
        resultado = self.select(query, (usuario,))
        
        if resultado is None:
            return False, "Usuario no registrado."
        #print(f"Lo que llega de la consulta Generica: {resultado}")
        respuesta_almacenada = resultado[0]["respuesta_seguridad"]
        if respuesta.lower() == respuesta_almacenada:
            return True, f"Respuesta correcta. {usuario}, puedes restablecer tu clave."
        else:
            return False, "Respuesta incorrecta."
    
    
    def restablecer_clave(self, usuario: str, nueva_clave: str) -> Tuple[bool, str]:
        """
        Restablece la clave de un usuario.

        Args:
            usuario (str): Nombre de usuario.
            nueva_clave (str): Nueva clave del usuario.

        Returns:
            Tuple[bool, str]:
                - Si la clave se restablece con éxito: (True, mensaje de éxito).
                - Si no se puede restablecer la clave: (False, mensaje de error).
        """
        clave_str = str(nueva_clave)
        #print(type(clave_str), clave_str)
        # Cifrar la nueva clave
        nuevo_hash = hashlib.sha256(clave_str.encode()).hexdigest()

        # Actualizar el hash en la base de datos
        exito = self.update(
            table="Usuarios",
            updates={"clave": nuevo_hash},
            where_condition="nombre_usuario = ?",
            where_params=(usuario,)
        )

        if exito:
            return True, "Clave restablecida con éxito."
        else:
            return False, "No se ha podido restablecer la clave."
        
    
    def id_usuario_nombre_actual(self, nombre_usuario) -> int:
        """
        Recupera el id del usuario actual.

        Args:
            nombre_usuario (str): Nombre de usuario actual

        Returns:
            int: - Retorna el ID del usuario
        """
        
        query = "SELECT id_usuario FROM Usuarios WHERE nombre_usuario LIKE ?"
        
        id_usuario_list = self.select(query, (nombre_usuario,))
        
        id_usuario = id_usuario_list[0]["id_usuario"]
        
        if id_usuario:
            return id_usuario
        else:
            messagebox.showerror("⚠️ Error", f"El usuario {nombre_usuario} no tiene un ID")
    
    def buscar_usuarios(self, text_busqueda: str) -> List[tuple]:
        """
        Realiza la busque de un Usuario en la base de datos.

        Args:
            text_busqueda (str): El nombre de usuario.

        Returns:
            List[tuple]: - Retorna una lista de tuplas.
        """
        query = "SELECT id_usuario, nombre_usuario, rol FROM Usuarios WHERE nombre_usuario LIKE ?"
        params = text_busqueda
        
        busqueda_dic = self.select(query, (f"%{params}%",))
        
        campos_usuario = [
            "id_usuario",
            "nombre_usuario",
            "rol"
        ]
        
        busqueda_list = [
            tuple(diccionario.get(campo) for campo in campos_usuario)
            for diccionario in busqueda_dic
        ]
        return busqueda_list
    
    def actualizar_usuario(self, id_usuario: int, nombre_usuario: str, rol: str, pregunta: str, respuesta: str, contraseña: str=None) -> bool:
        """
        Actualizar cualquier información de un Usuario.

        Args:
            id_usuario (int): _description_
            nombre_usuario (str): _description_
            rol (str): _description_
            contrasena (str, optional): _description_. Defaults to None:str.

        Returns:
            bool: - Retorna True si la actualización se realiza sin errores O False si fallo la actualización.
        """
        actualizar_usuario_ = None
        if contraseña:
            actualizar_usuario_ = {
                    "nombre_usuario": nombre_usuario,
                    "clave": contraseña,
                    "rol": rol,
                    "pregunta_seguridad": pregunta,
                    "respuesta_seguridad": respuesta
                }
        
        else:
            actualizar_usuario_ = {
                    "nombre_usuario": nombre_usuario,
                    "rol": rol,
                    "pregunta_seguridad": pregunta,
                    "respuesta_seguridad": respuesta
                }
        #print(actualizar_usuario_)
        actualizado = self.update(
            table="Usuarios",
            updates=actualizar_usuario_,
            where_condition="id_usuario = ?",
            where_params=(id_usuario,)
        )
        #print(actualizado)
        if actualizado:
            messagebox.showinfo("Éxito", "Usuario actualizado correctamente.")
        else:
            messagebox.showerror("⚠️ Error", f"El usuario {nombre_usuario} no se pudo actualizar")
            
    
    def obtener_nombres_usuarios(self) -> List[tuple]:
        """
        Selecciona todos los nombres de usuario.

        Returns:
            List[tuple]: - Retorna una lista con los datos.
        """
        
        query = 'SELECT nombre_usuario FROM Usuarios'
        
        nombres_dic = self.select(query)
        
        nombres_list = [nombre["nombre_usuario"] for nombre in nombres_dic]
        
        #print(nombres_list)
        return nombres_list
    
    
    def eliminar_usuario_bd_nombre(self, nombre_usuario: str) -> bool:
        """
        Eliminar usuario por el nombre.

        Args:
            nombre_usuario (str): El nombre del usuario que se desea eliminar.
        Returns:
            bool: - Returna True si se completa la eliminación False si no.
        """
        query = "nombre_usuario = ?"
        
        params = nombre_usuario
        
        eliminado = self.delete(
            table= "Usuarios",
            where_condition= query,
            where_params= (params,)
        )
        
        if eliminado:
            return True
        else:
            return False
        
    def eliminar_usuario_bd(self, id_usuario) -> bool:
        """
        Elimina usuario por el id de usuario.

        Returns:
            bool: - Retorna True si la eliminación es exitosa, False si no.
        """
        query = "id_usuario = ?"
        params = id_usuario
        
        eliminado = self.delete(
            table= "Usuarios",
            where_condition= query,
            where_params= (params,)
        )
        
        if eliminado:
            return True
        else:
            return False
        
        
#######################################################################################################################
################################################ SECCIÓN DE PROVEEDOR #################################################
#######################################################################################################################

    def insertar_proveedor(self, nombre: str, contacto: str, telefono: str, email: str, direccion: str) -> int:
        """
        Ingresa un nuevo proveedor en la base de datos.

        Args:
            nombre (str): Nombre del Proveedor
            contacto (str): Algún sitio web o red social
            telefono (str): Número telefónico de oficina
            email (str): Correo electrónico del Proveedor
            direccion (str): Dirección fiscal del Proveedor

        Returns:
            int:
            - devuelve el id del regustro insertado
            - devuelve -1 si ocurre un error en la inserción
        """
        nuevo_proveedor = {"nombre": nombre,
                            "contacto": contacto,
                            "telefono": telefono,
                            "email": email,
                            "direccion": direccion}
        
        id_nuevo_usuario = self.insert("Proveedores", nuevo_proveedor)
        
        return id_nuevo_usuario
    
    
    def obtener_proveedores(self) -> List[Dict[str, any]]:
        """Devuelve los proveedores existentes.

        Returns:
            list[dict[str, any]]: 
            - Devuelve una lista con los proveedores en un dict.
        """
        query = 'SELECT nombre FROM Proveedores'
        proveedores_db = self.select(query)
        
        # Iteración para recuperar a todos los proveedores
        proveedores = [proveedor["nombre"] for proveedor in proveedores_db]
        
        return proveedores
    
    
    def eliminar_proveedor_bd(self, nombre_proveedor: str) -> bool:
        """
        Eliminar Proveedores de la base de datos

        Args:
            nombre_proveedor (str): Bonbre del proveedor.

        Returns:
            bool: Retorna True se la eliminación es exitosa o False si no lo es.
        """
                
        eliminado = self.delete(
            table= "Proveedores",
            where_condition= "nombre = ?",
            where_params= (nombre_proveedor,)
        )

        if eliminado:
            return True
        else:
            messagebox.showerror("⚠️ Error", "No se ha podido eliminar al proveedor.")
            return False
        
        
    #######################################################################################################################
    ################################################### SECCIÓN DE PRODUCTOS ##############################################
    #######################################################################################################################    
    
    def obtener_materiales_por_producto(self, id_producto):
        """Devuelve los materiales asociados a un producto específico.

        Args:
            id_producto (int): ID del producto.

        Returns:
            list[dict[str, any]]:
            - Devuelve una lista de diccionarios con los materiales del producto.
        """
        query = """
            SELECT m.id_material, m.codigo, m.nombre, m.stock, d.cantidad, d.es_por_metro, d.cantidad_cm
            FROM Materiales m
            JOIN Detalle_Producto d ON m.id_material = d.id_material
            WHERE d.id_producto = ?
        """
        #print(f"DEBUG: id_producto recibido = {id_producto}")  # Verificar el valor de id_producto
        
        materiales = self.select(query, (id_producto,))
        #print((f"MATERIALES DEL PRODUCTO: {materiales}"))
        
        query_emp = "SELECT empaques FROM Productos WHERE id_producto = ?"
        empaque_producto = self.select(query_emp, (id_producto,))
        #print(f"El kit de empaque es: {empaque_producto}")
        
        return materiales, empaque_producto
    
    
    def descontar_materiales(self, materiales_requeridos, cantidad_a_fabricar) -> bool:
        """
        Descarta la cantidad de material del inventario.

        Args:
            materiales_requeridos (list): Lista de materiales usados en un producto.
            cantidad_a_fabricar (int): Cantidad de productos nuevos a fabricar.

        Returns:
            bool:
                - Retorna True si todas las actualizaciones fueron exitosas.
                - Retorna False si existe algún error en alguna actualización.
        """

        try:
            for material in materiales_requeridos:
                id_material = material["id_material"]
                es_por_metro = self.comprobar_si_es_por_metro(material["codigo"])
                print(f"Materiales {material["codigo"]}--- es por metro {es_por_metro}")
                if es_por_metro:
                    print(f"La Cantidad en CM DB: {material["cantidad_cm"]}")
                    cantidad_requerida_por_producto = material["cantidad_cm"]
                    #calcula_cantidad_cm = round(float(cantidad_requerida_por_producto), 4) / 100
                    cantidad_total_a_descontar = cantidad_requerida_por_producto * cantidad_a_fabricar
                    cantidad_total_a_descontar_float = float(cantidad_total_a_descontar)
                else:
                    cantidad_requerida_por_producto = material["cantidad"]
                    cantidad_total_a_descontar = cantidad_requerida_por_producto * cantidad_a_fabricar
                    cantidad_total_a_descontar_float = float(cantidad_total_a_descontar)
                    
                stock_actual = material["stock"]  # Usar el stock obtenido en la consulta inicial

                # Verificar que no se vaya a valores negativos
                if stock_actual < cantidad_total_a_descontar_float:
                    #print(f"Error: No hay suficiente stock del material {material['nombre']}.")
                    return False

                nuevo_stock = stock_actual - cantidad_total_a_descontar_float
                print(f"EL Nuevo Stock es: {nuevo_stock:.4f}")
                # Actualizar el stock del material
                exito = self.update(
                    table="Materiales",
                    updates={"stock": nuevo_stock},
                    where_condition="id_material = ?",
                    where_params=(id_material,)
                )

                if not exito:
                    #print(f"Error al actualizar el stock del material {material['nombre']}.")
                    return False

            return True  # Retornar True solo después de procesar todos los materiales

        except Exception as e:
            print(f"⚠️ Error al descontar materiales: {e}")
            return False

        
    def incrementar_stock_producto(self, id_producto, cantidad_a_fabricar) -> bool:
        """
        Realiza el incremento del stock de un producto.

        Args:
            id_producto (int): ID único del producto.
            cantidad (int): Cantidad a incrementar.

        Returns:
            bool:
                - Retorna True si la actualización fue exitosa.
                - Retorna False si existe algún error.
        """
        #print(f"INCREMENTAR PRODUCTO {id_producto} CANTIDAD {cantidad_a_fabricar}")
        # Obtener la cantidad actual del producto
        cantidad_actual = self.select(
            "SELECT cantidad FROM Productos WHERE id_producto = ?",
            (id_producto,),
            fetch_one=True
        )

        if cantidad_actual is None:
            return False

        nueva_cantidad = cantidad_actual["cantidad"] + cantidad_a_fabricar

        # Actualizar la cantidad del producto
        exito = self.update(
            table="Productos",
            updates={"cantidad": nueva_cantidad},
            where_condition="id_producto = ?",
            where_params=(id_producto,)
        )
        return exito
    
    
    def validar_codigo_producto(self) -> List[str]:
        """
        Recupera todos los códigos de los productos (evitar duplicados)

        Args:
            codigo (str): Recibe el código tipo string

        Returns:
            List[str]: Retorna una lista con los codigos.
        """
        query = "SELECT codigo FROM Productos"
        
        codigos = self.select(query)
        
        codigo_list = [codigo["codigo"] for codigo in codigos]
        
        if codigo_list:
            return codigo_list
        else:
            messagebox.showerror("⚠️ Error", "No se ha podido comprobar si el código existe.")
            
            
    def insertar_producto(self,codigo, nombre, tipo, costo_producto, precio_venta, materiales_usados, tiempo_fabricacion, cantidad, descripcion, empaque, cantidad_cm=None) -> int:
        """
        Guardar en la base de datos un producto nuevo con todos los datos usados para crearlo.

        Args:
            codigo (str): Código único que se asigna.
            nombre (str): Nombre del nuevo Producto.
            tipo (str): Si es Pulsera, Collar, etc.
            costo_producto (float): Costo del producto según matriales usados.
            precio_venta (float): Precio calculado para vender.
            materiales_usados (list): Se guardan los materiales en una lista.
            tiempo_fabricacion (int): Tiempo que ha tomado crear el producto.
            cantidad (int): La cantidad que se ha producido.
            descripcion (str): Una breve descripción del producto.
            empaque (list): Se guarda los materiales de empaques usados en una lista.

        Returns:
            int: - Retorna el id del nuevo producto.
        """
        #print(f"La Cantidad que llega a insertar_producto es: {cantidad}")
        fecha_registro = datetime.now().strftime("%d.%m.%Y %H:%M")
        #print(f"Lista de materiales usados: {materiales_usados}-----DB") # [{'codigo': 'P-CRIS2', 'color': 'Regenbogen', 'tipo': 'Cristal', 'tamaño': '6mm', 'cantidad': 5.0, 'es_por_metro': False}, {'codigo': 'CORDON', 'color': 'negro', 'tipo': 'cordor', 'tamaño': '3mm', 'cantidad': 25.0, 'es_por_metro': True}]
        #print(f"La cantidad necesaria es: {cantidad_cm}")
        
        
        cantidad_cm_dict = {}
        campos = ["codigo"]
        codigo_tupla = [
            tuple(diccionario.get(campo) for campo in campos)
            for diccionario in materiales_usados
        ]
        #print(f"LOS CODIGO TUPLA SON: {codigo_tupla}")
        for material_codigo in codigo_tupla:
            # Consultar si el material es por metros
            #print(f"material codigo es: {type(material_codigo)}, {material_codigo}")
            query_es_por_metro = "SELECT es_por_metro FROM Materiales WHERE codigo = ?"
            material_data = self.select(query_es_por_metro, material_codigo)
            
            if material_data and material_data[0]["es_por_metro"] == "Si":
                # Si el material es por metros, agregar al diccionario
                cantidad_cm_dict[material_codigo[0]] = cantidad_cm
                #print(f"CANTIDAD_CM_DICC: {cantidad_cm_dict}")  # hasta aqui bien
                
        # Convertir el diccionario a JSON string
        cantidad_cm_json = json.dumps(cantidad_cm_dict) if cantidad_cm_dict else "{}"
        print(f"Formato JSON: {cantidad_cm_json}")
        
        
        # Convertir materiales y empaques a strings
        materiales_reales = []
        for material in materiales_usados:
            nombre_db = self.obtener_nombre_material_por_codigo(material["codigo"])
            materiales_reales.append(nombre_db)
        materiales_str = ",".join(materiales_reales) if materiales_reales else ""
    
        producto_nuevo = {
            "codigo": codigo,
            "nombre": nombre,
            "tipo": tipo,
            "costo_producto": costo_producto,
            "precio_venta": precio_venta,
            "materiales_usados": materiales_str, # materiales_usados,
            "tiempo_fabricacion": tiempo_fabricacion,
            "cantidad": cantidad,
            "fecha_registro": fecha_registro,
            "descripcion": descripcion,
            "empaques": empaque,
            "cantidad_cm": cantidad_cm_json
        }
        
        id_nuevo_producto = self.insert("Productos", producto_nuevo)
        
        #print(f"Los DATOS del NUEVO Producto son: {producto_nuevo}")
        
        if id_nuevo_producto:
            return True
        else:
            messagebox.showerror("⚠️ Error", f"El Producto {codigo}, no se pudo guardar.")
            
    
    def existe_borrador(self, codigo_producto) -> bool:
        """
        Verifica si ya existe un borrador para el código de producto.

        Args:
            codigo_producto (str): Codigo para verificar si existe.

        Returns:
            bool: - Retorna True si existe o False si no existe.
        """
        query = "SELECT id FROM productos_borrador WHERE codigo_producto = ? AND estado = 'pendiente'"
        resultado = self.select(query, (codigo_producto,))
        
        return resultado[0]["id"] if resultado else None
    
    
    def actualizar_borrador(self, usuario_actual_id, 
                        nombre_usuario_actual, 
                        codigo_producto, tipo_producto, 
                        tiempo_invertido, cantidad_producida, 
                        descripcion, materiales_actuales, 
                        empaques) -> bool:
        """
        Actualiza el borrador existente

        Args:
            usuario_actual_id (int): id de usuario actual.
            nombre_usuario_actual (str): Nombre del usuario.
            codigo_producto (str): Código del producto.
            tipo_producto (str): Tipo: pulsera, collar, llavero, zarcillos.
            tiempo_invertido (int): Cuanto tiempo llevo crear el producto.
            cantidad_producida (int): Cuantas piezas fueron creadas.
            descripcion (str): Descripción breve del producto.
            materiales_actuales (str): Diferentes tipos de materiales usados en el producto.
            empaques (str): Los empaques seleccionados para empacar el producto.

        Returns:
            bool: - Retorna True si hay exito en la actualización si no muestra mensaje de error.
        """
        actualizar_el_borrador = self.update(
            table="Productos_borrador",
            updates={
                "usuario_creador_id":usuario_actual_id,
                "nombre_usuario_creador":nombre_usuario_actual,
                "codigo_producto":codigo_producto,
                "tipo_producto":tipo_producto,
                "tiempo_invertido":tiempo_invertido,
                "cantidad_producida":cantidad_producida,
                "descripcion":descripcion,
                "materiales":materiales_actuales,
                "empaques":empaques,
                "estado":"pendiente"
            },
            where_condition="codigo_producto = ?",
            where_params=(codigo_producto,)
        )
        if actualizar_el_borrador:
            messagebox.showinfo("Información", "✅ El Borrador se ha actualizado")
        else:
            messagebox.showerror("⚠️ Error", f"No se pudo Actualizar el borrador")
    
            
    def guardar_borrador_db(self,usuario_actual_id, 
                        nombre_usuario_actual, 
                        codigo_producto, tipo_producto, 
                        tiempo_invertido, cantidad_producida, 
                        descripcion, materiales_actuales, 
                        empaques) -> int:
        """
        Guardar un borrador de un producto en proceso de fabricación.

        Args:
            usuario_actual_id (int): id de usuario actual.
            nombre_usuario_actual (str): Nombre del usuario.
            codigo_producto (str): Código del producto.
            tipo_producto (str): Tipo: pulsera, collar, llavero, zarcillos.
            tiempo_invertido (int): Cuanto tiempo llevo crear el producto.
            cantidad_producida (int): Cuantas piezas fueron creadas.
            descripcion (str): Descripción breve del producto.
            materiales_actuales (str): Diferentes tipos de materiales usados en el producto.
            empaques (str): Los empaques seleccionados para empacar el producto.

        Returns:
            int: - Retorna el ID del borrador sino muestra mensaje de error.
        """
        
        dict_borrador = {
            "usuario_creador_id": usuario_actual_id,
            "nombre_usuario_creador": nombre_usuario_actual,
            "codigo_producto": codigo_producto,
            "tipo_producto": tipo_producto,
            "tiempo_invertido": tiempo_invertido,
            "cantidad_producida": cantidad_producida,
            "descripcion": descripcion,
            "materiales": materiales_actuales,
            "empaques": empaques,
            "estado": "pendiente"
        }
        
        id_borrador = self.insert("productos_borrador", dict_borrador)
        
        if id_borrador:
            messagebox.showinfo("✅ Éxito", "Borrador guardado correctamente.")
        else:
            messagebox.showerror("⚠️ Error", f"No se pudo guardar el borrador")
            
    def borradores_pendientes(self) -> list:
        """
        Recupera los datos de un borrador de un producto.

        Returns:
            list: - Retorna una lista con los datos.
        """
        query = """SELECT id, codigo_producto, nombre_usuario_creador, tipo_producto, tiempo_invertido, 
                cantidad_producida, descripcion, fecha_creacion
                FROM productos_borrador
                WHERE estado = 'pendiente'
                ORDER BY fecha_creacion DESC"""
        
        datos = self.select(query)
        
        orden_campos = [
            'id',
            'codigo_producto',
            'nombre_usuario_creador',
            'tipo_producto',
            'tiempo_invertido',
            'cantidad_producida',
            'descripcion',
            'fecha_creacion'
        ]
        lista_de_tuplas = [
            tuple(diccionario.get(campo) for campo in orden_campos)
            for diccionario in datos
        ]
        
        if lista_de_tuplas:
            return lista_de_tuplas
        else:
            messagebox.showerror("⚠️ Error", f"No se encontraron los borradores pendientes")
            
    
    def cargar_borrador_db(self, borrador_id) -> Dict:
        """
        Obtiene los datos de un borrador para cargarlo en pantalla.

        Args:
            borrador_id (int): Id del borrador.

        Returns:
            Dict[tuple]: - Retorna diccionaro de tuplas
        """
        query = """SELECT codigo_producto, tipo_producto, tiempo_invertido, cantidad_producida, descripcion, 
                materiales, empaques FROM productos_borrador WHERE id = ?"""
        
        borrador = self.select(query, (borrador_id,))
        
        orden_campos = [
            "codigo_producto",
            "tipo_producto",
            "tiempo_invertido",
            "cantidad_producida",
            "descripcion",
            "materiales",
            "empaques",
        ]
        
        # Convertir a lista de tuplas
        lista_de_tuplas = [
            tuple(diccionario.get(campo) for campo in orden_campos)
            for diccionario in borrador
        ]
        
        if lista_de_tuplas:
            return lista_de_tuplas[0]
            #print(lista_de_tuplas)
            
    def marcar_borrador_como_creado(self, codigo_borrador) -> bool:
        """
        Actualia el estado de un boraador cuando se termina.

        Args:
            codigo_borrador (str_): Se actualiza por el código.

        Returns:
            bool: retorna True si la actualización es un exito False si no lo es.
        """
        fecha_finalizacion = datetime.now().strftime("%Y-%m-%d %H:%M")
        estado_actualizado = self.update(
            table= "productos_borrador",
            updates= {"estado": "creado", "fecha_finalizacion": fecha_finalizacion},
            where_condition="codigo_producto = ?",
            where_params= (codigo_borrador,)
            )
        
        if estado_actualizado:
            messagebox.showinfo("✅ Éxito", "Borrador finalizado correctamente.")
        else:
            messagebox.showerror("⚠️ Error", "Error al actualizar el estado del borrador")
            return False
        
    
    def insertar_detalle_producto(self, id_producto, id_material, cantidad, tipo, tamaño, es_por_metro=False) -> int:
        """
        Inserta en tabla relacional Detalle_Producto.

        Args:
            id_producto (int): Id del producto.
            id_material (int): Id del material usado
            cantidad (float): Cantidad de material.
            tipo (str): Tipo de producto que se crea.
            tamaño (str): Tamaño del material usado.

        Returns:
            int: - Retorna id de la nueva relación creada.
        """
        
        detalle = {
            "id_producto": id_producto,
            "id_material": id_material,
            "cantidad": cantidad,
            "tipo_material": tipo,
            "tamaño_material": tamaño,
            "es_por_metro": "Si" if es_por_metro else "No",
            "cantidad_cm": cantidad / 100 if es_por_metro else 0  # Guardar la cantidad en cm si es por metros
        }

        id_detalle = self.insert("Detalle_Producto", detalle)
        
        if id_detalle:
            #print(f"El id de la relación es: {id_detalle}")
            return id_detalle
        else:
            return False
            #print(f"Algo salio mal No se guardo en Detalle_Producto")
            
    
    def obtener_materiales_pro(self) -> tuple:
        """
        Selecciona los materiales para la creación de un producto.

        Returns:
            tuple: - Retorna una Tupla con los materiales.
        """
        
        query = "SELECT id_material, codigo, nombre, tipo, tamaño, color, stock, precio, costo_unitario, id_proveedor FROM Materiales"
        
        datos = self.select(query)
    
        orden_campos = [
            "id_material",
            "codigo",
            "nombre",
            "tipo",
            "tamaño",
            "color",
            "stock",
            "precio",
            "costo_unitario",
            "id_proveedor"
            
        ]
        
        materiales_tupla = [
            tuple(diccionario.get(campo) for campo in orden_campos)
            for diccionario in datos
        ]
        #print(materiales_tupla)
        return materiales_tupla
    
    def obtener_productos(self) -> tuple:
        """
        Recupera todos los productos

        Returns:
            tuple: Retorna una tupla con los productos.
        """
        query = "SELECT * FROM Productos"
        productos_lis = self.select(query)
        
        orden_campos = [
            "id_producto",
            "codigo",
            "nombre",
            "tipo",
            "costo_producto",
            "precio_venta",
            "materiales_usados",
            "tiempo_fabricacion",
            "cantidad",
            "fecha_registro",
            "descripcion",
            "empaques"
        ]
        
        productos_tupla = [
            tuple(diccionario.get(campo) for campo in orden_campos)
            for diccionario in productos_lis
        ]
        #print(productos_tupla)
        return productos_tupla
        
    
    def obtener_color_por_material(self, codigo_material) -> str:
        """
        Recupera el color segun el código ingresado

        Args:
            codigo_material (str): Codigo del material.

        Returns:
            str: - Retorna el color del material.
        """
        #print(f"OBTENER TAMAÑO MATERIAL: {codigo_material}")
        query = "SELECT DISTINCT color FROM Materiales WHERE codigo  LIKE ?"
        
        color_list = self.select(query, (codigo_material,))
        #print(color_list)
        color_str = [color["color"] for color in color_list]
        #print(f"RESULTADO DE LA BUSQUEDA DEL COLOR: {color_str}")
        return color_str
        
    
    def obtener_tipos_por_material_y_color(self, codigo_material, color_material) -> str:
        """
        Selecciona el tipo de material segun el código y el color.

        Args:
            codigo_material (str): Código material.
            color_material (str): Color material.

        Returns:
            str: - Retorna el tipo de material.
        """
        #print(f"OBTENER TIPOS MATERIAL: {codigo_material}, {color_material}")
        query = "SELECT DISTINCT tipo FROM Materiales WHERE codigo = ? AND color = ?"
        params = (codigo_material, color_material,)
        #print(f"PARAMETROS PARA LA CONSULTA SELECT EN TIPO MATERIAL: {params}")
        tipo_list = self.select(query, params)
        #print(f"RESULTADO DE LA CONSULTA SELECT EN TIPO DE MATERIAL ES: {tipo_list}")
        tipos_str = [tipo["tipo"] for tipo in tipo_list]
        
        return tipos_str
    
    
    def obtener_tamaños_por_material_color_tipo(self, nombre_material, color_material, tipo_material) -> str:
        """
        Recupera el tamaño del material en base a los parametros dados.

        Returns:
            str: - Retorna el valor obtenido.
        """
        #print(f"VALORES QUE LLEGAN PARA TAMAÑO MATERIAL: {nombre_material}, {color_material}, {tipo_material}")
        query = "SELECT DISTINCT tamaño FROM Materiales WHERE codigo = ? AND color = ? AND tipo = ?"
            
        params = (nombre_material, color_material, tipo_material)
        #print(f"PARAMETROS PARA LA CONSULTA DEL TAMAÑO DEL MATERIAL ES: {params}")
        tamaño_material = self.select(query, params)
        #print(f"RESULTADO DE LA CONSULTA PARA OBTENER EL TAMAÑO ES: {tamaño_material}")
        tamaño_str = [tamaño["tamaño"] for tamaño in tamaño_material]
        return tamaño_str
    
    
    def comprobar_si_es_por_metro(self, codigo_material):
        """Comprobar si un material es por metros"""

        query = "SELECT es_por_metro FROM Materiales WHERE codigo = ?"
        resultado = self.select(query, (codigo_material,))
    
        articulo_por_metro = resultado[0]["es_por_metro"] == "Si"
    

        if articulo_por_metro:
            #print(f"ARTICULO ES POR METROS: {codigo_material} - {articulo_por_metro}")
            return articulo_por_metro
        else:
            #print(f"ARTICULO NO ES POR METROS: {codigo_material} - {articulo_por_metro}")
            return articulo_por_metro
        
    
    def eliminar_producto_bd(self, codigo_producto: str) -> bool:
        """_summary_

        Args:
            codigo_producto (str): Código del producto que se desea eliminar.

        Returns:
            bool: Si la eliminación es exitosa retorna True o False si no.
        """
        params = codigo_producto
        
        query0 = "SELECT id_producto, cantidad FROM Productos WHERE codigo = ?"
        id_prod = self.select(query0, (params,))
        id_num = id_prod[0]["id_producto"]
        print(id_num)        
        
        query1 = """SELECT dm.id_material, dm.cantidad, m.stock, m.es_por_metro
                    FROM Detalle_Producto dm
                    JOIN Materiales m ON dm.id_material = m.id_material
                    WHERE dm.id_producto = ?"""
        datos = self.select(query1, (id_num,))
        
        print(f"Datos de JOIN: {datos}")        
        true = "Si"
        
        for convertir in datos:
            if convertir["es_por_metro"] == true:
                
                cant_pro = convertir["cantidad"]
                #print(f"Cantidad en Metros: {cant_pro}")
                
                convertir_cm = cant_pro / 100
                #print(f"Cantidad en cm: {convertir_cm}")
                
                stock_act = convertir["stock"]
                #print(f"Stock en db: {stock_act}")
                
                reponer_stock = stock_act + convertir_cm
                #print(f"Nuevo stock para guardar: {reponer_stock}")
                
                id_material = convertir["id_material"]
                #print(f"El id Material en material por metro: {id_material}")
                actualizado = self.update(
                        table="Materiales",
                        updates={"stock": reponer_stock},
                        where_condition="id_material = ?",
                        where_params=(id_material,)
                        )
                
            else:                
                cant_pro = convertir["cantidad"]
                #print(f"Cantidad Entera: {cant_pro}")
                
                stock_act = convertir["stock"]
                #print(f"Stock en db : {stock_act}")
                
                reponer_stock = stock_act + cant_pro
                #print(f"Nuevo stock para guardar: {reponer_stock}")
                
                id_material = convertir["id_material"]
                #print(f"El id Material en material entero: {id_material}")
                actualizado = self.update(
                        table="Materiales",
                        updates={"stock": reponer_stock},
                        where_condition="id_material = ?",
                        where_params=(id_material,)
                        )
            
        producto_eliminado = self.delete(
            table= "Productos",
            where_condition= "codigo = ?",
            where_params= (params,) 
        )
        
        if producto_eliminado:
            return True
        else:
            messagebox.showerror("⚠️ Error", "No se ha podido eliminar el producto.")
            return False
    
    
    #######################################################################################################################
    ################################################# SECCIÓN DE INVENTARIO ###############################################
    #######################################################################################################################

    def obtener_codigo_materiales(self) -> List[dict[str, Any]]:
        """
        Obtener los códigos de los Materiales.

        Returns:
            List[dict[str, Any]]: Lista de diccionario con los codigos
        """
        query = "SELECT codigo FROM materiales"
        codigos = self.select(query)
        
        codigos_list = [codigo["codigo"] for codigo in codigos]
        
        if not codigos_list:
            return codigos_list
        
        return codigos_list
    
    
    def obtener_material_por_codigo(self, codigo) -> str:
        """
        Se obtiene el nombre, tipo, tamaño, color del material por el código actual.

        Args:
            codigo (str): Código del Material

        Returns:
            str:
            - Retorna los valores antes mensionados
        """
        #print(f"El Código que llega es: {codigo}")
        query = 'SELECT nombre, tipo, tamaño, color FROM Materiales WHERE codigo = ?'
        materiales = self.select(query, (codigo,))
        
        if not materiales:
            # Error al consultar la base de datos.
            #print(f"No se encontraron materiales con el código: {codigo}")
            return "", "", "", ""
            
        #print(materiales) 
        nombre = materiales[0]["nombre"]
        tipo = materiales[0]["tipo"]
        tamaño = materiales[0]["tamaño"]
        color = materiales[0]["color"]
        
        return nombre, tipo, tamaño, color
    
    
    def actualizar_material(self, codigo, stock, precio, costo_unit, es_por_metro) -> bool:
        """
        Actualiza el stock del material y el costo.

        Returns:
            bool:
            - Retorna True para una operación exitosa
            - Retorna False si la operación no tuvo éxito.
        """
        getcontext().prec = 6
        query = "SELECT stock, precio FROM Materiales WHERE codigo = ?"
        db_stock = self.select(query, (codigo,))
        
        stock_actual = Decimal(self.conversion_decimal(db_stock[0]["stock"]))
        precio_anterior = Decimal(self.conversion_decimal(db_stock[0]["precio"]))
        #print(f"Stock: {stock}")
        stock_incrementa = Decimal(self.conversion_decimal(stock))
        #print(f"Stock: {precio}")
        precio_material = Decimal(self.conversion_decimal(precio))
        
        # Calcular el nuevo stock y el nuevo costo total acumulado
        nuevo_stock = stock_actual + stock_incrementa
        nuevo_costo_total = precio_anterior + precio_material
        nuevo_costo_unitario = nuevo_costo_total / nuevo_stock
        
        #print(f"COSTO TOTAL NUEVO: {nuevo_costo_total}")
        #print(f"PRECIO UNI NUEVO: {nuevo_costo_unitario}")
        
        actualizar = self.update(
            table= "Materiales",
            updates= {"stock": round(float(nuevo_stock), 2),
                    "precio": round(float(nuevo_costo_total), 2), 
                    "costo_unitario": round(float(nuevo_costo_unitario), 4),
                    "es_por_metro": es_por_metro},
            where_condition= "codigo = ?",
            where_params= (codigo,)
        )
        
        if actualizar:
            return True, f"Stock actualizado. Nuevo stock: {nuevo_stock}, nuevo costo promedio: {nuevo_costo_unitario:.4f}€."  # , nuevo_costo_unitario
        else:
            return False, "No se pudo actualizar el material."
        
    
    def obtener_id_material_por_codigo(self, codigo) -> int:
        """
        Recuperar el id del material según el código.

        Args:
            codigo (str): Referencia str para recuperar id

        Returns:
            int: retorna el nñumero de id 
        """
        
        query = "SELECT id_material FROM Materiales WHERE codigo = ?"
        
        datos = self.select(query, (codigo,))
        
        if datos:
            return datos[0]["id_material"]
        else:
            messagebox.showerror("⚠️ Error", "No se encontraro el ID del material.")
    
    
    def buscar_codigos_like(self, texto) -> List:
        """
        Recupera los Códigos según el patron de escritura

        Args:
            texto (str): 

        Returns:
            List: - Retorna una lista con el resultado.
        """
        patron = f"%{texto}%"
        query = """
                SELECT DISTINCT codigo
                FROM Materiales
                WHERE codigo LIKE ?
            """
        datos = self.select(query, (patron,))
        
        resultados_str = [fila["codigo"] for fila in datos]
        
        return resultados_str
            
            
    def codigo_existe(self, codigo) -> bool:
        """
        Verificar que el codigo no exista

        Args:
            codigo (str): Códigotipo string

        Returns:
            bool: - si existe devuelve True sino False.
        """
        query = "SELECT codigo FROM Materiales WHERE codigo = ?"
        
        codigos = self.select(query, (codigo,))
        
        existe = [cod["codigo"] for cod in codigos]
        
        if existe:
            return True
        else:
            return False
        
    def insertar_material(self, codigo, nombre, tipo, tamaño, color, stock, precio, costo_unitario, es_por_metro, id_proveedor) -> int:
        """
        Inserta en la base de datos un nuevo material

        Args:
            codigo (str): Código de tipo str crerado por el usuario.
            nombre (str): Nombre tipo str del Material.
            tipo (str): Tipo de material.
            tama (str): Que tamaño tiene el material.
            color (str): Color del material.
            stock (float): Cantidad a insertar del material.
            precio (float): Precio total del material
            costo_unitario (float): Costo por unidad de material
            es_por_metro (str): El usuario selecciona si es por metro o no.
            id_proveedor (int): Id del Proveedor.

        Returns:
            int: - Retorna el id del material
        """        
        materiales = {
            "codigo": codigo,
            "nombre": nombre,
            "tipo": tipo,
            "tamaño": tamaño,
            "color": color,
            "stock": self.conversion_decimal(stock),
            "precio": self.conversion_decimal(precio),
            "costo_unitario": self.conversion_decimal(costo_unitario),
            "es_por_metro": es_por_metro if es_por_metro is None else "No",
            "id_proveedor": id_proveedor
        }
        
        id_nuevo_materia = self.insert("Materiales", materiales)
        #print(f"ID Asignado al insertar material: {id_nuevo_materia}")
        if id_nuevo_materia:
            return id_nuevo_materia
        else:
            messagebox.showerror("⚠️ Error", f"No se pudo guardar el material {nombre}")
            
    
    def obtener_stock_material(self, codigo_material) -> float:
        """
        Obtiene el stock actual de un material.

        Args:
            codigo_material (str): Código del material

        Returns:
            int: - Retorna un float
        """
        
        query = "SELECT stock FROM Materiales WHERE codigo = ?"
        
        resultado = self.select(query, (codigo_material,))
        
        stock = resultado[0]["stock"]
        #print(f"El stock del material es: {stock} de tipo {type(stock)}")
        return stock if stock else 0
    
    
    def actualizar_stock_material(self, codigo, cantidad_creada, cantidad, es_por_metro=False) -> bool:
        """
        Actualiza el stock del material.
        - Si el material es por metros, descuenta la cantidad en metros (cantidad / 100).
        - Si no es por metros, descuenta la cantidad en unidades.

        Args:
            codigo (str): Código del material.
            cantidad (float): Cantidad a descontar (en cm si es por metros, en unidades si no).
            es_por_metro (bool): Si el material es por metros.

        Returns:
            bool: True si es exitoso, False si no lo es.
        """
        ##print(f"LO QUE LLEGA EN actualizar_stock_material es : {es_por_metro}")
        # Consultar el stock actual
        query = "SELECT stock FROM Materiales WHERE codigo = ?"
        material_data = self.select(query, (codigo,))
        if not material_data:
            messagebox.showerror("⚠️ Error", f"Material {codigo} no encontrado.")
            return False

        stock_actual = material_data[0]["stock"]

        if es_por_metro:
            # Convertir cm a metros
            cantidad_m = cantidad * cantidad_creada#/ 100
            nuevo_stock = stock_actual - cantidad_m
            #print(f"NUEVO STOCK = {stock_actual} - {cantidad_m} RESULTADO -> {nuevo_stock}")
        else:
            # Descontar en unidades
            cantidad_u = cantidad * cantidad_creada
            nuevo_stock = stock_actual - cantidad_u
            #print(f"NUEVO STOCK = {stock_actual} - {cantidad} RESULTADO -> {nuevo_stock}")
        # Validar que no quede stock negativo
        if nuevo_stock < 0:
            messagebox.showerror(
                "⚠️ Error",
                f"No hay suficiente stock del material {codigo}. Stock actual: {stock_actual}"
            )
            return False

        # Actualizar el stock
        material_actualizado = self.update(
            table="Materiales",
            updates={"stock": nuevo_stock},
            where_condition="codigo = ?",
            where_params=(codigo,)
        )

        if material_actualizado:
            return True
        else:
            messagebox.showerror("⚠️ Error", f"No se pudo actualizar el material {codigo}.")
            return False
            
    
    def obtener_nombre_material_por_codigo(self, codigo_material) -> list:
        """_summary_

        Args:
            codigo_material (str): Se usa el código del material para recuperar el nombre.

        Returns:
            list: - Retorna una lista
        """
        query = "SELECT nombre FROM Materiales WHERE codigo = ?"
        
        datos = self.select(query, (codigo_material,))
        
        nombre = datos[0]["nombre"]
        #print(nombre)
        return nombre if nombre else "Desconocido"
    
    
    def obtener_codigo_material_por_nombre_color_tipo_tamaño(self, codigo, color, tipo, tamaño) -> List:
        """
        Selecciona los Materiales por nombre, tipo, tamaño para crear producto nuevo.

        Returns:
            list: - Retorna una lista.
        """
        #print("EL MATERIAL ACTUAL RECIBIDO PARA LA CONSULTA ES: ", codigo)
        if not self.connection:
            self.connect()
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                SELECT codigo
                FROM Materiales
                WHERE codigo = ? AND color = ? AND tipo = ? AND tamaño = ?
            ''', (codigo, color, tipo, tamaño))
            resultado = cursor.fetchone()
            #print(f"Resultado directo: {resultado}")  # Depuración
            return resultado[0] if resultado else None
        except sqlite3.Error as e:
            #print(f"Error en consulta directa: {e}")
            return None
        
    
    def obtener_costo_unitario_material(self, codigo_material) -> int:
        """
        Recupera el costo unitario de un material

        Args:
            codigo_material (str): Código del material que sera seleccionado.

        Returns:
            int: - Retorna el costo unitario del material
        """
        
        query = "SELECT costo_unitario FROM Materiales WHERE codigo = ?"
        costo_uni = self.select(query, (codigo_material,))
        
        if costo_uni:
            return costo_uni[0]["costo_unitario"] if costo_uni else 0.0
        else:
            messagebox.showerror("⚠️ Error", "El precio unitario no se encontrado")
            
    
    def obtener_nombres_proveedores(self, texto) -> List[str]:
        """
        Obtener una lista de nombres de proveedores.

        Args:
            texto (str): - Filtra por nombre de proveedor.

        Returns:
            List[str]: - Retorna una lista con los nombres filtrados
        """
        #print(f"Esto llega para actualizar proveedores: {texto}")
        query = "SELECT nombre FROM Proveedores WHERE nombre LIKE ?"
        params = (f'%{texto}%',)
        
        proveedores_filtrados = self.select(query, params)
        
        proveedores = [proveedores_filtrados[0]["nombre"]]
        #print(f"Los Proveedores a Actualizar son: {proveedores}")
        return proveedores
    
    
    def eliminar_material_bd(self, nombre_material: str) -> bool:
        """
        Eliminar materiales de la base de datos

        Args:
            nombre_material (str): Nombre del material que se eliminara.

        Returns:
            bool: Si la operación es exitosa retorna True o False si existe un error.
        """
        #print(f"El nombre es: {nombre_material}")
        codigo_material = nombre_material.split(" ")
        #print(f"El codigo es: {codigo_material[0]}")
        material_eliminado = self.delete(
            table= "Materiales",
            where_condition= "codigo = ?",
            where_params= (codigo_material[0],)
        )
        
        if material_eliminado:
            return True
        else:
            messagebox.showerror("⚠️ Error", "No se ha podido eliminar el material.")
            return False
        
    
    def existe_borrador_factura(self, numero_factura):
        """Verifica si ya existe un borrador PENDIENTE para ese número de factura."""
        query = "SELECT id FROM facturas_borrador WHERE numero_factura = ? AND estado = 'pendiente'"
        resultado = self.select(query, (numero_factura,))
        return resultado[0]["id"] if resultado else None

    def guardar_borrador_factura_db(self, id_creador, nombre_creador, proveedor,
                                    numero_factura, fecha_factura,
                                    materiales_json, empaques_json):
        """Guarda un nuevo borrador de factura."""
        return self.insert(
            table="facturas_borrador",
            data={
                "usuario_creador_id": id_creador,
                "nombre_usuario_creador": nombre_creador,
                "proveedor": proveedor,
                "numero_factura": numero_factura,
                "fecha_factura": fecha_factura,
                "materiales": materiales_json,
                "empaques": empaques_json,
                "estado": "pendiente"
            }
        )

    def actualizar_borrador_factura(self, id_creador, nombre_creador, proveedor,
                                    numero_factura, fecha_factura,
                                    materiales_json, empaques_json):
        """Actualiza un borrador de factura pendiente existente."""
        return self.update(
            table="facturas_borrador",
            updates={
                "usuario_creador_id": id_creador,
                "nombre_usuario_creador": nombre_creador,
                "proveedor": proveedor,
                "fecha_factura": fecha_factura,
                "materiales": materiales_json,
                "empaques": empaques_json
            },
            where_condition="numero_factura = ? AND estado = 'pendiente'",
            where_params=(numero_factura,)
        )

    def borradores_facturas_pendientes(self):
        """Devuelve todos los borradores pendientes. NUNCA devuelve None (fix del TypeError)."""
        query = """
            SELECT id, nombre_usuario_creador, proveedor, numero_factura,
                fecha_factura, materiales, empaques, fecha_creacion
            FROM facturas_borrador
            WHERE estado = 'pendiente'
            ORDER BY fecha_creacion DESC
        """
        borradores = self.select(query)
        return borradores if borradores else []

    def cargar_borrador_factura_db(self, borrador_id):
        """Carga un borrador completo de factura."""
        query = """
            SELECT id, proveedor, numero_factura, fecha_factura, materiales, empaques
            FROM facturas_borrador WHERE id = ?
        """
        resultado = self.select(query, (borrador_id,))
        return resultado[0] if resultado else None

    def finalizar_borrador_factura(self, borrador_id):
        """Marca el borrador como finalizado al guardar la factura definitiva."""
        return self.update(
            table="facturas_borrador",
            updates={
                "estado": "finalizado",
                "fecha_finalizacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            where_condition="id = ?",
            where_params=(borrador_id,)
        )
            
#######################################################################################################################
################################################## SECCIÓN DE EMBALAJES ###############################################
#######################################################################################################################

    def insertar_empaque(self, codigo, nombre, tamaño, cantidad, precio, costo_unitario, es_por_metro) -> int:
        """Recibe la información de un material de empaque para insertarlo en la base de datos.

        Args:
            codigo (srt): Código unico.
            nombre (str): Nombre del empaque
            tama (str): descripción del tamaño.
            cantidad (int): Cantidad disponible para insertar.
            precio (float): El precio del embalaje.
            costo_unitario (float): Precio por unidad.
            es_por_metro (str): El Usuario selecciona si o no es por metro.

        Returns:
            int: _description_
        """
        #print(" DESDE INSERTAR EMPAQUES: ", codigo, nombre, tamaño, cantidad, precio, costo_unitario, es_por_metro)
        query = {
            "codigo_emp": codigo,
            "nombre_emp": nombre,
            "tamaño_emp": tamaño,
            "stock_emp": self.conversion_decimal(cantidad),
            "precio_emp": self.conversion_decimal(precio),
            "costo_unitario_emp": self.conversion_decimal(costo_unitario),
            "es_por_metro": es_por_metro
        }
        
        empaque_cod = self.insert("Empaques", query)
        
        if empaque_cod:
            return True, "El Material de empaque se ha guradado exitosamente."
        else:
            return False, "No se pudo guardar el material de empaque."
        
        
    def selecion_empaques(self) -> List[Dict[str, Any]]:
        """
        Seleciona todos los tipos de empaque existentes.

        Returns:
            List[Dict[str, Any]]: retorna una lista de diccionarios con los tipos de empaques.
        """
        
        query = "SELECT nombre_emp FROM Empaques"
        
        empaques = self.select(query)
        
        tipos_de_empaques = [empaque["nombre_emp"] for empaque in empaques]
        #print(tipos_de_empaques)
        
        return tipos_de_empaques
        
    def costo_embalaje(self, emp_kit) -> List[Dict[str, Any]]:
        # Filtrar solo los empaques que no están vacíos
        #print(f"EMPAQUE SELECCIONADO ES: {emp_kit}")
        empaques = [e for e in emp_kit if e]

        if not empaques:  # Si no hay empaques, devolver lista vacía
            return []
        
        emp_kit_str = emp_kit[0]
        #print(emp_kit_str)
        query_emp = "SELECT items_del_kit FROM KitEmpaque WHERE codigo_kit = ?"
        nombre_empaques = self.select(query_emp, (emp_kit_str,))
        #print(nombre_empaques[0]['items_del_kit'])
        if nombre_empaques:
            empaques_list = ast.literal_eval(nombre_empaques[0]['items_del_kit'])  # Ahora es una lista.
            #print(empaques_list)
        else:
            pass
            #print("No se esta obteniendo el resultado de los empaques")

        # Crear la consulta con IN
        placeholders = ", ".join(["?"] * len(empaques_list))  # Ej: "?, ?, ?"
        #print(f"Los Placeholders: {placeholders}")
        query = f"""
            SELECT costo_unitario_emp
            FROM Empaques
            WHERE nombre_emp IN ({placeholders})
        """
        datos = self.select(query, tuple(empaques_list))
        costos = [costo["costo_unitario_emp"] for costo in datos]
        #print(costos)
        return costos
    
    
    def validar_stock_empaques(self, empaques) -> bool: # APLICAR AL CREAR EL KIT
        """
        Valida que haya stock suficiente de los empaques seleccionados.

        Args:
            empaques (str): Empaques a verificar.

        Returns:
            bool: - Si haz existencia retorna True si no False.
        """
        #print(f"Los empaques a validar son: {empaques}")  # lista con el kit no con los empaques
        
        emp_kit_str = empaques[0]
        #print(emp_kit_str)
        query_emp = "SELECT items_del_kit FROM KitEmpaque WHERE codigo_kit = ?"
        nombre_empaques = self.select(query_emp, (emp_kit_str,))
        #print(nombre_empaques)
        empaques_de_kit = ast.literal_eval(nombre_empaques[0]["items_del_kit"])  # Ahora es una lista.
        #print(empaques_de_kit)
        
        for empaque in empaques_de_kit:
            query = "SELECT stock_emp FROM Empaques WHERE nombre_emp = ?"
            resultado = self.select(query, (empaque,))
            #print(f"Cantidades DB: {resultado}-------------------------------------")
            if not resultado or resultado[0]["stock_emp"] < 1:
                return False, f"No hay suficiente stock del empaque {empaque}."
    
        
        return True, "Stock de empaques suficiente."
    

    def descontar_empaques(self, emp_list, cantidad_creada) -> bool: #Modificar aqui
        """
        Con los nombres se tomo el costo unitario y se retorna y se descuenta de inventario.

        Args:
            cantidad (list): - lista con los tipos de empaques.

        Returns:
            bool: 
            - si se guarda y descuenta de inventario retorna True.
            - si no retorna False.
        """
        # Filtrar solo los empaques que no están vacíos
        empaques = [e for e in emp_list if e]
        if not empaques:  # Si no hay empaques, devolver lista vacía
            return []

        print(f"Descontar empaques que llegan: {emp_list}")
        print(f"Descontar empaques que for interno: {empaques}")
        
        emp_kit_str = empaques[0]
        print(f"El codigo extraido es: {emp_kit_str}")
        query_emp = "SELECT items_del_kit, cantidad_cm FROM KitEmpaque WHERE codigo_kit = ?"
        nombre_empaques = self.select(query_emp, (emp_kit_str,))
        
        if not nombre_empaques:
            return False, f"No se encontró el kit {emp_kit_str}."
        
        empaques_de_kit = ast.literal_eval(nombre_empaques[0]["items_del_kit"])  # Ahora es una lista.
        cantidades_cm = json.loads(nombre_empaques[0]["cantidad_cm"]) # Centimetros usados para el empaque.
        
        empaques_sin_stock = []
        
        for empaque in empaques_de_kit:
            # Consultar si el empaque es por metros y su stock actual
            query_item = """
            SELECT es_por_metro, stock_emp
            FROM Empaques
            WHERE nombre_emp = ?
            """
            item_data = self.select(query_item, (empaque,))
            if not item_data:
                empaques_sin_stock.append(empaque)
                continue

            item = item_data[0]
            es_por_metro = item["es_por_metro"] == "Si"
            print(f"ES POR METROS: {item}--- O NO: {es_por_metro}")
            stock_actual = item["stock_emp"]

            if es_por_metro:
                print(f"ENTRO EN EL CONDICIONAL if es_por_metro:")
                # Obtener la cantidad en cm usada en el kit
                cm = cantidades_cm.get(empaque, 0)
                if cm <= 0:
                    empaques_sin_stock.append(empaque)
                    continue

                cantidad_m = cm / 100  # Convertir cm a metros

                # Validar stock
                if stock_actual < cantidad_m:
                    empaques_sin_stock.append(empaque)
                    continue
                
                cantidad_mts = cantidad_m * cantidad_creada
                # Descontar del stock
                nuevo_stock = stock_actual - cantidad_mts
                print(f"LA RESTA DEL EMPAQUE ES: {nuevo_stock}")
                self.update(
                    table="Empaques",
                    updates={"stock_emp": round(float(nuevo_stock), 4)},
                    where_condition="nombre_emp = ?",
                    where_params=(empaque,)
                )

            else:
                #print(f"ENTRO EN EL ELSE:")
                # Item normal: descontar 1 unidad
                if stock_actual < 1:
                    empaques_sin_stock.append(empaque)
                    continue

                nuevo_stock = stock_actual - cantidad_creada
                print(f"NO ES POR METRO: {nuevo_stock}")
                self.update(
                    table="Empaques",
                    updates={"stock_emp": nuevo_stock},
                    where_condition="nombre_emp = ?",
                    where_params=(empaque,)
                )
        
        # Notificar al usuario sobre los empaques faltantes
        if empaques_sin_stock:
            mensaje = (
            "⚠️ Advertencia: Los siguientes empaques NO se descontaron por stock insuficiente:\n"
            + "\n- ".join(empaques_sin_stock)
            + "\n\nLos demás empaques se descontaron correctamente."
            )
            return False, mensaje
        else:
            return True, "✅ Inventario de Empaques Actualizado."        
        
        
    def empaque_incremento_db(self, nombre_empaque) -> List[Dict[str, any]]:
        """
        Selcciona Código y Tamaño de un empaque para actualizar combobox de incremento de stock.

        Args:
            nombre_empaque (str): Nombre del empaque como condición

        Returns:
            List[Dict[str, any]]: Devuelve una lista de diccionarios.
        """
        #print(f"NOMBRE DE EMPAQUE: {nombre_empaque}")
        query = "SELECT codigo_emp, tamaño_emp  FROM Empaques WHERE nombre_emp = ?"
        
        datos = self.select(query, (nombre_empaque,))
        
        datos_list = [dato for dato in datos[0].values()]
        #print(datos_list)
        
        if datos_list:
            return datos_list
        else:
            messagebox.showerror("⚠️ Error", "No se encontraron los datos.")
            
            
    def stock_de_empaque(self, codigo) -> List[Dict[str, any]]:
        """
        Obtiene la cantidad en existencia de un empaque

        Returns:
            List[Dict[str, any]]: Devuelve una lista de diccionario
        """
        
        query = "SELECT stock_emp FROM Empaques WHERE codigo_emp = ?"
        
        stock_db = self.select(query, (codigo,))
        
        stock = [cantidad["stock_emp"] for cantidad in stock_db]
        #print(f"La Cantidad es: {stock[0]}")  # Es un int.
        stock_int = stock[0]
        if stock:
            return stock_int
        
        else:
            messagebox.showerror("⚠️ Error", "No se pudo obtener la cantidad de este empaque.")
    
    
    def actualiza_stock_db(self, nuevo_stock, codigo) -> bool:
        """
        Se actualiza el valor en la base de datos de el stock.

        Args:
            nuevo_stock (float): nuevo valor del stock

        Returns:
            bool: 
            - True si la actualización es exitosa
            - False si se manifiesta un problema 
        """
        #print(f"Valor a actualizar: {nuevo_stock}-- código es: {codigo}")
        actualizado = self.update(
            table="Empaques",
            updates={"stock_emp": nuevo_stock},
            where_condition="codigo_emp =  ?",
            where_params=(codigo,)
        )
    
        if actualizado:
            return True
        else:
            messagebox.showerror("⚠️ Error", "No se pudo actualizar el stock ")
            
            
    def actualiza_precio_db(self, precio, codigo) -> bool:
        """
        Actualiza el costo del material de empaque

        Args:
            precio (str): Nuevo costo de Compra.
            codigo (_type_): Codigo de el Empaque.

        Returns:
            bool: Devuelve True si la operación es exitosa sino sera False.
        """
        actualizado = self.update(
            table="Empaques",
            updates={"precio_emp": precio},
            where_condition="codigo_emp = ?",
            where_params=(codigo,)
        )
        
        if actualizado:
            return True
        else:
            messagebox.showerror("⚠️ Error", "No pudo actualizar el precio")
            
            
    def codigo_empaques(self) -> List[tuple]:
        """
        Recupera los codigos de los empaques

        Returns:
            List[tuple]: - Retorna una lista de tuplas
        """
        
        query = "SELECT codigo_emp FROM Empaques"
        
        codigos = self.select(query)
        
        codigo_list = [codigo["codigo_emp"] for codigo in codigos]

            
        #print(codigo_tupla)
        if codigo_list:
            return codigo_list
        else:
            messagebox.showerror("⚠️ Error", "No se pudo obtener la información.")
            
            
    def selecciona_empaque_por_codigo(self, codigo) -> list[Tuple]:
        """
        Seleciona un empaque por el código

        Returns:
            list[Tuple]: - Retorna una lista de tuplas
        """
        query = "SELECT nombre_emp, tamaño_emp, stock_emp, precio_emp FROM Empaques WHERE codigo_emp = ?"
        params = codigo
        
        empaque = self.select(query, (params,))
        
        dict_claves = [
            "nombre_emp",
            "tamaño_emp",
            "stock_emp",
            "precio_emp"
        ]
        
        empaque_tupla = [
            tuple(diccionario.get(campo) for campo in dict_claves)
            for diccionario in empaque
        ]
        
        if empaque_tupla:
            #print(empaque_tupla[0][0], empaque_tupla[0][1], empaque_tupla[0][2], empaque_tupla[0][3])
            return empaque_tupla[0][0], empaque_tupla[0][1], empaque_tupla[0][2], empaque_tupla[0][3]
        else:
            messagebox.showerror("⚠️ Error", "No se pudieron obtener los datos del empaque.")
            
            
    def codigo_existe_emp(self, codigo) -> bool:
        """
        Verifica si un código existe en data base

        Args:
            codigo (str): Código en string

        Returns:
            bool: - retorna True si existe False si no.
        """
        
        query = "SELECT codigo_emp FROM Empaques WHERE codigo_emp = ?"
        params = codigo
        #print(f"El codigo que llega para ver si existe es {codigo}")
        cod_existe = self.select(query, (params,))
        #print(cod_existe)
        if cod_existe:
            return True
        else:
            return False
    
    
    def actualizar_empaque(self, codigo, stock, precio, costo_unit, es_por_metro) -> bool:
        """
        Si el código existe entoces actualiza sus datos.

        Args:
            codigo (str): Código.
            stock (float): Cantidad a incrementar.
            precio (float): Precio.
            costo_unitario (float): Costo por unidad.
            es_por_metro (str): El usuario selecciona si o no
        Returns:
            bool: - Retorna True si es exitoso, False si no.
        """
        getcontext().prec = 6
        
        query = "SELECT stock_emp, precio_emp FROM Empaques WHERE codigo_emp = ?"
        db_stock = self.select(query, (codigo,))
        
        en_stock = Decimal(self.conversion_decimal(db_stock[0]["stock_emp"]))
        precio_anterior = Decimal(self.conversion_decimal(db_stock[0]["precio_emp"]))
        stock_incrementa = Decimal(self.conversion_decimal(stock))
        precio_empaque = Decimal(self.conversion_decimal(precio))
        
        # Calcular el nuevo stock y el nuevo costo total acumulado
        nuevo_stock = en_stock + stock_incrementa
        nuevo_costo_total = precio_anterior + precio_empaque
        nuevo_costo_unitario = nuevo_costo_total / nuevo_stock
        
        #print(f"COSTO TOTAL NUEVO: {nuevo_costo_total}")
        #print(f"PRECIO UNI NUEVO: {nuevo_costo_unitario}")
        
        actualizar = self.update(
            table= "Empaques",
            updates= {"stock_emp": round(float(nuevo_stock), 2),
                    "precio_emp": round(float(nuevo_costo_total), 2), 
                    "costo_unitario_emp": round(float(nuevo_costo_unitario), 4),
                    "es_por_metro": es_por_metro},                    
            where_condition= "codigo_emp = ?",
            where_params= (codigo,)
        )
        

        if actualizar:
            return True, f"Stock actualizado. Nuevo stock: {nuevo_stock}, nuevo costo promedio: {nuevo_costo_unitario:.2f}€."
        else:
            return False, f"No se pudo actualizar el empaque {codigo}."
        

    def eliminacion_de_kit(self, codigo: str)-> bool:
        """
        Recibe el código del kit para eliminar los datos.

        Args:
            codigo (str): Código del kit que se quiere eliminar.

        Returns:
            bool: Retorna True si el proceso es exitoso False si se genera un error.
        """
        
        params = codigo
        
        eliminado = self.delete(
            table="KitEmpaque",
            where_condition="codigo_kit = ?",
            where_params=(params,)
        )
        
        if eliminado:
            return True
        else:
            return False
        
        
#######################################################################################################################
############################################## SECCIÓN DE KIT EMBALAJE  ###############################################
#######################################################################################################################

    def guardar_kit(self, codigo_kit, items_kit, usuario, cantidad_cm=None) -> tuple:
        """
        Guarda en la base de datos el kit de empaque creado por un usuario.
        Si hay items por metros, usa las cantidades en cm para calcular su costo.

        Args:
            codigo_kit (str): Código del kit.
            items_kit (list): Lista con los items que conforman el kit.
            usuario (str): Usuario que crea el kit.
            cantidad_cm (dict): Diccionario {item: cantidad_en_cm} para items por metros.

        Returns:
            tuple: (costo_kit_total, mensaje)
        """
        if cantidad_cm is None:
            cantidad_cm = {}  # Si no se pasa, inicializar como vacío

        costo_kit = []
        fecha_registro_kit = datetime.now().strftime("%d.%m.%Y %H:%M")  # Corregí el formato de fecha

        costo_emp = "SELECT costo_unitario_emp, es_por_metro FROM Empaques WHERE nombre_emp = ?"

        for nombre in items_kit:
            costos_dict = self.select(costo_emp, (nombre,))
            if not costos_dict:
                return -1, f"El item '{nombre}' no existe en la base de datos."

            item = costos_dict[0]
            es_por_metro = item["es_por_metro"] == "Si"  # Asumo que el valor es "Si" o "No"
            costo_unitario = item["costo_unitario_emp"]

            if es_por_metro:
                # Si el item es por metros, usar la cantidad en cm
                cm = cantidad_cm.get(nombre, 0)
                #print(f"Los Centimetros son: {cm}")
                if cm <= 0:
                    return -1, f"No se especificó una cantidad válida en cm para '{nombre}'."

                # Convertir cm a metros y calcular el costo
                metros = cm / 100
                costo_item = metros * costo_unitario
                costo_kit.append(costo_item)
            else:
                # Item normal: usar el costo_unitario_emp directamente
                costo_kit.append(costo_unitario)

        costo_kit_total = sum(costo_kit)

        nuevo_kit = {
            "codigo_kit": codigo_kit,
            "items_del_kit": str(items_kit),
            "costo_kit": costo_kit_total,
            "cantidad_cm": json.dumps(cantidad_cm),  # Convertir el diccionario a JSON
            "fecha_creacion": fecha_registro_kit,
            "usuario_creador": usuario
        }

        id_kit_guardado = self.insert("KitEmpaque", nuevo_kit)

        if id_kit_guardado:
            return costo_kit_total, "El Kit de Empaque se ha guardado correctamente."
        else:
            return -1, "No se pudo guardar el kit de empaque."
        
    
    def selecion_kit_empaques(self) -> list:
        """
        Selecciona los codigos de los kit de enpaques y los materiales que contiene

        Returns:
            list: - Retorna una lista con los datos.
        """
        codigos = []
        items = []
        costo = []
        
        query = "SELECT codigo_kit, items_del_kit, costo_kit FROM KitEmpaque"
        
        datos_kit = self.select(query)
        
        for valor in datos_kit:
            codigos.append(valor["codigo_kit"])
            items.append(valor["items_del_kit"])
            costo.append(valor["costo_kit"])
        
        if codigos and items and costo:
            return codigos, items, costo
        else:
            messagebox.showerror("⚠️ Error", "No se pudo obtener la información.")
            
            
    def descripcion_kit_empaque(self, empaques) -> List: # APLICAR AL CREAR EL KIT
        """
        Obtiene los nombres de los empaques para mostrar en descripción del kit.

        Args:
            empaques (str): Kit de empaques a verificar.

        Returns:
            List: - Retorna una lista con los datos de para la descripción.
        """
        #print(f"Los empaques a validar son: {empaques}")  # lista con el kit no con los empaques
        
        emp_kit_str = empaques[0]
        #print(emp_kit_str)
        query_emp = "SELECT items_del_kit FROM KitEmpaque WHERE codigo_kit = ?"
        nombre_empaques = self.select(query_emp, (emp_kit_str,))
        
        return nombre_empaques[0]
    
    def obtener_kits(self) -> List[any]:
        """
        Obtiene los kit de embalajes disponibles.

        Returns:
            List[any]: - Retorna una lista con los resultados.
        """
        query = "SELECT codigo_kit FROM KitEmpaque"
        
        datos_dic = self.select(query)
        
        kit_empaque = [campos["codigo_kit"] for campos in datos_dic]
        
        return kit_empaque
    
    def obtener_detalles_kit(self, codigo_kit) -> List[any]:
        """
        Selecciona los items que contine un kit de empaque

        Args:
            codigo_kit (str): Se recupera mediante el codigo del kit

        Returns:
            List[any]: - Retorna una lista con los items
        """
        query = "SELECT id_kit, items_del_kit, costo_kit FROM KitEmpaque WHERE codigo_kit = ?"
        params = (codigo_kit,)
        items_dic = self.select(query, params)
        
        items_list = ast.literal_eval(items_dic[0]["items_del_kit"])
        
        return items_dic[0:] # se retorna el diccionario con los datos.
    
    def actualizar_kit(self, codigo_kit, empaques, usuario) -> str:
        """
        Actualiza los empaques que conforman un kit

        Args:
            codigo_kit (str): Código de identificación del Kit.
            empaques (list): Lista con los empaques actualizados.
            usuario (str): Usuario que realizo la actualización.

        Returns:
            str: - Retorna el nuevo costo del kit y mensaje de exito.
        """
        placeholders = ", ".join(["?"] * len(empaques))  # Ej: "?, ?, ?"
        query = f"SELECT costo_unitario_emp FROM Empaques WHERE nombre_emp IN ({placeholders})"
        costos_empaques = self.select(query, tuple(empaques))
        
        costos = [costos["costo_unitario_emp"] for costos in costos_empaques]
        
        costo_actualizado = sum(costos)
        actualizado_time = datetime.now().strftime("%d.%m.%Y %H:%M")
        
        actualizar_data = {
            "items_del_kit": str(empaques),
            "costo_kit": costo_actualizado,
            "usuario_creador": usuario,
            "actualizado": actualizado_time
        }
        
        actualiza = self.update(
            table= "KitEmpaque",
            updates= actualizar_data,
            where_condition= "codigo_kit = ?",
            where_params= (codigo_kit,)
        )
        
        if actualiza:
            #print(actualiza)
            return costo_actualizado, "Kit actualizado correctamente"
        else:
            messagebox.showerror("⚠️ Error", "No se pudo Actualizar el Kit de empaque.")
            
#######################################################################################################################
################################################## SECCIÓN DE FACTURAS  ###############################################
#######################################################################################################################
    
    def obtener_id_factura_por_numero(self, numero_factura) -> List[Dict[str,any]]:
        """
        Obtiene el id de la factura mediante el número.

        Args:
            numero_factura (int): numero de factura para recuperar id.

        Returns:
            List[Dict[str,any]]: Retorna una lista de diccionarios con el resultado.
        """
        query = "SELECT id_factura FROM Facturas WHERE numero_factura = ?"
        #print(f"El número de factura a buscar es: {numero_factura}")
        datos = self.select(query, (numero_factura,))
        #print(f"DICCIONARIO NUMERO FACTURA: {datos}")
        retorna_datos = datos[0]["id_factura"]
        #print(f"El valor del diccionario es: {retorna_datos}")
        if retorna_datos:
            return retorna_datos
        else:
            messagebox.showerror("⚠️ Error", "No se pudo obtener el id de factura.")
            
            
    def insertar_factura(self, numero_factura, fecha, nombre_proveedor) -> int:
        """
        Inserta los datos basicos de la factura.

        Args:
            numero_factura (int): número de factura
            fecha (str): Fecha de ingreso.
            nombre_proveedor (str): Nombre del Proveedor.

        Returns:
            int: retorna el id del registro
        """
        id_proveedor = self.obtener_id_proveedor_por_nombre(nombre_proveedor)
        
        # Si el proveedor no existe, crear uno nuevo
        if id_proveedor is None:
            factura = {
                "nombre": nombre_proveedor,
            }
            id_p = self.insert("Proveedores", factura)
            
            if id_p:
                id_proveedor = id_p
            else:
                messagebox.showerror("⚠️ Error", "Error al guardar Nombre de Proveedor")
        
        fecha_registro = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # Asegúrate de que id_proveedor sea un entero
        if isinstance(id_proveedor, tuple):
            id_proveedor = id_proveedor[0]
            
        datos_factura = {
            "numero_factura": numero_factura,
            "fecha": fecha,
            "fecha_registro": fecha_registro,
            "id_proveedor": id_proveedor
        }
        datos = self.insert("Facturas", datos_factura)
        if datos:
            return datos
        else:
            messagebox.showerror("⚠️ Error", "Error al guardar los datos de la factura")
            
    
    def insertar_detalle_factura(self, id_factura, id_material, stock,  precio, costo_unitario) -> int:
        """
        agrega la relacion de material y factura a la tabla de Detalle_Factura

        Args:
            id_factura (int): id de factura generado.
            id_material (int): id de material agregado.
            stock (float): Cantidad de material disponible.
            precio (float): Precio total de la compra.
            costo_unitario (float): Costo por unidad.

        Returns:
            int: Retorna el id de la relacion (id_detalle)
        """
        factura = {
            "id_factura": id_factura,
            "id_material": id_material,
            "stock": self.conversion_decimal(stock),
            "precio": self.conversion_decimal(precio),
            "costo_unitario": self.conversion_decimal(costo_unitario)
        }
        
        id_detalle = self.insert("Detalle_Factura", factura)
        
        if id_detalle:
            return id_detalle
        else:
            messagebox.showerror("⚠️ Error", f"No se Ha podido Guardar el detalle de la Factura.")
    
    
    def actualizar_estado_nota_entrega(self, id_nota_entrega:int, estado:str)-> bool:
        """
        Actualiza el estado de la nota de entrega a Facturado.

        Args:
            id_nota_entrega (int): Id de la nota de entrega.
            estado (str): Nuevo estado.

        Returns:
            bool: - Retorna True si la actialización es correcta o False si algo sale mal.
        """        
        query = estado
        
        actualizado = self.update(
            table="NotasEntrega",
            updates={"estado":query},
            where_condition="id_nota_entrega = ?",
            where_params=(id_nota_entrega,)
        )

        if actualizado:
            return True
        else:
            messagebox.showerror("⚠️ Error", f"No se Ha podido cambiar el estado de la nota a una factura.")
            
    
#######################################################################################################################
############################################## SECCIÓN DE COSTO Y GANANCIAS ###########################################
#######################################################################################################################

    def obtener_productos_para_costoventa(self) -> List[Tuple[any]]:
            """
            Calcula el costo de venta del producto.

            Returns:
                List[Tuple[any]]: - Retorna una lista de tuplas.
            """
            
            query = "SELECT id_producto, codigo, costo_producto FROM Productos"
            datos = self.select(query)
            
            orden_campos = [
                "id_producto",
                "codigo",
                "costo_producto"
            ]
            productos_tupla = [
                tuple(diccionario.get(campo) for campo in orden_campos)
                for diccionario in datos
            ]
            #print(productos_tupla)
            return productos_tupla
        
        
    def obtener_productos_para_acthistorial(self) -> List[Tuple[any]]:
        """
        Actualizar el historial de un producto

        Returns:
            List[Tuple[any]]: - Retorna una lista de tuplas con la información.
        """
        query = "SELECT id_producto, codigo, costo_producto, precio_venta FROM Productos"
        
        productos_h = self.select(query)
        
        orden_campos = [
            "id_producto",
            "codigo",
            "costo_producto",
            "precio_venta"
        ]
        
        productos_tupla = [
            tuple(diccionario.get(campo) for campo in orden_campos)
            for diccionario in productos_h
        ]
        #print(productos_tupla)
        return productos_tupla
    
    
    def guardar_historial(self, id_producto, mes_año, ganancia, margen):
        """
        Guarda historial del producto
        """
        datos_producto = {
            "id_producto": id_producto,
            "mes": mes_año,
            "ganancia_total": ganancia,
            "margen_promedio": margen
        }
        insertar_datos = self.insert("Historial_Ganancias", datos_producto)
        
        if insertar_datos:
            pass
            #messagebox.showinfo("Información", "✅ Historial de ganancias guardado exitosamente.")
        else:
            messagebox.showerror("⚠️ Error", f"No se Ha podido Guardar el historial de ganancias.")
            
            
    def registrar_historial_costo(self, id_producto, costo_anterior, costo_nuevo, es_por_lote, unidades=None, motivo=None):
        """
        Registra el cambio en el historial de costos
        
        """
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
        datos_registro = {
            "id_producto": id_producto,
            "fecha": fecha,
            "costo_anterior": costo_anterior,
            "costo_nuevo": costo_nuevo,
            "es_por_lote": es_por_lote,
            "unidades": unidades,
            "motivo": motivo
        }
        
        datos_registrados = self.insert("Historial_Costos", datos_registro)
        
        if datos_registrados:
            messagebox.showinfo("Información", "✅ Historial de Costos guardado exitosamente.")
        else:
            messagebox.showerror("⚠️ Error", f"No se ha podido Guardar el historial de Costos.")
    
    
    def mostrar_historial_costos_por_producto(self, codigo_producto) -> List[Tuple[Any]]:
        """
        Args:
            codigo_producto (_type_): _description_

        Returns:
            List[Tuple[Any]]: _description_
        """        """ """      
        query = """
            SELECT p.codigo, h.fecha, h.costo_anterior, h.costo_nuevo, h.es_por_lote, h.unidades, h.motivo
            FROM Historial_Costos h
            JOIN Productos p ON h.id_producto = p.id_producto
            WHERE p.codigo = ?
            ORDER BY h.fecha DESC
            """
        params = (codigo_producto,)
        historial_producto = self.select(query, params)
        
        datos_historial = [
            "codigo",
            "fecha",
            "costo_anterior",
            "costo_nuevo",
            "es_por_lote",
            "unidades",
            "motivo"
        ]
        historial_producto_tupla = [
            tuple(diccionario.get(campo) for campo in datos_historial)
            for diccionario in historial_producto
        ]
        #print(historial_producto_tupla)
        return historial_producto_tupla
    
    
    def mostrar_historial_costos_general(self) -> List[Tuple]:
        """
        Mostrar el historial de costos de todos los productos.

        Returns:
            str: - Retorna una lista de tuplas
        """
        
        query = """
                SELECT p.codigo, h.fecha, h.costo_anterior, h.costo_nuevo, h.es_por_lote, h.unidades, h.motivo
                FROM Historial_Costos h
                JOIN Productos p ON h.id_producto = p.id_producto
                ORDER BY h.fecha DESC
                """
            
        historial_general = self.select(query)
        
        datos_historial = [
            "codigo",
            "fecha",
            "costo_anterior",
            "costo_nuevo",
            "es_por_lote",
            "unidades",
            "motivo"
        ]
        
        historial_general_tuple = [
            tuple(diccionario.get(campo) for campo in datos_historial)
            for diccionario in historial_general
        ]
        #print(historial_general_tuple)
        return historial_general_tuple
    
    
    def mostrar_historial_ganancias_producto(self, codigo_producto) -> List[Tuple]:
        """
        Mostrar Historial de ganacias de un producto

        Args:
            codigo_producto (str): Código del producto

        Returns:
            List[Tuple]: - Retorna una lista con tupla
        """        
        
        query = """
                SELECT h.mes, h.ganancia_total, h.margen_promedio
                FROM Historial_Ganancias h
                JOIN Productos p ON h.id_producto = p.id_producto
                WHERE p.codigo = ?
                ORDER BY h.mes DESC
                """
        params = (codigo_producto,)
                
        historial = self.select(query, params)
        
        datos_historial = [
            "mes",
            "ganancia_total",
            "margen_promedio"
        ]
        
        historial_tupla = [
            tuple(diccionario.get(campo) for campo in datos_historial)
            for diccionario in historial
        ]
        #print(historial_tupla)
        return historial_tupla
    
    
    def mostrar_historial_general_mensual(self, mes_str) -> List[Tuple]:
        """
        Mostrar historial de ganancias general mensual.

        Args:
            mes_str (str): Mes del historial.

        Returns:
            List[Tuple] - Retorna una lista de tuplas
        """        
        
        query = """
            SELECT p.codigo, h.ganancia_total, h.margen_promedio
            FROM Historial_Ganancias h
            JOIN Productos p ON h.id_producto = p.id_producto
            WHERE h.mes = ?
            ORDER BY p.codigo
            """
        params = (mes_str,)

        historial_general_mensual = self.select(query, params)
        
        datos_historial = [
            "codigo",
            "ganancia_total",
            "margen_promedio",
        ]
        
        historial_general_mensual_tupla = [
            tuple(diccionario.get(campo) for campo in datos_historial)
            for diccionario in historial_general_mensual
        ]
        #print(historial_general_mensual_tupla)
        return historial_general_mensual_tupla
    
    
    def actualizar_costo_producto(self, nuevo_costo: float, id_producto: int) -> bool:
        """
        Actualiza el Costo de un producto en Base de datos.

        Args:
            nuevo_costo (float): Nuevo Costo del producto.
            id_producto (int): id del producto que se actualiza.

        Returns:
            bool: - Retorna True Si la actialización es exitosa o False si no.
        """
        actualiza_coto = {
            "costo_producto": nuevo_costo
        }
        params = id_producto
        #print(params, type(params))
        #print(actualiza_coto)
        costo_actualizado = self.update(
            table= "Productos",
            updates= actualiza_coto,
            where_condition= "id_producto = ?",
            where_params= (params,)
        )
        
        if costo_actualizado:
            #print(f"COSTO ACTUALIZADO? {costo_actualizado}")
            return True
        else: 
            return False
    
    def datos_costo_d_producto_actualizar(self, codigo_producto: str) -> bool:
        """
        Selecciona los datos de costos de producción de un articulo.

        Args:
            codigo_producto (str): Codigo del producto 

        Returns:
            bool: - Retorna True si la actualización es exitosa o False si no.
        """
        query = "SELECT id_producto, costo_producto, precio_venta FROM Productos WHERE codigo = ?"
        params = codigo_producto
        
        datos_dic = self.select(query, (params,))
        
        campos_dic = [
            "id_producto",
            "costo_producto",
            "precio_venta"
        ]
        
        datos_list = [
            tuple(diccionario.get(campo) for campo in campos_dic)
            for diccionario in datos_dic
        ]

        if datos_list:
            return datos_list
        else:
            messagebox.showerror("⚠️ Error", f"No se encontró el producto seleccionado con código {codigo_producto}")
            
    
    def actualizar_precio_venta(self, precio: float, id_producto: int) -> bool:
        """
        Actualizar el precio_venta en la base de datos.

        Args:
            precio (float): Nuevo precio de venta.
            id_producto (int): id del producto a actualizar.

        Returns:
            bool: - Retorna True si la actualización es exitosa o False si no.
        """
        actualizar_campos = {
            "precio_venta": precio
        }
        
        precio_actualizado = self.update(
            table="Productos",
            updates= actualizar_campos,
            where_condition="id_producto = ?",
            where_params= (id_producto,)
        )
        
        if precio_actualizado:
            return True
        else:
            messagebox.showerror("⚠️ Error", f"No se ha podido actualizar el nuevo precio de venta del producto.")
            return False
    
    
    # insertar lote en la base de datos
    def insertar_lote(self, codigo: str, descripcion: str, unidades: int, costo_lote: float, precio_venta: float) -> int:
        """
        Insertar lote en la base de datos.

        Args:
            codigo (str): Código asignado al lote.
            descripcion (str): Pequeña descripción del lote.
            unidades (int): Número de unidades que conforman el lote.
            costo_lote (float): Costo del lote
            precio_venta (float): Precio de venta de las unidades

        Returns:
            int: - Retorna el id si es exitosa la operación o -1 se se produce un error.
        """
        fecha = datetime.now().strftime("%d.%m.%Y %H:%M")     
        query = {
            "codigo_lote": codigo,
            "fecha_creacion": fecha,
            "descripcion": descripcion,
            "cantidad_unidades": unidades,
            "costo_lote": costo_lote,
            "precio_venta_lote": precio_venta
        }
        
        lote_id = self.insert("Lotes", query)
        
        if lote_id:
            messagebox.showinfo("✅ Éxito", "Lote creado correctamente.")
            return lote_id
        else:
            messagebox.showerror("⚠️ Error", f"No se ha podido crear el Lote.")
            
    
    def registrar_lote_productos(self, id_lote: int, id_producto: int, cantidad: int) -> int: # Antes era insertar_lote_producto
        """
        Insertar en la tabla lote_productos

        Args:
            id_lote (int): Id del lote creado.
            id_producto (int): Id de los productos que lo conforman.
            cantidad (int): Cantidad de productos dentro del lote.

        Returns:
            int: -Retorna el id si la operación es exitosa o -1 si no lo es.
        """
        query = {
            "id_lote": id_lote,
            "id_producto": id_producto,
            "cantidad_asignada": cantidad
        }
        insertado_id = self.insert("Lote_productos", query)
        #print(f"EL ID  ES: {insertado_id}")
        if insertado_id:
            pass
            # messagebox.showinfo("✅ Éxito", "Lote actualizado correctamente.")
        else:
            messagebox.showerror("⚠️ Error", f"No se ha podido actualizar el Lote.")
            
            
    def obtener_lotes(self) -> List[Tuple[Any]]:
        """
        Obtener todos los lotes existentes.

        Returns:
            List[Tuple[Any]]: -Retorna una lista de tuplas.
        """
        
        query = "SELECT id_lote, fecha_creacion, descripcion, cantidad_unidades FROM Lotes"
        
        lotes_dic = self.select(query)
        
        campos = [
            "id_lote",
            "fecha_creacion",
            "descripcion",
            "cantidad_unidades"
        ]
        
        lotes_tupla = [
            tuple(diccionario.get(campo) for campo in campos)
            for diccionario in lotes_dic
        ]
        return lotes_tupla
    
    
    def obtener_costo_actual_lote(self, id_lote: int) -> float:
        """
        Recupera el costo actual de un lote.

        Args:
            id_lote (int): ID del lote actual

        Returns:
            float: - Retorna una lista de tuplas.
        """        
        
        query = "SELECT costo_lote FROM Lotes WHERE id_lote = ?"
        params = id_lote
        costo_actual = self.select(query, (params,))
        
        return costo_actual[0]["costo_lote"] if costo_actual else 0.0
    
    
    def costo_anterior_lote(self, id_lote: int) -> float:
        """
        Obtener el costo anterior del lote

        Args:
            id_lote (int): ID del lote actual.

        Returns:
            float: - Retorna los datos tipo float.
        """        
        query = "SELECT costo_lote FROM Lotes WHERE id_lote = ?"
        params = id_lote
        
        anterior_costo = self.select(query, (params,))
        
        return anterior_costo[0]["costo_lote"]
    
    
    def actualizar_costo_lote(self, nuevo_costo: float, id_lote: int) -> bool:
        """
        Actualizar el costo del lote.

        Args:
            nuevo_costo (float): Nuevo costo del Lote.
            id_lote (int): ID del Lote Actual.

        Returns:
            bool: - Retorna True si la actualización es exitosa si no False.
        """
        actualizado = self.update(
            table="Lotes",
            updates= {"costo_lote": nuevo_costo},
            where_condition="id_lote = ?",
            where_params=(id_lote,)
        )
        if actualizado:
            pass
        else:
            messagebox.showerror("⚠️ Error", f"No se ha podido actualizar el costo del Lote.")
            
    
    def actualiza_precio_venta_lote(self, nuevo_precio: float, id_lote: int) -> bool:
        """
        Actualizar el precio de venta del lote en la base de datos

        Args:
            nuevo_precio (float): Actualiza el precio de Venta del Lote.
            id_lote (int): ID del lote actual.

        Returns:
            bool: - Si la actualización es exitosa retorna True si no retorna False.
        """
        actualizado = self.update(
            table="Lotes",
            updates= {"precio_venta_lote": nuevo_precio},
            where_condition="id_lote = ?",
            where_params=(id_lote,)
        )
        
        if actualizado:
            pass
        else:
            messagebox.showerror("⚠️ Error", f"No se ha podido actualizar el precio de venta del Lote.")
            
    
    def obtener_lotes_con_productos(self) -> List[Tuple[Any]]:
        """
        Obtener los productos de los lotes

        Returns:
            List[Tuple[Any]]: - Retorna una lista de tuplas
        """
        query = """
            SELECT
                l.id_lote,
                l.codigo_lote,
                l.descripcion,
                l.cantidad_unidades,
                l.costo_lote,
                l.precio_venta_lote,
                GROUP_CONCAT(p.codigo || ' (' || lp.cantidad_asignada || ')', ', ') as productos
            FROM Lotes l
            LEFT JOIN Lote_Productos lp ON l.id_lote = lp.id_lote
            LEFT JOIN Productos p ON lp.id_producto = p.id_producto
            GROUP BY l.id_lote
        """
        productos_lote = self.select(query)
        
        campos = [
            "id_lote",
            "codigo_lote",
            "descripcion",
            "cantidad_unidades",
            "costo_lote",
            "precio_venta_lote",
        ]
        
        productos_lote_tupla = [
            tuple(diccionario.get(campo) for campo in campos)
            for diccionario in productos_lote
        ]
        return productos_lote_tupla
    
    
    def obtener_productos_del_lote_con_cantidades(self, id_lote: int) -> List[Tuple[Any]]:
        """
        Obtiene los productos de un lote con sus cantidades.

        Args:
            id_lote (int): el id del lote

        Returns:
            List[Tuple[Any]]: - Retorna una Lista de tuplas.
        """
        query = """
            SELECT lp.id_producto, p.codigo, lp.cantidad_asignada
            FROM Lote_Productos lp
            JOIN Productos p ON lp.id_producto = p.id_producto
            WHERE lp.id_lote = ?
        """
        params = id_lote
        lote_dict = self.select(query, (params,))
        
        campos = [
            "id_producto",
            "codigo",
            "cantidad_asignada"
        ]
        lote_tupla = [
            tuple(diccionario.get(campo) for campo in campos)
            for diccionario in lote_dict
        ]
        return lote_tupla
    
    
    # En db.py o DataBaseManager
    def eliminar_lote(self, id_lote):
        """
        Elimina un lote de la base de datos.
        Args:
            id_lote (int): Usa el id del lote para la eliminación

        Returns:
            bool: - Retorna True si la eliminación es exitosa o False si no.
        """
        #print(f"EL ID a eliminar es: {id_lote} y es de tipo {type(id_lote)}")
        eliminado = self.delete(
            table= "Lotes",
            where_condition= "id_lote = ?",
            where_params= (id_lote,)
        )
        
        if eliminado:
            return True
        else:
            messagebox.showerror("⚠️ Error", f"No se ha podido eliminar el Lote.")
        

    def eliminar_lote_productos(self, id_lote: int) -> bool:
        """
        Elimina un lote de la base de datos.
        Args:
            id_lote (int): Usa el id del lote para la eliminación

        Returns:
            bool: - Retorna True si la eliminación es exitosa o False si no.
        """
        #print(f"EL ID a eliminar es: {id_lote} y es de tipo {type(id_lote)}")
        eliminado = self.delete(
            table= "Lote_Productos",
            where_condition= "id_lote = ?",
            where_params= (id_lote,)
        )
        
        if eliminado:
            # messagebox.showinfo("✅ Éxito", "El Lote ha sido eliminado exitosamente." )
            return True
        else:
            messagebox.showerror("⚠️ Error", f"No se ha podido eliminar el Lote.")
            

    def obtener_productos_del_lote(self, id_lote: int) -> List[dict[Any]]:
        """
        Obtiene los productos asociados a un lote.
        Args:
            id_lote (_type_): _description_

        Returns:
            List[dict[Any]]: - Retorna una lista con diccionarios
        """
        #print(f"CODIGO A BUSCAR en productos_del_lote: {id_lote}")  
        query = """
            SELECT p.id_producto, p.codigo
            FROM Lote_Productos lp
            JOIN Productos p ON lp.id_producto = p.id_producto
            WHERE lp.id_lote = ?
        """
        productos_del_lote = self.select(query, (id_lote,))
        
        campos = [
            "id_producto",
            "codigo"
        ]
        
        productos_tupla = [
            tuple(diccionario.get(campo) for campo in campos)
            for diccionario in productos_del_lote
        ]
        return productos_tupla
    

    def actualizar_lote(self, id_lote: int, codigo: str, descripcion: str, unidades: int, costo: float, precio_total: float) -> bool:
        """
        Actualiza la información de un lote.
        Args:
            codigo (str): Código asignado.
            id_lote (int): Id del lote.
            descripcion (str): descripción.
            unidades (int): unidades a actualizar.
            costo (float): Costo del lote actualizado.
            precio_total (float): Precio total del lote.

        Returns:
            bool: - Retorna True si la actualización es exitosa o False si no.
        """        
        actualizado = self.update(
            table="Lotes",
            updates={"codigo_lote": codigo, "descripcion": descripcion, "cantidad_unidades": unidades, "costo_lote": costo, "precio_venta_lote": precio_total},
            where_condition= "id_lote = ?",
            where_params= (id_lote,)
        )
        
        if actualizado:
            return actualizado
        else:
            messagebox.showerror("⚠️ Error", f"No se ha podido Actualizar el Lote.")
        
    
#######################################################################################################################
######################################### SECCIÓN DE VENTAS Y NOTAS ETREGA ############################################
#######################################################################################################################

    def encotrar_notas_entrega(self) -> List[Tuple]:
        """
        Selecciona Nota de entrega de un cliente

        Returns:
            List[Tuple]: - Retorna una lista de tuplas.
        """        
        
        query = """SELECT ne.id_nota_entrega, ne.fecha, c.nombre, ne.total, ne.estado
            FROM NotasEntrega ne
            JOIN Clientes c ON ne.id_cliente = c.id_cliente"""
        
        notas_entregas = self.select(query)
        
        datos_nota_entrega = [
            "id_nota_entrega",
            "fecha",
            "nombre",
            "total",
            "estado"
        ]
        notas_entregas_tuplas = [tuple(diccionario.get(campo) for campo in datos_nota_entrega) 
                                for diccionario in notas_entregas]
        #print(notas_entregas_tuplas)
        return notas_entregas_tuplas
    
    
    def encontrar_facturas(self) -> List[Tuple]:
        """
        Selecciona Factura de un cliente

        Returns:
            List[Tuple]: - Retorna una lista de tuplas
        """        
        
        query = """
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
            ORDER BY v.fecha
        """
        facturas = self.select(query)
        
        #print("Las facturas son:  ", facturas)
        
        datos_facturas = [
            "id_venta",
            "fecha",
            "nombre",
            "subtotal",
            "descuento",
            "impuesto",
            "total"
        ]
        
        facturas_tupla = [
            tuple(diccionario.get(campos) for campos in datos_facturas) 
            for diccionario in facturas
        ]
        #print("ESTOS SON LOS DATOS DE LA CONSULTA DE LAS FACTURAS", facturas_tupla)
        return facturas_tupla
    
    
    def verificar_stock_suficiente(self, id_producto: int, cantidad_solicitada: int) -> bool:
        """
        Verificar cantidad del producto para poder realizar la venta.

        Args:
            id_producto (int): Id del producto de venta.
            cantidad_solicitada (int): La cantidad que se desea vender.

        Returns:
            bool: - Retorna True si hay la cantidad requerida, cantidad actual, mensaje.
        """
        query = "SELECT cantidad FROM Productos WHERE id_producto = ?"
        params1 = id_producto
        params2 = cantidad_solicitada
        
        cantidad_act = self.select(query, (params1,))
        
        if not cantidad_act:
            return False, 0, "Producto no encontrado en la base de datos."

        stock_actual = cantidad_act[0]["cantidad"]
        #print(f"Stock disponible: {stock_actual}")
        if stock_actual <= 0:
            #print(f"⚠️ No hay stock disponible para este producto: {stock_actual}")
            return False, stock_actual, "No hay stock disponible para este producto."
        elif stock_actual < cantidad_solicitada:
            #print(f"⚠️ No hay suficiente stock. Stock disponible: {stock_actual}")
            return False, stock_actual, f"No hay suficiente stock. Stock disponible: {stock_actual}"
        else:
            #print(f"✅ Stock suficiente: {stock_actual}")
            return True, stock_actual, "Stock suficiente."
        
    
    def nuevo_cliente(self, nombre: str, direccion: str, casa_num: str, zona_postal: str, 
                        identificacion_fiscal: str, email: str, telefono: str) -> int:
        """
        Agregar nuevo Cliente en la base de datos.

        Args:
            nombre (str): Nombre del nuevo cliente.
            direccion (str): Dirección de casa u oficina del cliente.
            casa_num (str): Número de casa u oficina.
            zona_postal (str): Zona postal del país donde se ubica.
            identificacion_fiscal (str): Número de registro fiscal si posee.
            email (str): Correo electronico del cliente.
            telefono (str): Número telefonico del cliente.

        Returns:
            int: - Retorna el id del nuevo cliente.
        """
        query = {
            "nombre": nombre,
            "direccion": direccion,
            "casa_num": casa_num,
            "zona_postal": zona_postal,
            "identificacion_fiscal": identificacion_fiscal,
            "email": email,
            "telefono": telefono
        }
        
        cliente_id = self.insert("Clientes", query)
        
        return cliente_id
    
    
    def cargador_clientes(self) -> List[Tuple[Any]]:
        """
        Cargar los clientes disponibles para generar una factura.

        Returns:
            List[Tuple[Any]]: - Retorna una lista de tuplas.
        """
        query = "SELECT id_cliente, nombre FROM Clientes"
        
        clientes_dicc = self.select(query)
        
        campos_cliente = [
            "id_cliente",
            "nombre"
        ]
        
        clientes_list = [
            tuple(diccionario.get(campo) for campo in campos_cliente)
            for diccionario in clientes_dicc
        ]

        return clientes_list
    
    def cargador_productos(self) -> List[Tuple[Any]]:
        """
        Cargar productos disponibles para la venta con factura.

        Returns:
            List[Tuple[Any]]: - Retorna una lista de tuplas con los productos disponible.
        """
        query = "SELECT id_producto, codigo, tipo, precio_venta, cantidad FROM Productos WHERE cantidad > 0"
        
        productos_dicc = self.select(query)
        
        campos_productos = [
            "id_producto",
            "codigo",
            "tipo",
            "precio_venta",
            "cantidad"
        ]
        
        productos_list = [
            tuple(diccionario.get(campo) for campo in campos_productos)
            for diccionario in productos_dicc
        ]
        
        return productos_list
    
    
    def detalle_producto_venta(self, id_producto: int) -> List[Tuple[Any]]:
        """
        Obtener codigo y el precio de venta del producto a venta.

        Args:
            id_producto (int): Id del producto para la recuperación de los detalles.

        Returns:
            List[Tuple[Any]]: - Retorna una lista de tuplas con los detalles del producto.
        """
        query = "SELECT codigo, precio_venta FROM Productos WHERE id_producto = ?"
        params = id_producto
        
        datos_dicc = self.select(query, (params,))        
    
        codigo, precio_uni = datos_dicc[0].values()
        #print(f"Los datos del producto son: {codigo}, {precio_uni}")
        return codigo, precio_uni
        

    def guarda_venta_bd(self, id_venta: int,
                        id_cliente: int, fecha_actual: str,
                        tipo_documento: str, subtotal: float,
                        descuento: float, impuesto: float, total: float, usuario_actual:str) -> bool:
        """
        Insertar la venta en la base de datos "FACTURA"

        Args:
            id_venta (int): id de la venta realizada.
            id_cliente (int): id del comprador.
            fecha_actual (str): Fecha que se realiza la venta.
            tipo_documento (str): Tipo factura.
            subtotal (float): Subtotal de la factura.
            descuento (float): Descuento dado al comprador (opcional).
            impuesto (float): Taza del impuesto actual.
            total (float): Total del monto de la factua.
            usuario_actual (str): Usuario que realiza el proceso.

        Returns:
            bool: - Retorna True si se guarda correctamente False si se genera algún error.
        """
        query = {
            "id_venta": id_venta,
            "id_cliente": id_cliente,
            "fecha": fecha_actual,
            "tipo_documento": tipo_documento,
            "estado":"facturado",
            "usuario_creador":usuario_actual,
            "subtotal": subtotal,
            "descuento": descuento,
            "impuesto": impuesto,
            "total": total,
            }
        
        venta_realizada = self.insert("Ventas", query)
        
        return venta_realizada
    
    
    def agregar_detalle_venta(self, id_venta: int, id_producto: int, cantidad: int, precio_unitario: float, subtotal: float, descuento: float) -> int:
        """
        Insertar datos en detalle factura.

        Args:
            id_venta (int): id de venta. 
            id_producto (int): id del producto.
            cantidad (int): Cantidad vendida.
            precio_unitario (float): Precio por unidad.
            subtotal (float): Sub-total de la venta.
            descuento (float): Solo en caso de aplicar un descuento.

        Return"s:
            int: - Retorna el id de detalle factura.
        """
        #print(f"LOS DATOS PARA DETALLE FACTURA: {id_venta}-{id_producto}-{cantidad}-{precio_unitario}-{subtotal}-{descuento}")
        query = {
            "id_venta": id_venta,
            "id_producto": id_producto,
            "cantidad": cantidad,
            "precio_unitario": precio_unitario,
            "subtotal": subtotal,
            "descuento": descuento
        }
        id_detalle = self.insert("Detalle_venta", query)
        
        if id_detalle:
            return id_detalle
        else:
            messagebox.showerror("⚠️ Error", f"No se ha podido Guardar la venta correctamente.")
            
            
    def agregar_detalle_nota_entrega(self, nota_entrega: int, id_producto: int, cantidad: int, precio_unitario: float, subtotal: float, descuento: float) -> int:
        """
        Insertar datos en detalle Nota de entrega.

        Args:
            nota_entrega (int): id de la nota de entrega.
            id_producto (int): id del producto.
            cantidad (int): Cantidad del producto vendido.
            precio_unitario (float): Precio por unidad de producto.
            subtotal (float): Subtotal de Nota de entrega.
            descuento (float): Solo en caso de aplicar un descuento.

        Returns:
            int: - Retorna id de la nota de entraga si la inserta correctamente.
        """
        query = {
            "id_nota_entrega": nota_entrega,
            "id_producto": id_producto,
            "cantidad": cantidad,
            "precio_unitario": precio_unitario,
            "subtotal": subtotal,
            "descuento": descuento
        }
        
        id_nota = self.insert("DetalleNotaEntrega", query)
        
        if id_nota:
            return id_nota
        else:
            messagebox.showerror("⚠️ Error", f"No se ha podido Guardar los detalles de la nota de entrega correctamente.")
            
    
    def guardar_nota_entrega(self, id_cliente: int, fecha: str, subtotal: float, descuento: float, impuesto: float, total: float) -> int:
        """
        Guarda la nota de entrega generada.

        Args:
            id_cliente (int): id de un cliente.
            fecha (str): fecha de la creación de la nota de entrega.
            subtotal (float): Subtotal de la nota de entrega.
            descuento (float): Descuento solo si aplica.
            impuesto (float): taza de impuesto actual.
            total (float): Monto total.

        Returns:
            int: - Retorna id de la nota guardada.
        """
        query = {
            "id_cliente": id_cliente,
            "fecha": fecha,
            "subtotal": subtotal,
            "descuento": descuento,
            "impuesto": impuesto,
            "total": total
        }
        id_nota = self.insert("NotasEntrega", query)
        
        if id_nota:
            return id_nota
        else:
            messagebox.showerror("⚠️ Error", f"No se ha podido Guardar la nota de entrega correctamente.")
            
            
    def actualizar_stock_producto_venta(self, cantidad: int, id_producto: int) -> bool:
        """
        Actualiza el stock del producto vendido.

        Args:
            cantidad (int): Cantidad que se vende de un producto.
            id_producto (int): Id del producto vendido.

        Returns:
            bool: Si la actualización es exitosa retorna True sino retorna False.
        """
        #print(f"Cantidad a descontar: {cantidad} - id del producto: {id_producto}")
        query_1 = "SELECT cantidad FROM Productos WHERE id_producto = ?"
        cantidad_actual = self.select(query_1, (id_producto,))
        #print(f"El Monto seleccionado es: {cantidad_actual}")
        nueva_cantidad = cantidad_actual[0]["cantidad"] - cantidad
        #print(f"El Monto actualizado es: {nueva_cantidad}")
        query_2 = {"cantidad": nueva_cantidad}
        
        actualizado = self.update(
            table= "Productos",
            updates= query_2,
            where_condition= "id_producto = ?",
            where_params= (id_producto,)
        )
        
        if actualizado:
            return actualizado
        else:
            messagebox.showerror("⚠️ Error", f"No se ha podido Actualizar la cantidad correctamente.")
            return False
        
    def obtener_estado_nota_entrega(self, id_nota_entrega: int) -> str:
        """
        Obtiene el estado pendiente de una nota de entrega.

        Args:
            id_nota_entrega (int): id de la nota de entrega.

        Returns:
            str: - Retorna el estado de la nota de entrega.
        """
        query = "SELECT estado FROM NotasEntrega WHERE id_nota_entrega = ?"
        params = id_nota_entrega
        
        estado_nota = self.select(query, (params,))
        
        if estado_nota:
            return estado_nota[0]["estado"]
        else:
            return None
        
    
    def obtener_datos_nota_entrega(self, id_nota_entrega: int) -> tuple:
        """
        Se obtienen los datos de la nota de entrega con estatus pendiente.

        Args:
            id_nota_entrega (int): Id de la nota de entrega.

        Returns:
            tuple: - Retorna los datos de la nota de entrega.
        """
        query = """
        SELECT id_cliente, fecha, subtotal, descuento, impuesto, total
        FROM NotasEntrega
        WHERE id_nota_entrega = ?"""
        
        params = id_nota_entrega
        datos_dicc = self.select(query, (params,))
        
        campos = [
            "id_cliente",
            "fecha",
            "subtotal",
            "descuento",
            "impuesto",
            "total"
        ]
        
        datos_tupla = [
            tuple(diccionario.get(campo) for campo in campos)
            for diccionario in datos_dicc
        ]
    
        return datos_tupla
    
    
    def obtener_ultimo_numero_factura(self) -> List[Tuple[Any]]:
        """
        Toma el Ultimo número de factura

        Returns:
            List[Tuple[Any]]: - Retorna una lista con la tupla del ultimo número de factura.
        """            
        query = "SELECT ultimo_numero_factura FROM Configuracion WHERE id_configuracion = 1"
        
        ultimo_numero = self.select(query)
        
        return ultimo_numero[0]["ultimo_numero_factura"]
    
    
    def actualizar_ultimo_numero_factura(self, nuevo_numero: int) -> int:
        """
        Inserta en DB el nuevo ultimo número de factura para mantener correlación 

        Args:
            nuevo_numero (int): Ultimo número de factura actualizado.

        Returns:
            int: - Retorna el id del ultimo nñumero si todo sale bien si no retorna -1
        """
        query = {
            "ultimo_numero_factura":nuevo_numero
        }
        actualizado = self.update(
            table="Configuracion",
            updates=query,
            where_condition="id_configuracion = ?",
            where_params=(1,)
        )

        if not actualizado:
            messagebox.showerror("⚠️ Error", f"No se ha podido actualizar el ultimo número de factura. La correlación ha fallado.")

    def insertar_factura_venta(self, id_venta:int, id_cliente:int, fecha:str, subtotal:float, descuento:float, impuesto:float, total:float, usuario_actual:str)-> int:
        """
        Se guarda los datos de la factura realizada por venta.

        Args:
            id_venta (int): Id de la venta.
            id_cliente (int): Id del cliente.
            fecha (str): Fecha de la venta.
            subtotal (float): Subtotal de la venta.
            descuento (float): Descuento si aplíca.
            impuesto (float): Tasa delimpuesto actual.
            total (float): Total de factura.
            usuario_actual (str): Usuario que realiza el proceso.

        Returns:
            int: - Retorna el id de la venta si se inserta correctamente si no retorna -1.
        """
        query = {
            "id_venta":id_venta,
            "fecha":fecha,
            "tipo_documento":"Factura",
            "id_cliente":id_cliente,
            "estado":"pendiente",
            "usuario_creador":usuario_actual,
            "subtotal":subtotal,
            "descuento":descuento,
            "impuesto":impuesto,
            "total":total,
        }
        id_de_venta = self.insert("Ventas", query)

        if not id_de_venta:
            messagebox.showerror("⚠️ Error Crítico", f"Fallo el registro de la venta en el sistema.")
            
        
    def obtener_detalles_nota_entrega(self, id_nota_entrega:int)-> List[Tuple[Any]]:
        """
        Obtener los datos de la nota de entrega.

        Args:
            id_nota_entrega (int): Id de la nota de entrega.

        Returns:
            List[Tuple[Any]]: - Retorna una lista de tuplas de los datos.
        """
        query = "SELECT id_producto, cantidad, precio_unitario, subtotal, descuento FROM DetalleNotaEntrega WHERE id_nota_entrega = ?"
        params = id_nota_entrega
        
        detalles_nota_dicc = self.select(query, (params,))
        
        campos = [
            "id_producto",
            "cantidad",
            "precio_unitario",
            "subtotal",
            "descuento"
        ]
        detalles_nota_tupla = [
            tuple(diccionario.get(campo) for campo in campos)
            for diccionario in detalles_nota_dicc
        ]
    
        return detalles_nota_tupla
    
    
    def insertar_detalle_venta(self, id_venta:int, id_producto:int, cantidad:int, precio_unitario:float, subtotal_detalle:float, descuento:float)->int:
        """
        Recibe los datos de una nota de entrega ya facturada y se guardan el detalle de venta.

        Args:
            id_venta (int): id de venta.
            id_producto (int): id del producto vendido.
            cantidad (int): Cantidad vendida.
            precio_unitario (float): Precio por unidad.
            subtotal_detalle (float): Subtotal de factura.
            descuento (float): Descuento en factura si aplíca.

        Returns:
            int: - Retorna el id de venta si el proceso es exitoso si no retorna -1.
        """
        query = {
            "id_venta":id_venta,
            "id_producto":id_producto,
            "cantidad":cantidad,
            "precio_unitario":precio_unitario,
            "subtotal":subtotal_detalle,
            "descuento":descuento
        }
        detalle_id = self.insert("Detalle_Venta", query)
        
        if not detalle_id:
            messagebox.showerror("⚠️ Error", f"No se pudo guardar el detalle de la venta.")
        else:
            return detalle_id
        
    
    def obtener_facturas_no_anuladas(self)-> List[Tuple[Any]]:
        """
        Recupera todas las facturas no anuladas.

        Returns:
            List[Tuple[Any]]: - Retorna una lista de tuplas.
        """
        # Posible error con el comparativo !=.
        query = """
            SELECT id_venta, fecha, nombre
            FROM ventas v
            JOIN clientes c ON v.id_cliente = c.id_cliente
            WHERE estado != 'Anulada'
        """
        facturas_anuladas_dicc = self.select(query)
        
        campos = [
            "id_venta",
            "fecha",
            "nombre"
        ]
        facturas_anuladas_tupla = [
            tuple(diccionario.get(campo) for campo in campos)
            for diccionario in facturas_anuladas_dicc
        ]
        
        if facturas_anuladas_tupla:
            return facturas_anuladas_tupla
        else: 
            messagebox.showerror("⚠️ Error", f"No se pudo cargas las facturas con estado Factura.")
            
    
    def guardar_gutschrift(self, id_factura_original:int, id_cliente:int, fecha:str, subtotal:float, descuento:float, impuesto:float, total:float, motivo:str)-> int:
        """
        Guardar la Gutschrift / Anulación en la base de datos

        Args:
            id_factura_original (int): Id de la Factura.
            id_cliente (int): Id del Cliente.
            fecha (str): Fecha de la Factura.
            subtotal (float): SubTotal de la Factura.
            descuento (float): Descuento de la factura si aplica.
            impuesto (float): Taza del impuesto actual.
            total (float): Total de la Factura.
            motivo (str): Motivo de la Anulación.

        Returns:
            int: - Retorna el id de la Anulación si la inserción es exitosa si no -1.
        """
        query = {
            "id_factura_original":id_factura_original,
            "id_cliente":id_cliente,
            "fecha":fecha,
            "subtotal":subtotal,
            "descuento":descuento,
            "impuesto":impuesto,
            "total":total,
            "motivo":motivo
        }
        
        id_de_anulacion = self.insert("Anulaciones", query)
        
        if id_de_anulacion:
            return id_de_anulacion
        else:
            messagebox.showerror("⚠️ Error", f"No se pudo Guardar la Anulación de Factura.")
    
    
    def marcar_factura_como_anulada(self, id_factura:int)-> bool:
        """
        Marcar una factura como anulada

        Args:
            id_factura (int): id de la Factura anulada.

        Returns:
            bool: - Retorna True si el estado es actualizado correctamenre si no retorna False.
        """
        
        actualizado = self.update(
            table="Ventas",
            updates={"estado":"Anulada"},
            where_condition="id_venta = ?",
            where_params=(id_factura,)
        )
        
        if actualizado:
            return actualizado
        else:
            messagebox.showerror("⚠️ Error", f"No se pudo Actualizar el estado de la factura anulada, aún esta Activa.")
    
    
    
    def datos_gutschrift(self, id_gutschrift:int)-> List[Tuple[Any]]:
        """
        Obtener datos de una Gutschrift

        Args:
            id_gutschrift (int): id de la Anulación.

        Returns:
            List[Tuple[Any]]: - Retorna lista de tuplas.
        """
        #print(f"ID GUTSCHRIFT ES: {id_gutschrift}")
        query = """
            SELECT
            g.id_gutschrift,
            g.id_factura_original,
            g.fecha,
            c.nombre,
            c.direccion,
            c.casa_num,
            c.zona_postal,
            c.identificacion_fiscal,
            c.email,
            c.telefono,
            g.total,
            t.nombre AS nombre_tienda,
            t.direccion AS direccion_tienda,
            t.identificacion_fiscal AS id_fiscal_tienda,
            t.telefono AS telefono_tienda,
            t.email AS email_t,
            g.descuento,
            g.subtotal,
            g.impuesto,
            g.motivo
        FROM Anulaciones g
        JOIN Clientes c ON g.id_cliente = c.id_cliente
        JOIN Tienda t ON t.id_tienda = 1 
        WHERE g.id_gutschrift = ?
        """
        datos_anulacio_dicc = self.select(query, (id_gutschrift,))
        
        campos = [
            "id_gutschrift",
            "id_factura_original",
            "fecha",
            "nombre",
            "direccion",
            "casa_num",
            "zona_postal",
            "identificacion_fiscal",
            "email",
            "telefono",
            "total",
            "nombre_tienda",
            "direccion_tienda",
            "id_fiscal_tienda",
            "telefono_tienda",
            "email_t",
            "descuento",
            "subtotal",
            "impuesto",
            "motivo"
        ]
        
        datos_anulacio_tupla = [
            tuple(diccionario.get(campo) for campo in campos)
            for diccionario in datos_anulacio_dicc
        ]
        #print(f"DATOS GUTSCHRIFT-> {datos_anulacio_tupla}")
        if datos_anulacio_tupla:
            return datos_anulacio_tupla[0]
        else:
            messagebox.showerror("⚠️ Error", f"No se pudo Cargar los datos de la Factura de anulación.")
            
    
    def id_producto_a_anular(self, id_venta:int)-> int:
        """
        selecciona id de venta para la anulacion de factura.

        Args:
            id_venta (int): id de la venta.

        Returns:
            int: Retorna el id de venta. 
        """
        query = "SELECT id_producto FROM Detalle_Venta WHERE id_venta = ?"
        params = id_venta
        
        id_produc = self.select(query, (params,))
        
        if id_produc:
            return id_produc[0]["id_producto"]
        else:
            return None
        
    
    def guardar_detalle_gutschrift(self, id_gutschrift:int, id_producto:int, cantidad:int, precio_unitario:float, subtotal:float)-> int:
        """
        Guarda los detalles de la anulación.

        Args:
            id_gutschrift (int): id de la anulación.
            id_producto (int): id del producto.
            cantidad (int): Cantida del producto.
            precio_unitario (float): Precio por unidad.
            subtotal (float): Sub total de factura anulada.

        Returns:
            int: - Retorna el id de la anulación si todo es exitoso si no -1.
        """
        query = {
            "id_gutschrift":id_gutschrift,
            "id_producto":id_producto,
            "cantidad":cantidad,
            "precio_unitario":precio_unitario,
            "subtotal":subtotal
        }
        id_anulacion = self.insert("Detalles_Anulaciones", query)
        
        if id_anulacion:
            return id_anulacion
        else: 
            messagebox.showerror("⚠️ Error", f"No se pudieron guardar los detalles de  la anulación.")
            
    
    def detalle_gutschrift(self, id_gutschrift:int)-> List[Tuple[Any]]:
        """
        Obtener detalles de una Gutschrift

        Args:
            id_gutschrift (int): id de la anulación.

        Returns:
            List[Tuple[Any]]: - Retorna una lista de tuplas.
        """
        query = """
            SELECT
            p.codigo,
            dg.cantidad,
            dg.precio_unitario,
            dg.subtotal
        FROM Detalles_Anulaciones dg
        JOIN Productos p ON dg.id_producto = p.id_producto
        WHERE dg.id_gutschrift = ?
        """
        detalles_anulacion_dicc = self.select(query, (id_gutschrift,))
        
        campos = [
            "codigo",
            "cantidad",
            "precio_unitario",
            "subtotal"
        ]
        
        detalles_anulacion_tupla = [
            tuple(diccionario.get(campo) for campo in campos)
            for diccionario in detalles_anulacion_dicc
        ]
        
        if detalles_anulacion_tupla:
            return detalles_anulacion_tupla
        else:
            messagebox.showerror("⚠️ Error", f"No se pudo Cargar los detalles de la Factura de anulación.")
    
    
    def actualizar_stock_producto_devolucion(self, id_producto:int, cantidad:int)-> bool:
        """
        Actualizar el stock al devolver productos

        Args:
            id_producto (int): Id del producto devuelto.
            cantidad (int): Cantidad del producto.

        Returns:
            bool: - Retorna True si la actualizacion es exitosa si no False.
        """
        #print(f"ID: {id_producto} -- Cantidad: {cantidad}")
        query = "SELECT codigo, cantidad FROM Productos WHERE id_producto = ?"
        params = id_producto
        cantidad_bd = self.select(query, (params,))
        #print(f"Resultado de SELECT: {cantidad_bd}")
        cantidad_actual = cantidad_bd[0]["cantidad"]
        
        actualizado = self.update(
            table="Productos",
            updates={"cantidad":cantidad_actual + cantidad},
            where_condition="id_producto = ?",
            where_params=(params,)
        )
        
        if actualizado:
            return True
        else:
            messagebox.showerror("⚠️ Error", f"No se pudo actualizar la cantidad del producto {cantidad_bd[0]["codigo"]}.")
            
    
    def obtener_estado_venta(self, id_venta:int)-> str:
        """
        Recuperar el estado actual de la Factura.

        Args:
            id_venta (int): Id de la Factura.

        Returns:
            str: - Retorna un str con el estado de la factura.
        """
        query = """
            SELECT estado
            FROM ventas
            WHERE id_venta = ?
        """
        params = id_venta
        estado_factura = self.select(query, (params,))
        
        if estado_factura:
            return estado_factura[0]["estado"]
        else:
            messagebox.showerror("⚠️ Error", f"No se pudo obtener el estado de la factura.")
            
    
    def datos_de_la_venta(self, id_venta:int)-> List[Tuple[Any]]:
        """
        Datos de la venta.

        Args:
            id_venta (int): Id de la venta facturada.

        Returns:
            List[Tuple[Any]]: - Retorna una lista con los datos de la venta.
        """
        query = """
            SELECT
                v.id_venta,
                v.fecha,
                c.id_cliente,
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
                t.telefono AS telf_tienda,
                t.email AS email_t,
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
        """
        params = id_venta
        datos_venta_dicc = self.select(query, (params,))
        
        campos = [
            "id_venta", # 0
            "fecha", # 1
            "id_cliente",  # 2
            "nombre",  # 3
            "direccion",  # 4
            "casa_num",  # 5
            "zona_postal",  # 6
            "identificacion_fiscal", # 7
            "email",  # 8
            "telefono",  # 9
            "total",  # 10
            "tipo_documento", # 11
            "tienda_nombre",  # 12
            "tienda_direccion",  # 13
            "tienda_identificacion_fiscal", # 14
            "telf_tienda",# 15
            "email_t",  # 16
            "descuento", # 17
            "subtotal",  # 18
            "impuesto"  # 19
        ]
        
        datos_venta_tupla = [
            tuple(diccionario.get(campo) for campo in campos)
            for diccionario in datos_venta_dicc
        ]
        #print(f"Datos para imprimir: {datos_venta_tupla[0]}")
        return datos_venta_tupla[0]
    
    
    def detalle_de_la_venta(self, id_venta:int) -> list[Tuple[Any]]:
        """
        Detalles de la venta

        Args:
            id_venta (int): Id de la venta.

        Returns:
            list[Tuple[Any]]: - Retorna una lista con tupla.
        """
        query = """
            SELECT p.codigo, dv.cantidad, dv.precio_unitario, dv.subtotal
            FROM Detalle_Venta dv
            JOIN Productos p ON dv.id_producto = p.id_producto
            WHERE dv.id_venta = ?
        """
        #print(f"Detalle de venta id: {id_venta}")
        params = id_venta
        
        detalle_venta_dicc = self.select(query, (params,))
        
        campos = [
            #"id_producto"
            "codigo",
            "cantidad",
            "precio_unitario",
            "subtotal"
        ] 
        
        detalle_venta_tupla = [
            tuple(diccionario.get(campo) for campo in campos)
            for diccionario in detalle_venta_dicc
            ]        
        #print(f"LOS DETALLES DE LA VENTA SON: {detalle_venta_tupla[0]}")
        return detalle_venta_tupla
    
    
    def obtener_nombre_cliente(self, id_cliente:int)-> List[Tuple[Any]]:
        """
        Obtener los datos del cliente para la anulación de la factura.

        Args:
            id_cliente (int): Id del cliente.

        Returns:
            List[Tuple[Any]: - Retorna Una lista de tupla.
        """
        query = "SELECT nombre, direccion, casa_num, zona_postal, email, telefono FROM Clientes WHERE id_cliente = ?"
        params = id_cliente
        
        cliente_dicc = self.select(query, (params,))
        #print(f"El cliente: {cliente_dicc}")
        #print(f"El cliente: {cliente_dicc[0]["nombre"]}")
        if cliente_dicc:
            return cliente_dicc
        else:
            messagebox.showerror("⚠️ Error", f"No se pudo obtener datos del cliente.")
            
    
    def datos_nota_entrega(self, id_nota_entrega:int)-> List[Tuple[Any]]:
        """
        Recupera los datos para crear un PDF con la nota de entrega.

        Args:
            id_nota_entrega (int): Id de la nota que se desea crear el PDF.

        Returns:
            List[Tuple[Any]]: - Retorna una lista con tupla.
        """
        query = """
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
                t.identificacion_fiscal AS tienda_identificacion_fiscal,
                t.telefono AS tienda_tlf,
                t.email AS email_t
            FROM
                NotasEntrega ne
            JOIN
                Clientes c ON ne.id_cliente = c.id_cliente
            CROSS JOIN
                Tienda t
            WHERE
                ne.id_nota_entrega = ?
        """
        params = id_nota_entrega
        nota_data_dicc = self.select(query, (params,))
        
        campos = [
            "id_nota_entrega",
            "fecha",
            "nombre",
            "direccion",
            "casa_num",
            "zona_postal",
            "identificacion_fiscal",
            "email",
            "telefono",
            "total",
            "subtotal",
            "descuento",
            "impuesto",
            "tienda_nombre",
            "tienda_direccion",
            "tienda_identificacion_fiscal",
            "tienda_tlf",
            "email_t"
        ]
        
        nota_data_tupla = [
            tuple(diccionario.get(campo) for campo in campos)
            for diccionario in nota_data_dicc
        ]
        
        if nota_data_tupla:
            return nota_data_tupla
        else:
            return False
    
    
    def detalle_nota_entrega(self, id_nota_entrega:int)-> List[Tuple[Any]]:
        """
        Obtiene la información necesaria para cargar al PDF que se generará.

        Args:
            id_nota_entrega (int): Id de la Nota de entrega para cargar los datos.

        Returns:
            List[Tuple[Any]]: - Retorna una lista con tupla.
        """
        query = """
            SELECT p.codigo, dne.cantidad, dne.precio_unitario, dne.subtotal
            FROM DetalleNotaEntrega dne
            JOIN Productos p ON dne.id_producto = p.id_producto
            WHERE dne.id_nota_entrega = ?
        """
        params = id_nota_entrega
        
        detalles_nota_dicc = self.select(query, (params,))
        #print(f"DETALLES TUPLA NOTA ENTREGA DICC: {detalles_nota_dicc}")
        campos = [
            "codigo",
            "cantidad",
            "precio_unitario",
            "subtotal"
        ]

        detalles_nota_tupla = [
            tuple(diccionario.get(campo) for campo in campos)
            for diccionario in detalles_nota_dicc
        ]
        #print(f"DETALLES TUPLA NOTA ENTREGA: {detalles_nota_tupla[0]}")
        if detalles_nota_tupla:
            return detalles_nota_tupla
        else:
            return False
    
    
    # Obtener el ultimo número de factura y crear el siguiente úmero de factura.
    def siguiente_numero_factura(self)-> bool:
        """
        Obterner el ultimo número de factura y actualizar el incremento.

        Returns:
            bool: - Retorna True si todo va bien, False si algo sale mal.
        """        
        query = "SELECT ultimo_numero_factura FROM Configuracion WHERE id_configuracion = 1"
        ultimo_en_db = self.select(query)
        ultimo_numero = ultimo_en_db[0]["ultimo_numero_factura"]
        nuevo_numero = ultimo_numero + 1
        id_venta_actualizado = self.update(
            table="Configuracion",
            updates={"ultimo_numero_factura": nuevo_numero},
            where_condition="id_configuracion = ?",
            where_params=(1,)
        )
        
        #print(f"EL SIGUIENTE ID DE VENTA ES: {id_venta_actualizado}")
        if id_venta_actualizado:
            return id_venta_actualizado
        else:
            return False
        
        
    def comprabar_estado_facturacion(self) -> bool:
        """
        Comprueba si no se ha facturado antes de generar la nota de entrega.
        Comprueba si una factura esta pendiente o fue anulada.

        Args:
            id_venta (int): Id de venta a comprobar.

        Returns:
            bool: Retorna True si ya se ha facturado False si no existe
        """
        
        query = "SELECT MAX(id_venta) AS ultimo_id FROM Ventas"
        #params = id_venta
        
        data_dicc = self.select(query)#, (params,))
        #print(f"El documento es: {data_dicc}")
        documento_id = data_dicc[0]["ultimo_id"] if data_dicc else None
        #estado_documento = data_dicc[0]["estado"] if data_dicc else None
        
        if documento_id: 
            return True        
        else:
            return False
            
#######################################################################################################################
########################################## SECCIÓN DE DATOS DE LA TIENDA ##############################################
#######################################################################################################################

    def guardar_info_tienda(self, tienda: str, direccion: str, id_fiscal: str, telefono: str, correo: str) -> bool:
        """
        Se Registra la información de la tienda por primera vez.

        Args:
            tienda (str): Nombre de la tienda.
            direccion (str): Dirección legal.
            id_fiscal (str): Id Fiscal si aplíca.
            telefono (str): Número telefoníco de la tienda.
            correo (str): Correo electroníco de la tienda.

        Returns:
            bool: - Si el registro es exitoso retorno True si no retorna False.
        """        
        query = {
            "nombre":tienda,
            "direccion":direccion,
            "identificacion_fiscal":id_fiscal,
            "telefono": telefono,
            "email":correo
        }
        id_tienda_ = self.insert("Tienda", query)
        
        if id_tienda_:
            return id_tienda_
        else:
            return id_tienda_
        
    
    def datos_registrados_tienda(self) -> List[Tuple[Any]]:
        """
        Recuperar la información de la tienda registrada.

        Returns:
            List[Tuple[Any]]: _description_
        """
        query =  "SELECT id_tienda, direccion, identificacion_fiscal, telefono, email FROM Tienda WHERE id_tienda = 1"
        
        datos_dicc = self.select(query)
        
        campos = [
            "id_tienda",
            "direccion",
            "identificacion_fiscal",
            "telefono",
            "email"
        ]
        
        datos_tupla = [
            tuple(diccionario.get(campo) for campo in campos)
            for diccionario in datos_dicc
        ]
        return datos_tupla
    
    
    def actualizar_datos_tienda(self, direccion: str, telefono: str, correo: str, id_tienda: str) -> bool:
        """
        Actualiza datos que pueden cambiar con el tiempo.

        Args:
            direccion (str): Nueva dirección.
            telefono (str): Nuevo Telefono.
            correo (str): Nuevo Correo electroníco.
            id_tienda (str): Id de la única tienda registrada.

        Returns:
            bool: - Retorna True si la actualización es exitosa False si algo sale mal.
        """        
        actualizado = self.update(
            table="Tienda",
            updates={"direccion":direccion, "telefono":telefono, "email":correo},
            where_condition="id_tienda = ?",
            where_params=(id_tienda,)
            )

        if actualizado:
            return  True
        else:
            return False
        

#######################################################################################################################
############################# SECCIÓN DE UMBRAL Y ALERTAS DE MATERIALES Y PRODUCTOS ###################################
#######################################################################################################################

    def obtener_umbrales_alertas(self)-> List[Tuple[Any]]:
        """
        Obtener Umbrales de Alertas.

        Returns:
            List[Tuple[Any]]: - Retorna una lista con tupla.
        """
        query = "SELECT tipo, id_item, umbral FROM UmbralesAlerta"
        
        umbrales_dicc = self.select(query)
        
        campos = [
            "tipo",
            "id_item",
            "umbral"
        ]
        umbrales_tupla = [
            tuple(diccionario.get(campo) for campo in campos)
            for diccionario in umbrales_dicc
        ]
        if umbrales_tupla:
            return umbrales_tupla
        else:
            return False
    
    
    def verificar_stock_bajo(self):
        umbrales = self.obtener_umbrales_alertas()
        
        alertas = []
        item = None
        
        for tipo, id_item, umbral in umbrales:
            #print(f"El Umbral es: {umbral}")
            if tipo == 'material':
                query = "SELECT nombre, tipo, tamaño, color, stock FROM Materiales WHERE id_material = ?"
                umbral_materiales = self.select(query, (id_item,))
                campos = [
                    "nombre", "tipo", "tamaño", "color", "stock"
                ]
                item = [
                    tuple(diccionario.get(campo) for campo in campos)
                    for diccionario in umbral_materiales
                ]
                
            elif tipo == 'producto':
                query = "SELECT codigo, tipo, cantidad FROM Productos WHERE id_producto = ?"
                umbral_productos = self.select(query, (id_item,))
                campos = [
                    "codigo", "tipo", "cantidad"
                ]
                item = [
                    tuple(diccionario.get(campo) for campo in campos)
                    for diccionario in umbral_productos
                ]

            # item = cursor.fetchone()
            if item:
                cantidad_actual = item[0][-1]  # La cantidad es el último elemento de la tupla
                if cantidad_actual <= umbral:
                    if tipo == 'material':
                        #print(f"El material es: {item[0]}")
                        nombre, tipo_material, tamaño, color, cantidad = item[0]
                        alertas.append({
                            'tipo': tipo,
                            'nombre': nombre,
                            'tipo_material': tipo_material,
                            'tamaño': tamaño,
                            'color': color,
                            'cantidad': cantidad
                        })
                    elif tipo == 'producto':
                        #print(f"El producto es: {item[0]}")
                        codigo, tipo_producto, cantidad = item[0]
                        alertas.append({
                            'tipo': tipo,
                            'codigo': codigo,
                            'tipo_producto': tipo_producto,
                            'cantidad': cantidad
                        })
        #print(alertas)
        return alertas
    
    
    
    def cargar_items(self, tipo:str)-> List[Tuple[Any]]:
        """
        Crear advetencias de stock para materiles y productos

        Args:
            tipo (str): Tipo de advertencia si es para materiales o productos.

        Returns:
            List[Tuple[Any]]: - Retorna una lista con tuplas.
        """
        tipo_dicc = None
        campos = []
        if tipo == 'material':
            query = "SELECT id_material, nombre, tipo, tamaño, color, stock FROM Materiales"
            tipo_dicc = self.select(query)
            campos = [
                "id_material", "nombre", "tipo", "tamaño", "color", "stock"
                ]
        elif tipo == 'producto':
            query = "SELECT id_producto, codigo, tipo, cantidad FROM Productos"
            tipo_dicc = self.select(query)
            campos = [
                "id_producto", "codigo", "tipo", "cantidad"
                ]
        #print(f"Los Campos son: {campos}")
        #print(f"El tipo_dicc es: {tipo_dicc}")  
        items = [
            tuple(diccionario.get(campo) for campo in campos)
            for diccionario in tipo_dicc
            ]
        #print(f"Los Items son: {items}")
        if items:
            return items
        else:
            return False
            
    
    def configurar_umbral_alerta(self, tipo:str, id_item:int, umbral:int)-> bool:
        """
        Configurar el umbral para las alertas.

        Args:
            tipo (str): Si es material o producto.
            id_item (int): id del item seleccionado.
            umbral (int): Umbral deseado para la alerta.

        Returns:
            bool: - Retorna True si todo va bien o False si no.
        """
        query_select = "SELECT id_umbral FROM UmbralesAlerta WHERE tipo = ? AND id_item = ?"
        
        # Verificar si ya existe un umbral para este item
        
        umbral_dicc = self.select(query_select, (tipo, id_item))
        #print(f"EL UMBRAL DICC ES: {umbral_dicc}")
        campos = ["id_umbral"]
        umbral_tupla = [tuple(diccionario.get(campo) for campo in campos)
                        for diccionario in umbral_dicc]  # -> int 15

        if umbral_tupla:
            # Actualizar el umbral existente
            actualiza_umbral = self.update(
                table="UmbralesAlerta",
                updates={"umbral":umbral},
                where_condition="WHERE id_umbral = ?",
                where_params=(umbral_tupla)
                )
            if actualiza_umbral:
                return True
            else:
                return False
        else:   
            # Insertar un nuevo umbral
            query = {
                "tipo":tipo,
                "id_item":id_item,
                "umbral":umbral
            }
            id_umbral_item = self.insert("UmbralesAlerta", query)
            
            if id_umbral_item:
                return id_umbral_item
            else:
                return False
            

#######################################################################################################################
########################################## PERSONALIZACIÓN DE LA SESIÓN ###############################################
#######################################################################################################################

    def configurar_perfil(self, usuario_actual:str)-> List[dict[Any]]:
        """
        Cargar la configuración guardada por el usuario.

        Args:
            usuario_actual (str): Nombre del Usuario.

        Returns:
            List[Dict[Any]]: Retorna un diccionario con los datos del usuario.
        """        
        pass

#######################################################################################################################
########################################## BORRADO COMPLETO DE BASE DE DATOS ##########################################
#######################################################################################################################

    # Borrado total de la base de datos
    def borrar_base_datos(self):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Desactivar las restricciones de claves foráneas
        cursor.execute("PRAGMA foreign_keys = OFF;")

        # Eliminar datos de las tablas en el orden correcto
        # Primero, elimina datos de tablas que tienen claves foráneas
        
        # cursor.execute("DELETE FROM Detalle_Venta;")
        # cursor.execute("DELETE FROM Ventas;")
        # cursor.execute("DELETE FROM DetalleNotaEntrega;")
        # cursor.execute("DELETE FROM NotasEntrega;")
        # cursor.execute("DELETE FROM Detalles_Anulaciones;")
        # cursor.execute("DELETE FROM Anulaciones;")
        # cursor.execute("DELETE FROM Clientes;")
        # cursor.execute("DELETE FROM Productos;")
        # cursor.execute("DELETE FROM Detalle_Producto;")
        # cursor.execute("DELETE FROM Historial_Costos;")
        # cursor.execute("DELETE FROM Historial_Ganancias;")
        # cursor.execute("DELETE FROM Materiales;")
        # cursor.execute("DELETE FROM Proveedores;")
        # cursor.execute("DELETE FROM Detalle_Factura;")
        # cursor.execute("DELETE FROM Facturas;")
        # cursor.execute("DELETE FROM Configuracion;")
        # cursor.execute("DELETE FROM Empaques;")
        # cursor.execute("DELETE FROM KitEmpaque;")
        # cursor.execute("DELETE FROM Lote_Productos;")
        # cursor.execute("DELETE FROM Lotes;")
        # cursor.execute("DELETE FROM Tienda;")
        # cursor.execute("DELETE FROM UmbralesAlerta;")
        # cursor.execute("DELETE FROM Usuarios;")
        # cursor.execute("DELETE FROM productos_borrador;")
        # Añade aquí más tablas según sea necesario

        # Volver a activar las restricciones de claves foráneas
        cursor.execute("PRAGMA foreign_keys = ON;")

        conn.commit()
        conn.close()
        messagebox.showinfo("Información", " Base de datos borrada")



    def conversion_decimal(self, dato:str) -> float:
        """
        Realizar conversión de coma (,) a punto (.)

        Args:
            dato (str): Recibe una dato con coma y retorna un dato con punto.
        """
        
        dato_str = str(dato)
        conversion = dato_str.replace(",", ".")
        dato_float = float(conversion)
        
        return dato_float
        
    


if __name__ == "__main__":
    probar = DataBaseManager()
    #probar.borrar_base_datos()
    #probar.actualiza_stock_db(70,"EMP-1") #"Caja de carton 11x15", "Estuche de tela con Logo", "Tarjeta de instrucciones"])
    #probar.obtener_id_factura_por_numero(987654321)
    #probar.encontrar_facturas()
    #probar.mostrar_historial_costos_general("WINTER08")
    #probar.seleccion_empaque_por_codigo()
    #probar.codigo_existe_emp("EMP-1")
    #probar.selecion_kit_empaques()
    #probar.selecion_empaques()
    #probar.costo_embalaje(["KIT-1"])
    #probar.validar_stock_empaques(["KIT-2"])
    #probar.descontar_empaques(["KIT-2"])
    #probar.obtener_tamaños_por_material_color_tipo("P-AC", "Azul celeste", "Acrilicas")
    #probar.descripcion_kit_empaque(["KIT-1"])
    #probar.obtener_kits()
    #probar.obtener_detalles_kit("KIT-1")
    #probar.buscar_usuarios("Adm")
    #probar.obtener_nombres_usuarios()
    #probar.datos_costo_d_producto_actualizar()
    #probar.actualizar_costo_producto(2.50, 40)
    #probar.actualizar_precio_venta(10.25, 40)
    #probar.verificar_stock_suficiente(3, 1)
    #probar.nuevo_cliente("Joseline Sequera", "Drosselstr", "22", "73079 Suessen", "LT5248HJ4", "jjsequera@gmail.com", "018533333333")
    #probar.cargador_clientes()
    #probar.cargador_productos()
    #probar.detalle_producto_venta(3)
    #probar.guarda_venta_bd(20, 3, "2026-04-30", "factura", 110, 10, 19, 119)
    #probar.actualizar_stock_producto_venta(2, 40)
    #probar.obtener_lotes()
    #probar.eliminar_material_bd("NUEVO-2")
    #probar.obtener_materiales_pro()
    #probar.obtener_productos_del_lote_con_cantidades(3)
    #probar.obtener_productos_del_lote(3)
    #probar.obtener_ultimo_numero_factura()
    #probar.datos_de_la_venta(21)
    #probar.actualizar_stock_producto_devolucion(35, 1)
    #probar.obtener_nombre_cliente(5)
    #probar.siguiente_numero_factura()
    #probar.verificar_stock_bajo()
    #probar.cargar_items("material")
    #probar.actualizar_material("ESP-P-V", 20, 1.10, 0.05)
    #probar.actualizar_empaque("BT-2", 20, 8.5, 0.425)
    #probar.comprabar_estado_facturacion()
    #probar.eliminar_producto_bd("Probando_descontado_cm")
    probar.configuracion_usuario([{'fondo_pantalla': "ffffff"}, {'fondo_letra': None}, {'fondo_menu': None}, {'imag_fondo': None}])
