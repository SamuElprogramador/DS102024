"""
Modelos de datos para el ETL de taxis de Nueva York usando Pydantic
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator

class TaxiTrip(BaseModel):
    """Modelo Pydantic para validar los datos de viajes de taxi"""
    
    # Campos de identificación
    vendor_id: int = Field(..., description="ID del proveedor del taxi")
    
    # Campos de tiempo
    pickup_datetime: datetime = Field(..., description="Fecha y hora de recogida")
    dropoff_datetime: datetime = Field(..., description="Fecha y hora de entrega")
    
    # Campos de ubicación
    pickup_location_id: int = Field(..., description="ID de la ubicación de recogida")
    dropoff_location_id: int = Field(..., description="ID de la ubicación de entrega")
    
    # Campos de pasajeros
    passenger_count: Optional[float] = Field(None, description="Número de pasajeros")
    
    # Campos de distancia
    trip_distance: float = Field(..., description="Distancia del viaje en millas")
    
    # Campos de tarifa
    fare_amount: float = Field(..., description="Tarifa base en dólares")
    extra: float = Field(..., description="Cargos extra")
    mta_tax: float = Field(..., description="Impuesto MTA")
    tip_amount: float = Field(..., description="Propina en dólares")
    tolls_amount: float = Field(..., description="Peajes en dólares")
    improvement_surcharge: float = Field(..., description="Recargo por mejora")
    total_amount: float = Field(..., description="Monto total en dólares")
    congestion_surcharge: Optional[float] = Field(None, description="Recargo por congestión")
    airport_fee: Optional[float] = Field(None, description="Tarifa de aeropuerto")
    
    # Campos de pago
    payment_type: int = Field(..., description="Tipo de pago (1=Tarjeta de crédito, 2=Efectivo, etc.)")
    
    # Validadores
    @validator('trip_distance')
    def trip_distance_must_be_positive(cls, v):
        if v < 0:
            raise ValueError('La distancia del viaje debe ser positiva')
        return v
    
    @validator('fare_amount', 'total_amount')
    def amount_must_be_valid(cls, v):
        if v < 0:
            raise ValueError('Los montos deben ser positivos o cero')
        return v
    
    @validator('dropoff_datetime')
    def dropoff_after_pickup(cls, v, values):
        if 'pickup_datetime' in values and v < values['pickup_datetime']:
            raise ValueError('La fecha de entrega debe ser posterior a la fecha de recogida')
        return v
    
    @validator('passenger_count')
    def passenger_count_must_be_valid(cls, v):
        if v is not None and (v < 0 or v > 9):
            raise ValueError('El número de pasajeros debe estar entre 0 y 9')
        return v

class Location(BaseModel):
    """Modelo Pydantic para validar los datos de ubicaciones"""
    
    location_id: int = Field(..., description="ID único de la ubicación")
    borough: str = Field(..., description="Distrito")
    zone: str = Field(..., description="Zona")
    service_zone: str = Field(..., description="Zona de servicio")
    
    @validator('location_id')
    def location_id_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('El ID de ubicación debe ser positivo')
        return v
