"""
Implementación de DAGs y tareas para el ejercicio ETL de taxis de Nueva York
"""
from datetime import datetime
import os
from pathlib import Path
from typing import List, Dict, Any, Optional

import polars as pl
from prefect import task, flow
from sqlalchemy.orm import Session

from etl_exercise.etl_config import TAXI_DATA_FILE, BATCH_SIZE
from etl_exercise.logger import setup_logger
from etl_exercise.models import TaxiTrip
from etl_exercise.database import init_db, get_session, TaxiTripRecord, TaxiLocation

# TODO: Configurar el logger
# logger = setup_logger("etl_exercise_dag")

@task(name="extract_taxi_data")
def extract_taxi_data(file_path: str = str(TAXI_DATA_FILE)) -> pl.DataFrame:
    """
    Extrae los datos del archivo parquet utilizando Polars
    
    Args:
        file_path: Ruta al archivo parquet
        
    Returns:
        DataFrame de Polars con los datos extraídos
    """
    # TODO: Implementar la extracción de datos del archivo parquet
    # 1. Leer el archivo parquet con Polars
    # 2. Renombrar las columnas para que coincidan con nuestro modelo
    # 3. Registrar información sobre los datos extraídos
    # 4. Devolver el DataFrame
    pass

@task(name="transform_taxi_data")
def transform_taxi_data(df: pl.DataFrame) -> pl.DataFrame:
    """
    Transforma los datos utilizando Polars
    
    Args:
        df: DataFrame de Polars con los datos extraídos
        
    Returns:
        DataFrame de Polars con los datos transformados
    """
    # TODO: Implementar la transformación de datos
    # 1. Filtrar viajes con distancia válida (mayor a 0)
    # 2. Filtrar viajes con tarifa válida (mayor o igual a 0)
    # 3. Calcular la duración del viaje en minutos
    # 4. Filtrar viajes con duración válida (mayor a 0)
    # 5. Calcular la velocidad promedio (millas por hora)
    # 6. Filtrar velocidades razonables (menos de 100 mph)
    # 7. Manejar valores nulos
    # 8. Registrar información sobre la transformación
    # 9. Devolver el DataFrame transformado
    pass

@task(name="validate_taxi_data")
def validate_taxi_data(df: pl.DataFrame) -> List[Dict[str, Any]]:
    """
    Valida los datos utilizando el modelo Pydantic
    
    Args:
        df: DataFrame de Polars con los datos transformados
        
    Returns:
        Lista de diccionarios con los datos validados
    """
    # TODO: Implementar la validación de datos con Pydantic
    # 1. Convertir el DataFrame a diccionarios
    # 2. Validar cada registro con el modelo Pydantic
    # 3. Registrar información sobre la validación
    # 4. Devolver la lista de registros validados
    pass

@task(name="load_taxi_data")
def load_taxi_data(validated_data: List[Dict[str, Any]]) -> None:
    """
    Carga los datos validados en la base de datos SQLite
    
    Args:
        validated_data: Lista de diccionarios con los datos validados
    """
    # TODO: Implementar la carga de datos en la base de datos
    # 1. Inicializar la base de datos
    # 2. Obtener una sesión
    # 3. Procesar los datos en lotes
    # 4. Registrar información sobre la carga
    pass

# TODO: Implementar la función auxiliar _load_batch para cargar un lote de registros
def _load_batch(session: Session, batch: List[Dict[str, Any]]) -> None:
    """
    Carga un lote de registros en la base de datos
    
    Args:
        session: Sesión de SQLAlchemy
        batch: Lote de registros a cargar
    """
    # TODO: Implementar la carga de un lote de registros
    # 1. Asegurar que las ubicaciones existan
    # 2. Crear los registros de viajes
    # 3. Manejar errores y hacer rollback si es necesario
    pass

@flow(name="NYC Taxi ETL Exercise")
def nyc_taxi_etl_flow():
    """
    Flujo principal de ETL para los datos de taxis de Nueva York
    """
    # TODO: Implementar el flujo principal de ETL
    # 1. Extraer datos
    # 2. Transformar datos
    # 3. Validar datos
    # 4. Cargar datos
    # 5. Registrar información sobre el flujo
    pass

if __name__ == "__main__":
    # TODO: Ejecutar el flujo principal
    pass
