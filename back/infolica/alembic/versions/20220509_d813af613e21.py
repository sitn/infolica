"""ajout contrôle bâtiment

Revision ID: d813af613e21
Revises: 3a2d967c76fc
Create Date: 2022-05-09 10:14:19.740324

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd813af613e21'
down_revision = '3a2d967c76fc'
branch_labels = None
depends_on = None

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('controle_mutation', sa.Column('bat_4', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('controle_mutation', 'bat_4')
    # ### end Alembic commands ###
