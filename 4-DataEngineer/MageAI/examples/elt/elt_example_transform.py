# Ejemplo de Transformación de Datos (Transform) para ELT

En esta sección, crearemos un bloque de transformación que opera directamente sobre los datos ya cargados en la base de datos DuckDB, siguiendo el enfoque ELT.

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
    db_path = 'sales_data_elt.duckdb'
    
    # Conectar a la base de datos
    con = duckdb.connect(db_path)
    
    try:
        # Crear esquema para datos transformados si no existe
        con.execute("CREATE SCHEMA IF NOT EXISTS transformed")
        
        # 1. Crear tabla de dimensión de productos
        con.execute("""
            CREATE OR REPLACE TABLE transformed.dim_product AS
            SELECT DISTINCT
                product_id,
                product_name,
                category
            FROM raw.sales
        """)
        
        # 2. Crear tabla de dimensión de clientes
        con.execute("""
            CREATE OR REPLACE TABLE transformed.dim_customer AS
            SELECT DISTINCT
                customer_id,
                shipping_city,
                shipping_zip,
                shipping_country
            FROM raw.sales
        """)
        
        # 3. Crear tabla de dimensión de fechas
        con.execute("""
            CREATE OR REPLACE TABLE transformed.dim_date AS
            SELECT DISTINCT
                order_date,
                EXTRACT(YEAR FROM order_date::DATE) AS year,
                EXTRACT(MONTH FROM order_date::DATE) AS month,
                EXTRACT(DAY FROM order_date::DATE) AS day,
                EXTRACT(DOW FROM order_date::DATE) AS day_of_week
            FROM raw.sales
        """)
        
        # 4. Crear tabla de hechos de ventas
        con.execute("""
            CREATE OR REPLACE TABLE transformed.fact_sales AS
            SELECT
                id AS sale_id,
                customer_id,
                product_id,
                order_date,
                quantity,
                unit_price,
                discount,
                total_amount,
                payment_method,
                status,
                (unit_price * quantity) AS gross_amount,
                (unit_price * quantity * discount) AS discount_amount,
                (unit_price * quantity * (1 - discount)) AS net_amount
            FROM raw.sales
        """)
        
        # 5. Crear vista para análisis de ventas por categoría
        con.execute("""
            CREATE OR REPLACE VIEW transformed.sales_by_category AS
            SELECT
                p.category,
                SUM(f.quantity) AS total_quantity,
                SUM(f.total_amount) AS total_sales,
                COUNT(DISTINCT f.customer_id) AS customer_count,
                SUM(f.total_amount) / COUNT(DISTINCT f.customer_id) AS avg_sales_per_customer
            FROM transformed.fact_sales f
            JOIN transformed.dim_product p ON f.product_id = p.product_id
            GROUP BY p.category
        """)
        
        # 6. Crear vista para análisis de ventas por tiempo
        con.execute("""
            CREATE OR REPLACE VIEW transformed.sales_by_time AS
            SELECT
                d.year,
                d.month,
                SUM(f.total_amount) AS total_sales,
                COUNT(*) AS order_count,
                SUM(f.quantity) AS total_quantity
            FROM transformed.fact_sales f
            JOIN transformed.dim_date d ON f.order_date = d.order_date
            GROUP BY d.year, d.month
            ORDER BY d.year, d.month
        """)
        
        # Obtener una muestra de los datos transformados para verificación
        sales_by_category = con.execute("SELECT * FROM transformed.sales_by_category").fetchdf()
        sales_by_time = con.execute("SELECT * FROM transformed.sales_by_time").fetchdf()
        
        print("Transformaciones completadas exitosamente en la base de datos.")
        print("\nVentas por categoría:")
        print(sales_by_category)
        print("\nVentas por tiempo:")
        print(sales_by_time)
        
        # Devolver una muestra de los datos transformados
        return sales_by_category
        
    finally:
        # Cerrar la conexión
        con.close()

# Para probar la función en el entorno de Mage.ai
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
    transformed_data = transform_data_in_database()
    print("\nMuestra de datos transformados devueltos:")
    print(transformed_data)
```

Este bloque de código:
1. Importa las bibliotecas necesarias
2. Define una función decorada con `@data_loader` (aunque realiza transformaciones, usamos este decorador para devolver una muestra de los datos transformados)
3. Conecta a la base de datos DuckDB donde se cargaron los datos sin procesar
4. Realiza múltiples transformaciones directamente en la base de datos:
   - Crea tablas de dimensiones (productos, clientes, fechas)
   - Crea una tabla de hechos (ventas)
   - Crea vistas para análisis (ventas por categoría, ventas por tiempo)
5. Devuelve una muestra de los datos transformados para verificación
6. Incluye código para probar la función fuera del pipeline

**Nota importante sobre ELT vs ETL**: En un enfoque ELT, las transformaciones se realizan directamente en el sistema de destino (en este caso, DuckDB) después de cargar los datos sin procesar. Esto aprovecha la potencia de procesamiento del sistema de destino y permite realizar transformaciones más complejas utilizando SQL. En contraste, en ETL las transformaciones se realizarían antes de cargar los datos, típicamente en memoria o en un servidor intermedio.
