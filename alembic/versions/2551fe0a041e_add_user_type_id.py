"""add user type id

Revision ID: 2551fe0a041e
Revises: 140949976ecb
Create Date: 2014-05-04 23:52:44.739433

"""

# revision identifiers, used by Alembic.
revision = '2551fe0a041e'
down_revision = '140949976ecb'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('user_type_id', sa.Integer(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'user_type_id')
    ### end Alembic commands ###
