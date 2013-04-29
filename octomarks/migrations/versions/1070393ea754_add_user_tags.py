"""add user tags

Revision ID: 1070393ea754
Revises: d1e861f2dda
Create Date: 2013-04-28 19:23:30.461589

"""

# revision identifiers, used by Alembic.
revision = '1070393ea754'
down_revision = 'd1e861f2dda'

from alembic import op
import sqlalchemy as db


def upgrade():
    op.create_table(
        'gb_user_tags',
        db.Column('id', db.Integer, primary_key=True),
        db.Column('tag_id', db.Integer, nullable=False),
        db.Column('user_id', db.Integer, nullable=False),
    )


def downgrade():
    op.drop_table('gb_user_tags')
