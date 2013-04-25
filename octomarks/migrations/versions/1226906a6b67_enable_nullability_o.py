"""enable nullability on certain HttpCache fields

Revision ID: 1226906a6b67
Revises: b695424e9e8
Create Date: 2013-04-24 23:47:05.820431

"""

# revision identifiers, used by Alembic.
revision = '1226906a6b67'
down_revision = 'b695424e9e8'

from alembic import op
import sqlalchemy as db


def upgrade():
    op.alter_column("gb_http_cache", "content", nullable=True,
                    type_=db.UnicodeText)
    op.alter_column("gb_http_cache", "status_code", nullable=True,
                    type_=db.Integer)
    op.alter_column("gb_http_cache", "headers", nullable=True,
                    type_=db.UnicodeText)
    op.alter_column("gb_http_cache", "token", nullable=True,
                    type_=db.String(length=200))


def downgrade():
    op.alter_column("gb_http_cache", "token", nullable=False,
                    type_=db.String(length=200))
    op.alter_column("gb_http_cache", "headers", nullable=False,
                    type_=db.UnicodeText)
    op.alter_column("gb_http_cache", "status_code", nullable=False,
                    type_=db.Integer)
    op.alter_column("gb_http_cache", "content", nullable=False,
                    type_=db.UnicodeText)
