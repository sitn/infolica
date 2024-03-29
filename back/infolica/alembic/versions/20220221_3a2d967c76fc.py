"""add etape nb_jours_hors_sgrf

Revision ID: 3a2d967c76fc
Revises: efd033d9fa0a
Create Date: 2022-02-21 11:42:23.182343

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3a2d967c76fc'
down_revision = 'efd033d9fa0a'
branch_labels = None
depends_on = None

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('affaire_etape', sa.Column('nb_jours_hors_sgrf', sa.Integer(), nullable=True))
    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('affaire_etape', 'nb_jours_hors_sgrf')
    # ### end Alembic commands ###
