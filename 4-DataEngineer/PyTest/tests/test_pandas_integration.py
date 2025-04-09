import pytest
import pandas as pd
import numpy as np

def filtrar_por_categoria(df, categoria):
    """Filtra un DataFrame por categoría."""
    return df[df['categoria'] == categoria].reset_index(drop=True)

def test_filtrar_por_categoria():
    # Creamos un DataFrame de prueba
    data = {
        'id': [1, 2, 3, 4],
        'categoria': ['A', 'B', 'A', 'C'],
        'valor': [10, 20, 30, 40]
    }
    df = pd.DataFrame(data)
    
    # Filtramos por categoría 'A'
    resultado = filtrar_por_categoria(df, 'A')
    
    # Creamos el DataFrame esperado
    esperado = pd.DataFrame({
        'id': [1, 3],
        'categoria': ['A', 'A'],
        'valor': [10, 30]
    })
    
    # Comparamos los DataFrames
    pd.testing.assert_frame_equal(resultado, esperado)

def test_filtrar_por_categoria_vacio():
    # Creamos un DataFrame de prueba
    data = {
        'id': [1, 2, 3, 4],
        'categoria': ['A', 'B', 'A', 'C'],
        'valor': [10, 20, 30, 40]
    }
    df = pd.DataFrame(data)
    
    # Filtramos por una categoría que no existe
    resultado = filtrar_por_categoria(df, 'D')
    
    # Verificamos que el resultado sea un DataFrame vacío con las mismas columnas
    assert len(resultado) == 0
    assert list(resultado.columns) == ['id', 'categoria', 'valor']
