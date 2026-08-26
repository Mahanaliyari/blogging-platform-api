"""add new columns to posts table

Revision ID: 722ef8d2caf6
Revises: d6921d9ac07e
Create Date: 2026-08-26 13:32:16.181624

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '722ef8d2caf6'
down_revision: Union[str, Sequence[str], None] = 'd6921d9ac07e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
     op.add_column("posts",sa.Column("published", sa.Boolean, nullable= False, server_default= 'True'))
     op.add_column("posts",sa.Column("created_at", sa.TIMESTAMP(timezone=True),
                                     server_default= sa.text('now()'), nullable= False))


def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")