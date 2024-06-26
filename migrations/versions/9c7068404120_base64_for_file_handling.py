"""base64 for file handling

Revision ID: 9c7068404120
Revises: 27ce56bd107b
Create Date: 2024-03-29 03:07:13.655103

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '9c7068404120'
down_revision = '27ce56bd107b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('image', 'filename',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    op.alter_column('image', 'data',
               existing_type=postgresql.BYTEA(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('image', 'data',
               existing_type=postgresql.BYTEA(),
               nullable=True)
    op.alter_column('image', 'filename',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    # ### end Alembic commands ###
