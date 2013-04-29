"""adding log table

Revision ID: 23e54f7ee497
Revises: 942e35cb6b7
Create Date: 2013-04-29 12:29:58.590582

"""

# revision identifiers, used by Alembic.
revision = '23e54f7ee497'
down_revision = '942e35cb6b7'


from datetime import datetime
from alembic import op
import sqlalchemy as db


def now():
    return datetime.now()


def upgrade():
    op.create_table(
        'gb_log',
        db.Column('id', db.Integer, primary_key=True),
        db.Column('user_id', db.Integer, nullable=True),
        db.Column('message', db.UnicodeText, nullable=True),
        db.Column('data', db.UnicodeText, nullable=True),
        db.Column('created_at', db.DateTime, default=now),
    )


def downgrade():
    op.drop_table('gb_log')
