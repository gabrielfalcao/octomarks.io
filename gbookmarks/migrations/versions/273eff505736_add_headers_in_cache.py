"""add headers in cache table

Revision ID: 273eff505736
Revises: 1b2bf3070e6a
Create Date: 2013-04-13 23:10:35.699654

"""

# revision identifiers, used by Alembic.
revision = '273eff505736'
down_revision = '1b2bf3070e6a'

from alembic import op
import sqlalchemy as db


def upgrade():
    op.add_column('gb_http_cache',
                  db.Column('headers', db.UnicodeText, nullable=False))


def downgrade():
    op.remove_column('gb_http_cache',
                     db.Column('headers', db.UnicodeText, nullable=False))
