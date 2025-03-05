from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.depends import get_db_session, token_verifier
from app.services.server_service import ServerService
from app.schemas import Server
from app.db.models import UserModel

router = APIRouter(prefix='/servers')

@router.post('/', status_code=status.HTTP_201_CREATED)
def server_register(
    server: Server,
    db_session: Session = Depends(get_db_session),
    user_on_db: UserModel = Depends(token_verifier)
):
    server_service = ServerService(db_session=db_session)
    server_service.create(server=server, user=user_on_db)
    
    return server_service.create(server=server, user=user_on_db)
