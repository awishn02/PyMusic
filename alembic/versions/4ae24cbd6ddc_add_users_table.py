"""add users table

Revision ID: 4ae24cbd6ddc
Revises: 56b2d32003b8
Create Date: 2014-04-28 11:19:40.592658

"""

# revision identifiers, used by Alembic.
revision = '4ae24cbd6ddc'
down_revision = '56b2d32003b8'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    ### end Alembic commands ###
