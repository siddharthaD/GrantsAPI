import datetime

from sqlalchemy.orm import Session
from core.models.app_models import User, UserDB
from database.models import User as UserSchema


def get_user_by_id(db: Session, id: int) -> User | None:
    user = db.query(UserSchema).where(UserSchema.id == id).one_or_none()
    return User(**user.__dict__) if user else None


def get_user_by_email(db: Session, email: str) -> User | None:
    user = db.query(UserSchema).where(UserSchema.email == email).one_or_none()
    return User(**user.__dict__) if user else None


def get_user_password(db: Session, user_id: int) -> str | None:
    pwd = db.query(UserSchema.hashed_password).where(UserSchema.id == user_id).scalar()
    return pwd if pwd else None


def update_headline(db: Session, user_id: int, headline: str) -> bool:
    user = db.query(UserSchema).where(UserSchema.id == id).one_or_none()
    user.headline = headline
    user.changed_at = datetime.datetime.utcnow()
    db.commit()


def create_user(db:Session,userData:UserDB):
    user = UserSchema(**userData.__dict__)
    user.created_at = datetime.datetime.utcnow()
    db.add(user)
    db.commit()
    return user.id

