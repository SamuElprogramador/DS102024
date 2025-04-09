# Ejemplo de Extracción de Datos (Extract) para ELT

En esta sección, crearemos un bloque de extracción para obtener datos de ventas desde una API REST.

```python
import pandas as pd
import requests
import json

@data_loader
def extract_sales_data_for_elt() -> pd.DataFrame:
    """
    Extrae datos de ventas desde una API REST.
    
    En un enfoque ELT, nos interesa extraer todos los datos disponibles
    sin realizar transformaciones significativas, ya que estas se harán
    después de cargar los datos en el destino.
    
    Returns:
        pd.DataFrame: DataFrame con los datos de ventas sin procesar
    """
    # URL de la API (ejemplo)
    url = "https://api.mockaroo.com/api/89b3f8d0?count=100&key=ff7856d0"
    
    try:
        # Realizar la petición a la API
        response = requests.get(url)
        
        # Verificar si la petición fue exitosa
        if response.status_code == 200:
            # Convertir la respuesta JSON a un DataFrame
            data = response.json()
            return pd.DataFrame(data)
        else:
            # Si la API falla, usar datos de respaldo
            print(f"Error al obtener datos de la API: {response.status_code}")
            print("Usando datos de respaldo...")
            
            # Datos de respaldo (simulados)
            backup_data = {
                'id': range(1, 21),
                'order_date': pd.date_range(start='2023-01-01', periods=20).astype(str).tolist(),
                'customer_id': [f'CUST{i:03d}' for i in range(1, 21)],
                'product_id': [f'PROD{i:03d}' for i in range(101, 121)],
                'product_name': [f'Product {i}' for i in range(101, 121)],
                'category': ['Electronics', 'Clothing', 'Home', 'Books', 'Food'] * 4,
                'quantity': [i for i in range(1, 11)] * 2,
                'unit_price': [round(10 + i * 2.5, 2) for i in range(20)],
                'discount': [round(i * 0.01, 2) for i in range(20)],
                'total_amount': [round((10 + i * 2.5) * ((i % 10) + 1) * (1 - i * 0.01), 2) for i in range(20)],
                'payment_method': ['Credit Card', 'PayPal', 'Cash', 'Bank Transfer'] * 5,
                'shipping_address': [f'Address {i}' for i in range(1, 21)],
                'shipping_city': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'] * 4,
                'shipping_zip': [f'{10000 + i * 100}' for i in range(20)],
                'shipping_country': ['USA'] * 20,
                'status': ['Delivered', 'Shipped', 'Processing', 'Cancelled'] * 5
            }
            return pd.DataFrame(backup_data)
    
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        raise

# Para probar la función en el entorno de Mage.ai
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
    sales_df = extract_sales_data_for_elt()
    print(f"Datos extraídos: {sales_df.shape[0]} filas y {sales_df.shape[1]} columnas")
    print(sales_df.head())
```

Este bloque de código:
1. Importa las bibliotecas necesarias
2. Define una función decorada con `@data_loader`
3. Intenta obtener datos de una API REST
4. Proporciona datos de respaldo en caso de que la API falle
5. Devuelve los datos sin procesar como un DataFrame
6. Incluye código para probar la función fuera del pipeline

**Nota importante sobre ELT vs ETL**: En un enfoque ELT, la fase de extracción se centra en obtener todos los datos disponibles sin realizar transformaciones significativas, ya que estas se harán después de cargar los datos en el destino. Esto contrasta con ETL, donde podríamos realizar algunas transformaciones básicas durante la extracción.
