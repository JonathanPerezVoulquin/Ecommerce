"""empty message

Revision ID: ac0a426342a6
Revises: a708eb639974
Create Date: 2022-01-09 17:44:19.847890

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ac0a426342a6'
down_revision = 'a708eb639974'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('customer_order', 'invoice')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('customer_order', sa.Column('invoice', sa.VARCHAR(length=20), nullable=False))
    # ### end Alembic commands ###
