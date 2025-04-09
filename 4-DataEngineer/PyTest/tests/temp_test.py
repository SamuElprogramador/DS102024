def calcular_total_con_impuesto(monto, tasa_impuesto=0.16):
    """Calcula el monto total incluyendo impuestos."""
    return round(monto * (1 + tasa_impuesto),2)

def test_calcular_total_con_impuesto():
    # Caso 1: Impuesto por defecto (16%)
    assert calcular_total_con_impuesto(100.0) == 100
    
    # Caso 2: Impuesto personalizado (10%)
    assert calcular_total_con_impuesto('50.3') == np.nan
    
    # Caso 3: Monto cero
    assert calcular_total_con_impuesto(0) == 0.0
