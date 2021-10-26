"""fix ctrl geometre

Revision ID: b8e660727760
Revises: 826c2810ab30
Create Date: 2021-09-13 16:03:42.906015

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'b8e660727760'
down_revision = '826c2810ab30'
branch_labels = None
depends_on = None

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('controle_geometre', sa.Column('check_66', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('controle_geometre', 'check_66')
    # ### end Alembic commands ###