"""
Modelos de datos para el ejercicio ETL de taxis de Nueva York usando Pydantic
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator

# TODO: Completar el modelo Pydantic para validar los datos de viajes de taxi
# Debe incluir todos los campos necesarios y validadores apropiados
class TaxiTrip(BaseModel):
    """Modelo Pydantic para validar los datos de viajes de taxi"""
    
    # Campos de identificación
    vendor_id: int = Field(..., description="ID del proveedor del taxi")
    
    # TODO: Añadir los campos de tiempo (pickup_datetime, dropoff_datetime)
    
    # TODO: Añadir los campos de ubicación (pickup_location_id, dropoff_location_id)
    
    # TODO: Añadir los campos de pasajeros (passenger_count)
    
    # TODO: Añadir los campos de distancia (trip_distance)
    
    # TODO: Añadir los campos de tarifa (fare_amount, extra, mta_tax, etc.)
    
    # TODO: Añadir los campos de pago (payment_type)
    
    # TODO: Implementar validadores para asegurar la integridad de los datos
    # Por ejemplo, validar que trip_distance sea positivo
    @validator('vendor_id')
    def vendor_id_must_be_valid(cls, v):
        if v not in [1, 2]:
            raise ValueError('El ID del proveedor debe ser 1 o 2')
        return v
    
    # Añadir más validadores según sea necesario

# TODO: Implementar el modelo Location para las ubicaciones
class Location(BaseModel):
    """Modelo Pydantic para validar los datos de ubicaciones"""
    
    # TODO: Añadir los campos necesarios (location_id, borough, zone, service_zone)
    
    # TODO: Implementar validadores para asegurar la integridad de los datos
