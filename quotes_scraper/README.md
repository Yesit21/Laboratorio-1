# Laboratorio ETL - Extracción, Transformación y Almacenamiento de Datos

## Descripción
Pipeline ETL completo que extrae productos desde dos fuentes web (laptops y libros), transforma los datos y los almacena en una base de datos SQLite relacional.

## Fuentes de Datos
1. **Laptops:** https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops
2. **Libros:** https://books.toscrape.com/

## Estructura del Proyecto

```
quotes_scraper/
├── quotes_scraper/
│   ├── spiders/
│   │   ├── laptops_spider.py      # Spider para extraer laptops
│   │   └── libreria.py            # Spider para extraer libros
│   ├── items.py                   # Definición de items
│   ├── pipelines.py               # Pipelines de procesamiento
│   └── settings.py                # Configuración de Scrapy
├── etl_pipeline.py                # Pipeline ETL completo
├── transform_data.py              # Transformación de datos
├── database_schema.py             # Esquema de base de datos
├── sql_queries.py                 # 8 consultas SQL
├── DIAGRAMA_ER.md                 # Diagrama entidad-relación
├── catalogo_productos.db          # Base de datos SQLite
└── scrapy.cfg                     # Configuración de Scrapy
```

## Instalación

```bash
pip install scrapy pandas
```

## Ejecución

### Pipeline completo (Extract + Transform + Load):
```bash
python etl_pipeline.py
```

### Consultas SQL:
```bash
python sql_queries.py
```

## Resultados

- **Total productos:** 1,117 (117 laptops + 1,000 libros)
- **Base de datos:** 5 tablas normalizadas (3FN)
- **Consultas SQL:** 8 consultas ejecutadas con resultados en CSV

## Base de Datos

### Tablas:
1. **fuentes** (2 registros)
2. **categorias** (1 registro)
3. **productos** (1,117 registros)
4. **tecnologia** (117 registros)
5. **libros** (1,000 registros)

### Relaciones:
- FUENTES → PRODUCTOS (1:N)
- PRODUCTOS → TECNOLOGIA (1:1)
- PRODUCTOS → LIBROS (1:1)
- CATEGORIAS → LIBROS (1:N)

## Archivos Generados

### Datos transformados:
- `catalog_transformed.csv` - Catálogo unificado
- `catalog_transformed.json` - Catálogo en JSON

### Resultados de consultas:
- `query_1_results.csv` - Productos con fuente
- `query_2_results.csv` - Información por categorías
- `query_3_results.csv` - Productos por tipo
- `query_4_results.csv` - Producto más costoso
- `query_5_results.csv` - Producto más económico
- `query_6_results.csv` - Precio promedio
- `query_7_results.csv` - Calificación promedio
- `query_8_results.csv` - Fuente con más productos

## Tecnologías

- Python 3.14
- Scrapy
- Pandas
- SQLite3

## Autor

Laboratorio ETL - 2026
