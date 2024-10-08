"""simplied relationships

Revision ID: c7f30a2e557a
Revises: 
Create Date: 2024-08-27 01:07:09.334197

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c7f30a2e557a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('full_name', sa.String(length=60), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('hashed_password', sa.String(length=512), nullable=False),
    sa.Column('headline', sa.String(length=200), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('changed_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('organisations',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=60), nullable=False),
    sa.Column('location', sa.String(length=60), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.Column('super_admin_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('changed_at', sa.DateTime(), nullable=True),
    sa.Column('changed_by', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['super_admin_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_organisations',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('organisation_id', sa.Integer(), nullable=False),
    sa.Column('is_administrator', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('changed_at', sa.DateTime(), nullable=True),
    sa.Column('changed_by', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'organisation_id')
    )
    op.create_table('grants',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(length=1024), nullable=False),
    sa.Column('requirements', sa.String(length=1024), nullable=False),
    sa.Column('status', sa.Enum('CREATED', 'APPLICATION', 'REVIEW', 'CLOSED', name='grantstatus'), nullable=False),
    sa.Column('organisation_id', sa.Integer(), nullable=False),
    sa.Column('created_by', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('changed_at', sa.DateTime(), nullable=True),
    sa.Column('changed_by', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['organisation_id'], ['organisations.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('applications',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(length=1024), nullable=False),
    sa.Column('applicant_id', sa.Integer(), nullable=False),
    sa.Column('grant_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.Enum('CREATED', 'SUBMITTED', 'REVIEW', 'REJECTED', 'APPROVED', name='applicationstatus'), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('changed_at', sa.DateTime(), nullable=True),
    sa.Column('changed_by', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['applicant_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['grant_id'], ['grants.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('application_files',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('application_id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=100), nullable=False),
    sa.Column('file_storage_key', sa.String(length=100), nullable=False),
    sa.Column('is_archived', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('changed_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['application_id'], ['applications.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('application_history',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('application_id', sa.Integer(), nullable=False),
    sa.Column('changed_by', sa.Integer(), nullable=False),
    sa.Column('changed_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['application_id'], ['applications.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('application_history')
    op.drop_table('application_files')
    op.drop_table('applications')
    op.drop_table('grants')
    op.drop_table('user_organisations')
    op.drop_table('organisations')
    op.drop_table('users')
    # ### end Alembic commands ###
