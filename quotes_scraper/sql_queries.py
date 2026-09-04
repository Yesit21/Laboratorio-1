#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CONSULTAS SQL - ANÁLISIS DE DATOS

Este script ejecuta las 8 consultas SQL requeridas para analizar
los datos del catálogo de productos.

Consultas:
1. Mostrar el producto junto con la fuente
2. Mostrar información relacionada con categorías
3. ¿Cuántos productos existen de cada tipo?
4. ¿Cuál es el producto más costoso?
5. ¿Cuál es el producto más económico?
6. ¿Cuál es el precio promedio?
7. ¿Cuál es la calificación promedio?
8. ¿Qué fuente proporciona más productos?
"""

import sqlite3
import pandas as pd
from datetime import datetime


class SQLQueryExecutor:
    """Ejecuta y muestra consultas SQL sobre la base de datos"""
    
    def __init__(self, db_name='catalogo_productos.db'):
        """
        Inicializa el ejecutor de consultas
        
        Args:
            db_name: Nombre del archivo de base de datos
        """
        self.db_name = db_name
        self.conn = None
        self.results = {}
    
    def connect(self):
        """Conecta a la base de datos"""
        try:
            self.conn = sqlite3.connect(self.db_name)
            print(f"✓ Conectado a base de datos: {self.db_name}\n")
        except Exception as e:
            print(f"✗ Error al conectar: {e}")
            raise
    
    def close(self):
        """Cierra la conexión"""
        if self.conn:
            self.conn.close()
    
    def execute_query(self, query_num, title, sql, description=""):
        """
        Ejecuta una consulta SQL y guarda los resultados
        
        Args:
            query_num: Número de la consulta
            title: Título descriptivo
            sql: Consulta SQL
            description: Descripción adicional
        """
        print("="*70)
        print(f"CONSULTA {query_num}: {title}")
        print("="*70)
        
        if description:
            print(f"\n{description}\n")
        
        print("SQL:")
        print("-" * 70)
        print(sql)
        print("-" * 70)
        
        try:
            df = pd.read_sql_query(sql, self.conn)
            
            print(f"\nResultados ({len(df)} registros):\n")
            
            # Configurar pandas para mostrar mejor
            pd.set_option('display.max_columns', None)
            pd.set_option('display.width', None)
            pd.set_option('display.max_colwidth', 50)
            
            print(df.to_string(index=False))
            print("\n")
            
            # Guardar resultados
            self.results[query_num] = {
                'title': title,
                'sql': sql,
                'data': df,
                'description': description
            }
            
            return df
            
        except Exception as e:
            print(f"✗ Error ejecutando consulta: {e}\n")
            return None
    
    def query_1_products_with_source(self):
        """Consulta 1: Mostrar el producto junto con la fuente"""
        sql = """
            SELECT 
                p.id_producto,
                p.nombre AS producto,
                p.tipo,
                p.precio,
                p.moneda,
                p.calificacion,
                f.nombre AS fuente,
                f.url AS url_fuente
            FROM productos p
            INNER JOIN fuentes f ON p.id_fuente = f.id_fuente
            ORDER BY p.id_producto
            LIMIT 20;
        """
        
        self.execute_query(
            1,
            "Productos con su Fuente",
            sql,
            "Muestra cada producto junto con la información de su fuente de datos"
        )
    
    def query_2_categories_info(self):
        """Consulta 2: Mostrar información relacionada con categorías"""
        sql = """
            SELECT 
                c.nombre AS categoria,
                COUNT(l.id_libro) AS total_libros,
                ROUND(AVG(p.precio), 2) AS precio_promedio,
                ROUND(AVG(p.calificacion), 2) AS calificacion_promedio,
                MIN(p.precio) AS precio_min,
                MAX(p.precio) AS precio_max
            FROM categorias c
            LEFT JOIN libros l ON c.id_categoria = l.id_categoria
            LEFT JOIN productos p ON l.id_producto = p.id_producto
            GROUP BY c.id_categoria, c.nombre
            HAVING total_libros > 0
            ORDER BY total_libros DESC;
        """
        
        self.execute_query(
            2,
            "Información por Categorías",
            sql,
            "Muestra estadísticas de productos agrupados por categoría"
        )
    
    def query_3_count_by_type(self):
        """Consulta 3: ¿Cuántos productos existen de cada tipo?"""
        sql = """
            SELECT 
                tipo,
                COUNT(*) AS cantidad,
                ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM productos), 2) AS porcentaje
            FROM productos
            GROUP BY tipo
            ORDER BY cantidad DESC;
        """
        
        self.execute_query(
            3,
            "Cantidad de Productos por Tipo",
            sql,
            "Cuenta cuántos productos hay de cada tipo (laptop/libro)"
        )
    
    def query_4_most_expensive(self):
        """Consulta 4: ¿Cuál es el producto más costoso?"""
        sql = """
            SELECT 
                p.nombre AS producto,
                p.tipo,
                p.precio,
                p.moneda,
                p.calificacion,
                f.nombre AS fuente,
                CASE 
                    WHEN p.tipo = 'laptop' THEN t.descripcion
                    ELSE NULL
                END AS descripcion
            FROM productos p
            INNER JOIN fuentes f ON p.id_fuente = f.id_fuente
            LEFT JOIN tecnologia t ON p.id_producto = t.id_producto
            WHERE p.precio IS NOT NULL
            ORDER BY p.precio DESC
            LIMIT 5;
        """
        
        self.execute_query(
            4,
            "Productos Más Costosos",
            sql,
            "Muestra los 5 productos con el precio más alto"
        )
    
    def query_5_least_expensive(self):
        """Consulta 5: ¿Cuál es el producto más económico?"""
        sql = """
            SELECT 
                p.nombre AS producto,
                p.tipo,
                p.precio,
                p.moneda,
                p.calificacion,
                f.nombre AS fuente
            FROM productos p
            INNER JOIN fuentes f ON p.id_fuente = f.id_fuente
            WHERE p.precio IS NOT NULL
            ORDER BY p.precio ASC
            LIMIT 5;
        """
        
        self.execute_query(
            5,
            "Productos Más Económicos",
            sql,
            "Muestra los 5 productos con el precio más bajo"
        )
    
    def query_6_average_price(self):
        """Consulta 6: ¿Cuál es el precio promedio?"""
        sql = """
            SELECT 
                tipo,
                COUNT(*) AS total_productos,
                ROUND(AVG(precio), 2) AS precio_promedio,
                ROUND(MIN(precio), 2) AS precio_minimo,
                ROUND(MAX(precio), 2) AS precio_maximo,
                ROUND(
                    (MAX(precio) - MIN(precio)), 2
                ) AS rango_precios
            FROM productos
            WHERE precio IS NOT NULL
            GROUP BY tipo
            
            UNION ALL
            
            SELECT 
                'GENERAL' AS tipo,
                COUNT(*) AS total_productos,
                ROUND(AVG(precio), 2) AS precio_promedio,
                ROUND(MIN(precio), 2) AS precio_minimo,
                ROUND(MAX(precio), 2) AS precio_maximo,
                ROUND(
                    (MAX(precio) - MIN(precio)), 2
                ) AS rango_precios
            FROM productos
            WHERE precio IS NOT NULL;
        """
        
        self.execute_query(
            6,
            "Estadísticas de Precios",
            sql,
            "Calcula precio promedio, mínimo y máximo por tipo y general"
        )
    
    def query_7_average_rating(self):
        """Consulta 7: ¿Cuál es la calificación promedio?"""
        sql = """
            SELECT 
                tipo,
                COUNT(*) AS total_productos,
                ROUND(AVG(CAST(calificacion AS FLOAT)), 2) AS calificacion_promedia,
                MIN(calificacion) AS calificacion_minima,
                MAX(calificacion) AS calificacion_maxima,
                SUM(CASE WHEN calificacion = 5 THEN 1 ELSE 0 END) AS total_5_estrellas,
                SUM(CASE WHEN calificacion = 1 THEN 1 ELSE 0 END) AS total_1_estrella
            FROM productos
            WHERE calificacion IS NOT NULL
            GROUP BY tipo
            
            UNION ALL
            
            SELECT 
                'GENERAL' AS tipo,
                COUNT(*) AS total_productos,
                ROUND(AVG(CAST(calificacion AS FLOAT)), 2) AS calificacion_promedia,
                MIN(calificacion) AS calificacion_minima,
                MAX(calificacion) AS calificacion_maxima,
                SUM(CASE WHEN calificacion = 5 THEN 1 ELSE 0 END) AS total_5_estrellas,
                SUM(CASE WHEN calificacion = 1 THEN 1 ELSE 0 END) AS total_1_estrella
            FROM productos
            WHERE calificacion IS NOT NULL;
        """
        
        self.execute_query(
            7,
            "Estadísticas de Calificaciones",
            sql,
            "Calcula calificación promedio y distribución por tipo"
        )
    
    def query_8_source_with_most_products(self):
        """Consulta 8: ¿Qué fuente proporciona más productos?"""
        sql = """
            SELECT 
                f.nombre AS fuente,
                f.tipo AS tipo_fuente,
                f.url,
                COUNT(p.id_producto) AS total_productos,
                ROUND(COUNT(p.id_producto) * 100.0 / (SELECT COUNT(*) FROM productos), 2) AS porcentaje,
                SUM(CASE WHEN p.tipo = 'laptop' THEN 1 ELSE 0 END) AS laptops,
                SUM(CASE WHEN p.tipo = 'libro' THEN 1 ELSE 0 END) AS libros,
                ROUND(AVG(p.precio), 2) AS precio_promedio,
                ROUND(AVG(CAST(p.calificacion AS FLOAT)), 2) AS calificacion_promedia
            FROM fuentes f
            LEFT JOIN productos p ON f.id_fuente = p.id_fuente
            GROUP BY f.id_fuente, f.nombre, f.tipo, f.url
            ORDER BY total_productos DESC;
        """
        
        self.execute_query(
            8,
            "Fuentes con Más Productos",
            sql,
            "Muestra qué fuente proporciona más productos y sus estadísticas"
        )
    
    def run_all_queries(self):
        """Ejecuta todas las consultas SQL"""
        print("\n" + "="*70)
        print("EJECUTANDO CONSULTAS SQL")
        print("="*70)
        print(f"Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        try:
            self.connect()
            
            # Ejecutar todas las consultas
            self.query_1_products_with_source()
            self.query_2_categories_info()
            self.query_3_count_by_type()
            self.query_4_most_expensive()
            self.query_5_least_expensive()
            self.query_6_average_price()
            self.query_7_average_rating()
            self.query_8_source_with_most_products()
            
            print("="*70)
            print("✓ TODAS LAS CONSULTAS EJECUTADAS EXITOSAMENTE")
            print("="*70)
            print(f"\nTotal de consultas ejecutadas: {len(self.results)}")
            print("\nPara generar el reporte PDF, ejecute:")
            print("  python generate_report.py")
            print("\n")
            
        except Exception as e:
            print(f"✗ Error ejecutando consultas: {e}")
        finally:
            self.close()
        
        return self.results
    
    def export_results_to_csv(self):
        """Exporta los resultados a archivos CSV"""
        print("\nExportando resultados a CSV...")
        
        for query_num, result in self.results.items():
            filename = f"query_{query_num}_results.csv"
            result['data'].to_csv(filename, index=False, encoding='utf-8')
            print(f"  ✓ {filename}")
        
        print("\n✓ Resultados exportados\n")


def main():
    """Función principal"""
    executor = SQLQueryExecutor()
    results = executor.run_all_queries()
    executor.export_results_to_csv()


if __name__ == '__main__':
    main()
