from datetime import datetime, timedelta
from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt, JWTError
from app.db.models import UserModel
from app.schemas import User
from decouple import config

SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')

crypt_context = CryptContext(schemes=['sha256_crypt'])

class UserUseCase:
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def user_register(self, user: User):
        user_model = UserModel(
            email = user.email,
            password = crypt_context.hash(user.password)
        )
        try:
            self.db_session.add(user_model)
            self.db_session.commit()
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='user alrealdy exists'
            )
    def user_login(self, user: User, expires_in: int = 30):
        user_on_db = self.db_session.query(UserModel).filter_by(email = user.email).first()
        if user_on_db is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='invalid username or password'
            )
        
        if not crypt_context.verify(user.password, user_on_db.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='invalid username or password'
            )
        exp = datetime.utcnow() + timedelta(minutes=expires_in)
        payload = {
            'sub': user.email,
            'exp': int(exp.timestamp())
        }

        access_tokan = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        return {
            'access_token': access_tokan,
            'exp': exp.isoformat()
        }

    def verify_token(self, access_token):
        try:
            data = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f'Invalid access token: {str(e)}'  
            )
        
        user_on_db = self.db_session.query(UserModel).filter_by(email = data['sub']).first()

        # if user_on_db is None:
        #     raise HTTPException(
        #         status_code=status.HTTP_401_UNAUTHORIZED,
        #         detail='invalid access token'
        #     )
        
        return user_on_db
    
    
    


        

    
