"""
Configuración del sistema de logging para el ETL de taxis de Nueva York
"""
import logging
import sys
from pathlib import Path

from etl_example.etl_config import LOG_FILE, LOG_LEVEL, LOG_FORMAT

def setup_logger(name, log_file=LOG_FILE, level=LOG_LEVEL):
    """Configura y devuelve un logger con el nombre especificado"""
    
    # Crear el directorio de logs si no existe
    log_dir = Path(log_file).parent
    log_dir.mkdir(exist_ok=True)
    
    # Configurar el logger
    logger = logging.getLogger(name)
    
    # Establecer el nivel de logging
    level_obj = getattr(logging, level)
    logger.setLevel(level_obj)
    
    # Crear un manejador para archivo
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level_obj)
    
    # Crear un manejador para consola
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level_obj)
    
    # Crear el formato
    formatter = logging.Formatter(LOG_FORMAT)
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Agregar los manejadores al logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger
