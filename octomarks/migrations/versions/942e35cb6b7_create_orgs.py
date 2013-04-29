"""create orgs

Revision ID: 942e35cb6b7
Revises: 1070393ea754
Create Date: 2013-04-28 23:13:52.232539

"""

# revision identifiers, used by Alembic.
revision = '942e35cb6b7'
down_revision = '1070393ea754'

from datetime import datetime
from alembic import op
import sqlalchemy as db


def now():
    return datetime.now()


def upgrade():
    op.create_table(
        'gb_organization',
        db.Column('id', db.Integer, primary_key=True),
        db.Column('owner_id', db.Integer, nullable=False),
        db.Column('name', db.String(80), nullable=False),
        db.Column('email', db.String(100), nullable=False, unique=True),
        db.Column('company', db.UnicodeText, nullable=True),
        db.Column('blog', db.UnicodeText, nullable=True),
        db.Column('avatar_url', db.UnicodeText, nullable=True),
        db.Column('created_at', db.DateTime, default=now),
        db.Column('updated_at', db.DateTime, default=now),
    )
    op.create_table(
        'gb_organization_users',
        db.Column('id', db.Integer, primary_key=True),
        db.Column('user_id', db.Integer, nullable=False),
        db.Column('organization_id', db.Integer, nullable=False),
    )


def downgrade():
    op.drop_table('gb_organization')
    op.drop_table('gb_organization_users')
