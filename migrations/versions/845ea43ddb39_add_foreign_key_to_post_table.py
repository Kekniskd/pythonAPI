"""add foreign-key to post table

Revision ID: 845ea43ddb39
Revises: 01f6e037cd98
Create Date: 2022-01-09 15:55:49.711612

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '845ea43ddb39'
down_revision = '01f6e037cd98'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts",  referent_table="users", local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
