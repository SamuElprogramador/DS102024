# Módulo de utilidades para el tutorial de pytest
# Este archivo permite que Python trate el directorio como un paquete

from .data_processing import calcular_metricas_ventas, categorizar_productos_por_precio, calcular_tendencia_ventas
from .data_validation import validar_completitud, validar_tipos_datos, validar_rango_valores