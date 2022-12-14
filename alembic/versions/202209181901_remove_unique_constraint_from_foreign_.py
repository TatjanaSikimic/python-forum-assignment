"""Remove unique constraint from foreign keys in Post.

Revision ID: 422038e78180
Revises: 0628783f9609
Create Date: 2022-09-18 19:01:27.069395

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '422038e78180'
down_revision = '0628783f9609'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('attachments_post_id_key', 'attachments', type_='unique')
    op.drop_constraint('posts_thread_id_key', 'posts', type_='unique')
    op.drop_constraint('posts_user_id_key', 'posts', type_='unique')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('posts_user_id_key', 'posts', ['user_id'])
    op.create_unique_constraint('posts_thread_id_key', 'posts', ['thread_id'])
    op.create_unique_constraint('attachments_post_id_key', 'attachments', ['post_id'])
    # ### end Alembic commands ###
