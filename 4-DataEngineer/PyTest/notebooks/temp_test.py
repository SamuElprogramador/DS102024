def calcular_total_con_impuesto(monto, tasa_impuesto=0.16):
    """Calcula el monto total incluyendo impuestos."""
    return monto * (1 + tasa_impuesto)

def test_calcular_total_con_impuesto():
    # Caso 1: Impuesto por defecto (16%)
    assert calcular_total_con_impuesto(100) == 116.0
    
    # Caso 2: Impuesto personalizado (10%)
    assert calcular_total_con_impuesto(100, 0.10) == 110.0
    
    # Caso 3: Monto cero
    assert calcular_total_con_impuesto(0) == 0.0
