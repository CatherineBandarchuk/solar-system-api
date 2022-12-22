"""update planet model add livable

Revision ID: 927e0daedb50
Revises: 953c913d5e2a
Create Date: 2022-12-21 12:45:10.302200

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '927e0daedb50'
down_revision = '953c913d5e2a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('planet', sa.Column('livable', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('planet', 'livable')
    # ### end Alembic commands ###