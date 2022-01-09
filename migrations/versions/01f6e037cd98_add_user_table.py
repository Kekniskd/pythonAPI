"""add user table

Revision ID: 01f6e037cd98
Revises: b609a773b3e5
Create Date: 2022-01-09 15:40:40.279666

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.schema import PrimaryKeyConstraint, UniqueConstraint


# revision identifiers, used by Alembic.
revision = '01f6e037cd98'
down_revision = 'b609a773b3e5'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade():
    op.drop_table('users')
    pass
