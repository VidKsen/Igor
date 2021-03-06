"""empty message

Revision ID: e39313f5549f
Revises: 8632f717512d
Create Date: 2020-10-18 15:42:38.267387

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e39313f5549f'
down_revision = '8632f717512d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('firstname', sa.String(length=64), nullable=True))
    op.add_column('user', sa.Column('lastname', sa.String(length=64), nullable=True))
    op.add_column('user', sa.Column('patronumic', sa.String(length=64), nullable=True))
    op.create_index(op.f('ix_user_firstname'), 'user', ['firstname'], unique=False)
    op.create_index(op.f('ix_user_lastname'), 'user', ['lastname'], unique=False)
    op.create_index(op.f('ix_user_patronumic'), 'user', ['patronumic'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_patronumic'), table_name='user')
    op.drop_index(op.f('ix_user_lastname'), table_name='user')
    op.drop_index(op.f('ix_user_firstname'), table_name='user')
    op.drop_column('user', 'patronumic')
    op.drop_column('user', 'lastname')
    op.drop_column('user', 'firstname')
    # ### end Alembic commands ###
