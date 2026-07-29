"""add category model

Revision ID: ee8e4ea276a2
Revises: 932e892c17f9
Create Date: 2026-07-24 10:08:40.171376

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ee8e4ea276a2'
down_revision: Union[str, Sequence[str], None] = '932e892c17f9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('category_id', sa.Integer(), nullable=True))
        batch_op.create_index(batch_op.f('ix_posts_category_id'), ['category_id'], unique=False)
        batch_op.create_foreign_key(
            'fk_posts_category_id_categories',
            'categories', ['category_id'], ['id']
        )


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.drop_constraint(
            'fk_posts_category_id_categories',
            type_='foreignkey'
        )
        batch_op.drop_index(batch_op.f('ix_posts_category_id'))
        batch_op.drop_column('category_id')

    op.drop_table('categories')