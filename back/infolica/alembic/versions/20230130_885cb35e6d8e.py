"""add affaire_section check to affaire_type table

Revision ID: 885cb35e6d8e
Revises: d6c830d7fbfb
Create Date: 2023-01-30 16:16:17.412528

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '885cb35e6d8e'
down_revision = 'd6c830d7fbfb'
branch_labels = None
depends_on = None

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('affaire_type', sa.Column('affaire_section_suivi', sa.Boolean(), server_default=sa.text('true'), nullable=True))
    op.add_column('affaire_type', sa.Column('affaire_section_preavis', sa.Boolean(), server_default=sa.text('false'), nullable=True))
    op.add_column('affaire_type', sa.Column('affaire_section_numeros', sa.Boolean(), server_default=sa.text('true'), nullable=True))
    op.add_column('affaire_type', sa.Column('affaire_section_facture', sa.Boolean(), server_default=sa.text('false'), nullable=True))
    op.add_column('affaire_type', sa.Column('affaire_section_ctrl_chefprojet_mo', sa.Boolean(), server_default=sa.text('false'), nullable=True))
    op.add_column('affaire_type', sa.Column('affaire_section_ctrl_chefprojet_ppe', sa.Boolean(), server_default=sa.text('false'), nullable=True))
    op.add_column('affaire_type', sa.Column('affaire_section_ctrl_coordprojets', sa.Boolean(), server_default=sa.text('false'), nullable=True))
    op.add_column('affaire_type', sa.Column('affaire_section_ctrl_geometre', sa.Boolean(), server_default=sa.text('false'), nullable=True))
    op.add_column('affaire_type', sa.Column('affaire_section_documents', sa.Boolean(), server_default=sa.text('true'), nullable=True))
    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('affaire_type', 'affaire_section_documents')
    op.drop_column('affaire_type', 'affaire_section_ctrl_geometre')
    op.drop_column('affaire_type', 'affaire_section_ctrl_coordprojets')
    op.drop_column('affaire_type', 'affaire_section_ctrl_chefprojet_ppe')
    op.drop_column('affaire_type', 'affaire_section_ctrl_chefprojet_mo')
    op.drop_column('affaire_type', 'affaire_section_facture')
    op.drop_column('affaire_type', 'affaire_section_numeros')
    op.drop_column('affaire_type', 'affaire_section_preavis')
    op.drop_column('affaire_type', 'affaire_section_suivi')
    # ### end Alembic commands ###
