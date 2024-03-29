"""ajout table preavis_glossaire

Revision ID: bb9331cedec2
Revises: 39d1b5c44dee
Create Date: 2022-06-16 14:17:20.398489

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bb9331cedec2'
down_revision = '39d1b5c44dee'
branch_labels = None
depends_on = None

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('preavis_glossaire',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('service_id', sa.BigInteger(), nullable=False),
    sa.Column('ordre', sa.Integer(), nullable=True),
    sa.Column('titre', sa.Text(), nullable=False),
    sa.Column('texte', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['service_id'], ['infolica.service.id'], name=op.f('fk_preavis_glossaire_service_id_service')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_preavis_glossaire')),
    schema='infolica'
    )
    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('preavis_glossaire', schema='infolica')
    # ### end Alembic commands ###
