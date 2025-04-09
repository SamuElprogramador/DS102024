"""
Implementación de ETL para taxis de Nueva York usando sistema de DAGs personalizado
"""
from typing import List, Dict, Any
import time

import polars as pl
from sqlalchemy.orm import Session

from etl_example.etl_config import TAXI_DATA_FILE_SMALL, BATCH_SIZE
from etl_example.logger import setup_logger
from etl_example.models import TaxiTrip
from etl_example.database import init_db, get_session, TaxiTripRecord, TaxiLocation
from utils import DAG

# Configurar el logger
logger = setup_logger("nyc_taxi_etl")

# Crear el DAG
taxi_dag = DAG(
    dag_id="nyc_taxi_etl",
    description="ETL para procesar datos de taxis de Nueva York"
)

def extract_taxi_data(file_path: str = str(TAXI_DATA_FILE_SMALL)) -> pl.DataFrame:
    """Extrae los datos del archivo parquet utilizando Polars"""
    logger.info(f"Extrayendo datos del archivo: {file_path}")

    try:
        # Usar Polars para leer el archivo parquet
        df = pl.read_parquet(file_path)

        # Renombrar columnas para que coincidan con nuestro modelo
        column_mapping = {
            "VendorID": "vendor_id",
            "tpep_pickup_datetime": "pickup_datetime",
            "tpep_dropoff_datetime": "dropoff_datetime",
            "PULocationID": "pickup_location_id",
            "DOLocationID": "dropoff_location_id",
            "passenger_count": "passenger_count",
            "trip_distance": "trip_distance",
            "fare_amount": "fare_amount",
            "extra": "extra",
            "mta_tax": "mta_tax",
            "tip_amount": "tip_amount",
            "tolls_amount": "tolls_amount",
            "improvement_surcharge": "improvement_surcharge",
            "total_amount": "total_amount",
            "congestion_surcharge": "congestion_surcharge",
            "Airport_fee": "airport_fee",
            "payment_type": "payment_type"
        }

        # Renombrar columnas
        for old_name, new_name in column_mapping.items():
            if old_name in df.columns:
                df = df.rename({old_name: new_name})

        logger.info(f"Datos extraídos exitosamente. Filas: {df.shape[0]}, Columnas: {df.shape[1]}")
        return df

    except Exception as e:
        logger.error(f"Error al extraer datos: {str(e)}")
        raise

def transform_taxi_data(df: pl.DataFrame) -> pl.DataFrame:
    """Transforma los datos utilizando Polars"""
    logger.info("Iniciando transformación de datos")

    try:
        # Filtrar viajes con distancia válida (mayor a 0)
        df = df.filter(pl.col("trip_distance") > 0)

        # Filtrar viajes con tarifa válida (mayor o igual a 0)
        df = df.filter(pl.col("fare_amount") >= 0)

        # Calcular la duración del viaje en minutos
        df = df.with_columns([
            ((pl.col("dropoff_datetime").dt.epoch() - pl.col("pickup_datetime").dt.epoch()) / 60).alias("trip_duration_minutes")
        ])

        # Filtrar viajes con duración válida (mayor a 0)
        df = df.filter(pl.col("trip_duration_minutes") > 0)

        # Calcular la velocidad promedio (millas por hora)
        df = df.with_columns([
            (pl.col("trip_distance") / (pl.col("trip_duration_minutes") / 60)).alias("avg_speed_mph")
        ])

        # Filtrar velocidades razonables (menos de 100 mph)
        df = df.filter(pl.col("avg_speed_mph") < 100)

        # Manejar valores nulos
        df = df.with_columns([
            pl.col("passenger_count").fill_null(1),
            pl.col("congestion_surcharge").fill_null(0),
            pl.col("airport_fee").fill_null(0)
        ])

        logger.info(f"Transformación completada. Filas restantes: {df.shape[0]}")
        return df

    except Exception as e:
        logger.error(f"Error en la transformación de datos: {str(e)}")
        raise

def validate_taxi_data(df: pl.DataFrame) -> List[Dict[str, Any]]:
    """Valida los datos usando el modelo Pydantic"""
    logger.info("Iniciando validación de datos con Pydantic")
    valid_records = []
    error_count = 0

    chunk_size = BATCH_SIZE
    total_rows = df.height

    try:
        for start in range(0, total_rows, chunk_size):
            chunk = df.slice(start, chunk_size)
            records = chunk.to_dicts()

            for i, record in enumerate(records, start=start):
                try:
                    validated_record = TaxiTrip(**record)
                    valid_records.append(validated_record.dict())
                except Exception as e:
                    error_count += 1
                    if error_count <= 10:  # Limitar el número de errores registrados
                        logger.warning(f"Error de validación en el registro {i}: {str(e)}")

        logger.info(f"Validación completada. Registros válidos: {len(valid_records)}, Errores: {error_count}")
        return valid_records

    except Exception as e:
        logger.error(f"Error en la validación de datos: {str(e)}")
        raise

def load_taxi_data(validated_data: List[Dict[str, Any]]) -> None:
    """Carga los datos validados en la base de datos"""
    logger.info("Iniciando carga de datos en la base de datos")

    try:
        # Inicializar la base de datos
        init_db()

        # Obtener una sesión
        session = get_session()

        # Procesar en lotes para evitar problemas de memoria
        total_records = len(validated_data)
        batch_size = min(BATCH_SIZE, total_records)

        for i in range(0, total_records, batch_size):
            batch = validated_data[i:i+batch_size]

            # Crear registros en la base de datos
            _load_batch(session, batch)

            logger.info(f"Lote procesado: {i+1} a {min(i+batch_size, total_records)} de {total_records}")

        logger.info("Carga de datos completada exitosamente")

    except Exception as e:
        logger.error(f"Error en la carga de datos: {str(e)}")
        raise

def _load_batch(session: Session, batch: List[Dict[str, Any]]) -> None:
    """Carga un lote de registros en la base de datos"""
    try:
        # Asegurar que las ubicaciones existan
        location_ids = set()
        for record in batch:
            location_ids.add(record['pickup_location_id'])
            location_ids.add(record['dropoff_location_id'])

        # Verificar qué ubicaciones ya existen en la base de datos
        existing_locations = {loc.location_id for loc in session.query(TaxiLocation.location_id).filter(TaxiLocation.location_id.in_(location_ids)).all()}

        # Crear las ubicaciones que no existen
        for location_id in location_ids:
            if location_id not in existing_locations:
                # Crear una ubicación temporal
                location = TaxiLocation(
                    location_id=location_id,
                    borough="Unknown",
                    zone=f"Zone {location_id}",
                    service_zone="Unknown"
                )
                session.add(location)

        # Guardar las ubicaciones
        session.commit()

        # Crear los registros de viajes
        for record in batch:
            trip = TaxiTripRecord(
                vendor_id=record['vendor_id'],
                pickup_datetime=record['pickup_datetime'],
                dropoff_datetime=record['dropoff_datetime'],
                pickup_location_id=record['pickup_location_id'],
                dropoff_location_id=record['dropoff_location_id'],
                passenger_count=record['passenger_count'],
                trip_distance=record['trip_distance'],
                fare_amount=record['fare_amount'],
                extra=record['extra'],
                mta_tax=record['mta_tax'],
                tip_amount=record['tip_amount'],
                tolls_amount=record['tolls_amount'],
                improvement_surcharge=record['improvement_surcharge'],
                total_amount=record['total_amount'],
                congestion_surcharge=record['congestion_surcharge'],
                airport_fee=record['airport_fee'],
                payment_type=record['payment_type']
            )
            session.add(trip)

        # Guardar los viajes
        session.commit()

    except Exception as e:
        session.rollback()
        logger.error(f"Error al cargar lote en la base de datos: {str(e)}")
        raise

# Definir las tareas del DAG
extract_task = taxi_dag.task("extract_data", extract_taxi_data)
transform_task = taxi_dag.task("transform_data", transform_taxi_data)
validate_task = taxi_dag.task("validate_data", validate_taxi_data)
load_task = taxi_dag.task("load_data", load_taxi_data)

# Configurar las dependencias
extract_task.set_downstream(transform_task)
transform_task.set_downstream(validate_task)
validate_task.set_downstream(load_task)

# Versión síncrona del flujo ETL
def nyc_taxi_etl_flow():
    """Ejecuta el flujo ETL para taxis de Nueva York de forma secuencial"""
    logger.info("Iniciando flujo ETL para datos de taxis de Nueva York")

    # Extraer datos
    raw_data = extract_taxi_data()

    # Transformar datos
    transformed_data = transform_taxi_data(raw_data)

    # Validar datos
    validated_data = validate_taxi_data(transformed_data)

    # Cargar datos
    load_taxi_data(validated_data)

    logger.info("Flujo ETL completado exitosamente")

# Versión asíncrona para ejecutar el DAG completo
async def run_taxi_etl_dag():
    """Ejecuta el DAG de ETL de forma asíncrona"""
    logger.info("Iniciando DAG de ETL para taxis de Nueva York")

    try:
        results = await taxi_dag.run()
        logger.info("DAG de ETL completado exitosamente")
        return results
    except Exception as e:
        logger.error(f"Error al ejecutar el DAG de ETL: {str(e)}")
        raise
