import pytest
import pandas as pd
import time

# Esta fixture se ejecutará una vez por sesión de pytest
@pytest.fixture(scope="session")
def df_ventas_session():
    print("\nCargando dataset (scope=session)...")
    time.sleep(1)  # Simulamos una carga lenta
    df = pd.read_csv('../data/ventas_productos.csv')
    print("Dataset cargado (scope=session)")
    return df

# Esta fixture se ejecutará una vez por función de test
@pytest.fixture(scope="function")
def df_ventas_function():
    print("\nCargando dataset (scope=function)...")
    time.sleep(0.5)  # Simulamos una carga lenta
    df = pd.read_csv('../data/ventas_productos.csv')
    print("Dataset cargado (scope=function)")
    return df

def test_1_con_session_fixture(df_ventas_session):
    print("Ejecutando test_1_con_session_fixture")
    assert len(df_ventas_session) > 0

def test_2_con_session_fixture(df_ventas_session):
    print("Ejecutando test_2_con_session_fixture")
    assert 'total' in df_ventas_session.columns

def test_1_con_function_fixture(df_ventas_function):
    print("Ejecutando test_1_con_function_fixture")
    assert len(df_ventas_function) > 0

def test_2_con_function_fixture(df_ventas_function):
    print("Ejecutando test_2_con_function_fixture")
    assert 'total' in df_ventas_function.columns
