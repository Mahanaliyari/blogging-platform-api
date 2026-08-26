"""add foreign key to posts table

Revision ID: d6921d9ac07e
Revises: 87a67cafef45
Create Date: 2026-08-26 13:14:19.870278

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd6921d9ac07e'
down_revision: Union[str, Sequence[str], None] = '87a67cafef45'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column('owner_id', sa.Integer,nullable= False))
    op.create_foreign_key('post_users_fk', source_table= 'posts', referent_table= 'users',
                          local_cols= ['owner_id'], remote_cols=['id'], ondelete= 'CASCADE' )


def downgrade() -> None:
    op.drop_constraint("post_users_fk","posts")
    op.drop_column("posts", "owner_id")
