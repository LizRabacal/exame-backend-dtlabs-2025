from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.depends import get_db_session, token_verifier
from app.services.server_service import ServerService

router = APIRouter(prefix='/health', dependencies=[Depends(token_verifier)])

@router.get("/all", status_code=200)
def get_all_servers_health_status(db_session: Session = Depends(get_db_session)):
    server_service = ServerService(db_session=db_session)
    servers_status = server_service.get_all_servers_health_status()
    
    return servers_status

@router.get("/{server_ulid}", status_code=200)
def get_server_health_status(server_ulid: str, db_session: Session = Depends(get_db_session)):
    server_service = ServerService(db_session=db_session)
    server_status = server_service.get_server_health_status(server_ulid=server_ulid)
    
    return server_status
