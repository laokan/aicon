"""add three view fields to movie characters

Revision ID: 020
Revises: 019
Create Date: 2025-12-23 14:44:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '020'
down_revision = '019'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('movie_characters', sa.Column('era_background', sa.String(length=200), nullable=True, comment='时代背景(如: 1940s WWII, Victorian Era)'))
    op.add_column('movie_characters', sa.Column('occupation', sa.String(length=200), nullable=True, comment='职业/社会地位'))
    op.add_column('movie_characters', sa.Column('key_visual_traits', postgresql.JSON(astext_type=sa.Text()), nullable=True, comment='核心视觉特征列表(3-4个关键特征)'))
    op.add_column('movie_characters', sa.Column('generated_prompt', sa.Text(), nullable=True, comment='生成的三视图提示词'))


def downgrade():
    op.drop_column('movie_characters', 'generated_prompt')
    op.drop_column('movie_characters', 'key_visual_traits')
    op.drop_column('movie_characters', 'occupation')
    op.drop_column('movie_characters', 'era_background')
