import pandas as pd
import numpy as np

def validar_completitud(df, columnas_requeridas=None):
    """Valida que no haya valores nulos en las columnas requeridas.
    
    Args:
        df: DataFrame a validar
        columnas_requeridas: Lista de columnas a verificar. Si es None, se verifican todas.
        
    Returns:
        dict: Diccionario con resultados de la validación
    """
    if columnas_requeridas is None:
        columnas_requeridas = df.columns.tolist()
    
    # Verificamos que todas las columnas requeridas existan
    columnas_faltantes = [col for col in columnas_requeridas if col not in df.columns]
    if columnas_faltantes:
        return {
            'valido': False,
            'error': f"Columnas faltantes: {', '.join(columnas_faltantes)}"
        }
    
    # Verificamos valores nulos
    nulos_por_columna = {col: int(df[col].isnull().sum()) for col in columnas_requeridas}
    tiene_nulos = any(nulos_por_columna.values())
    
    if tiene_nulos:
        columnas_con_nulos = [col for col, nulos in nulos_por_columna.items() if nulos > 0]
        return {
            'valido': False,
            'error': f"Valores nulos encontrados en: {', '.join(columnas_con_nulos)}",
            'detalle': nulos_por_columna
        }
    
    return {
        'valido': True,
        'mensaje': "No se encontraron valores nulos en las columnas requeridas"
    }

def validar_tipos_datos(df, tipos_esperados):
    """Valida que las columnas tengan los tipos de datos esperados.
    
    Args:
        df: DataFrame a validar
        tipos_esperados: Diccionario con columnas y sus tipos esperados
        
    Returns:
        dict: Diccionario con resultados de la validación
    """
    # Verificamos que todas las columnas existan
    columnas_faltantes = [col for col in tipos_esperados.keys() if col not in df.columns]
    if columnas_faltantes:
        return {
            'valido': False,
            'error': f"Columnas faltantes: {', '.join(columnas_faltantes)}"
        }
    
    # Verificamos los tipos de datos
    tipos_incorrectos = {}
    for columna, tipo_esperado in tipos_esperados.items():
        tipo_actual = df[columna].dtype
        if not pd.api.types.is_dtype_equal(tipo_actual, tipo_esperado):
            # Para tipos numéricos, verificamos si podemos convertir sin pérdida de información
            if pd.api.types.is_numeric_dtype(tipo_esperado) and pd.api.types.is_numeric_dtype(tipo_actual):
                continue
            
            # Para fechas, verificamos si podemos convertir
            if tipo_esperado == 'datetime64[ns]' and pd.api.types.is_string_dtype(tipo_actual):
                try:
                    pd.to_datetime(df[columna])
                    continue
                except:
                    pass
            
            tipos_incorrectos[columna] = {'esperado': tipo_esperado, 'actual': str(tipo_actual)}
    
    if tipos_incorrectos:
        return {
            'valido': False,
            'error': f"Tipos de datos incorrectos en {len(tipos_incorrectos)} columnas",
            'detalle': tipos_incorrectos
        }
    
    return {
        'valido': True,
        'mensaje': "Todos los tipos de datos son correctos"
    }

def validar_rango_valores(df, rangos):
    """Valida que los valores estén dentro de los rangos especificados.
    
    Args:
        df: DataFrame a validar
        rangos: Diccionario con columnas y sus rangos (min, max)
        
    Returns:
        dict: Diccionario con resultados de la validación
    """
    # Verificamos que todas las columnas existan
    columnas_faltantes = [col for col in rangos.keys() if col not in df.columns]
    if columnas_faltantes:
        return {
            'valido': False,
            'error': f"Columnas faltantes: {', '.join(columnas_faltantes)}"
        }
    
    # Verificamos los rangos
    fuera_de_rango = {}
    for columna, (min_val, max_val) in rangos.items():
        # Verificamos mínimo
        if min_val is not None:
            valores_bajo_minimo = df[df[columna] < min_val]
            if not valores_bajo_minimo.empty:
                if columna not in fuera_de_rango:
                    fuera_de_rango[columna] = {}
                fuera_de_rango[columna]['bajo_minimo'] = {
                    'cantidad': len(valores_bajo_minimo),
                    'minimo_esperado': min_val,
                    'valor_minimo_encontrado': float(valores_bajo_minimo[columna].min())
                }
        
        # Verificamos máximo
        if max_val is not None:
            valores_sobre_maximo = df[df[columna] > max_val]
            if not valores_sobre_maximo.empty:
                if columna not in fuera_de_rango:
                    fuera_de_rango[columna] = {}
                fuera_de_rango[columna]['sobre_maximo'] = {
                    'cantidad': len(valores_sobre_maximo),
                    'maximo_esperado': max_val,
                    'valor_maximo_encontrado': float(valores_sobre_maximo[columna].max())
                }
    
    if fuera_de_rango:
        return {
            'valido': False,
            'error': f"Valores fuera de rango en {len(fuera_de_rango)} columnas",
            'detalle': fuera_de_rango
        }
    
    return {
        'valido': True,
        'mensaje': "Todos los valores están dentro de los rangos especificados"
    }
