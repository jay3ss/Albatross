"""add about_me to user model

Revision ID: aca5e9af6850
Revises: ceda05a6a8ff
Create Date: 2023-04-23 18:01:39.433626

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aca5e9af6850'
down_revision = 'ceda05a6a8ff'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('about', sa.String(length=280), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('about')

    # ### end Alembic commands ###