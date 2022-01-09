"""add content column to posts table

Revision ID: b609a773b3e5
Revises: 80d5bc23a531
Create Date: 2022-01-09 15:34:37.877519

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b609a773b3e5'
down_revision = '80d5bc23a531'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
