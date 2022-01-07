"""第五次

Revision ID: 61202874fcf3
Revises: 0aa73a40d9da
Create Date: 2022-01-05 22:37:28.121000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '61202874fcf3'
down_revision = '0aa73a40d9da'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('t_meun', sa.Column('Level', sa.Integer(), nullable=True))
    op.drop_column('t_meun', 'pid')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('t_meun', sa.Column('pid', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_column('t_meun', 'Level')
    # ### end Alembic commands ###
