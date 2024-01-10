"""fix models emoluments

Revision ID: 1317c98cd991
Revises: 743ef3c2c7ff
Create Date: 2023-12-14 11:45:14.566991

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1317c98cd991'
down_revision = '743ef3c2c7ff'
branch_labels = None
depends_on = None

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tableau_emoluments', sa.Column('categorie_id', sa.Integer(), nullable=True))
    op.add_column('tableau_emoluments', sa.Column('sous_categorie_id', sa.Integer(), nullable=True))
    op.add_column('tableau_emoluments', sa.Column('nom_auto', sa.Boolean(), nullable=True))
    op.add_column('tableau_emoluments', sa.Column('champ_editable', sa.Boolean(), nullable=True))
    op.add_column('tableau_emoluments', sa.Column('calcul_auto', sa.Text(), nullable=True))
    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tableau_emoluments', 'calcul_auto')
    op.drop_column('tableau_emoluments', 'champ_editable')
    op.drop_column('tableau_emoluments', 'nom_auto')
    op.drop_column('tableau_emoluments', 'sous_categorie_id')
    op.drop_column('tableau_emoluments', 'categorie_id')
    # ### end Alembic commands ###