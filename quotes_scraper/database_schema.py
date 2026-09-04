#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ETAPA 4: DISEÑO Y CREACIÓN DE BASE DE DATOS

Este script diseña e implementa la base de datos relacional para almacenar
productos de diferentes fuentes (laptops y libros).

ESQUEMA DE BASE DE DATOS:
- fuentes: Información de las fuentes de datos
- categorias: Categorías de productos (para libros)
- productos: Información común de todos los productos
- tecnologia: Información específica de productos tecnológicos (laptops)
- libros: Información específica de libros
"""

import sqlite3
import pandas as pd
from datetime import datetime


class DatabaseManager:
    """Gestiona la base de datos del catálogo de productos"""
    
    def __init__(self, db_name='catalogo_productos.db'):
        """
        Inicializa el gestor de base de datos
        
        Args:
            db_name: Nombre del archivo de base de datos SQLite
        """
        self.db_name = db_name
        self.conn = None
        self.cursor = None
    
    def connect(self):
        """Establece conexión con la base de datos"""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            print(f"✓ Conectado a base de datos: {self.db_name}")
        except Exception as e:
            print(f"✗ Error al conectar a la base de datos: {e}")
            raise
    
    def close(self):
        """Cierra la conexión con la base de datos"""
        if self.conn:
            self.conn.commit()
            self.conn.close()
            print(f"✓ Conexión cerrada")
    
    def create_tables(self):
        """Crea las tablas de la base de datos"""
        print("\n" + "="*60)
        print("CREANDO ESTRUCTURA DE BASE DE DATOS")
        print("="*60 + "\n")
        
        # Tabla: fuentes
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS fuentes (
                id_fuente INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre VARCHAR(100) NOT NULL UNIQUE,
                url TEXT NOT NULL,
                tipo VARCHAR(50),
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✓ Tabla 'fuentes' creada")
        
        # Tabla: categorias
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS categorias (
                id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre VARCHAR(100) NOT NULL UNIQUE,
                descripcion TEXT,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✓ Tabla 'categorias' creada")
        
        # Tabla: productos (información común)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
                id_fuente INTEGER NOT NULL,
                tipo VARCHAR(20) NOT NULL CHECK(tipo IN ('laptop', 'libro')),
                nombre VARCHAR(255) NOT NULL,
                precio DECIMAL(10, 2),
                moneda VARCHAR(3),
                calificacion INTEGER CHECK(calificacion BETWEEN 1 AND 5),
                url TEXT,
                imagen_url TEXT,
                fecha_scraping TIMESTAMP,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (id_fuente) REFERENCES fuentes(id_fuente)
            )
        """)
        print("✓ Tabla 'productos' creada")
        
        # Tabla: tecnologia (específica para laptops)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tecnologia (
                id_tecnologia INTEGER PRIMARY KEY AUTOINCREMENT,
                id_producto INTEGER NOT NULL UNIQUE,
                descripcion TEXT,
                num_reviews INTEGER DEFAULT 0,
                disponibilidad VARCHAR(50),
                FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
                    ON DELETE CASCADE
            )
        """)
        print("✓ Tabla 'tecnologia' creada")
        
        # Tabla: libros (específica para libros)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS libros (
                id_libro INTEGER PRIMARY KEY AUTOINCREMENT,
                id_producto INTEGER NOT NULL UNIQUE,
                id_categoria INTEGER,
                disponibilidad VARCHAR(100),
                FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
                    ON DELETE CASCADE,
                FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria)
            )
        """)
        print("✓ Tabla 'libros' creada")
        
        self.conn.commit()
        print("\n✓ Estructura de base de datos creada exitosamente")
    
    def create_indexes(self):
        """Crea índices para mejorar el rendimiento"""
        print("\n" + "="*60)
        print("CREANDO ÍNDICES")
        print("="*60 + "\n")
        
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_productos_fuente ON productos(id_fuente)",
            "CREATE INDEX IF NOT EXISTS idx_productos_tipo ON productos(tipo)",
            "CREATE INDEX IF NOT EXISTS idx_productos_precio ON productos(precio)",
            "CREATE INDEX IF NOT EXISTS idx_productos_calificacion ON productos(calificacion)",
            "CREATE INDEX IF NOT EXISTS idx_libros_categoria ON libros(id_categoria)",
        ]
        
        for idx_sql in indexes:
            self.cursor.execute(idx_sql)
            print(f"✓ Índice creado")
        
        self.conn.commit()
        print("\n✓ Índices creados exitosamente")
    
    def insert_sources(self):
        """Inserta las fuentes de datos"""
        print("\n" + "="*60)
        print("INSERTANDO FUENTES DE DATOS")
        print("="*60 + "\n")
        
        sources = [
            ('WebScraper - Laptops', 'https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops', 'tecnologia'),
            ('Books to Scrape', 'https://books.toscrape.com/', 'libros')
        ]
        
        for nombre, url, tipo in sources:
            try:
                self.cursor.execute("""
                    INSERT OR IGNORE INTO fuentes (nombre, url, tipo)
                    VALUES (?, ?, ?)
                """, (nombre, url, tipo))
                print(f"✓ Fuente insertada: {nombre}")
            except Exception as e:
                print(f"✗ Error insertando fuente {nombre}: {e}")
        
        self.conn.commit()
    
    def load_data_from_csv(self, csv_file='catalog_transformed.csv'):
        """
        Carga datos transformados desde CSV a la base de datos
        
        Args:
            csv_file: Archivo CSV con datos transformados
        """
        print("\n" + "="*60)
        print("CARGANDO DATOS EN BASE DE DATOS")
        print("="*60 + "\n")
        
        try:
            # Leer CSV
            df = pd.read_csv(csv_file)
            print(f"✓ Leídos {len(df)} registros del archivo {csv_file}")
            
            # Obtener IDs de fuentes
            self.cursor.execute("SELECT id_fuente, nombre FROM fuentes")
            sources = {name: id_fuente for id_fuente, name in self.cursor.fetchall()}
            
            laptops_count = 0
            books_count = 0
            
            for _, row in df.iterrows():
                try:
                    # Determinar tipo y fuente
                    if row['source'] == 'laptops':
                        tipo = 'laptop'
                        id_fuente = sources.get('WebScraper - Laptops')
                    else:
                        tipo = 'libro'
                        id_fuente = sources.get('Books to Scrape')
                    
                    # Insertar producto
                    self.cursor.execute("""
                        INSERT INTO productos (
                            id_fuente, tipo, nombre, precio, moneda, 
                            calificacion, url, imagen_url, fecha_scraping
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        id_fuente,
                        tipo,
                        row['product_name'],
                        row['price'] if pd.notna(row['price']) else None,
                        row['currency'],
                        int(row['rating']) if pd.notna(row['rating']) else None,
                        row['product_url'],
                        row['image_url'],
                        row['scraped_at']
                    ))
                    
                    id_producto = self.cursor.lastrowid
                    
                    # Insertar información específica según tipo
                    if tipo == 'laptop':
                        self.cursor.execute("""
                            INSERT INTO tecnologia (
                                id_producto, descripcion, num_reviews, disponibilidad
                            ) VALUES (?, ?, ?, ?)
                        """, (
                            id_producto,
                            row['description'] if pd.notna(row['description']) else None,
                            int(row['review_count']) if pd.notna(row['review_count']) else 0,
                            row['availability'] if pd.notna(row['availability']) else None
                        ))
                        laptops_count += 1
                    
                    else:  # libro
                        # Insertar o obtener categoría
                        categoria = row['category'] if pd.notna(row['category']) else 'Sin categoría'
                        
                        self.cursor.execute("""
                            INSERT OR IGNORE INTO categorias (nombre)
                            VALUES (?)
                        """, (categoria,))
                        
                        self.cursor.execute("""
                            SELECT id_categoria FROM categorias WHERE nombre = ?
                        """, (categoria,))
                        id_categoria = self.cursor.fetchone()[0]
                        
                        self.cursor.execute("""
                            INSERT INTO libros (
                                id_producto, id_categoria, disponibilidad
                            ) VALUES (?, ?, ?)
                        """, (
                            id_producto,
                            id_categoria,
                            row['availability'] if pd.notna(row['availability']) else None
                        ))
                        books_count += 1
                
                except Exception as e:
                    print(f"✗ Error insertando producto {row.get('product_name', 'N/A')}: {e}")
                    continue
            
            self.conn.commit()
            
            print(f"\n✓ Datos cargados exitosamente:")
            print(f"  - {laptops_count} laptops")
            print(f"  - {books_count} libros")
            print(f"  - Total: {laptops_count + books_count} productos")
            
        except Exception as e:
            print(f"✗ Error cargando datos: {e}")
            self.conn.rollback()
            raise
    
    def get_table_counts(self):
        """Muestra el conteo de registros en cada tabla"""
        print("\n" + "="*60)
        print("RESUMEN DE LA BASE DE DATOS")
        print("="*60 + "\n")
        
        tables = ['fuentes', 'categorias', 'productos', 'tecnologia', 'libros']
        
        for table in tables:
            self.cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = self.cursor.fetchone()[0]
            print(f"  - {table}: {count} registros")
    
    def setup_database(self, csv_file='catalog_transformed.csv'):
        """Configura la base de datos completa"""
        print("\n" + "="*60)
        print("ETAPA 4: CREACIÓN DE BASE DE DATOS")
        print("="*60)
        
        try:
            # Conectar
            self.connect()
            
            # Crear tablas
            self.create_tables()
            
            # Crear índices
            self.create_indexes()
            
            # Insertar fuentes
            self.insert_sources()
            
            # Cargar datos
            self.load_data_from_csv(csv_file)
            
            # Mostrar resumen
            self.get_table_counts()
            
            print("\n" + "="*60)
            print("✓ BASE DE DATOS CREADA EXITOSAMENTE")
            print("="*60 + "\n")
            
        except Exception as e:
            print(f"\n✗ Error configurando base de datos: {e}")
            raise
        finally:
            self.close()


def main():
    """Función principal"""
    db = DatabaseManager()
    db.setup_database()


if __name__ == '__main__':
    main()
