"""add facture_parametres

Revision ID: 743ef3c2c7ff
Revises: 3a451b565980
Create Date: 2023-11-27 11:17:20.125711

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '743ef3c2c7ff'
down_revision = '3a451b565980'
branch_labels = None
depends_on = None

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('facture_parametres',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('nom', sa.Text(), nullable=False),
    sa.Column('valeur', sa.Float(), nullable=False),
    sa.Column('valable_de', sa.Date(), nullable=False),
    sa.Column('valable_a', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_facture_parametres')),
    schema='infolica'
    )
    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('facture_parametres', schema='infolica')
    # ### end Alembic commands ###
