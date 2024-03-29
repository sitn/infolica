"""controle étape

Revision ID: a35fb9eedd8c
Revises: 6529461c9152
Create Date: 2021-12-10 15:44:01.206334

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a35fb9eedd8c'
down_revision = '6529461c9152'
branch_labels = None
depends_on = None

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('controle_etape',
    sa.Column('nom', sa.String(length=40), nullable=False),
    sa.Column('etape_id', sa.BigInteger(), nullable=True),
    sa.Column('force', sa.String(length=15), nullable=True),
    sa.Column('detail', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['etape_id'], ['infolica.affaire_etape_index.id'], name=op.f('fk_controle_etape_etape_id_affaire_etape_index')),
    sa.PrimaryKeyConstraint('nom', name=op.f('pk_controle_etape')),
    schema='infolica'
    )
    op.create_table('controle_etape_type_affaire',
    sa.Column('affaire_type_id', sa.BigInteger(), nullable=False),
    sa.Column('controle_etape_nom', sa.String(length=40), nullable=False),
    sa.ForeignKeyConstraint(['affaire_type_id'], ['infolica.affaire_type.id'], name=op.f('fk_controle_etape_type_affaire_affaire_type_id_affaire_type')),
    sa.ForeignKeyConstraint(['controle_etape_nom'], ['infolica.controle_etape.nom'], name=op.f('fk_controle_etape_type_affaire_controle_etape_nom_controle_etape')),
    sa.PrimaryKeyConstraint('affaire_type_id', 'controle_etape_nom', name=op.f('pk_controle_etape_type_affaire')),
    schema='infolica'
    )
    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('controle_etape_type_affaire', schema='infolica')
    op.drop_table('controle_etape', schema='infolica')
    # ### end Alembic commands ###
