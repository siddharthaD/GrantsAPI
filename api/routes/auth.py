import json
from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status
from api.dependencies import verify_password
from core.repository import UserRepository
from database.db import get_session

auth = APIRouter(tags=["auth"])


@auth.post("/token")
def login(username: Annotated[str, Form()], password: Annotated[str, Form()],
          db: Annotated[Session, Depends(get_session)]):
    user = UserRepository.get_user_by_id(db=db, id=1)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="incorrect username or password")

    pwd = UserRepository.get_user_password(db=db, user_id=user.id)
    if not verify_password(pwd, password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": {user.email}, "token_type": "bearer"}
