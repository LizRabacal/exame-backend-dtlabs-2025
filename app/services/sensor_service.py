from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.db.models import SensorDataModel
from app.schemas import Sensor
from app.services.server_service import ServerService
from fastapi import status
from fastapi.exceptions import HTTPException
from datetime import datetime
from dateutil.parser import isoparse
from typing import Optional
from app.schemas import SensorReadResult

import ulid


class SensorService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, sensor: Sensor):
        server_service = ServerService(db_session= self.db_session)
        if not server_service.exists_by_id(sensor.server_ulid):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Server ULID not found"
            )
        if all(value is None for value in [sensor.temperature, sensor.humidity, sensor.voltage, sensor.current]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one sensor value must be provided"
            )
        
        
        self.is_valid_timestamp(sensor.timestamp) 
     
        
        sensor_data = SensorDataModel( 
            id = str(ulid.new()),
            server_ulid = sensor.server_ulid,
            timestamp = isoparse(sensor.timestamp),
            temperature = sensor.temperature or None,
            humidity = sensor.humidity or None,
            voltage = sensor.voltage or None,
            current = sensor.current or None,
        )

        self.db_session.add(sensor_data)
        self.db_session.commit()
    

    
    def read(
        self,
        server_ulid: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        sensor_type: Optional[str] = None,
        aggregation: Optional[str] = None
    ):
        query = self.db_session.query(SensorDataModel)
        if server_ulid:
            query = query.filter(SensorDataModel.server_ulid == server_ulid)

        if start_time:
            query = query.filter(SensorDataModel.timestamp >= start_time)

        if end_time:
            query = query.filter(SensorDataModel.timestamp <= end_time)


        if sensor_type and hasattr(SensorDataModel, sensor_type):
            if sensor_type not in ["temperature", "humidity", "voltage", "current"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid sensor type"
                )
            
            sensor_column = getattr(SensorDataModel, sensor_type)
            query = query.with_entities(SensorDataModel.timestamp, sensor_column).filter(sensor_column.isnot(None))


            if aggregation:
                if aggregation not in ["minute", "hour", "day"]:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Invalid aggregation type. Allowed: minute, hour, day"
                    )

                time_group = func.date_trunc(aggregation, SensorDataModel.timestamp).label("timestamp")
                query = self.db_session.query(time_group, func.avg(sensor_column).label(sensor_type))
                query = query.group_by(time_group)
                query = query.order_by(time_group)



            results = query.all()
            return [{"timestamp": row[0].isoformat(), sensor_type: row[1]} for row in results]
    
         
        
        results = query.all()

        return [
            SensorReadResult(
                timestamp=row.timestamp.isoformat(),
                temperature=row.temperature,
                humidity=row.humidity,
                voltage=row.voltage,
                current=row.current
            )
            for row in results
        ]
        
    def is_valid_timestamp(self, timestamp: str):
        try:
            datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid timestamp format. Must be in ISO 8601."
            )
    
    def get_latest_sensor_data(self, id: str):
        return (
            self.db_session.query(SensorDataModel)
            .filter(SensorDataModel.server_ulid == id)
            .order_by(desc(SensorDataModel.timestamp)) 
            .first()  
        )
            

    


    



        

    
