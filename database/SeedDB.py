from typing import Annotated, Generator

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from database.models import User


def seed_data(session: Session):
    user1 = User(full_name="Cheetah", email="cheetha@123.com", hashed_password="123dumpy",
                 headline="I am just a employee")
    session.add(user1)
    usrDbRec = session.query(User).first()
    print(usrDbRec.id)
    # session.add(user1)
