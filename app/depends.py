from fastapi import Depends, status
from app.db.connection import Session
from fastapi.security import OAuth2PasswordBearer
from app.services.auth_user import UserUseCase
from sqlalchemy.orm import Session as Session2
from decouple import config


SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')

oauth_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')


def get_db_session():
    try:
        session = Session()
        yield session
    finally:
        session.close()

def token_verifier(
        db_session: Session2 = Depends(get_db_session), 
        token = Depends(oauth_scheme)
):
    uc = UserUseCase(db_session=db_session)
    return uc.verify_token(token)



