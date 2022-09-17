"""user_has_message added.

Revision ID: f9235a7f8424
Revises: c37eae2b8ed8
Create Date: 2022-09-17 11:44:08.877192

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f9235a7f8424'
down_revision = 'c37eae2b8ed8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('association',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('message_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['message_id'], ['messages.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )
    op.create_unique_constraint(None, 'comments', ['id'])
    op.drop_constraint('messages_recipient_id_key', 'messages', type_='unique')
    op.drop_constraint('messages_sender_id_key', 'messages', type_='unique')
    op.create_unique_constraint(None, 'messages', ['id'])
    op.drop_constraint('messages_recipient_id_fkey', 'messages', type_='foreignkey')
    op.drop_constraint('messages_sender_id_fkey', 'messages', type_='foreignkey')
    op.drop_column('messages', 'sender_id')
    op.drop_column('messages', 'recipient_id')
    op.create_unique_constraint(None, 'threads', ['id'])
    op.create_unique_constraint(None, 'users', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_constraint(None, 'threads', type_='unique')
    op.add_column('messages', sa.Column('recipient_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('messages', sa.Column('sender_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('messages_sender_id_fkey', 'messages', 'users', ['sender_id'], ['id'])
    op.create_foreign_key('messages_recipient_id_fkey', 'messages', 'users', ['recipient_id'], ['id'])
    op.drop_constraint(None, 'messages', type_='unique')
    op.create_unique_constraint('messages_sender_id_key', 'messages', ['sender_id'])
    op.create_unique_constraint('messages_recipient_id_key', 'messages', ['recipient_id'])
    op.drop_constraint(None, 'comments', type_='unique')
    op.drop_table('association')
    # ### end Alembic commands ###