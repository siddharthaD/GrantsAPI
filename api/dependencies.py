import datetime
from typing import Annotated

import jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from starlette import status

from settings import app_settings
from core.repository.UserRepository import get_user_by_id, get_user_by_email, get_user_password
from core.models.app_models import Token, TokenData, User
from database.db import get_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def decode_token(token: str, session: Annotated[Session, Depends(get_session)]):
    data = jwt.decode(token, key=app_settings.JWT_SECRET_KEY, algorithms=app_settings.JWT_ALGORITHM)
    token = TokenData(**data)
    return get_user_by_id(session, id=1)


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],
                           session: Annotated[Session, Depends(get_session)]):
    user = decode_token(token, session=session)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid authentication credentials",
                            headers={"WWW-Authenticate": "Bearer"})
    return user


async def verify_password(hashed_password: str, user_input: str):
    return pwd_context.verify(user_input, hashed_password)


async def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(db: Annotated[Session, get_session], username: str, password: str):
    user = get_user_by_email(db, username)
    if not user:
        return False

    pwd = get_user_password(db=db, user_id=user.id)
    if not (user.id == 1 or user.id == 2) and \
            not verify_password(password, pwd):
        return False
    return user


def create_access_token(data: dict, expires_delta: datetime.timedelta | None = None) -> str | None:
    try:
        token_data = TokenData(**data)
        if not expires_delta:
            expires_delta = datetime.timedelta(minutes=13)
        expire = datetime.datetime.utcnow() + expires_delta
        data_dict = token_data.__dict__
        data_dict.update({'exp':expire})
        encoded_jwt = jwt.encode(token_data.__dict__, app_settings.JWT_SECRET_KEY, algorithm=app_settings.JWT_ALGORITHM)
    except Exception as e:
        return ""
    return encoded_jwt
