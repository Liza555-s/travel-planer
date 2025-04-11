"""Initial migration

Revision ID: e6873567afaa
Revises: 
Create Date: 2025-03-28 13:05:21.219831

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e6873567afaa'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('place_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_post_place_id', 'place', ['place_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_constraint('fk_post_place_id', type_='foreignkey')
        batch_op.drop_column('place_id')

    # ### end Alembic commands ###
