"""add start and end date to services

Revision ID: 7f61c1192ef6
Revises: 1317c98cd991
Create Date: 2024-03-21 11:54:07.109451

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7f61c1192ef6'
down_revision = '1317c98cd991'
branch_labels = None
depends_on = None

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('service', sa.Column('date_entree', sa.Date(), nullable=True))
    op.add_column('service', sa.Column('date_sortie', sa.Date(), nullable=True))
    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('service', 'date_sortie')
    op.drop_column('service', 'date_entree')
    # ### end Alembic commands ###
