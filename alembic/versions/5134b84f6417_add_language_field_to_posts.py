"""add language field to posts

Revision ID: 5134b84f6417
Revises: 9182b857d582
Create Date: 2026-08-04 12:16:16.716151

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5134b84f6417'
down_revision: Union[str, Sequence[str], None] = '9182b857d582'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('language', sa.String(), nullable=False, server_default='en'))


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.drop_column('language')