from datetime import datetime

from pydantic import BaseModel

from database.models import GrantStatus, ApplicationStatus


class Token(BaseModel):
    access_token: str
    token_type: str = "Bearer"


class TokenData(BaseModel):
    email: str
    full_name: str | None = None
    id: int


class UserBase(BaseModel):
    email: str
    full_name: str


class User(UserBase):
    id: int
    created_at: datetime | None
    changed_at: datetime | None = None
    headline: str | None = None


class UserDB(User):
    password: str


class Organisation(BaseModel):
    id: int
    name: str
    location: str
    description: str
    super_admin_id: int
    created_at: datetime
    changed_at: datetime
    changed_by: int


class UserOrganisation(BaseModel):
    user_id: int
    organisation_id: int
    is_administrator: bool
    created_at: datetime
    changed_at: datetime
    changed_by: int


class Grants(BaseModel):
    id: int
    title: str
    description: str
    requirements: str
    status: GrantStatus
    organisation_id: int
    created_by: int
    created_at: datetime
    changed_at: datetime
    changed_by: int


class ApplicationBase(BaseModel):
    title: str
    description: str


class ApplicationFilesBase(BaseModel):
    description: str
    file_storage_key: str


class ApplicationFiles(ApplicationFilesBase):
    id: int
    is_archived: bool
    created_at: datetime
    changed_at: datetime


class ApplicationHistory(BaseModel):
    id: int
    old_status: str
    new_status: str
    remarks: str
    changed_by: int
    changed_at: datetime


class Applications(ApplicationBase):
    id: int
    status: ApplicationStatus
    created_at: datetime
    changed_at: datetime
    changed_by: int
    applicant: User
    grant: Grants

    history: list[ApplicationHistory]
    files: list[ApplicationFiles]


class ApplicationCreate(ApplicationBase):
    grant_id: int
    applicant_id: int
