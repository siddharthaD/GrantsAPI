from typing import Annotated

from fastapi import APIRouter, Depends

from api.dependencies import oauth2_scheme, get_current_user, User
from api.routes.auth import auth
from api.routes.grants import grants

baseapi = APIRouter()
baseapi.include_router(auth, prefix="/auth")
baseapi.include_router(grants, prefix='/grants', tags=["Grants"])


@baseapi.get("/")
async def hello(current_user: Annotated[User, Depends(get_current_user)]):
    """

    :param current_user:
    :type token: object
    """
    return {"message": "One more hello", "token": current_user}
