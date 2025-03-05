from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.depends import get_db_session
from app.services.auth_user import UserUseCase
from app.schemas import User

router = APIRouter(prefix='/auth')

@router.post('/register', status_code=status.HTTP_201_CREATED)
def user_register(user: User, db_session: Session = Depends(get_db_session)):
    user_use_case = UserUseCase(db_session=db_session)
    user_use_case.user_register(user=user)
    return {'msg': 'success'}

@router.post('/login', status_code=status.HTTP_200_OK)
def user_login(
    login_request_form: OAuth2PasswordRequestForm = Depends(),
    db_session: Session = Depends(get_db_session)
):
    user_use_case = UserUseCase(db_session=db_session)
    
    user = User(
        email=login_request_form.username,
        password=login_request_form.password
    )

    token_data = user_use_case.user_login(user=user, expires_in=60)
    return token_data
