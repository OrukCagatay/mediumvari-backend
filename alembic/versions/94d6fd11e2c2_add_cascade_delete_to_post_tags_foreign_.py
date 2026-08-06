"""add cascade delete to post_tags foreign keys

Revision ID: 94d6fd11e2c2
Revises: 065e26c0c235
Create Date: 2026-08-06 12:34:56.512458

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '94d6fd11e2c2'
down_revision: Union[str, Sequence[str], None] = '065e26c0c235'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table('post_tags', schema=None) as batch_op:
        batch_op.drop_constraint('fk_post_tags_post_id_posts', type_='foreignkey')
        batch_op.drop_constraint('fk_post_tags_tag_id_tags', type_='foreignkey')
        batch_op.create_foreign_key(batch_op.f('fk_post_tags_tag_id_tags'), 'tags', ['tag_id'], ['id'], ondelete='CASCADE')
        batch_op.create_foreign_key(batch_op.f('fk_post_tags_post_id_posts'), 'posts', ['post_id'], ['id'], ondelete='CASCADE')


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('post_tags', schema=None) as batch_op:
        batch_op.drop_constraint('fk_post_tags_post_id_posts', type_='foreignkey')
        batch_op.drop_constraint('fk_post_tags_tag_id_tags', type_='foreignkey')
        batch_op.create_foreign_key('fk_post_tags_tag_id_tags', 'tags', ['tag_id'], ['id'])
        batch_op.create_foreign_key('fk_post_tags_post_id_posts', 'posts', ['post_id'], ['id'])