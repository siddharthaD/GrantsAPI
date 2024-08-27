import datetime

from sqlalchemy import String, DateTime, Enum, Column, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase, relationship
import datetime
from enum import Enum as PyEnum


class GrantStatus(PyEnum):
    CREATED = 'Created'
    APPLICATION = 'Application'
    REVIEW = 'Review'
    CLOSED = 'Closed'


class ApplicationStatus(PyEnum):
    CREATED = 'Created'
    SUBMITTED = 'Submitted'
    REVIEW = 'Review'
    REJECTED = 'Rejected'
    APPROVED = 'Approved'


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String(60))
    email: Mapped[str] = mapped_column(String(255))
    hashed_password: Mapped[str] = mapped_column(String(512))
    headline: Mapped[str] = mapped_column(String(200))
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.datetime.utcnow())
    changed_at: Mapped[DateTime | None] = mapped_column(DateTime)

    applications = relationship('Applications', back_populates='applicant')


class Organisation(Base):
    __tablename__ = "organisations"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(60))
    location: Mapped[str] = mapped_column(String(60))
    description: Mapped[str] = mapped_column(String(255))
    super_admin_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.datetime.utcnow())
    changed_at: Mapped[DateTime | None] = mapped_column(DateTime)
    changed_by: Mapped[int]
    grants = relationship('Grants', back_populates='organisation')


class UserOrganisation(Base):
    __tablename__ = "user_organisations"
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
    organisation_id: Mapped[int] = mapped_column(primary_key=True)
    is_administrator: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.datetime.utcnow())
    changed_at: Mapped[DateTime | None] = mapped_column(DateTime)
    changed_by: Mapped[int | None]



class Grants(Base):
    __tablename__ = "grants"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(1024))
    requirements: Mapped[str] = mapped_column(String(1024))
    status: Mapped[str] = mapped_column(Enum(GrantStatus))
    organisation_id: Mapped[int] = mapped_column(ForeignKey('organisations.id'))
    created_by: Mapped[int]
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.datetime.utcnow())
    changed_at: Mapped[DateTime | None] = mapped_column(DateTime)
    changed_by: Mapped[int]

    organisation = relationship('Organisation', back_populates='grants')


class Applications(Base):
    __tablename__ = "applications"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(1024))
    applicant_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    grant_id: Mapped[int] = mapped_column(ForeignKey('grants.id'))
    status: Mapped[str] = mapped_column(Enum(ApplicationStatus))
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.datetime.utcnow())
    changed_at: Mapped[DateTime | None] = mapped_column(DateTime, default=datetime.datetime.utcnow())
    changed_by: Mapped[int]

    applicant = relationship('User', foreign_keys=[applicant_id], back_populates='applications')
    history = relationship('ApplicationHistory', back_populates='application')
    files = relationship('ApplicationFiles',back_populates='application')


class ApplicationFiles(Base):
    __tablename__ = "application_files"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    application_id: Mapped[int] = mapped_column(ForeignKey('applications.id'))
    description: Mapped[str] = mapped_column(String(100))
    file_storage_key: Mapped[str] = mapped_column(String(100))
    is_archived: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.datetime.utcnow())
    changed_at: Mapped[DateTime | None] = mapped_column(DateTime)

    application = relationship('Applications',back_populates='files')

class ApplicationHistory(Base):
    __tablename__ = "application_history"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    application_id: Mapped[int] = mapped_column(ForeignKey('applications.id'))
    changed_by: Mapped[int]
    changed_at: Mapped[DateTime | None] = mapped_column(DateTime)

    application = relationship('Applications', back_populates='history')