import pandas as pd
import numpy as np

def calcular_metricas_ventas(df):
    """Calcula métricas de ventas a partir de un DataFrame de ventas.
    
    Args:
        df: DataFrame con columnas 'precio', 'cantidad', 'descuento' y 'total'
        
    Returns:
        dict: Diccionario con métricas calculadas
    """
    metricas = {
        'total_ventas': df['total'].sum(),
        'promedio_venta': df['total'].mean(),
        'total_productos_vendidos': df['cantidad'].sum(),
        'precio_promedio': df['precio'].mean(),
        'descuento_promedio': df['descuento'].mean(),
        'ahorro_total': (df['precio'] * df['cantidad'] * df['descuento']).sum()
    }
    return metricas

def categorizar_productos_por_precio(df):
    """Categoriza productos según su precio.
    
    Args:
        df: DataFrame con columna 'precio'
        
    Returns:
        DataFrame: DataFrame original con columna 'categoria_precio' añadida
    """
    df = df.copy()  # Evitamos modificar el DataFrame original
    
    # Definimos las categorías de precio
    condiciones = [
        (df['precio'] < 50),
        (df['precio'] >= 50) & (df['precio'] < 100),
        (df['precio'] >= 100) & (df['precio'] < 200),
        (df['precio'] >= 200)
    ]
    categorias = ['Económico', 'Estándar', 'Premium', 'Lujo']
    
    # Creamos la nueva columna
    df['categoria_precio'] = np.select(condiciones, categorias, default='Sin categoría')
    
    return df

def calcular_tendencia_ventas(df):
    """Calcula la tendencia de ventas por mes.
    
    Args:
        df: DataFrame con columnas 'fecha' y 'total'
        
    Returns:
        DataFrame: DataFrame con ventas totales por mes y variación porcentual
    """
    # Convertimos la columna fecha a datetime
    df = df.copy()
    df['fecha'] = pd.to_datetime(df['fecha'])
    
    # Extraemos el mes y agrupamos
    df['mes'] = df['fecha'].dt.to_period('M')
    ventas_mensuales = df.groupby('mes')['total'].sum().reset_index()
    ventas_mensuales['mes'] = ventas_mensuales['mes'].astype(str)
    
    # Calculamos la variación porcentual
    ventas_mensuales['variacion_porcentual'] = ventas_mensuales['total'].pct_change() * 100
    
    return ventas_mensuales
