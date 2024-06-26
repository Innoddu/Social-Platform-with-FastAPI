"""Add autoincrement to feeds.id

Revision ID: 45f69482cd18
Revises: a81e280d8739
Create Date: 2024-05-26 09:16:18.218684

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '45f69482cd18'
down_revision: Union[str, None] = 'a81e280d8739'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_feeds_id', table_name='feeds')
    op.drop_index('ix_feeds_title', table_name='feeds')
    op.drop_table('feeds')
    op.drop_index('ix_comments_id', table_name='comments')
    op.drop_table('comments')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comments',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('content', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('author_email', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('feed_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['author_email'], ['users.email'], name='comments_author_email_fkey'),
    sa.ForeignKeyConstraint(['feed_id'], ['feeds.id'], name='comments_feed_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='comments_pkey')
    )
    op.create_index('ix_comments_id', 'comments', ['id'], unique=False)
    op.create_table('feeds',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('content', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('author_email', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['author_email'], ['users.email'], name='feeds_author_email_fkey'),
    sa.PrimaryKeyConstraint('id', name='feeds_pkey')
    )
    op.create_index('ix_feeds_title', 'feeds', ['title'], unique=False)
    op.create_index('ix_feeds_id', 'feeds', ['id'], unique=False)
    # ### end Alembic commands ###
