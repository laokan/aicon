"""add scene image fields to movie_scenes

Revision ID: 023
Revises: 022
Create Date: 2025-12-25 09:09:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '023'
down_revision = '022'
branch_labels = None
depends_on = None


def upgrade():
    """Add scene_image_url and scene_image_prompt fields to movie_scenes table"""
    # Add scene_image_url column
    op.add_column('movie_scenes', 
        sa.Column('scene_image_url', sa.String(500), nullable=True, comment='场景图片URL（无人物的场景环境图）')
    )
    
    # Add scene_image_prompt column
    op.add_column('movie_scenes', 
        sa.Column('scene_image_prompt', sa.Text(), nullable=True, comment='场景图生成提示词')
    )


def downgrade():
    """Remove scene image fields from movie_scenes table"""
    op.drop_column('movie_scenes', 'scene_image_prompt')
    op.drop_column('movie_scenes', 'scene_image_url')
