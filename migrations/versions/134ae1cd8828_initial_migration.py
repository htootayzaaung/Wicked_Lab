"""initial migration

Revision ID: 134ae1cd8828
Revises: 
Create Date: 2022-12-17 00:56:29.602507

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '134ae1cd8828'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('User',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_User_email'), 'User', ['email'], unique=True)
    op.create_index(op.f('ix_User_username'), 'User', ['username'], unique=True)
    op.create_table('perfumes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('pname', sa.String(length=140), nullable=False),
    sa.Column('price', sa.Text(), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('image', sa.String(length=140), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('userperf',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('perfume_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['perfume_id'], ['perfumes.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['User.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('userperf')
    op.drop_table('perfumes')
    op.drop_index(op.f('ix_User_username'), table_name='User')
    op.drop_index(op.f('ix_User_email'), table_name='User')
    op.drop_table('User')
    # ### end Alembic commands ###