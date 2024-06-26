"""empty message

Revision ID: b9af48ea6316
Revises: 9c7068404120
Create Date: 2024-03-30 23:21:38.773841

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b9af48ea6316'
down_revision = '9c7068404120'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('image', 'user_id',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.drop_constraint('image_user_id_fkey', 'image', type_='foreignkey')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key('image_user_id_fkey', 'image', 'user', ['user_id'], ['id'])
    op.alter_column('image', 'user_id',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###
