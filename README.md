# Laboratorio ETL - Extracción, Transformación y Almacenamiento de Datos

Pipeline ETL completo desarrollado con Python y Scrapy que extrae información de productos desde dos fuentes web diferentes, transforma los datos, los almacena en una base de datos relacional SQLite y ejecuta consultas analíticas.

## 🎯 Objetivo

Desarrollar un proceso ETL que permita:
1. **Extraer** información de diferentes fuentes web
2. **Transformar** y limpiar los datos
3. **Almacenar** en una base de datos relacional normalizada
4. **Analizar** mediante consultas SQL

## 📊 Fuentes de Datos

### 1. Laptops (Tecnología)
- **URL:** https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops
- **Productos:** 117 laptops
- **Datos:** Nombre, precio ($), calificación, especificaciones técnicas, reviews

### 2. Libros (Literatura)
- **URL:** https://books.toscrape.com/
- **Productos:** 1,000 libros
- **Datos:** Título, precio (£), calificación, categoría, disponibilidad

## 🚀 Instalación

### Requisitos
- Python 3.10 o superior
- pip

### Dependencias
```bash
pip install scrapy pandas
```

## 📁 Estructura del Proyecto

```
quotes_scraper/
├── quotes_scraper/
│   ├── spiders/
│   │   ├── laptops_spider.py      # Extractor de laptops
│   │   └── libreria.py            # Extractor de libros
│   ├── items.py                   # Definición de items
│   ├── pipelines.py               # Pipelines de procesamiento
│   └── settings.py                # Configuración
├── etl_pipeline.py                # Pipeline ETL completo
├── transform_data.py              # Transformación de datos
├── database_schema.py             # Esquema de base de datos
├── sql_queries.py                 # 8 consultas SQL
├── DIAGRAMA_ER.md                 # Diagrama entidad-relación
├── catalogo_productos.db          # Base de datos SQLite
└── README.md
```

## 🔄 Ejecución

### Pipeline Completo (Extract + Transform + Load)
```bash
cd quotes_scraper
python etl_pipeline.py
```

### Consultas SQL
```bash
python sql_queries.py
```

### Spiders Individuales
```bash
# Extraer laptops
scrapy crawl laptops

# Extraer libros
scrapy crawl libreria
```

## 📈 Resultados

### Datos Extraídos
- **Total productos:** 1,117
  - Laptops: 117 (10.47%)
  - Libros: 1,000 (89.53%)

### Base de Datos
- **Archivo:** `catalogo_productos.db` (504 KB)
- **Tablas:** 5 (normalizadas en 3FN)
- **Registros totales:** 1,117 productos

### Estructura de la Base de Datos

```
FUENTES (2)
    ↓ (1:N)
PRODUCTOS (1,117)
    ↓ (1:1)          ↓ (1:1)
TECNOLOGIA (117)   LIBROS (1,000)
                       ↓ (N:1)
                   CATEGORIAS (1)
```

## 📊 Consultas SQL Implementadas

1. **Productos con su fuente** - 1,117 registros
2. **Información por categorías** - Análisis de categorías de libros
3. **Productos por tipo** - Distribución laptops/libros
4. **Producto más costoso** - Asus ROG Strix SCAR ($1,799)
5. **Producto más económico** - An Abundance of Katherines (£10.00)
6. **Precio promedio** - Laptops: $909.39, Libros: £35.07
7. **Calificación promedio** - Laptops: 2.34/4, Libros: 2.92/5
8. **Fuente con más productos** - Books to Scrape (1,000 productos)

## 📄 Archivos Generados

### Datos Transformados
- `catalog_transformed.csv` - Catálogo unificado
- `catalog_transformed.json` - Formato JSON
- `laptops_transformed.csv` - Laptops procesados
- `books_transformed.csv` - Libros procesados

### Resultados de Consultas
- `query_1_results.csv` hasta `query_8_results.csv`

## 🗄️ Esquema de Base de Datos

### FUENTES
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id_fuente (PK) | INTEGER | Identificador único |
| nombre | VARCHAR(100) | Nombre de la fuente |
| url | TEXT | URL de origen |

### PRODUCTOS
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id_producto (PK) | INTEGER | Identificador único |
| id_fuente (FK) | INTEGER | Referencia a fuentes |
| tipo | VARCHAR(20) | 'laptop' o 'libro' |
| nombre | VARCHAR(255) | Nombre del producto |
| precio | DECIMAL(10,2) | Precio |
| calificacion | INTEGER | Rating 1-5 |

### TECNOLOGIA (1:1 con productos tipo laptop)
- Descripción técnica
- Número de reviews
- Disponibilidad

### LIBROS (1:1 con productos tipo libro)
- Categoría
- Disponibilidad en stock

### CATEGORIAS
- Categorías de libros

## 🔍 Características

### Extracción (Extract)
- ✅ Web scraping con Scrapy
- ✅ Manejo de paginación automática
- ✅ Extracción de múltiples campos
- ✅ Gestión de errores

### Transformación (Transform)
- ✅ Limpieza de espacios innecesarios
- ✅ Conversión de precios a valores numéricos
- ✅ Normalización de calificaciones
- ✅ Estandarización de columnas
- ✅ Eliminación de duplicados
- ✅ Validación de tipos de datos

### Carga (Load)
- ✅ Base de datos SQLite
- ✅ Esquema normalizado (3FN)
- ✅ Relaciones con PKs y FKs
- ✅ Índices para optimización
- ✅ Integridad referencial

## 🛠️ Tecnologías

- **Python 3.14**
- **Scrapy** - Web scraping
- **Pandas** - Transformación de datos
- **SQLite3** - Base de datos relacional

## 📖 Documentación

Ver `DIAGRAMA_ER.md` para el diagrama completo de la base de datos con todas las relaciones y restricciones.

## 👤 Autor

Laboratorio ETL - 2026

## 📝 Licencia

Proyecto educativo - Laboratorio de Extracción, Transformación y Almacenamiento de Datos
