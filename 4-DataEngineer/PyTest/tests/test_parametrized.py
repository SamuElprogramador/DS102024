import pytest

def validar_formato_fecha(fecha):
    """Valida que una fecha tenga el formato YYYY-MM-DD."""
    import re
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    return bool(re.match(pattern, fecha))

@pytest.mark.parametrize("fecha,esperado", [
    ("2023-01-05", True),   # Formato correcto
    ("2023-1-5", False),    # Día y mes sin ceros iniciales
    ("01-05-2023", False),  # Formato incorrecto (DD-MM-YYYY)
    ("2023/01/05", False),  # Separadores incorrectos
    ("20230105", False),    # Sin separadores
    ("2023-01-32", True),   # Día inválido pero formato correcto
    ("", False),            # Cadena vacía
])
def test_validar_formato_fecha(fecha, esperado):
    """Test parametrizado para la función de validación de fechas."""
    assert validar_formato_fecha(fecha) == esperado, f"La validación de '{fecha}' debería ser {esperado}"
