import pytest
import pandas as pd
import numpy as np
from utils import calcular_metricas_ventas, categorizar_productos_por_precio, calcular_tendencia_ventas

@pytest.fixture
def df_ventas_sample():
    """Fixture que crea un pequeño DataFrame de muestra para testing."""
    data = {
        'id': [1, 2, 3],
        'fecha': ['2023-01-05', '2023-01-10', '2023-01-15'],
        'producto': ['Laptop HP', 'Monitor Dell', 'Teclado Logitech'],
        'categoria': ['Electrónica', 'Electrónica', 'Accesorios'],
        'precio': [899.99, 249.99, 59.99],
        'cantidad': [1, 2, 3],
        'descuento': [0.05, 0.00, 0.10],
        'total': [854.99, 499.98, 161.97]
    }
    return pd.DataFrame(data)

def test_calcular_metricas_ventas(df_ventas_sample):
    """Test para la función de cálculo de métricas de ventas."""
    metricas = calcular_metricas_ventas(df_ventas_sample)
    
    # Verificamos que todas las métricas esperadas estén presentes
    assert set(metricas.keys()) == {'total_ventas', 'promedio_venta', 'total_productos_vendidos', 
                                    'precio_promedio', 'descuento_promedio', 'ahorro_total'}
    
    # Verificamos algunos cálculos específicos
    assert metricas['total_ventas'] == pytest.approx(1516.94, 0.01)
    assert metricas['total_productos_vendidos'] == 6
    assert metricas['precio_promedio'] == pytest.approx(403.32, 0.01)

def test_categorizar_productos_por_precio(df_ventas_sample):
    """Test para la función de categorización de productos por precio."""
    df_categorizado = categorizar_productos_por_precio(df_ventas_sample)
    
    # Verificamos que se haya añadido la columna de categoría de precio
    assert 'categoria_precio' in df_categorizado.columns
    
    # Verificamos que las categorías sean correctas
    assert df_categorizado.loc[0, 'categoria_precio'] == 'Lujo'  # Laptop HP: 899.99
    assert df_categorizado.loc[1, 'categoria_precio'] == 'Premium'  # Monitor Dell: 249.99
    assert df_categorizado.loc[2, 'categoria_precio'] == 'Estándar'  # Teclado Logitech: 59.99
    
    # Verificamos que el DataFrame original no se haya modificado
    assert 'categoria_precio' not in df_ventas_sample.columns

def test_calcular_tendencia_ventas(df_ventas_sample):
    """Test para la función de cálculo de tendencia de ventas."""
    tendencia = calcular_tendencia_ventas(df_ventas_sample)
    
    # Verificamos que el DataFrame tenga las columnas esperadas
    assert set(tendencia.columns) == {'mes', 'total', 'variacion_porcentual'}
    
    # Verificamos que solo haya un mes (ya que todas las fechas son de enero 2023)
    assert len(tendencia) == 1
    assert tendencia.iloc[0]['mes'] == '2023-01'
    assert tendencia.iloc[0]['total'] == pytest.approx(1516.94, 0.01)
    assert np.isnan(tendencia.iloc[0]['variacion_porcentual'])  # No hay mes anterior para comparar
