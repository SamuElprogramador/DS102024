# Ejemplo de Extracción de Datos (Extract)

En esta sección, crearemos un bloque de extracción para obtener datos de ventas desde un archivo CSV en línea.

```python
import pandas as pd
import io
import requests

@data_loader
def extract_sales_data() -> pd.DataFrame:
    """
    Extrae datos de ventas desde un archivo CSV en línea.
    
    Returns:
        pd.DataFrame: DataFrame con los datos de ventas
    """
    # URL del archivo CSV (ejemplo)
    url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/supermarket_sales.csv"
    
    # Descargar el archivo
    response = requests.get(url)
    
    # Verificar si la descarga fue exitosa
    if response.status_code == 200:
        # Leer el CSV en un DataFrame
        return pd.read_csv(io.StringIO(response.text))
    else:
        raise Exception(f"Error al descargar los datos: {response.status_code}")

# Para probar la función en el entorno de Mage.ai
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
    sales_df = extract_sales_data()
    print(f"Datos extraídos: {sales_df.shape[0]} filas y {sales_df.shape[1]} columnas")
    print(sales_df.head())
```

Este bloque de código:
1. Importa las bibliotecas necesarias
2. Define una función decorada con `@data_loader`
3. Descarga datos de ventas desde un archivo CSV en línea
4. Convierte los datos en un DataFrame de pandas
5. Incluye código para probar la función fuera del pipeline
