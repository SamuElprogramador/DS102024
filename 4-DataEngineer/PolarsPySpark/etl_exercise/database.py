"""
Configuración de la base de datos SQLite para el ejercicio ETL de taxis de Nueva York
"""
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

from etl_exercise.etl_config import DB_URI

# Crear la base para los modelos SQLAlchemy
Base = declarative_base()

# TODO: Implementar el modelo SQLAlchemy para la tabla de ubicaciones
class TaxiLocation(Base):
    """Modelo SQLAlchemy para la tabla de ubicaciones"""
    __tablename__ = 'locations'
    
    # TODO: Definir las columnas (location_id, borough, zone, service_zone)
    
    # TODO: Definir las relaciones con los viajes (pickup_trips, dropoff_trips)

# TODO: Implementar el modelo SQLAlchemy para la tabla de viajes de taxi
class TaxiTripRecord(Base):
    """Modelo SQLAlchemy para la tabla de viajes de taxi"""
    __tablename__ = 'taxi_trips'
    
    # TODO: Definir las columnas (id, vendor_id, pickup_datetime, dropoff_datetime, etc.)
    
    # TODO: Definir las relaciones con las ubicaciones (pickup_location, dropoff_location)

def init_db():
    """Inicializa la base de datos creando todas las tablas"""
    # TODO: Implementar la inicialización de la base de datos
    pass

def get_session():
    """Crea y devuelve una sesión de SQLAlchemy"""
    # TODO: Implementar la creación de una sesión
    pass
