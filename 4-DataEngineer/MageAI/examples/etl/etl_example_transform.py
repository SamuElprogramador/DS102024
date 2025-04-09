# Ejemplo de Transformación de Datos (Transform)

En esta sección, crearemos un bloque de transformación para limpiar y enriquecer los datos de ventas extraídos.

```python
import pandas as pd
import numpy as np

@transformer
def transform_sales_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transforma los datos de ventas:
    1. Limpia nombres de columnas
    2. Convierte fechas
    3. Calcula métricas adicionales
    4. Filtra datos relevantes
    
    Args:
        df: DataFrame con los datos extraídos
        
    Returns:
        pd.DataFrame: DataFrame con los datos transformados
    """
    # Crear una copia para no modificar el original
    transformed_df = df.copy()
    
    # 1. Limpiar nombres de columnas (convertir a snake_case)
    transformed_df.columns = [col.lower().replace(' ', '_') for col in transformed_df.columns]
    
    # 2. Convertir columna de fecha a datetime
    if 'date' in transformed_df.columns:
        transformed_df['date'] = pd.to_datetime(transformed_df['date'])
        # Extraer componentes de fecha útiles
        transformed_df['year'] = transformed_df['date'].dt.year
        transformed_df['month'] = transformed_df['date'].dt.month
        transformed_df['day'] = transformed_df['date'].dt.day
        transformed_df['day_of_week'] = transformed_df['date'].dt.dayofweek
    
    # 3. Calcular métricas adicionales
    # Calcular margen de ganancia si tenemos las columnas necesarias
    if 'unit_price' in transformed_df.columns and 'cost_of_goods_sold' in transformed_df.columns:
        transformed_df['profit_margin'] = (transformed_df['unit_price'] - transformed_df['cost_of_goods_sold']) / transformed_df['unit_price']
    elif 'gross_income' in transformed_df.columns and 'total' in transformed_df.columns:
        # Alternativa si tenemos ingresos brutos y total
        transformed_df['profit_margin'] = transformed_df['gross_income'] / transformed_df['total']
    
    # 4. Categorizar ventas
    if 'total' in transformed_df.columns:
        bins = [0, 50, 100, 200, 500, float('inf')]
        labels = ['muy_pequeña', 'pequeña', 'mediana', 'grande', 'muy_grande']
        transformed_df['venta_categoria'] = pd.cut(transformed_df['total'], bins=bins, labels=labels)
    
    # 5. Eliminar filas con valores nulos en columnas críticas
    critical_columns = ['invoice_id', 'customer_type', 'total']
    critical_columns = [col for col in critical_columns if col in transformed_df.columns]
    transformed_df = transformed_df.dropna(subset=critical_columns)
    
    return transformed_df

# Para probar la función en el entorno de Mage.ai
if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
    # Crear un DataFrame de ejemplo si no tenemos datos reales
    sample_data = {
        'Invoice ID': ['101', '102', '103'],
        'Date': ['01/01/2023', '02/01/2023', '03/01/2023'],
        'Customer type': ['Member', 'Normal', 'Member'],
        'Unit price': [10.5, 20.3, 15.7],
        'Total': [105, 203, 157],
        'gross income': [5.25, 10.15, 7.85]
    }
    sample_df = pd.DataFrame(sample_data)
    transformed_df = transform_sales_data(sample_df)
    print("Datos transformados:")
    print(transformed_df.head())
```

Este bloque de código:
1. Importa las bibliotecas necesarias
2. Define una función decorada con `@transformer`
3. Realiza varias transformaciones en los datos:
   - Limpieza de nombres de columnas
   - Conversión de tipos de datos
   - Cálculo de métricas adicionales
   - Categorización de datos
   - Eliminación de valores nulos
4. Incluye código para probar la función fuera del pipeline
