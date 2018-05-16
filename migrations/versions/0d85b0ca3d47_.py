"""empty message

Revision ID: 0d85b0ca3d47
Revises: 013abd1c992d
Create Date: 2018-05-14 23:41:48.908526

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0d85b0ca3d47'
down_revision = '013abd1c992d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('blacklist_token')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blacklist_token',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('token', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='blacklist_token_pkey')
    )
    # ### end Alembic commands ###
