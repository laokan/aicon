"""Add task_type field to video_tasks table

Revision ID: 026_add_video_task_type
Revises: 025_add_error_message_to_transitions
Create Date: 2025-12-25 21:55:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '026'
down_revision = '025'
branch_labels = None
depends_on = None


def upgrade():
    # 添加 task_type 字段，默认值为 'picture_narration'
    op.add_column('video_tasks', sa.Column('task_type', sa.String(length=30), nullable=False, server_default='picture_narration', comment='任务类型（picture_narration/movie_composition）'))
    
    # 创建索引
    op.create_index('idx_video_task_type', 'video_tasks', ['task_type'], unique=False)


def downgrade():
    # 删除索引
    op.drop_index('idx_video_task_type', table_name='video_tasks')
    
    # 删除字段
    op.drop_column('video_tasks', 'task_type')
