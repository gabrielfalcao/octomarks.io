"""add unique constraint for url + token

Revision ID: b695424e9e8
Revises: 273eff505736
Create Date: 2013-04-13 23:54:39.619365

"""

# revision identifiers, used by Alembic.
revision = 'b695424e9e8'
down_revision = '273eff505736'

from alembic import op


def upgrade():
    op.drop_constraint('url', 'gb_http_cache', 'unique')
    op.drop_constraint('token', 'gb_http_cache', 'unique')


def downgrade():
    op.create_unique_constraint("url", "gb_http_cache", ["url"])
    op.create_unique_constraint("token", "gb_http_cache", ["token"])
