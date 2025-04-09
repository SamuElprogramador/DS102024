# Ejemplo de Carga de Datos (Load) para ELT

En esta sección, crearemos un bloque de carga para almacenar los datos sin procesar en una base de datos DuckDB, preparándolos para su posterior transformación.

```python
import pandas as pd
import duckdb
import os

@data_exporter
def load_raw_sales_data(df: pd.DataFrame) -> None:
    """
    Carga los datos sin procesar en una base de datos DuckDB.
    
    En un enfoque ELT, cargamos los datos tal como están, sin transformaciones
    significativas. Las transformaciones se realizarán posteriormente
    directamente en la base de datos.
    
    Args:
        df: DataFrame con los datos extraídos
    """
    # Definir la ruta de la base de datos
    db_path = 'sales_data_elt.duckdb'
    
    # Conectar a la base de datos (se creará si no existe)
    con = duckdb.connect(db_path)
    
    try:
        # Crear esquema para datos sin procesar si no existe
        con.execute("CREATE SCHEMA IF NOT EXISTS raw")
        
        # Crear tabla para datos sin procesar si no existe
        # Nota: En ELT, generalmente creamos una tabla que refleja exactamente la estructura de los datos de origen
        con.execute("""
            CREATE TABLE IF NOT EXISTS raw.sales AS
            SELECT * FROM df
            WHERE 1=0
        """)
        
        # Cargar los datos sin procesar en la tabla
        # En ELT, a menudo usamos un enfoque de "append" para mantener un historial de cargas
        con.execute("INSERT INTO raw.sales SELECT * FROM df")
        
        # Verificar que los datos se cargaron correctamente
        result = con.execute("SELECT COUNT(*) FROM raw.sales").fetchone()
        print(f"Se cargaron {result[0]} registros en la tabla 'raw.sales'")
        
        # Crear una vista de metadatos para seguimiento de cargas
        con.execute("""
            CREATE TABLE IF NOT EXISTS raw.load_metadata (
                load_id INTEGER,
                load_timestamp TIMESTAMP,
                record_count INTEGER,
                source_name VARCHAR
            )
        """)
        
        # Registrar esta carga en los metadatos
        next_load_id = con.execute("SELECT COALESCE(MAX(load_id), 0) + 1 FROM raw.load_metadata").fetchone()[0]
        con.execute(f"""
            INSERT INTO raw.load_metadata VALUES
            ({next_load_id}, CURRENT_TIMESTAMP, {len(df)}, 'sales_api')
        """)
        
        # Mostrar algunos datos para verificar
        sample = con.execute("SELECT * FROM raw.sales LIMIT 5").fetchdf()
        print("\nMuestra de datos cargados:")
        print(sample)
        
    finally:
        # Cerrar la conexión
        con.close()
    
    print(f"Datos sin procesar cargados exitosamente en {os.path.abspath(db_path)}")

# Para probar la función en el entorno de Mage.ai
if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter
    # Crear un DataFrame de ejemplo si no tenemos datos reales
    sample_data = {
        'id': range(1, 6),
        'order_date': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05'],
        'customer_id': ['CUST001', 'CUST002', 'CUST003', 'CUST004', 'CUST005'],
        'product_id': ['PROD101', 'PROD102', 'PROD103', 'PROD104', 'PROD105'],
        'product_name': ['Product 101', 'Product 102', 'Product 103', 'Product 104', 'Product 105'],
        'category': ['Electronics', 'Clothing', 'Home', 'Books', 'Food'],
        'quantity': [1, 2, 3, 4, 5],
        'unit_price': [12.5, 15.0, 17.5, 20.0, 22.5],
        'discount': [0.0, 0.01, 0.02, 0.03, 0.04],
        'total_amount': [12.5, 29.7, 51.45, 77.6, 108.0],
        'payment_method': ['Credit Card', 'PayPal', 'Cash', 'Bank Transfer', 'Credit Card'],
        'shipping_address': ['Address 1', 'Address 2', 'Address 3', 'Address 4', 'Address 5'],
        'shipping_city': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'],
        'shipping_zip': ['10100', '10200', '10300', '10400', '10500'],
        'shipping_country': ['USA', 'USA', 'USA', 'USA', 'USA'],
        'status': ['Delivered', 'Shipped', 'Processing', 'Cancelled', 'Delivered']
    }
    sample_df = pd.DataFrame(sample_data)
    load_raw_sales_data(sample_df)
```

Este bloque de código:
1. Importa las bibliotecas necesarias
2. Define una función decorada con `@data_exporter`
3. Conecta a una base de datos DuckDB
4. Crea un esquema y una tabla para datos sin procesar
5. Carga los datos sin procesar en la tabla
6. Registra metadatos sobre la carga
7. Verifica que los datos se cargaron correctamente
8. Incluye código para probar la función fuera del pipeline

**Nota importante sobre ELT vs ETL**: En un enfoque ELT, la fase de carga se centra en almacenar los datos tal como están, sin transformaciones significativas. Esto contrasta con ETL, donde los datos ya estarían transformados antes de la carga. En ELT, a menudo creamos un esquema "raw" o "stage" para los datos sin procesar, que luego serán transformados en el siguiente paso.
