from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from api.dependencies import authenticate_user, create_access_token, Token
from database.db import get_session

auth = APIRouter(tags=["auth"])


@auth.post("/token", response_model=Token)
def login(username: Annotated[str, Form()], password: Annotated[str, Form()],
          db: Annotated[Session, Depends(get_session)]):
    user = authenticate_user(db, username, password)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="incorrect username or password")

    token = create_access_token(user.__dict__)
    return Token(access_token=token)
