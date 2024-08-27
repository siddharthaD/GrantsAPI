from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.dependencies import get_current_user, get_password_hash
from core.models.app_models import User
from core.repository.UserRepository import update_headline, create_user
from database.db import get_session

users = APIRouter()


@users.get("/me")
async def read_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


@users.post("/headline")
async def update_headline(headline: str, current_user: Annotated[User, Depends(get_current_user)],
                          db: Annotated[Session, Depends(get_session)]):
    update_success = await update_headline(db=db, user_id=current_user.id, headline=headline)

    return {"update-success": update_success}


@users.post("/")
async def create_user(user: User, password: str, db: Annotated[Session, Depends(get_session)]):
    pwd_hash = await get_password_hash(password)
    id = await create_user(user, pwd_hash, db=db)

    return {"message": f"User created with ID :{id}"}
