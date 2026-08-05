"""add version tracking and outdated status for translations/podcasts

Revision ID: 065e26c0c235
Revises: a5eec79ceddb
Create Date: 2026-08-05 19:12:24.369289

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '065e26c0c235'
down_revision: Union[str, Sequence[str], None] = 'a5eec79ceddb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table('post_translations', schema=None) as batch_op:
        batch_op.add_column(sa.Column('source_version', sa.Integer(), nullable=False, server_default='1'))

    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('version', sa.Integer(), nullable=False, server_default='1'))


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.drop_column('version')

    with op.batch_alter_table('post_translations', schema=None) as batch_op:
        batch_op.drop_column('source_version')