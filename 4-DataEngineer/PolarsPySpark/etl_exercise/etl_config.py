"""
Configuración para el ejercicio ETL de taxis de Nueva York
"""
import os
from pathlib import Path

# Rutas de archivos
BASE_DIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = BASE_DIR / "data" / "processed"
OUTPUT_DIR = BASE_DIR / "etl_exercise" / "output"
LOG_DIR = BASE_DIR / "etl_exercise" / "logs"

# Asegurar que los directorios existan
OUTPUT_DIR.mkdir(exist_ok=True, parents=True)
LOG_DIR.mkdir(exist_ok=True, parents=True)

# Configuración de la base de datos
DB_PATH = OUTPUT_DIR / "nyc_taxi_exercise.db"
DB_URI = f"sqlite:///{DB_PATH}"

# Configuración de logging
LOG_FILE = LOG_DIR / "etl_exercise.log"
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Configuración del dataset
TAXI_DATA_FILE = DATA_DIR / "yellow_tripdata.parquet"

# Configuración de procesamiento
BATCH_SIZE = 100000  # Número de filas a procesar en cada lote
