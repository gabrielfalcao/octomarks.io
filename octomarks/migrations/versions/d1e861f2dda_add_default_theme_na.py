"""add default theme name field to user

Revision ID: d1e861f2dda
Revises: 1226906a6b67
Create Date: 2013-04-25 00:42:58.513540

"""

# revision identifiers, used by Alembic.
revision = 'd1e861f2dda'
down_revision = '1226906a6b67'


from alembic import op
import sqlalchemy as db


def upgrade():
    op.add_column('gb_user',
                  db.Column('default_theme_name', db.String(255), nullable=True))


def downgrade():
    op.drop_column('gb_user', 'default_theme_name')
