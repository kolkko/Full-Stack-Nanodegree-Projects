"""empty message

Revision ID: 438b315b6cc1
Revises: 01eb64bcfc5a
Create Date: 2020-11-30 15:28:17.698380

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '438b315b6cc1'
down_revision = '01eb64bcfc5a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('shows', sa.Column('start_time', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('shows', 'start_time')
    # ### end Alembic commands ###
