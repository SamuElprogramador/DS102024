"""
Configuración de la base de datos SQLite para el ETL de taxis de Nueva York
"""
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

from etl_example.etl_config import DB_URI

# Crear la base para los modelos SQLAlchemy
Base = declarative_base()

class TaxiLocation(Base):
    """Modelo SQLAlchemy para la tabla de ubicaciones"""
    __tablename__ = 'locations'
    
    location_id = Column(Integer, primary_key=True)
    borough = Column(String, nullable=False)
    zone = Column(String, nullable=False)
    service_zone = Column(String, nullable=False)
    
    # Relación con los viajes (pickup)
    pickup_trips = relationship("TaxiTripRecord", foreign_keys="TaxiTripRecord.pickup_location_id", back_populates="pickup_location")
    # Relación con los viajes (dropoff)
    dropoff_trips = relationship("TaxiTripRecord", foreign_keys="TaxiTripRecord.dropoff_location_id", back_populates="dropoff_location")

class TaxiTripRecord(Base):
    """Modelo SQLAlchemy para la tabla de viajes de taxi"""
    __tablename__ = 'taxi_trips'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    vendor_id = Column(Integer, nullable=False)
    
    # Campos de tiempo
    pickup_datetime = Column(DateTime, nullable=False)
    dropoff_datetime = Column(DateTime, nullable=False)
    
    # Campos de ubicación con relaciones
    pickup_location_id = Column(Integer, ForeignKey('locations.location_id'), nullable=False)
    dropoff_location_id = Column(Integer, ForeignKey('locations.location_id'), nullable=False)
    
    # Relaciones
    pickup_location = relationship("TaxiLocation", foreign_keys=[pickup_location_id], back_populates="pickup_trips")
    dropoff_location = relationship("TaxiLocation", foreign_keys=[dropoff_location_id], back_populates="dropoff_trips")
    
    # Campos de pasajeros
    passenger_count = Column(Float)
    
    # Campos de distancia
    trip_distance = Column(Float, nullable=False)
    
    # Campos de tarifa
    fare_amount = Column(Float, nullable=False)
    extra = Column(Float, nullable=False)
    mta_tax = Column(Float, nullable=False)
    tip_amount = Column(Float, nullable=False)
    tolls_amount = Column(Float, nullable=False)
    improvement_surcharge = Column(Float, nullable=False)
    total_amount = Column(Float, nullable=False)
    congestion_surcharge = Column(Float)
    airport_fee = Column(Float)
    
    # Campos de pago
    payment_type = Column(Integer, nullable=False)

def init_db():
    """Inicializa la base de datos creando todas las tablas"""
    engine = create_engine(DB_URI)
    Base.metadata.create_all(engine)
    return engine

def get_session():
    """Crea y devuelve una sesión de SQLAlchemy"""
    engine = create_engine(DB_URI)
    Session = sessionmaker(bind=engine)
    return Session()
