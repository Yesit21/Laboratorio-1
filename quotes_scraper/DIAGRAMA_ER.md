# DIAGRAMA ENTIDAD-RELACIÓN

```
┌─────────────────────────┐
│       FUENTES           │
├─────────────────────────┤
│ PK  id_fuente          │
│     nombre (UNIQUE)     │
│     url                 │
│     tipo                │
│     fecha_creacion      │
└────────┬────────────────┘
         │
         │ 1:N
         │
         ▼
┌────────────────────────────────┐
│        PRODUCTOS               │
├────────────────────────────────┤
│ PK  id_producto               │
│ FK  id_fuente                 │
│     tipo (laptop/libro)       │
│     nombre                     │
│     precio                     │
│     moneda                     │
│     calificacion (1-5)        │
│     url                        │
│     imagen_url                 │
│     fecha_scraping             │
│     fecha_creacion             │
└────────┬───────────┬───────────┘
         │           │
    ┌────┘           └────┐
    │                     │
    │ 1:1                 │ 1:1
    ▼                     ▼
┌──────────────────┐  ┌──────────────────────┐
│   TECNOLOGIA     │  │       LIBROS         │
├──────────────────┤  ├──────────────────────┤
│ PK id_tecnologia │  │ PK  id_libro        │
│ FK id_producto   │  │ FK  id_producto     │
│    descripcion   │  │ FK  id_categoria    │
│    num_reviews   │  │     disponibilidad   │
│    disponibilidad│  └──────┬───────────────┘
└──────────────────┘         │
                             │ N:1
                             ▼
                    ┌─────────────────────┐
                    │    CATEGORIAS       │
                    ├─────────────────────┤
                    │ PK id_categoria    │
                    │    nombre (UNIQUE)  │
                    │    descripcion      │
                    │    fecha_creacion   │
                    └─────────────────────┘
```

## TABLAS

### FUENTES
| Campo          | Tipo        |
|----------------|-------------|
| id_fuente (PK) | INTEGER     |
| nombre         | VARCHAR(100)|
| url            | TEXT        |
| tipo           | VARCHAR(50) |
| fecha_creacion | TIMESTAMP   |

### PRODUCTOS
| Campo          | Tipo          |
|----------------|---------------|
| id_producto (PK)| INTEGER      |
| id_fuente (FK) | INTEGER       |
| tipo           | VARCHAR(20)   |
| nombre         | VARCHAR(255)  |
| precio         | DECIMAL(10,2) |
| moneda         | VARCHAR(3)    |
| calificacion   | INTEGER       |
| url            | TEXT          |
| imagen_url     | TEXT          |
| fecha_scraping | TIMESTAMP     |
| fecha_creacion | TIMESTAMP     |

### TECNOLOGIA
| Campo          | Tipo        |
|----------------|-------------|
| id_tecnologia (PK)| INTEGER  |
| id_producto (FK)| INTEGER    |
| descripcion    | TEXT        |
| num_reviews    | INTEGER     |
| disponibilidad | VARCHAR(50) |

### LIBROS
| Campo          | Tipo         |
|----------------|--------------|
| id_libro (PK)  | INTEGER      |
| id_producto (FK)| INTEGER     |
| id_categoria (FK)| INTEGER    |
| disponibilidad | VARCHAR(100) |

### CATEGORIAS
| Campo          | Tipo         |
|----------------|--------------|
| id_categoria (PK)| INTEGER    |
| nombre         | VARCHAR(100) |
| descripcion    | TEXT         |
| fecha_creacion | TIMESTAMP    |

## RELACIONES
- FUENTES → PRODUCTOS (1:N)
- PRODUCTOS → TECNOLOGIA (1:1)
- PRODUCTOS → LIBROS (1:1)
- CATEGORIAS → LIBROS (1:N)
