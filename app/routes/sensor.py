from fastapi import APIRouter, Depends, status, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime

from app.depends import get_db_session, token_verifier
from app.services.sensor_service import SensorService
from app.schemas import Sensor

router = APIRouter(prefix='/data')

@router.post('/', status_code=status.HTTP_201_CREATED)
def sensor_register(
    sensor: Sensor,
    db_session: Session = Depends(get_db_session),
):
    sensor_service = SensorService(db_session=db_session)
    sensor_service.create(sensor=sensor)
    
    return {'msg': 'success'}

@router.get("/", status_code=status.HTTP_200_OK, dependencies=[Depends(token_verifier)])
def get_sensor_data(
    db_session: Session = Depends(get_db_session),
    server_ulid: Optional[str] = Query(None, description="Filtrar por servidor específico"),
    start_time: Optional[datetime] = Query(None, description="Data inicial no formato ISO 8601"),
    end_time: Optional[datetime] = Query(None, description="Data final no formato ISO 8601"),
    sensor_type: Optional[str] = Query(None, description="Tipo de sensor (temperature, humidity, etc.)"),
    aggregation: Optional[str] = Query(None, description="Agregação: minute, hour, day")
):
    sensor_service = SensorService(db_session=db_session)
    
    return sensor_service.read(server_ulid, start_time, end_time, sensor_type, aggregation)
