"""empty message

Revision ID: 4fa15768bea4
Revises: c088d36a5ece
Create Date: 2016-12-03 16:35:08.699666

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4fa15768bea4'
down_revision = 'c088d36a5ece'
branch_labels = None
depends_on = None


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('parsed', sa.Text(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('comments', 'parsed')
    ### end Alembic commands ###
