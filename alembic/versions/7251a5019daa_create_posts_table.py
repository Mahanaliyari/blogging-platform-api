"""create posts table

Revision ID: 7251a5019daa
Revises: 
Create Date: 2026-08-26 10:49:32.117689

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7251a5019daa'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Function for doing the action
def upgrade() -> None:
    op.create_table("posts", sa.Column("id",sa.Integer,nullable= False, primary_key= True),
                    sa.Column("title", sa.String,nullable = False)) 
                   


# Function to undo the action 
def downgrade() -> None:
    op.drop_table("posts")