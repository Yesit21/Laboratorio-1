# 📦 RESUMEN DEL PROYECTO - LABORATORIO ETL

## 🎯 Proyecto Completo Subido a GitHub

**Repositorio:** https://github.com/Yesit21/Laboratorio-1.git

---

## 📊 CONTENIDO DEL REPOSITORIO

### 📁 Código Fuente (7 archivos principales)

#### Scripts ETL:
1. ✅ `etl_pipeline.py` - Pipeline ETL completo (Extract + Transform + Load)
2. ✅ `transform_data.py` - Transformación y limpieza de datos
3. ✅ `database_schema.py` - Creación de esquema de base de datos
4. ✅ `sql_queries.py` - 8 consultas SQL analíticas

#### Spiders Scrapy:
5. ✅ `quotes_scraper/spiders/laptops_spider.py` - Extractor de laptops
6. ✅ `quotes_scraper/spiders/libreria.py` - Extractor de libros

#### Configuración Scrapy:
7. ✅ `quotes_scraper/items.py` - Definición de items
8. ✅ `quotes_scraper/pipelines.py` - Pipelines de procesamiento
9. ✅ `quotes_scraper/settings.py` - Configuración del proyecto
10. ✅ `scrapy.cfg` - Configuración de Scrapy

---

### 📄 Datos y Resultados (15 archivos)

#### Datos Transformados:
- ✅ `catalog_transformed.csv` (334 KB) - Catálogo unificado
- ✅ `catalog_transformed.json` (650 KB) - Formato JSON
- ✅ `laptops_transformed.csv` (36 KB) - 117 laptops
- ✅ `books_transformed.csv` (298 KB) - 1,000 libros

#### Base de Datos:
- ✅ `catalogo_productos.db` (516 KB) - Base de datos SQLite

#### Resultados de Consultas SQL (8 archivos CSV):
- ✅ `query_1_results.csv` - Productos con fuente
- ✅ `query_2_results.csv` - Información por categorías
- ✅ `query_3_results.csv` - Productos por tipo
- ✅ `query_4_results.csv` - Producto más costoso
- ✅ `query_5_results.csv` - Producto más económico
- ✅ `query_6_results.csv` - Precio promedio
- ✅ `query_7_results.csv` - Calificación promedio
- ✅ `query_8_results.csv` - Fuente con más productos

---

### 📚 Documentación (3 archivos)

1. ✅ `README.md` (raíz) - Documentación completa del proyecto
2. ✅ `quotes_scraper/README.md` - Documentación técnica
3. ✅ `DIAGRAMA_ER.md` - Diagrama entidad-relación detallado

---

## 📈 ESTADÍSTICAS DEL PROYECTO

### Datos Extraídos:
- **Total productos:** 1,117
  - Laptops: 117 (10.47%)
  - Libros: 1,000 (89.53%)

### Base de Datos:
- **Tablas:** 5 (normalizadas en 3FN)
- **Relaciones:** 4 (con PKs y FKs)
- **Índices:** 5 (optimización de consultas)
- **Tamaño:** 516 KB

### Archivos:
- **Total archivos:** 37
- **Código Python:** 10 archivos
- **Datos CSV/JSON:** 13 archivos
- **Documentación:** 3 archivos
- **Tamaño total:** ~2 MB

---

## 🔄 COMMITS REALIZADOS

```
Commit 1: 4985361
"Laboratorio ETL completo: Extract, Transform, Load con Scrapy y SQLite"
- 25 archivos nuevos
- 21,864 líneas insertadas
- Pipeline completo funcional

Commit 2: f439742
"Actualizar README con documentación completa del laboratorio ETL"
- README.md actualizado
- Documentación profesional
```

---

## ✅ ETAPAS COMPLETADAS

### ✅ ETAPA 1: Exploración de Fuentes
- Análisis de 2 sitios web
- Identificación de información común y específica
- Detección de problemas de calidad

### ✅ ETAPA 2: Extracción (Extract)
- Spider de laptops: 117 productos
- Spider de libros: 1,000 productos
- Paginación automática
- Exportación JSON y CSV

### ✅ ETAPA 3: Transformación (Transform)
- Limpieza de espacios
- Normalización de precios y calificaciones
- Eliminación de duplicados
- Estandarización de columnas
- Validación de tipos de datos

### ✅ ETAPA 4: Base de Datos (Load)
- Diseño normalizado (3FN)
- 5 tablas con relaciones
- 1,117 registros cargados
- 8 consultas SQL ejecutadas

---

## 🎓 TECNOLOGÍAS UTILIZADAS

- **Python 3.14**
- **Scrapy** - Framework de web scraping
- **Pandas** - Análisis y transformación de datos
- **SQLite3** - Base de datos relacional
- **Git** - Control de versiones

---

## 🌐 FUENTES DE DATOS

1. **Laptops**
   - URL: https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops
   - Productos: 117
   - Moneda: USD ($)

2. **Libros**
   - URL: https://books.toscrape.com/
   - Productos: 1,000
   - Moneda: GBP (£)

---

## 📊 RESULTADOS DE CONSULTAS SQL

1. **Productos con fuente:** 1,117 registros vinculados
2. **Categorías:** 1 categoría con 1,000 libros
3. **Distribución:** 89.53% libros, 10.47% laptops
4. **Más costoso:** Asus ROG Strix SCAR - $1,799.00
5. **Más económico:** An Abundance of Katherines - £10.00
6. **Precio promedio:** Laptops $909.39, Libros £35.07
7. **Calificación promedio:** Laptops 2.34/4, Libros 2.92/5
8. **Fuente líder:** Books to Scrape (1,000 productos)

---

## 🚀 CÓMO USAR EL PROYECTO

### Clonar el repositorio:
```bash
git clone https://github.com/Yesit21/Laboratorio-1.git
cd Laboratorio-1/quotes_scraper
```

### Instalar dependencias:
```bash
pip install scrapy pandas
```

### Ejecutar pipeline completo:
```bash
python etl_pipeline.py
```

### Ejecutar consultas SQL:
```bash
python sql_queries.py
```

---

## ✨ CARACTERÍSTICAS DESTACADAS

- ✅ Pipeline ETL automatizado de inicio a fin
- ✅ Manejo de múltiples fuentes de datos
- ✅ Transformación y limpieza robusta
- ✅ Base de datos normalizada (3FN)
- ✅ Integridad referencial con PKs/FKs
- ✅ Consultas SQL optimizadas
- ✅ Documentación completa
- ✅ Código limpio y modular

---

## 📝 ENTREGABLES COMPLETADOS

1. ✅ Código del desarrollo (10 archivos Python)
2. ✅ Diagrama ER de la base de datos (DIAGRAMA_ER.md)
3. ✅ Resultados de 8 consultas SQL (8 archivos CSV)
4. ✅ Base de datos funcional (catalogo_productos.db)
5. ✅ Documentación completa (README.md)

---

**Proyecto 100% completo y subido a GitHub** 🎉

**Repositorio:** https://github.com/Yesit21/Laboratorio-1.git
