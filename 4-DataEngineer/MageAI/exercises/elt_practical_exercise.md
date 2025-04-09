# Ejercicio Práctico: ELT con Mage.ai

Este ejercicio te permitirá aplicar los conceptos de ELT (Extract, Load, Transform) utilizando Mage.ai. Trabajarás con datos de comercio electrónico para crear un pipeline ELT completo.

## Objetivo

Crear un pipeline ELT que:
1. Extraiga datos de pedidos y productos desde archivos CSV
2. Cargue los datos sin procesar en una base de datos
3. Transforme los datos directamente en la base de datos para crear un modelo dimensional

## Datos

Utilizaremos archivos CSV simulando datos de un sistema de comercio electrónico:
- `orders.csv`: Información sobre pedidos
- `products.csv`: Información sobre productos
- `customers.csv`: Información sobre clientes

## Instrucciones

### Paso 1: Configuración

1. Asegúrate de tener Mage.ai ejecutándose en Docker
2. Crea un nuevo pipeline llamado "ecommerce_elt_exercise"
3. Selecciona "Standard (batch)" como tipo de pipeline

### Paso 2: Extracción (Extract)

Crea un bloque de tipo "Data loader" con el siguiente código base:

```python
import pandas as pd
import io
import requests

@data_loader
def extract_ecommerce_data() -> dict:
    """
    Extrae datos de comercio electrónico desde archivos CSV.
    
    Returns:
        dict: Diccionario con DataFrames para orders, products y customers
    """
    # URLs de los archivos CSV (ejemplo)
    # En un entorno real, estos podrían ser archivos locales o URLs reales
    
    # TODO: Implementa la lógica para cargar los datos desde archivos CSV
    # Puedes usar datos de ejemplo si no tienes acceso a archivos reales
    
    # Datos de ejemplo para orders
    orders_data = """
    order_id,customer_id,order_date,status,total_amount
    1001,5001,2023-01-15,completed,125.30
    1002,5002,2023-01-16,processing,75.50
    1003,5001,2023-01-20,completed,220.00
    1004,5003,2023-01-25,shipped,45.80
    1005,5002,2023-01-30,completed,150.20
    """
    
    # Datos de ejemplo para products
    products_data = """
    product_id,name,category,price,stock_quantity
    2001,Laptop,Electronics,899.99,45
    2002,Smartphone,Electronics,499.99,120
    2003,Headphones,Electronics,89.99,200
    2004,T-shirt,Clothing,19.99,500
    2005,Jeans,Clothing,49.99,300
    """
    
    # Datos de ejemplo para customers
    customers_data = """
    customer_id,name,email,registration_date,country
    5001,Juan Pérez,juan@example.com,2022-10-15,España
    5002,María García,maria@example.com,2022-11-20,México
    5003,Carlos López,carlos@example.com,2022-12-05,Argentina
    5004,Ana Martínez,ana@example.com,2023-01-10,Colombia
    5005,Roberto Sánchez,roberto@example.com,2023-01-12,Chile
    """
    
    # Cargar los datos en DataFrames
    orders_df = pd.read_csv(io.StringIO(orders_data))
    products_df = pd.read_csv(io.StringIO(products_data))
    customers_df = pd.read_csv(io.StringIO(customers_data))
    
    # Retornar un diccionario con los DataFrames
    return {
        'orders': orders_df,
        'products': products_df,
        'customers': customers_df
    }
```

**Tarea**: Completa la función para extraer datos de comercio electrónico. Puedes expandir los datos de ejemplo o implementar la carga desde archivos reales si los tienes disponibles.

### Paso 3: Carga (Load)

Crea un bloque de tipo "Data exporter" con el siguiente código base:

```python
import pandas as pd
import duckdb
import os

@data_exporter
def load_raw_ecommerce_data(data: dict) -> None:
    """
    Carga los datos sin procesar en una base de datos DuckDB.
    
    Args:
        data: Diccionario con DataFrames para orders, products y customers
    """
    # Definir la ruta de la base de datos
    db_path = 'ecommerce_data.duckdb'
    
    # TODO: Implementa la lógica para:
    # 1. Conectar a la base de datos DuckDB
    # 2. Crear un esquema 'raw' si no existe
    # 3. Crear tablas para orders, products y customers en el esquema 'raw'
    # 4. Cargar los datos sin procesar en las tablas
    # 5. Verificar que los datos se cargaron correctamente
    # 6. Cerrar la conexión
```

**Tarea**: Completa la función para cargar los datos sin procesar en una base de datos DuckDB, siguiendo el enfoque ELT donde los datos se cargan tal como están, sin transformaciones significativas.

### Paso 4: Transformación (Transform)

Crea un bloque de tipo "Data loader" (usamos este tipo porque queremos devolver datos) con el siguiente código base:

```python
import duckdb
import pandas as pd

@data_loader
def transform_data_in_database() -> pd.DataFrame:
    """
    Transforma los datos directamente en la base de datos DuckDB.
    
    En un enfoque ELT, las transformaciones se realizan después de cargar los datos,
    aprovechando la potencia de procesamiento del sistema de destino.
    
    Returns:
        pd.DataFrame: Muestra de los datos transformados para verificación
    """
    # Definir la ruta de la base de datos
    db_path = 'ecommerce_data.duckdb'
    
    # TODO: Implementa la lógica para:
    # 1. Conectar a la base de datos DuckDB
    # 2. Crear un esquema 'transformed' si no existe
    # 3. Implementar las siguientes transformaciones usando SQL:
    #    a. Crear una tabla de dimensión para productos (dim_product)
    #    b. Crear una tabla de dimensión para clientes (dim_customer)
    #    c. Crear una tabla de dimensión para fechas (dim_date)
    #    d. Crear una tabla de hechos para pedidos (fact_order)
    #    e. Crear vistas para análisis (ej. ventas por categoría, ventas por país)
    # 4. Devolver una muestra de los datos transformados para verificación
    # 5. Cerrar la conexión
```

**Tarea**: Completa la función para transformar los datos directamente en la base de datos DuckDB, siguiendo el enfoque ELT donde las transformaciones se realizan después de cargar los datos.

### Paso 5: Ejecución y Verificación

1. Ejecuta cada bloque en secuencia
2. Verifica que los datos se extraen correctamente
3. Comprueba que los datos se cargan correctamente en la base de datos
4. Confirma que las transformaciones se aplican según lo esperado

### Paso 6: Documentación

Documenta tu pipeline:
1. Añade comentarios explicativos en tu código
2. Crea un bloque de markdown en el pipeline explicando lo que hace cada bloque
3. Describe las diferencias clave entre este enfoque ELT y el enfoque ETL del ejercicio anterior
4. Explica las ventajas y desventajas del enfoque ELT para este caso específico

## Entrega

Cuando hayas completado el ejercicio, deberás entregar:
1. Capturas de pantalla del pipeline en Mage.ai
2. El código de cada bloque (extracción, carga, transformación)
3. Una breve explicación de tu enfoque y las decisiones que tomaste
4. Una comparación entre tu implementación ELT y la implementación ETL del ejercicio anterior

## Criterios de Evaluación

Tu solución será evaluada según:
1. Funcionalidad: ¿El pipeline extrae, carga y transforma los datos correctamente?
2. Calidad del código: ¿El código está bien estructurado, comentado y sigue buenas prácticas?
3. Transformaciones SQL: ¿Las transformaciones en la base de datos son efectivas y están bien implementadas?
4. Documentación: ¿Has documentado adecuadamente tu solución y las diferencias entre ETL y ELT?

¡Buena suerte!
