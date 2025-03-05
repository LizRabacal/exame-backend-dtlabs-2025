from sqlalchemy import Column, String, Integer, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime

class UserModel(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    servers = relationship("ServerModel", back_populates="user")

class ServerModel(Base):
    __tablename__ = "server"
    id = Column(String, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    name = Column(String, nullable=False)

    user = relationship("UserModel", back_populates="servers")
    sensors = relationship("SensorDataModel", back_populates="server")
    
class SensorDataModel(Base):
    __tablename__ = "sensor_data"
    id = Column(String, primary_key=True, index=True)
    server_ulid = Column(String, ForeignKey("server.id"), index=True, nullable=False)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    temperature = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)
    voltage = Column(Float, nullable=True)
    current = Column(Float, nullable=True)
    
    server = relationship("ServerModel")
