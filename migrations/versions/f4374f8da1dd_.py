"""empty message

Revision ID: f4374f8da1dd
Revises: f139d4e01260
Create Date: 2018-07-03 10:37:51.731629

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f4374f8da1dd'
down_revision = 'f139d4e01260'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('kitchen', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'kitchen')
    # ### end Alembic commands ###
