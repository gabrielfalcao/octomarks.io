"""creating sale table

Revision ID: a6de9d7f3ea
Revises: 23e54f7ee497
Create Date: 2013-06-26 15:08:42.247039

"""

# revision identifiers, used by Alembic.
revision = 'a6de9d7f3ea'
down_revision = '23e54f7ee497'

from datetime import datetime
from alembic import op
import sqlalchemy as db


def now():
    return datetime.now()


def upgrade():
    op.create_table(
        'gb_user',
        db.Column('id', db.Integer, primary_key=True),
        db.Column('github_id', db.Integer, nullable=False, unique=True),
        db.Column('github_token', db.String(256), nullable=True),
        db.Column('gravatar_id', db.String(40), nullable=False, unique=True),
        db.Column('username', db.String(80), nullable=False, unique=True),
        db.Column('gb_token', db.String(40), nullable=False, unique=True),
        db.Column('email', db.String(100), nullable=False, unique=True),
        db.Column('created_at', db.DateTime, default=now),
        db.Column('default_theme_name', db.String(255), default='tango',
                  nullable=False),
        db.Column('updated_at', db.DateTime, default=now),
    )


def downgrade():
    pass
