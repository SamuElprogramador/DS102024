"""
Configuración del sistema de logging para el ejercicio ETL de taxis de Nueva York
"""
import logging
import sys
from pathlib import Path

from etl_exercise.etl_config import LOG_FILE, LOG_LEVEL, LOG_FORMAT

# TODO: Implementar la función setup_logger para configurar y devolver un logger
def setup_logger(name, log_file=LOG_FILE, level=LOG_LEVEL):
    """
    Configura y devuelve un logger con el nombre especificado
    
    Args:
        name: Nombre del logger
        log_file: Ruta al archivo de log
        level: Nivel de logging (INFO, DEBUG, etc.)
        
    Returns:
        Un objeto logger configurado
    """
    # TODO: Crear el directorio de logs si no existe
    
    # TODO: Configurar el logger
    
    # TODO: Establecer el nivel de logging
    
    # TODO: Crear un manejador para archivo
    
    # TODO: Crear un manejador para consola
    
    # TODO: Crear el formato
    
    # TODO: Agregar los manejadores al logger
    
    # TODO: Devolver el logger configurado
    pass
