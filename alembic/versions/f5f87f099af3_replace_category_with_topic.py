"""replace category with topic

Revision ID: f5f87f099af3
Revises: 188ae75dee9a
Create Date: 2026-07-27 10:02:40.962889

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f5f87f099af3'
down_revision: Union[str, Sequence[str], None] = '188ae75dee9a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('topics',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False, unique=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('topics', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_topics_name'), ['name'], unique=True)

    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('topic_id', sa.Integer(), nullable=True))
        batch_op.drop_index(batch_op.f('ix_posts_category_id'))
        batch_op.create_index(batch_op.f('ix_posts_topic_id'), ['topic_id'], unique=False)
        batch_op.drop_constraint(batch_op.f('fk_posts_category_id_categories'), type_='foreignkey')
        batch_op.create_foreign_key(
            'fk_posts_topic_id_topics',
            'topics', ['topic_id'], ['id']
        )
        batch_op.drop_column('category_id')

    op.drop_table('categories')


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('category_id', sa.INTEGER(), nullable=True))
        batch_op.drop_constraint(
            'fk_posts_topic_id_topics',   # ✅ aynı isim
            type_='foreignkey'
        )
        batch_op.create_foreign_key(
            batch_op.f('fk_posts_category_id_categories'),
            'categories', ['category_id'], ['id']
        )
        batch_op.drop_index(batch_op.f('ix_posts_topic_id'))
        batch_op.create_index(batch_op.f('ix_posts_category_id'), ['category_id'], unique=False)
        batch_op.drop_column('topic_id')

    op.create_table('categories',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(), nullable=False),
    sa.Column('created_at', sa.DATETIME(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    with op.batch_alter_table('topics', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_topics_name'))

    op.drop_table('topics')