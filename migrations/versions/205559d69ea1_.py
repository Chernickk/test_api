"""empty message

Revision ID: 205559d69ea1
Revises: 
Create Date: 2022-01-19 15:13:10.703046

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '205559d69ea1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('news',
    sa.Column('title', sa.String(length=140), nullable=False),
    sa.Column('picture_url', sa.String(length=140), nullable=False),
    sa.Column('posted_at', sa.DateTime(), nullable=False),
    sa.Column('parsed_at', sa.DateTime(), nullable=True),
    sa.Column('text', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('title', 'picture_url', 'posted_at')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('news')
    # ### end Alembic commands ###
