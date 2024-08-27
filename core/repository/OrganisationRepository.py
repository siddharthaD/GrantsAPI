import datetime

from sqlalchemy.orm import Session
from core.models.app_models import Organisation, UserOrganisation

from database.models import Organisation as OrgSchema, UserOrganisation as UsrOrgSchema


def get_org_by_id(db: Session, id: int) -> Organisation | None:
    org = db.query(OrgSchema).where(OrgSchema.id == id).one_or_none()
    return Organisation(**org.__dict__) if org else None


def update_organisation(db: Session, org_data: Organisation, user_id: int) -> bool:
    org_db = db.query(OrgSchema).where(OrgSchema.id == id).one_or_none()
    if org_db.description != org_data.description:
        org_db.description = org_data.description
    if org_db.location != org_data.location:
        org_db.location = org_data.location
    if org_db.super_admin_id != org_data.super_admin_id:
        org_db.super_admin_id = org_data.super_admin_id

    org_db.changed_at = datetime.datetime.utcnow()
    org_db.changed_by = user_id
    db.commit()


def create_organisation(db: Session, org_data: Organisation, user_id: int):
    org = OrgSchema(**org_data.__dict__)
    org.created_at = datetime.datetime.utcnow()
    org.super_admin_id = user_id
    db.add(org)
    db.commit()
    return org.id


def get_user_organisations(db: Session, user_id: int) -> list[UserOrganisation]:
    return [UserOrganisation(**usr_org.__dict__) for usr_org in
            db.query(UsrOrgSchema).where(UsrOrgSchema.user_id == user_id)]


def is_user_member_organisation(db: Session, user_id: int, organisation_id) -> bool:
    output = db.query(UsrOrgSchema).where(
        UsrOrgSchema.user_id == user_id and UsrOrgSchema.organisation_id == organisation_id).one_or_none()

    return True if output else False
