"""Second migration

Revision ID: 33e119e27a5e
Revises: 0b43648d51c6
Create Date: 2022-09-12 22:54:22.810894

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '33e119e27a5e'
down_revision = '0b43648d51c6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('threads',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.Column('dtCreated', sa.DateTime(), nullable=True),
    sa.Column('dtUpdated', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # op.create_table('user_thread_link',
    # sa.Column('user_id', sa.Integer(), nullable=False),
    # sa.Column('thread_id', sa.Integer(), nullable=False),
    # sa.ForeignKeyConstraint(['thread_id'], ['threads.id'], ),
    # sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    # sa.PrimaryKeyConstraint('user_id', 'thread_id')
    # )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_table('user_thread_link')
    op.drop_table('threads')
    # ### end Alembic commands ###