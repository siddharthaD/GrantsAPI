from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse

from api.api import baseapi
from settings import app_settings
from database.db import SessionLocal, get_session
from database.SeedDB import seed_data

app = FastAPI()
app.include_router(baseapi, prefix="/api")


@app.get("/")
async def root(db: Session = Depends(get_session)):
    return RedirectResponse('/docs')
    # return {"message": "Please visit /docs for swagger ui"}

@app.post("/seed")
async def seed(db: Session = Depends(get_session)):
    if app_settings.APP_SEED_DATA:
        seed_data(session=db)


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
