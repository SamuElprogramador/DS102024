import pytest
import numpy as np

def normalizar_array(arr):
    """Normaliza un array para que sus valores estén entre 0 y 1."""
    min_val = np.min(arr)
    max_val = np.max(arr)
    if min_val == max_val:
        return np.zeros_like(arr)
    return (arr - min_val) / (max_val - min_val)

def test_normalizar_array():
    # Creamos un array de prueba
    arr = np.array([10, 20, 30, 40, 50])
    
    # Normalizamos
    resultado = normalizar_array(arr)
    
    # Creamos el array esperado
    esperado = np.array([0.0, 0.25, 0.5, 0.75, 1.0])
    
    # Comparamos los arrays
    np.testing.assert_allclose(resultado, esperado)

def test_normalizar_array_constante():
    # Creamos un array constante
    arr = np.array([10, 10, 10])
    
    # Normalizamos
    resultado = normalizar_array(arr)
    
    # Creamos el array esperado (todos ceros)
    esperado = np.array([0.0, 0.0, 0.0])
    
    # Comparamos los arrays
    np.testing.assert_array_equal(resultado, esperado)
