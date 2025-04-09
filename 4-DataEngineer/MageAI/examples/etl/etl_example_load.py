# Ejemplo de Carga de Datos (Load)

En esta sección, crearemos un bloque de carga para almacenar los datos transformados en una base de datos DuckDB.

```python
import pandas as pd
import duckdb
import os

@data_exporter
def load_sales_data(df: pd.DataFrame) -> None:
    """
    Carga los datos transformados en una base de datos DuckDB.
    
    Args:
        df: DataFrame con los datos transformados
    """
    # Definir la ruta de la base de datos
    db_path = 'sales_data.duckdb'
    
    # Conectar a la base de datos (se creará si no existe)
    con = duckdb.connect(db_path)
    
    try:
        # Crear tabla si no existe
        con.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                invoice_id VARCHAR,
                date DATE,
                customer_type VARCHAR,
                gender VARCHAR,
                product_line VARCHAR,
                unit_price FLOAT,
                quantity INT,
                total FLOAT,
                year INT,
                month INT,
                day INT,
                day_of_week INT,
                profit_margin FLOAT,
                venta_categoria VARCHAR
            )
        """)
        
        # Cargar los datos en la tabla
        # Usamos replace para sobrescribir datos existentes
        con.execute("DELETE FROM sales")  # Limpiar datos existentes
        con.execute("INSERT INTO sales SELECT * FROM df")
        
        # Verificar que los datos se cargaron correctamente
        result = con.execute("SELECT COUNT(*) FROM sales").fetchone()
        print(f"Se cargaron {result[0]} registros en la tabla 'sales'")
        
        # Mostrar algunos datos para verificar
        sample = con.execute("SELECT * FROM sales LIMIT 5").fetchdf()
        print("\nMuestra de datos cargados:")
        print(sample)
        
    finally:
        # Cerrar la conexión
        con.close()
    
    print(f"Datos cargados exitosamente en {os.path.abspath(db_path)}")

# Para probar la función en el entorno de Mage.ai
if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter
    # Crear un DataFrame de ejemplo si no tenemos datos reales
    sample_data = {
        'invoice_id': ['101', '102', '103'],
        'date': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03']),
        'customer_type': ['Member', 'Normal', 'Member'],
        'gender': ['Male', 'Female', 'Male'],
        'product_line': ['Electronics', 'Clothing', 'Food'],
        'unit_price': [10.5, 20.3, 15.7],
        'quantity': [10, 5, 8],
        'total': [105, 101.5, 125.6],
        'year': [2023, 2023, 2023],
        'month': [1, 1, 1],
        'day': [1, 2, 3],
        'day_of_week': [5, 6, 0],
        'profit_margin': [0.05, 0.07, 0.06],
        'venta_categoria': ['mediana', 'mediana', 'mediana']
    }
    sample_df = pd.DataFrame(sample_data)
    load_sales_data(sample_df)
```

Este bloque de código:
1. Importa las bibliotecas necesarias
2. Define una función decorada con `@data_exporter`
3. Conecta a una base de datos DuckDB
4. Crea una tabla si no existe
5. Carga los datos transformados en la tabla
6. Verifica que los datos se cargaron correctamente
7. Incluye código para probar la función fuera del pipeline
