"""cache table

Revision ID: 1b2bf3070e6a
Revises: 1861097a2bbc
Create Date: 2013-04-13 21:05:20.854618

"""

# revision identifiers, used by Alembic.
revision = '1b2bf3070e6a'
down_revision = '1861097a2bbc'

from datetime import datetime
from alembic import op
import sqlalchemy as db


def now():
    return datetime.now()


def upgrade():
    op.create_table(
        'gb_http_cache',
        db.Column('id', db.Integer, primary_key=True),
        db.Column('url', db.Unicode(length=200), nullable=False, unique=True),
        db.Column('token', db.String(length=200), nullable=False, unique=True),
        db.Column('content', db.UnicodeText, nullable=False),
        db.Column('status_code', db.Integer, nullable=False),
        db.Column('updated_at', db.DateTime, default=now)
    )


def downgrade():
    op.drop_table('gb_http_cache')
