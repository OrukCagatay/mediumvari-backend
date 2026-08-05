"""add podcast fields to posts

Revision ID: 9182b857d582
Revises: cd0985e019b4
Create Date: 2026-08-03 20:20:34.302030

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9182b857d582'
down_revision: Union[str, Sequence[str], None] = 'cd0985e019b4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('audio_url', sa.String(), nullable=True))
        batch_op.add_column(sa.Column(
            'podcast_status',
            sa.Enum('none', 'pending', 'processing', 'completed', 'failed', name='podcaststatus'),
            nullable=False,
            server_default='none'
        ))


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.drop_column('podcast_status')
        batch_op.drop_column('audio_url')