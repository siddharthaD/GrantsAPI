import datetime

from sqlalchemy.orm import Session
from core.models.app_models import Grants

from database.models import Grants as GrantsSchema


def get_grant_by_id(db: Session, grant_id: int) -> Grants | None:
    grant = db.query(GrantsSchema).where(GrantsSchema.id == grant_id).one_or_none()
    return Grants(**grant.__dict__) if grant else None


def update_grant(db: Session, grant_data: Grants, user_id: int) -> bool:

    try:
        grant_db = db.query(GrantsSchema).where(GrantsSchema.id == id).one_or_none()

        if grant_db.description != grant_data.description:
            grant_db.description = grant_data.description

        if grant_db.title != grant_data.title:
            grant_db.title = grant_data.title

        if grant_db.requirements != grant_data.requirements:
            grant_db.requirements = grant_data.requirements

        if grant_db.status != grant_data.status:
            grant_db.status = grant_data.status

        grant_db.changed_at = datetime.datetime.utcnow()
        grant_db.changed_by = user_id
        db.commit()
    except Exception as e:
        return False
    return True


def create_grant(db: Session, grant_data: Grants, user_id: int):
    grant = GrantsSchema(**grant_data.__dict__)
    grant.created_at = datetime.datetime.utcnow()
    grant.created_by = user_id
    grant.changed_by = user_id
    db.add(grant)
    db.commit()
    return grant.id
