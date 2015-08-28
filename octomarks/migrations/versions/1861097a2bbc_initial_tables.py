"""initial tables

Revision ID: 1861097a2bbc
Revises: None
Create Date: 2013-04-13 21:04:48.456444

"""

# revision identifiers, used by Alembic.
revision = '1861097a2bbc'
down_revision = None

from datetime import datetime
from alembic import op
import sqlalchemy as db


def now():
    return datetime.now()


def upgrade():
    op.create_table('gb_user',
        db.Column('id', db.Integer, primary_key=True),
        db.Column('github_id', db.Integer, nullable=False, unique=True),
        db.Column('github_token', db.String(256), nullable=True),
        db.Column('gravatar_id', db.String(40), nullable=False, unique=True),
        db.Column('username', db.String(80), nullable=False, unique=True),
        db.Column('gb_token', db.String(40), nullable=False, unique=True),
        db.Column('email', db.String(100), nullable=True, unique=True),
        db.Column('created_at', db.DateTime, default=now),
        db.Column('updated_at', db.DateTime, default=now),
    )
    op.create_table('gb_tag',
        db.Column('id', db.Integer, primary_key=True),
        db.Column('name', db.String(80), nullable=False, unique=True),
        db.Column('slug', db.String(80), nullable=False, unique=True),
        db.Column('created_at', db.DateTime, default=now),
        db.Column('updated_at', db.DateTime, default=now),
    )
    op.create_table('gb_bookmark',
        db.Column('id', db.Integer, primary_key=True),
        db.Column('user_id', db.Integer),
        db.Column('url', db.Text, nullable=False),
        db.Column('created_at', db.DateTime, default=now),
        db.Column('updated_at', db.DateTime, default=now),
    )
    op.create_table('gb_bookmark_tags',
        db.Column('id', db.Integer, primary_key=True),
        db.Column('tag_id', db.Integer, nullable=False),
        db.Column('bookmark_id', db.Integer, nullable=False),
    )


def downgrade():
    op.drop_table('gb_user')
    op.drop_table('gb_tag')
    op.drop_table('gb_bookmark')
    op.drop_table('gb_bookmark_tags')
