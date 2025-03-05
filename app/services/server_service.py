from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session
from app.db.models import ServerModel
from app.schemas import Server
from app.db.models import UserModel
from fastapi.exceptions import HTTPException
from fastapi import status
import ulid



class ServerService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, server: Server, user: UserModel):
        server_model = ServerModel(
            id = str(ulid.new()),
            name = server.server_name,
            user_id = user.id
        )
        self.db_session.add(server_model)
        self.db_session.commit()

        return server_model.id
    
    def exists_by_id(self, id: str):
        return self.db_session.query(ServerModel).filter_by(id = id).first() is not None
    

    def _get_server_status(self, server):
        from app.services.sensor_service import SensorService
        sensor_service = SensorService(db_session=self.db_session)
        last_sensor_data = sensor_service.get_latest_sensor_data(server.id)

        now = datetime.now(timezone.utc) - timedelta(hours=3)
        ten_seconds_ago = now - timedelta(seconds=10)

        if last_sensor_data:
            last_sensor_timestamp = last_sensor_data.timestamp.replace(tzinfo=timezone.utc)
            server_status = "offline" if last_sensor_timestamp < ten_seconds_ago else "online"
        else:
            server_status = "offline"  

        return {
            'server_ulid': server.id,
            'status': server_status,
            'server_name': server.name
        }

    def get_server_health_status(self, server_ulid: str):
        server = self.db_session.query(ServerModel).filter_by(id=server_ulid).first()
        if not server:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Server ULID not found"
            )

        return self._get_server_status(server)

    def get_all_servers_health_status(self):
        servers = self.db_session.query(ServerModel).all()
        if not servers:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No servers found"
            )

        return [self._get_server_status(server) for server in servers]

        