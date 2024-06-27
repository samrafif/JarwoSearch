"""empty message

Revision ID: 614262981be9
Revises: 26fa81a4a179
Create Date: 2024-06-27 11:12:46.850220

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '614262981be9'
down_revision = '26fa81a4a179'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('documents', schema=None) as batch_op:
        batch_op.drop_column('page_count')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('documents', schema=None) as batch_op:
        batch_op.add_column(sa.Column('page_count', sa.INTEGER(), autoincrement=False, nullable=True))

    # ### end Alembic commands ###
