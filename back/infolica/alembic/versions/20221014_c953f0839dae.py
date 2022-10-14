"""ajout ctrl facture_domaine_ofrou au suivi_mandat

Revision ID: c953f0839dae
Revises: 583faa835866
Create Date: 2022-10-14 10:18:51.494238

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c953f0839dae'
down_revision = '583faa835866'
branch_labels = None
depends_on = None

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('suivi_mandat', sa.Column('fact_domaine_ofrou', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('suivi_mandat', 'fact_domaine_ofrou')
    # ### end Alembic commands ###
