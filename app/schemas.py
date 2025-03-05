import re
from pydantic import BaseModel, field_validator, ConfigDict
from typing import Optional

class User(BaseModel):
    email: str
    password: str
    

class Server(BaseModel):
    server_name: str


class Sensor(BaseModel):
    server_ulid: str
    timestamp: str
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    voltage: Optional[float] = None
    current: Optional[float] = None

class SensorReadResult(BaseModel):
    timestamp: str
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    voltage: Optional[float] = None
    current: Optional[float] = None

    model_config = ConfigDict(exclude_none=True, exclude_defaults=True)