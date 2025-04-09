import pytest
import pandas as pd
import numpy as np
from utils import validar_completitud, validar_tipos_datos, validar_rango_valores

@pytest.fixture
def df_valido():
    """Fixture que crea un DataFrame válido para testing."""
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

@pytest.fixture
def df_con_nulos():
    """Fixture que crea un DataFrame con valores nulos."""
    data = {
        'id': [1, 2, 3],
        'fecha': ['2023-01-05', None, '2023-01-15'],
        'producto': ['Laptop HP', 'Monitor Dell', 'Teclado Logitech'],
        'categoria': ['Electrónica', 'Electrónica', None],
        'precio': [899.99, 249.99, 59.99],
        'cantidad': [1, 2, None],
        'descuento': [0.05, 0.00, 0.10],
        'total': [854.99, 499.98, 161.97]
    }
    return pd.DataFrame(data)

@pytest.fixture
def df_tipos_incorrectos():
    """Fixture que crea un DataFrame con tipos de datos incorrectos."""
    data = {
        'id': [1, 2, 3],
        'fecha': ['2023-01-05', '2023-01-10', '2023-01-15'],
        'producto': ['Laptop HP', 'Monitor Dell', 'Teclado Logitech'],
        'categoria': ['Electrónica', 'Electrónica', 'Accesorios'],
        'precio': ['899.99', '249.99', '59.99'],  # Strings en lugar de float
        'cantidad': [1, 2, 3],
        'descuento': [0.05, 0.00, 0.10],
        'total': [854.99, 499.98, 161.97]
    }
    return pd.DataFrame(data)

@pytest.fixture
def df_fuera_de_rango():
    """Fixture que crea un DataFrame con valores fuera de rango."""
    data = {
        'id': [1, 2, 3],
        'fecha': ['2023-01-05', '2023-01-10', '2023-01-15'],
        'producto': ['Laptop HP', 'Monitor Dell', 'Teclado Logitech'],
        'categoria': ['Electrónica', 'Electrónica', 'Accesorios'],
        'precio': [899.99, 249.99, 59.99],
        'cantidad': [1, 2, -3],  # Valor negativo
        'descuento': [0.05, 0.00, 1.5],  # Descuento mayor a 1 (100%)
        'total': [854.99, 499.98, 161.97]
    }
    return pd.DataFrame(data)

def test_validar_completitud_sin_nulos(df_valido):
    """Test para validar completitud en un DataFrame sin valores nulos."""
    resultado = validar_completitud(df_valido)
    assert resultado['valido'] is True
    assert 'mensaje' in resultado

def test_validar_completitud_con_nulos(df_con_nulos):
    """Test para validar completitud en un DataFrame con valores nulos."""
    resultado = validar_completitud(df_con_nulos)
    assert resultado['valido'] is False
    assert 'error' in resultado
    assert 'detalle' in resultado
    assert resultado['detalle']['fecha'] == 1
    assert resultado['detalle']['categoria'] == 1
    assert resultado['detalle']['cantidad'] == 1

def test_validar_completitud_columnas_especificas(df_con_nulos):
    """Test para validar completitud solo en columnas específicas."""
    # Validamos solo columnas que no tienen nulos
    resultado = validar_completitud(df_con_nulos, ['id', 'producto', 'precio', 'descuento', 'total'])
    assert resultado['valido'] is True
    
    # Validamos una columna que tiene nulos
    resultado = validar_completitud(df_con_nulos, ['id', 'fecha'])
    assert resultado['valido'] is False
    assert resultado['detalle']['fecha'] == 1

def test_validar_tipos_datos_correctos(df_valido):
    """Test para validar tipos de datos correctos."""
    tipos_esperados = {
        'id': 'int64',
        'precio': 'float64',
        'cantidad': 'int64',
        'descuento': 'float64',
        'total': 'float64'
    }
    resultado = validar_tipos_datos(df_valido, tipos_esperados)
    assert resultado['valido'] is True

def test_validar_tipos_datos_incorrectos(df_tipos_incorrectos):
    """Test para validar tipos de datos incorrectos."""
    tipos_esperados = {
        'id': 'int64',
        'precio': 'float64',  # En df_tipos_incorrectos, precio es string
        'cantidad': 'int64',
        'descuento': 'float64',
        'total': 'float64'
    }
    resultado = validar_tipos_datos(df_tipos_incorrectos, tipos_esperados)
    assert resultado['valido'] is False
    assert 'precio' in resultado['detalle']

def test_validar_rango_valores_dentro_de_rango(df_valido):
    """Test para validar rangos de valores dentro de los límites."""
    rangos = {
        'precio': (0, 1000),
        'cantidad': (0, 10),
        'descuento': (0, 1),
        'total': (0, 1000)
    }
    resultado = validar_rango_valores(df_valido, rangos)
    assert resultado['valido'] is True

def test_validar_rango_valores_fuera_de_rango(df_fuera_de_rango):
    """Test para validar rangos de valores fuera de los límites."""
    rangos = {
        'precio': (0, 1000),
        'cantidad': (0, 10),  # En df_fuera_de_rango, hay un valor negativo
        'descuento': (0, 1),  # En df_fuera_de_rango, hay un descuento > 1
        'total': (0, 1000)
    }
    resultado = validar_rango_valores(df_fuera_de_rango, rangos)
    assert resultado['valido'] is False
    assert 'cantidad' in resultado['detalle']
    assert 'descuento' in resultado['detalle']
    assert 'bajo_minimo' in resultado['detalle']['cantidad']
    assert 'sobre_maximo' in resultado['detalle']['descuento']
