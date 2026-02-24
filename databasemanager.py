"Base de datos nueva más organizada y matenible"
import sqlite3
import hashlib
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
        
        
    def connect(self) ->None:
        """
        Establece la conexión a la base de datos.
        """
        try:
            self.connection = sqlite3.connect(self.db_name)
            print(f"Conección establecida con exito")
        except sqlite3.Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            
            
    def close(self) -> None:
        """
        Cierra la conexión a la base de datos.
        """
        try:
            self.connection.close()
            print(f"Base de datos cerrada correctamente.")
            return True
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

            # Convertir los resultados a una lista de diccionarios
            return [dict(zip(columns, row)) for row in resultados]

        except sqlite3.Error as e:
            print(f"Error al realizar la búsqueda: {e}")
            return []
        
    
    def update_search(self, tipo_busqueda: str, nuevos_valores: Dict[str, Any], valores_originales: List[Any]) -> bool:
        """
        Realiza una actualización en la base de datos según el tipo de búsqueda especificado.

        Args:
            tipo_busqueda (str): Tipo de búsqueda a realizar.
            nuevos_valores (Dict[str, Any]): Diccionario con los nuevos valores.
            valores_originales (List[Any]): Lista con los valores originales.

        Returns:
            bool: True si la actualización fue exitosa, False en caso contrario.
        """
        if not self.connection:
            self.connect()

        try:
            if tipo_busqueda == "Todos los Materiales":
                codigo = nuevos_valores.get("Código", valores_originales[0])
                return self.update(
                    table="Materiales",
                    updates={
                        "nombre": nuevos_valores.get("Nombre", valores_originales[1]),
                        "tipo": nuevos_valores.get("Tipo", valores_originales[2]),
                        "tamaño": nuevos_valores.get("Tamaño", valores_originales[3]),
                        "color": nuevos_valores.get("Color", valores_originales[4]),
                        "stock": nuevos_valores.get("Stock", valores_originales[5]),
                        "precio": nuevos_valores.get("Costo", valores_originales[6]),
                        "costo_unitario": nuevos_valores.get("Costo Unit.", valores_originales[7])
                    },
                    where_condition="codigo = ?",
                    where_params=(codigo,)
                )

            elif tipo_busqueda == "Material especifico":
                codigo = nuevos_valores.get("Código", valores_originales[3])
                return self.update(
                    table="Materiales",
                    updates={
                        "nombre": nuevos_valores.get("Nombre", valores_originales[4]),
                        "tipo": nuevos_valores.get("Tipo", valores_originales[5]),
                        "tamaño": nuevos_valores.get("Tamaño", valores_originales[7]),
                        "color": nuevos_valores.get("Color", valores_originales[7]),
                        "stock": nuevos_valores.get("Stock", valores_originales[8]),
                        "precio": nuevos_valores.get("Costo", valores_originales[9]),
                        "costo_unitario": nuevos_valores.get("Costo Unit.", valores_originales[10])
                    },
                    where_condition="codigo = ?",
                    where_params=(codigo,)
                )

            elif tipo_busqueda == "Código especifico":
                codigo = nuevos_valores.get("Código", valores_originales[3])
                id_material = self.obtener_codigo_por_id(codigo)
                if not id_material:
                    return False
                return self.update(
                    table="Materiales",
                    updates={"codigo": codigo},
                    where_condition="id_material = ?",
                    where_params=(id_material,)
                )

            elif tipo_busqueda == "Proveedor especifico":
                proveedor = nuevos_valores.get("Proveedor", valores_originales[0])
                id_proveedor = self.obtener_id_proveedor_por_nombre(proveedor)
                if not id_proveedor:
                    return False
                return self.update(
                    table="Proveedores",
                    updates={"nombre": proveedor},
                    where_condition="id_proveedor = ?",
                    where_params=(id_proveedor,)
                )

            elif tipo_busqueda == "Factura Proveedor":
                factura_n = nuevos_valores.get("Factura N°", valores_originales[1])
                fecha = nuevos_valores.get("Fecha", valores_originales[2])
                id_proveedor = self.obtener_id_proveedor_por_nombre(valores_originales[0])
                if not id_proveedor:
                    return False
                id_factura = self.obtener_id_factura_por_proveedor(id_proveedor, valores_originales[1])
                if not id_factura:
                    return False
                return self.update(
                    table="Facturas",
                    updates={"numero_factura": factura_n, "fecha": fecha},
                    where_condition="id_factura = ?",
                    where_params=(id_factura,)
                )

            elif tipo_busqueda in ["Todos los Productos", "Producto especifico"]:
                id_producto = self.obtener_id_producto_por_codigo(valores_originales[0])
                if not id_producto:
                    return False
                return self.update(
                    table="Productos",
                    updates={
                        "codigo": nuevos_valores.get("Código", valores_originales[0]),
                        "tipo": nuevos_valores.get("Tipo", valores_originales[1]),
                        "costo_producto": nuevos_valores.get("Costo Venta", valores_originales[2]),
                        "precio_venta": nuevos_valores.get("Precio Venta", valores_originales[3]),
                        "materiales_usados": nuevos_valores.get("Materiales Usados", valores_originales[4]),
                        "tiempo_fabricacion": nuevos_valores.get("Tiempo Fabricación", valores_originales[5]),
                        "cantidad": nuevos_valores.get("Cantidad", valores_originales[6]),
                        "fecha_registro": nuevos_valores.get("Fecha R", valores_originales[7]),
                        "descripcion": nuevos_valores.get("Descripción", valores_originales[8])
                    },
                    where_condition="id_producto = ?",
                    where_params=(id_producto,)
                )

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
    ############################################ SECCIÓN INCREMENTO DE PRODUCTOS ##########################################
    #######################################################################################################################

    
    def obtener_id_producto_por_codigo(self, codigo_unico) -> List[Dict[str, any]]:
        """
        Se obtiene el Id del producto que se quiere incrementar.

        Args:
            codigo_unico (str): 
            - ID del producto 

        Returns:
            List[Dict[str, any]]: 
            - Devuelve una lista de diccionarios
        """
        print(f"DEBUG Código del producto recibido: {codigo_unico}")
        query = "SELECT id_producto FROM Productos WHERE codigo = ?"
        
        resultado = self.select(query, (codigo_unico,))
        
        # Extraer el primer id_producto (asumiendo que hay solo uno)
        if resultado:
            id_producto = resultado[0]["id_producto"]
            print(f"DEBUG ID del producto obtenido: {id_producto}")
            return id_producto
        else:
            print("DEBUG: No se encontró ningún producto con ese código.")
            return None
    
    
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
    
    #######################################################################################################################
    ############################################ SECCIÓN INCREMENTO DE MATERIALES #########################################
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
    
    
    def obtener_materiales(self, codigo) -> List[dict[str, Any]]:
        """
        Se obtiene el nombre, tipo, tamaño, color del material por el código actual.

        Args:
            codigo (str): Código del Material

        Returns:
            List[dict[str, Any]]:
            - retorna un dict teniendo como clave el código actual y los valores antes mensionados
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
        print(f"suma inventeario {en_stock} + {stock} = {nuevo_stock}")
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
        

if __name__ == "__main__":
    probar = DataBaseManager()
    probar.obtener_materiales()