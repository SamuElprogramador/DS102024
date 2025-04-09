# Ejercicio Práctico: ETL con Mage.ai

Este ejercicio te permitirá aplicar los conceptos de ETL (Extract, Transform, Load) utilizando Mage.ai. Trabajarás con datos de películas para crear un pipeline ETL completo.

## Objetivo

Crear un pipeline ETL que:
1. Extraiga datos de películas desde una API
2. Transforme los datos para hacerlos más útiles para análisis
3. Cargue los datos transformados en una base de datos

## Datos

Utilizaremos la API pública de The Movie Database (TMDb) para obtener datos de películas populares.

## Instrucciones

### Paso 1: Configuración

1. Asegúrate de tener Mage.ai ejecutándose en Docker
2. Crea un nuevo pipeline llamado "movies_etl_exercise"
3. Selecciona "Standard (batch)" como tipo de pipeline

### Paso 2: Extracción (Extract)

Crea un bloque de tipo "Data loader" con el siguiente código base:

```python
import pandas as pd
import requests

@data_loader
def extract_movies_data() -> pd.DataFrame:
    """
    Extrae datos de películas populares desde la API de TMDb.
    
    Returns:
        pd.DataFrame: DataFrame con los datos de películas
    """
    # URL base de la API
    base_url = "https://api.themoviedb.org/3"
    
    # Endpoint para películas populares
    endpoint = "/movie/popular"
    
    # Parámetros de la petición
    # Nota: Normalmente necesitarías una API key, pero para este ejercicio
    # puedes usar datos de ejemplo si no tienes acceso a la API
    params = {
        "api_key": "tu_api_key",  # Reemplaza con tu API key si tienes una
        "language": "es-ES",
        "page": 1
    }
    
    # TODO: Implementa la lógica para hacer la petición a la API
    # y convertir la respuesta en un DataFrame
    
    # Si no tienes acceso a la API, puedes usar estos datos de ejemplo:
    example_data = [
        {"id": 1, "title": "Película 1", "release_date": "2023-01-15", "popularity": 100.5, "vote_average": 7.8, "vote_count": 1500, "overview": "Descripción de la película 1", "genre_ids": [28, 12, 878]},
        {"id": 2, "title": "Película 2", "release_date": "2023-02-20", "popularity": 95.2, "vote_average": 6.9, "vote_count": 1200, "overview": "Descripción de la película 2", "genre_ids": [35, 10749]},
        {"id": 3, "title": "Película 3", "release_date": "2023-03-10", "popularity": 88.7, "vote_average": 8.1, "vote_count": 950, "overview": "Descripción de la película 3", "genre_ids": [18, 53]},
        # Añade más películas de ejemplo aquí
    ]
    
    return pd.DataFrame(example_data)
```

**Tarea**: Completa la función para extraer datos de películas populares desde la API de TMDb. Si no tienes acceso a la API, puedes expandir los datos de ejemplo.

### Paso 3: Transformación (Transform)

Crea un bloque de tipo "Transformer" con el siguiente código base:

```python
import pandas as pd
from datetime import datetime

@transformer
def transform_movies_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transforma los datos de películas:
    1. Limpia y formatea las fechas
    2. Calcula métricas adicionales
    3. Categoriza las películas por puntuación
    
    Args:
        df: DataFrame con los datos extraídos
        
    Returns:
        pd.DataFrame: DataFrame con los datos transformados
    """
    # Crear una copia para no modificar el original
    transformed_df = df.copy()
    
    # TODO: Implementa las siguientes transformaciones:
    # 1. Convierte 'release_date' a tipo datetime
    # 2. Extrae el año, mes y día en columnas separadas
    # 3. Calcula una columna 'score_weighted' que combine 'vote_average' y 'vote_count'
    #    (Fórmula sugerida: vote_average * (vote_count / (vote_count + 1000)))
    # 4. Categoriza las películas según su puntuación en 'poor', 'average', 'good' o 'excellent'
    # 5. Limpia la columna 'overview' eliminando caracteres especiales si es necesario
    
    return transformed_df
```

**Tarea**: Completa la función para transformar los datos de películas según las instrucciones.

### Paso 4: Carga (Load)

Crea un bloque de tipo "Data exporter" con el siguiente código base:

```python
import pandas as pd
import duckdb
import os

@data_exporter
def load_movies_data(df: pd.DataFrame) -> None:
    """
    Carga los datos transformados en una base de datos DuckDB.
    
    Args:
        df: DataFrame con los datos transformados
    """
    # Definir la ruta de la base de datos
    db_path = 'movies_data.duckdb'
    
    # TODO: Implementa la lógica para:
    # 1. Conectar a la base de datos DuckDB
    # 2. Crear una tabla 'movies' si no existe
    # 3. Cargar los datos transformados en la tabla
    # 4. Verificar que los datos se cargaron correctamente
    # 5. Cerrar la conexión
```

**Tarea**: Completa la función para cargar los datos transformados en una base de datos DuckDB.

### Paso 5: Ejecución y Verificación

1. Ejecuta cada bloque en secuencia
2. Verifica que los datos se extraen correctamente
3. Comprueba que las transformaciones se aplican según lo esperado
4. Confirma que los datos se cargan correctamente en la base de datos

### Paso 6: Documentación

Documenta tu pipeline:
1. Añade comentarios explicativos en tu código
2. Crea un bloque de markdown en el pipeline explicando lo que hace cada bloque
3. Describe cualquier desafío que hayas enfrentado y cómo lo resolviste

## Entrega

Cuando hayas completado el ejercicio, deberás entregar:
1. Capturas de pantalla del pipeline en Mage.ai
2. El código de cada bloque (extracción, transformación, carga)
3. Una breve explicación de tu enfoque y las decisiones que tomaste

## Criterios de Evaluación

Tu solución será evaluada según:
1. Funcionalidad: ¿El pipeline extrae, transforma y carga los datos correctamente?
2. Calidad del código: ¿El código está bien estructurado, comentado y sigue buenas prácticas?
3. Transformaciones: ¿Las transformaciones son útiles y están bien implementadas?
4. Documentación: ¿Has documentado adecuadamente tu solución?

¡Buena suerte!
