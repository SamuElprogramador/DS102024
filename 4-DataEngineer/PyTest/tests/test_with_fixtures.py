import pytest
import pandas as pd

@pytest.fixture
def df_ventas(): 
    """Fixture que carga el dataset de ventas."""
    return pd.read_csv('../data/ventas_productos.csv')

def calcular_ingresos_por_categoria(df):
    """Calcula los ingresos totales por categoría de producto."""
    return df.groupby('categoria')['total'].sum().to_dict()

def test_calcular_ingresos_por_categoria(df_ventas):
    """Test que verifica el cálculo de ingresos por categoría."""
    # Calculamos los ingresos por categoría
    ingresos = calcular_ingresos_por_categoria(df_ventas)
    
    # Verificamos que todas las categorías esperadas estén presentes
    assert set(ingresos.keys()) == {'Electrónica', 'Accesorios', 'Almacenamiento', 'Componentes', 'Audio', 'Redes', 'Wearables'}
    
    # Verificamos que los ingresos sean números positivos
    for categoria, ingreso in ingresos.items():
        assert ingreso > 0, f"Los ingresos para {categoria} deberían ser positivos"
