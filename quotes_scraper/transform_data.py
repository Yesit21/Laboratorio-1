#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ETAPA 3: TRANSFORMACIÓN DE DATOS

Este script limpia, normaliza y valida los datos extraídos:
- Elimina espacios innecesarios
- Convierte precios a valores numéricos
- Convierte calificaciones a números
- Normaliza nombres
- Identifica valores faltantes
- Elimina duplicados
- Estandariza nombres de columnas
- Valida tipos de datos
"""

import pandas as pd
import json
import re
from datetime import datetime


class DataTransformer:
    """Clase para transformar y limpiar datos extraídos"""
    
    def __init__(self, laptops_file='laptops_data.json', books_file='libreria_data.json'):
        """
        Inicializa el transformador
        
        Args:
            laptops_file: Archivo JSON con datos de laptops
            books_file: Archivo JSON con datos de libros
        """
        self.laptops_file = laptops_file
        self.books_file = books_file
        self.laptops_df = None
        self.books_df = None
        self.unified_df = None
        
        # Estadísticas de transformación
        self.stats = {
            'records_before': 0,
            'records_after': 0,
            'duplicates_removed': 0,
            'nulls_found': {},
            'data_types_converted': [],
            'columns_standardized': []
        }
    
    def load_data(self):
        """Carga los datos desde archivos JSON"""
        print("\n" + "="*60)
        print("CARGANDO DATOS")
        print("="*60 + "\n")
        
        try:
            # Cargar laptops
            with open(self.laptops_file, 'r', encoding='utf-8') as f:
                laptops_data = json.load(f)
            self.laptops_df = pd.DataFrame(laptops_data)
            print(f"✓ Cargados {len(self.laptops_df)} registros de laptops")
            
            # Cargar libros
            with open(self.books_file, 'r', encoding='utf-8') as f:
                books_data = json.load(f)
            self.books_df = pd.DataFrame(books_data)
            print(f"✓ Cargados {len(self.books_df)} registros de libros")
            
            self.stats['records_before'] = len(self.laptops_df) + len(self.books_df)
            print(f"\nTotal registros cargados: {self.stats['records_before']}")
            
        except Exception as e:
            print(f"✗ Error al cargar datos: {e}")
            raise
    
    def clean_text_fields(self, df):
        """Elimina espacios innecesarios en campos de texto"""
        text_columns = ['product_name', 'description', 'category', 'availability']
        
        for col in text_columns:
            if col in df.columns:
                # Eliminar espacios al inicio y final
                df[col] = df[col].str.strip()
                # Reemplazar múltiples espacios por uno solo
                df[col] = df[col].str.replace(r'\s+', ' ', regex=True)
        
        return df
    
    def normalize_prices(self, df):
        """Asegura que los precios sean numéricos"""
        if 'price' in df.columns:
            # Convertir a numérico, valores inválidos se vuelven NaN
            df['price'] = pd.to_numeric(df['price'], errors='coerce')
            
            # Eliminar precios negativos o cero
            df.loc[df['price'] <= 0, 'price'] = None
        
        return df
    
    def normalize_ratings(self, df):
        """Asegura que los ratings sean enteros entre 1-5"""
        if 'rating' in df.columns:
            # Convertir a entero
            df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
            
            # Validar rango 1-5
            df.loc[(df['rating'] < 1) | (df['rating'] > 5), 'rating'] = None
            
            # Convertir a entero
            df['rating'] = df['rating'].astype('Int64')  # Int64 permite NaN
        
        return df
    
    def normalize_product_names(self, df):
        """Normaliza nombres de productos"""
        if 'product_name' in df.columns:
            # Eliminar caracteres especiales innecesarios
            df['product_name'] = df['product_name'].str.replace(r'[^\w\s\-\.\,\(\)]', '', regex=True)
            
            # Eliminar puntos suspensivos
            df['product_name'] = df['product_name'].str.replace('...', '', regex=False)
        
        return df
    
    def identify_missing_values(self, df, name):
        """Identifica y reporta valores faltantes"""
        null_counts = df.isnull().sum()
        null_percentages = (null_counts / len(df) * 100).round(2)
        
        missing_info = {}
        for col, count in null_counts.items():
            if count > 0:
                missing_info[col] = {
                    'count': int(count),
                    'percentage': float(null_percentages[col])
                }
        
        if missing_info:
            self.stats['nulls_found'][name] = missing_info
            print(f"\n⚠ Valores faltantes en {name}:")
            for col, info in missing_info.items():
                print(f"  - {col}: {info['count']} ({info['percentage']}%)")
        else:
            print(f"\n✓ Sin valores faltantes en {name}")
        
        return df
    
    def remove_duplicates(self, df, name):
        """Elimina registros duplicados"""
        before = len(df)
        
        # Eliminar duplicados basados en product_url (identificador único)
        if 'product_url' in df.columns:
            df = df.drop_duplicates(subset=['product_url'], keep='first')
        else:
            df = df.drop_duplicates()
        
        after = len(df)
        removed = before - after
        
        if removed > 0:
            self.stats['duplicates_removed'] += removed
            print(f"\n✓ Eliminados {removed} duplicados en {name}")
        else:
            print(f"\n✓ Sin duplicados en {name}")
        
        return df
    
    def standardize_columns(self, df):
        """Estandariza nombres de columnas y orden"""
        # Orden estándar de columnas
        standard_order = [
            'source', 'product_name', 'price', 'currency', 'rating', 
            'review_count', 'description', 'category', 'availability',
            'product_url', 'image_url', 'scraped_at'
        ]
        
        # Reordenar columnas existentes
        existing_cols = [col for col in standard_order if col in df.columns]
        other_cols = [col for col in df.columns if col not in standard_order]
        
        df = df[existing_cols + other_cols]
        
        return df
    
    def validate_data_types(self, df):
        """Valida y convierte tipos de datos"""
        # Definir tipos esperados
        type_mapping = {
            'source': 'string',
            'product_name': 'string',
            'price': 'float64',
            'currency': 'string',
            'rating': 'Int64',
            'review_count': 'int64',
            'description': 'string',
            'category': 'string',
            'availability': 'string',
            'product_url': 'string',
            'image_url': 'string'
        }
        
        for col, dtype in type_mapping.items():
            if col in df.columns:
                try:
                    if dtype == 'string':
                        df[col] = df[col].astype('string')
                    elif dtype == 'float64':
                        df[col] = pd.to_numeric(df[col], errors='coerce')
                    elif dtype == 'Int64':
                        df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')
                    elif dtype == 'int64':
                        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype('int64')
                except Exception as e:
                    print(f"⚠ Error convirtiendo {col}: {e}")
        
        return df
    
    def transform_laptops(self):
        """Aplica transformaciones específicas a laptops"""
        print("\n" + "="*60)
        print("TRANSFORMANDO DATOS DE LAPTOPS")
        print("="*60)
        
        df = self.laptops_df.copy()
        
        # Limpiar campos de texto
        df = self.clean_text_fields(df)
        
        # Normalizar precios y ratings
        df = self.normalize_prices(df)
        df = self.normalize_ratings(df)
        
        # Normalizar nombres de productos
        df = self.normalize_product_names(df)
        
        # Identificar valores faltantes
        df = self.identify_missing_values(df, 'laptops')
        
        # Eliminar duplicados
        df = self.remove_duplicates(df, 'laptops')
        
        # Estandarizar columnas
        df = self.standardize_columns(df)
        
        # Validar tipos de datos
        df = self.validate_data_types(df)
        
        self.laptops_df = df
        print(f"\n✓ Transformación de laptops completada: {len(df)} registros")
    
    def transform_books(self):
        """Aplica transformaciones específicas a libros"""
        print("\n" + "="*60)
        print("TRANSFORMANDO DATOS DE LIBROS")
        print("="*60)
        
        df = self.books_df.copy()
        
        # Limpiar campos de texto
        df = self.clean_text_fields(df)
        
        # Normalizar precios y ratings
        df = self.normalize_prices(df)
        df = self.normalize_ratings(df)
        
        # Normalizar nombres de productos
        df = self.normalize_product_names(df)
        
        # Identificar valores faltantes
        df = self.identify_missing_values(df, 'books')
        
        # Eliminar duplicados
        df = self.remove_duplicates(df, 'books')
        
        # Estandarizar columnas
        df = self.standardize_columns(df)
        
        # Validar tipos de datos
        df = self.validate_data_types(df)
        
        self.books_df = df
        print(f"\n✓ Transformación de libros completada: {len(df)} registros")
    
    def create_unified_dataset(self):
        """Crea dataset unificado con datos limpios"""
        print("\n" + "="*60)
        print("CREANDO DATASET UNIFICADO")
        print("="*60)
        
        # Concatenar ambos dataframes
        self.unified_df = pd.concat([self.laptops_df, self.books_df], ignore_index=True)
        
        self.stats['records_after'] = len(self.unified_df)
        
        print(f"\n✓ Dataset unificado creado: {len(self.unified_df)} registros")
        print(f"\n--- Resumen por Fuente ---")
        print(self.unified_df['source'].value_counts())
    
    def save_transformed_data(self):
        """Guarda datos transformados"""
        print("\n" + "="*60)
        print("GUARDANDO DATOS TRANSFORMADOS")
        print("="*60)
        
        # Guardar datasets individuales
        self.laptops_df.to_csv('laptops_transformed.csv', index=False, encoding='utf-8')
        self.books_df.to_csv('books_transformed.csv', index=False, encoding='utf-8')
        
        # Guardar dataset unificado
        self.unified_df.to_csv('catalog_transformed.csv', index=False, encoding='utf-8')
        self.unified_df.to_json('catalog_transformed.json', orient='records', force_ascii=False, indent=2)
        
        print("\n✓ Archivos guardados:")
        print("  - laptops_transformed.csv")
        print("  - books_transformed.csv")
        print("  - catalog_transformed.csv")
        print("  - catalog_transformed.json")
    
    def show_statistics(self):
        """Muestra estadísticas de transformación"""
        print("\n" + "="*60)
        print("ESTADÍSTICAS DE TRANSFORMACIÓN")
        print("="*60)
        
        print(f"\nRegistros iniciales: {self.stats['records_before']}")
        print(f"Registros finales: {self.stats['records_after']}")
        print(f"Duplicados eliminados: {self.stats['duplicates_removed']}")
        
        if self.stats['nulls_found']:
            print("\n--- Valores Faltantes por Fuente ---")
            for source, nulls in self.stats['nulls_found'].items():
                print(f"\n{source.upper()}:")
                for col, info in nulls.items():
                    print(f"  - {col}: {info['count']} ({info['percentage']}%)")
        
        # Mostrar información del dataset final
        print("\n--- Información del Dataset Final ---")
        print(f"Total de productos: {len(self.unified_df)}")
        print(f"\nTipos de datos:")
        print(self.unified_df.dtypes)
        
        print(f"\n--- Estadísticas de Precios ---")
        print(f"Precio mínimo: ${self.unified_df['price'].min():.2f}")
        print(f"Precio máximo: ${self.unified_df['price'].max():.2f}")
        print(f"Precio promedio: ${self.unified_df['price'].mean():.2f}")
        print(f"Precio mediano: ${self.unified_df['price'].median():.2f}")
        
        print(f"\n--- Estadísticas de Ratings ---")
        print(f"Rating promedio: {self.unified_df['rating'].mean():.2f}")
        print(self.unified_df['rating'].value_counts().sort_index())
    
    def run_transformation(self):
        """Ejecuta el proceso completo de transformación"""
        print("\n" + "="*60)
        print("ETAPA 3: TRANSFORMACIÓN DE DATOS")
        print("="*60)
        
        # Cargar datos
        self.load_data()
        
        # Transformar datos
        self.transform_laptops()
        self.transform_books()
        
        # Crear dataset unificado
        self.create_unified_dataset()
        
        # Guardar datos transformados
        self.save_transformed_data()
        
        # Mostrar estadísticas
        self.show_statistics()
        
        print("\n" + "="*60)
        print("✓ TRANSFORMACIÓN COMPLETADA")
        print("="*60 + "\n")
        
        return self.unified_df


def main():
    """Función principal"""
    transformer = DataTransformer()
    unified_df = transformer.run_transformation()
    
    print("\n✓ Datos listos para carga en base de datos")


if __name__ == '__main__':
    main()
