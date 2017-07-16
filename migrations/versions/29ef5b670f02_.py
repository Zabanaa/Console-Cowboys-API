"""empty message

Revision ID: 29ef5b670f02
Revises: 7a969cfa89c7
Create Date: 2017-07-16 11:17:48.470678

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '29ef5b670f02'
down_revision = '7a969cfa89c7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'job', ['listing_url'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'job', type_='unique')
    # ### end Alembic commands ###
