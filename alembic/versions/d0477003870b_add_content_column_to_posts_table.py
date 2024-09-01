"""add content column to posts table

Revision ID: d0477003870b
Revises: c764e935109d
Create Date: 2024-09-01 14:12:08.796795

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd0477003870b'
down_revision: Union[str, None] = 'c764e935109d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.Text(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
