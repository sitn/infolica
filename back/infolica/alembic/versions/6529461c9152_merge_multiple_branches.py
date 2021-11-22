"""merge multiple branches

Revision ID: 6529461c9152
Revises: 72499d23d034, f013078b6c2f
Create Date: 2021-11-05 10:42:28.553987

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6529461c9152'
down_revision = ('72499d23d034', 'f013078b6c2f')
branch_labels = None
depends_on = None

def upgrade():
    pass

def downgrade():
    pass
