"""token column tu User

Revision ID: 8435a69366ea
Revises: 0c29ce175984
Create Date: 2021-06-15 00:18:37.416163

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8435a69366ea'
down_revision = '0c29ce175984'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('token', sa.String(length=32), nullable=True))
    op.add_column('user', sa.Column('token_expiration', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_user_token'), 'user', ['token'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_token'), table_name='user')
    op.drop_column('user', 'token_expiration')
    op.drop_column('user', 'token')
    # ### end Alembic commands ###
