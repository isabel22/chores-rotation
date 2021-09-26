"""empty message

Revision ID: 60d8221f43e2
Revises: d55365651569
Create Date: 2021-09-26 17:30:53.816736

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '60d8221f43e2'
down_revision = 'd55365651569'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'users', ['email'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    # ### end Alembic commands ###
