"Base de datos nueva más organizada y matenible"
import sqlite3
import hashlib
from datetime import datetime
from tkinter import messagebox
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
            print(f"Error al conectar a la base de datos: {e}")
            
    
    def begin_transaction(self) -> bool:
        """Inicia una transacción."""
        
        if not self.connection:
            self.connect()
            
        try:
            if not self.in_transaction:
                self.connection.execute("BEGIN TRANSACTION")
                self.in_transaction = True
                print("Transacción iniciada.")
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
            print(f"Error al cerrar la base de datos: {e}")
            
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
        print(f"Los datos de la consulta son: {params}")  # imprime el usuario
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

            else:
                raise ValueError(f"Tipo de búsqueda no válido: {tipo_busqueda}")

            cursor.execute(query, params if 'params' in locals() else ())
            resultados = cursor.fetchall()

            # Obtener los nombres de las columnas
            columns = [column[0] for column in cursor.description]
            print(columns)
            # Convertir los resultados a una lista de diccionarios
            #return [dict(zip(columns, row)) for row in resultados]
            print(resultados) # duvuelve una lista de diccionarios con los valores
            return resultados

        except sqlite3.Error as e:
            print(f"Error al realizar la búsqueda: {e}")
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
        print(f"Tipo de búsqueda: {tipo_busqueda}")
        print(f"Nuevos valores: {nuevos_valores}")
        print(f"Valores originales: {valores_originales}")

        if not self.connection:
            self.connect()

        try:
            # --- Todos los Materiales ---
            if tipo_busqueda == "Todos los Materiales":
                codigo_original = valores_originales[0]  # Usar el código original para el WHERE
                print(f"Actualizando material con código original: {codigo_original}")

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
                    print("Actualización exitosa para 'Todos los Materiales'.")
                    return True
                else:
                    print("No se actualizó ningún registro para 'Todos los Materiales'.")
                    return False

            # --- Material Específico ---
            elif tipo_busqueda == "Material especifico":
                codigo_original = valores_originales[3]  # Índice correcto para el código original
                print(f"Actualizando material específico con código original: {codigo_original}")

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
                    print("Actualización exitosa para 'Material Específico'.")
                    return True
                else:
                    print("No se actualizó ningún registro para 'Material Específico'.")
                    return False

            # --- Código Específico ---
            elif tipo_busqueda == "Código especifico":
                codigo_nuevo = nuevos_valores.get("Código", valores_originales[3])
                id_material = self.obtener_codigo_por_id(codigo_nuevo)
                print(f"ID del material para código {codigo_nuevo}: {id_material}")

                if not id_material:
                    print("No se encontró el ID del material.")
                    return False

                resultado = self.update(
                    table="Materiales",
                    updates={"codigo": codigo_nuevo},
                    where_condition="id_material = ?",
                    where_params=(id_material,)
                )

                if resultado:
                    self.connection.commit()
                    print("Actualización exitosa para 'Código Específico'.")
                    return True
                else:
                    print("No se actualizó ningún registro para 'Código Específico'.")
                    return False

            # --- Proveedor Específico ---
            elif tipo_busqueda == "Proveedor especifico":
                proveedor_nuevo = nuevos_valores.get("Proveedor", valores_originales[0])
                id_proveedor = self.obtener_id_proveedor_por_nombre(proveedor_nuevo)
                print(f"ID del proveedor para {proveedor_nuevo}: {id_proveedor}")

                if not id_proveedor:
                    print("No se encontró el ID del proveedor.")
                    return False

                resultado = self.update(
                    table="Proveedores",
                    updates={"nombre": proveedor_nuevo},
                    where_condition="id_proveedor = ?",
                    where_params=(id_proveedor,)
                )

                if resultado:
                    self.connection.commit()
                    print("Actualización exitosa para 'Proveedor Específico'.")
                    return True
                else:
                    print("No se actualizó ningún registro para 'Proveedor Específico'.")
                    return False

            # --- Factura Proveedor ---
            elif tipo_busqueda == "Factura Proveedor":
                factura_nueva = nuevos_valores.get("Factura N°", valores_originales[1])
                fecha_nueva = nuevos_valores.get("Fecha", valores_originales[2])
                proveedor_original = valores_originales[0]

                id_proveedor = self.obtener_id_proveedor_por_nombre(proveedor_original)
                print(f"ID del proveedor para {proveedor_original}: {id_proveedor}")

                if not id_proveedor:
                    print("No se encontró el ID del proveedor.")
                    return False

                id_factura = self.obtener_id_factura_por_proveedor(id_proveedor, valores_originales[1])
                print(f"ID de la factura: {id_factura}")

                if not id_factura:
                    print("No se encontró el ID de la factura.")
                    return False

                resultado = self.update(
                    table="Facturas",
                    updates={"numero_factura": factura_nueva, "fecha": fecha_nueva},
                    where_condition="id_factura = ?",
                    where_params=(id_factura,)
                )

                if resultado:
                    self.connection.commit()
                    print("Actualización exitosa para 'Factura Proveedor'.")
                    return True
                else:
                    print("No se actualizó ningún registro para 'Factura Proveedor'.")
                    return False

            # --- Todos los Productos / Producto Específico ---
            elif tipo_busqueda in ["Todos los Productos", "Producto especifico"]:
                codigo_original = valores_originales[0]
                id_producto = self.obtener_id_producto_por_codigo(codigo_original)
                print(f"ID del producto para código {codigo_original}: {id_producto}")

                if not id_producto:
                    print("No se encontró el ID del producto.")
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
                    print("Actualización exitosa para 'Productos'.")
                    return True
                else:
                    print("No se actualizó ningún registro para 'Productos'.")
                    return False

            else:
                raise ValueError(f"Tipo de búsqueda no válido: {tipo_busqueda}")

        except Exception as e:
            print(f"Error al actualizar la base de datos: {e}")
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
        print("EL Código para obtener el idi es: ",codigo_producto)
        query = "SELECT id_producto FROM Productos WHERE codigo LIKE ?"
        resultado = self.select(query, (f"%{codigo_producto}%",), fetch_one=True)
        
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
            print(f"Error al registrar al usuario {e}")
            return False, f"Error al registrar al usuario {e}"
    
    
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
        print(f"DataBaseManager: {resultado}")
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
        print(f"La pregunta de seguridad se ve asi: {resultado}")
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
        print(f"Los argumentos para la respuesta son: {usuario}, y {respuesta}")
        
        resultado = self.select(query, (usuario,))
        
        if resultado is None:
            return False, "Usuario no registrado."
        print(f"Lo que llega de la consulta Generica: {resultado}")
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
        print(type(clave_str), clave_str)
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
            SELECT m.id_material, m.codigo, m.nombre, d.cantidad, m.stock
            FROM Materiales m
            JOIN Detalle_Producto d ON m.id_material = d.id_material
            WHERE d.id_producto = ?
        """
        print(f"DEBUG: id_producto recibido = {id_producto}")  # Verificar el valor de id_producto
        materiales = self.select(query, (id_producto,))
        return materiales
    
    
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
        print(f"DEBUG: materiales_requeridos = {materiales_requeridos}")
        print(f"DEBUG: cantidad_a_fabricar = {cantidad_a_fabricar}")

        try:
            for material in materiales_requeridos:
                id_material = material["id_material"]
                cantidad_requerida_por_producto = material["cantidad"]
                cantidad_total_a_descontar = cantidad_requerida_por_producto * cantidad_a_fabricar
                stock_actual = material["stock"]  # Usar el stock obtenido en la consulta inicial

                print(f"DEBUG: Descontando {cantidad_total_a_descontar} unidades del material {material['nombre']} (Stock actual: {stock_actual})")

                # Verificar que no se vaya a valores negativos
                if stock_actual < cantidad_total_a_descontar:
                    print(f"Error: No hay suficiente stock del material {material['nombre']}.")
                    return False

                nuevo_stock = stock_actual - cantidad_total_a_descontar

                # Actualizar el stock del material
                exito = self.update(
                    table="Materiales",
                    updates={"stock": nuevo_stock},
                    where_condition="id_material = ?",
                    where_params=(id_material,)
                )

                if not exito:
                    print(f"Error al actualizar el stock del material {material['nombre']}.")
                    return False

            return True  # Retornar True solo después de procesar todos los materiales

        except Exception as e:
            print(f"Error al descontar materiales: {e}")
            return False

        
    def incrementar_stock_producto(self, id_producto, cantidad) -> bool:
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
        # Obtener la cantidad actual del producto
        cantidad_actual = self.select(
            "SELECT cantidad FROM Productos WHERE id_producto = ?",
            (id_producto,),
            fetch_one=True
        )

        if cantidad_actual is None:
            return False

        nueva_cantidad = cantidad_actual["cantidad"] + cantidad

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
            
    def insertar_producto(self,codigo, nombre, tipo, costo_producto, precio_venta, materiales_usados, tiempo_fabricacion, cantidad, descripcion, empaque) -> int:
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
        fecha_registro = datetime.now().strftime("%Y-%m-%d %H:%M")
        producto_nuevo = {
            "codigo": codigo,
            "nombre": nombre,
            "tipo": tipo,
            "costo_producto": costo_producto,
            "precio_venta": precio_venta,
            "materiales_usados": materiales_usados,
            "tiempo_fabricacion": tiempo_fabricacion,
            "cantidad": cantidad,
            "fecha_registro": fecha_registro,
            "descripcion": descripcion,
            "empaques": empaque
        }
        
        id_nuevo_producto = self.insert("Productos", producto_nuevo)
        
        if id_nuevo_producto:
            return True
        else:
            messagebox.showerror("⚠️ Error", f"El Producto {codigo}, no se pudo guardar.")
            
            
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
            messagebox.showerror("⚠️ Error", f"No se pudieron cargar los borradores pendientes")
            
    
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
        fecha_finalizacion = datetime().strftime("%Y-%m-%d %H:%M")
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
        
    
    def insertar_detalle_producto(self, id_producto, id_material, cantidad, tipo, tamaño) -> int:
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
        
        query = {
            "id_producto": id_producto,
            "id_material": id_material,
            "cantidad": cantidad,
            "tipo_material": tipo,
            "tamaño_material": tamaño
        }
            
        id_detalle = self.insert("Detalle_Producto", query)
        
        if id_detalle:
            print(f"El id de la relación es: {id_detalle}")
        else:
            print(f"Algo salio mal No se guardo en Detalle_Producto")
            
    
    def obtener_materiales_pro(self) -> tuple:
        """
        Selecciona los materiales para la creación de un producto.

        Returns:
            tuple: - Retorna una Tupla con los materiales.
        """
        
        query = "SELECT * FROM Materiales"
        
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
        print(f"El Código que llega es: {codigo}")
        query = 'SELECT nombre, tipo, tamaño, color FROM Materiales WHERE codigo = ?'
        materiales = self.select(query, (codigo,))
        
        if not materiales:
            # Error al consultar la base de datos.
            print(f"No se encontraron materiales con el código: {codigo}")
            return "", "", "", ""
            
        print(materiales) 
        nombre = materiales[0]["nombre"]
        tipo = materiales[0]["tipo"]
        tamaño = materiales[0]["tamaño"]
        color = materiales[0]["color"]
        
        return nombre, tipo, tamaño, color
    
    
    def actualizar_material(self, codigo, stock, precio, costo_unit) -> bool:
        """
        Actualiza el stock del material y el costo.

        Returns:
            bool:
            - Retorna True para una operación exitosa
            - Retorna False si la operación no tuvo éxito.
        """
        query = "SELECT stock FROM Materiales WHERE codigo = ?"
        db_stock = self.select(query, (codigo,))
        en_stock = db_stock[0]["stock"]
        
        nuevo_stock = en_stock + stock
        
        actualizar = self.update(
            table= "Materiales",
            updates= {"stock": nuevo_stock, "precio": precio, "costo_unitario": costo_unit},
            where_condition= "codigo = ?",
            where_params= (codigo,)
        )
        
        if actualizar:
            return True, "Factura agregada exitosamente, stock actualizado."
        else:
            return False, "No se pudo completar la operación."
        
    
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
        
        resultados = [fila for fila in datos]
        print(resultados[0]["codigo"])
        return resultados[0]["codigo"]
            
            
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
        
    def insertar_material(self, codigo, nombre, tipo, tamaño, color, stock, precio, costo_unitario, id_proveedor) -> int:
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
            "stock": stock,
            "precio": precio,
            "costo_unitario": costo_unitario,
            "id_proveedor": id_proveedor
        }
        
        id_nuevo_materia = self.insert("Materiales", materiales)
        print(f"ID Asignado al insertar material: {id_nuevo_materia}")
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
        print(f"El stock del material es: {stock}")
        return stock if stock else 0
    
    
    def actualizar_stock_material(self, codigo, cantidad) -> bool:
        """
        Actualizar el stock del Material.

        Args:
            codigo (str): Código del material.
            cantidad (float): Cantidad del reajuste.

        Returns:
            bool: - True si es exitoso o False si no lo es.
        """
        
        query = "SELECT stock FROM Materiales WHERE codigo = ?"
        stock_material = self.select(query, (codigo,))
        
        en_stock = stock_material[0]["stock"]
        nuevo_stock = en_stock - cantidad
        
        material_actualizado = self.update(
            table= "Materiales",
            updates= {"stock": nuevo_stock},  # Esto guarda stock - 5
            where_condition= "codigo = ?",
            where_params= (codigo,)
        )
        
        if material_actualizado:
            messagebox.showinfo("Actualizado", "✅ Inventario de materiales actualizado.")
        else:
            print("Material no actualizado")
            
            
#######################################################################################################################
################################################## SECCIÓN DE EMBALAJES ###############################################
#######################################################################################################################

    def insertar_empaque(self, codigo, nombre, tamaño, cantidad, precio, costo_unitario) -> int:
        """Recibe la información de un material de empaque para insertarlo en la base de datos.

        Args:
            codigo (srt): Código unico.
            nombre (str): Nombre del empaque
            tama (str): descripción del tamaño.
            cantidad (int): Cantidad disponible para insertar.
            precio (float): El precio del embalaje.
            costo_unitario (float): Precio por unidad.

        Returns:
            int: _description_
        """
        query = {
            "codigo_emp": codigo,
            "nombre_emp": nombre,
            "tamaño_emp": tamaño,
            "stock_emp": cantidad,
            "precio_emp": precio,
            "costo_unitario_emp": costo_unitario
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
        print(tipos_de_empaques)
        
        return tipos_de_empaques
        
    def costo_embalaje(self, emp_list) -> List[Dict[str, Any]]:
        # Filtrar solo los empaques que no están vacíos
        empaques = [e for e in emp_list if e]

        if not empaques:  # Si no hay empaques, devolver lista vacía
            return []

        # Crear la consulta con IN
        placeholders = ", ".join(["?"] * len(empaques))  # Ej: "?, ?, ?"
        query = f"""
            SELECT stock_emp, costo_unitario_emp
            FROM Empaques
            WHERE nombre_emp IN ({placeholders})
        """

        datos = self.select(query, tuple(empaques))
        
        costos = [costo["costo_unitario_emp"] for costo in datos]
        print(costos)
        stock = [cantidad["stock_emp"] for cantidad in datos]
        print(stock)
        
        costos_sum = sum(costos)
        print(costos_sum)
        return costos
    
    
    def validar_stock_empaques(self, empaques) -> bool:
        """
        Valida que haya stock suficiente de los empaques seleccionados.

        Args:
            empaques (str): Empaques a verificar.

        Returns:
            bool: - Si haz existencia retorna True si no False.
        """
        
        for empaque in empaques:
            query = "SELECT stock_emp FROM Empaques WHERE nombre_emp = ?"
            resultado = self.select(query, (empaque,))
            if not resultado or resultado[0]["stock_emp"] < 1:
                return False, f"No hay suficiente stock del empaque {empaque}."
            
        return True, "Stock de empaques suficiente."
    

    def descontar_empaques(self, emp_list) -> bool:
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

        # Crear la consulta con IN
        placeholders = ", ".join(["?"] * len(empaques))  # Ej: "?, ?, ?"
        query = f"""
            SELECT stock_emp
            FROM Empaques
            WHERE nombre_emp IN ({placeholders})
        """
        stock_actual = self.select(query, tuple(empaques))
        cantidad = 1
        stock_db = [cant["stock_emp"] for cant in stock_actual]
        empaques_sin_stock = []
        for i, empaque in zip(stock_db, empaques):
            if i < 1:
                empaques_sin_stock.append(empaque)
                continue
            
            nuevo_stock = i - cantidad
            print(f"La resta es: {nuevo_stock}")
                
            self.update(
                table="Empaques",
                updates={"stock_emp": nuevo_stock},
                where_condition="nombre_emp = ?",
                where_params=(empaque,)  # Tupla con un solo elemento
            )
            print(f"Actualizado: {empaque}")
        
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
        print(f"Valor a actualizar: {nuevo_stock}-- código es: {codigo}")
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
        
        datos = self.select(query, (numero_factura,))
        
        retorna_datos = datos[0]["id_factura"]
        
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
            nombre = self.insert("Proveedores", factura)
            
            if datos:
                return nombre
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
            "stock": stock,
            "precio": precio,
            "costo_unitario": costo_unitario
        }
        
        id_detalle = self.insert("Detalle_Factura", factura)
        
        if id_detalle:
            return id_detalle
        else:
            messagebox.showerror("⚠️ Error", f"No se Ha podido Guardar el detalle de la Factura.")
        
    
if __name__ == "__main__":
    probar = DataBaseManager()
    #probar.actualiza_stock_db(70,"EMP-1") #"Caja de carton 11x15", "Estuche de tela con Logo", "Tarjeta de instrucciones"])
    #probar.obtener_id_factura_por_numero(987654321)
    probar.buscar_codigos_like("ALF")