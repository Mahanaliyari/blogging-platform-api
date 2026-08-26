"""add content column to posts table

Revision ID: 2dd81234038e
Revises: 7251a5019daa
Create Date: 2026-08-26 11:02:52.979918

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2dd81234038e'
down_revision: Union[str, Sequence[str], None] = '7251a5019daa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# add the content column 
def upgrade() -> None:
    op.add_column("posts",sa.Column("content", sa.String, nullable = False))


# delete the content column 
def downgrade() -> None:
    op.drop_column("posts", "content")
