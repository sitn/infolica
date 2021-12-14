"""fix foreign keys on emoluments

Revision ID: 00fffec915db
Revises: a35fb9eedd8c
Create Date: 2021-12-13 12:32:03.563530

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '00fffec915db'
down_revision = 'a35fb9eedd8c'
branch_labels = None
depends_on = None

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(op.f('fk_emolument_tableau_emolument_id_tableau_emoluments'), 'emolument', 'tableau_emoluments', ['tableau_emolument_id'], ['id'], source_schema='infolica', referent_schema='infolica')
    op.create_foreign_key(op.f('fk_emolument_emolument_affaire_id_emolument_affaire'), 'emolument', 'emolument_affaire', ['emolument_affaire_id'], ['id'], source_schema='infolica', referent_schema='infolica')
    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('fk_emolument_emolument_affaire_id_emolument_affaire'), 'emolument', schema='infolica', type_='foreignkey')
    op.drop_constraint(op.f('fk_emolument_tableau_emolument_id_tableau_emoluments'), 'emolument', schema='infolica', type_='foreignkey')
    # ### end Alembic commands ###