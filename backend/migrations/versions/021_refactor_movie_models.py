"""refactor movie models and add transition table

Revision ID: 021
Revises: 020
Create Date: 2025-12-24 15:33:00.000000

Changes:
1. MovieScene: Remove location, time_of_day, atmosphere, description
   Add: scene (Text), characters (JSON)
2. MovieShot: Remove performance_prompt, first_frame_url, first_frame_prompt,
   last_frame_url, last_frame_prompt, video_url, video_prompt, video_task_id,
   api_key_id, status, last_error
   Add: characters (JSON), keyframe_url (String)
3. Add new table: MovieShotTransition
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '021'
down_revision = '020'
branch_labels = None
depends_on = None


def upgrade():
    # 1. Create movie_shot_transitions table
    op.create_table(
        'movie_shot_transitions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('script_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('from_shot_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('to_shot_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('order_index', sa.Integer(), nullable=False),
        sa.Column('video_prompt', sa.Text(), nullable=True),
        sa.Column('video_url', sa.String(length=500), nullable=True),
        sa.Column('video_task_id', sa.String(length=100), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=True),
        sa.ForeignKeyConstraint(['script_id'], ['movie_scripts.id'], ),
        sa.ForeignKeyConstraint(['from_shot_id'], ['movie_shots.id'], ),
        sa.ForeignKeyConstraint(['to_shot_id'], ['movie_shots.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_movie_shot_transitions_script_id'), 'movie_shot_transitions', ['script_id'], unique=False)
    op.create_index(op.f('ix_movie_shot_transitions_from_shot_id'), 'movie_shot_transitions', ['from_shot_id'], unique=False)
    op.create_index(op.f('ix_movie_shot_transitions_to_shot_id'), 'movie_shot_transitions', ['to_shot_id'], unique=False)
    op.create_index(op.f('ix_movie_shot_transitions_status'), 'movie_shot_transitions', ['status'], unique=False)

    # 2. Modify movie_scenes table
    # Add new columns
    op.add_column('movie_scenes', sa.Column('scene', sa.Text(), nullable=True))
    op.add_column('movie_scenes', sa.Column('characters', postgresql.JSON(astext_type=sa.Text()), nullable=True))
    
    # Migrate data: combine old fields into new 'scene' field
    op.execute("""
        UPDATE movie_scenes 
        SET scene = COALESCE(description, '') || 
                   CASE WHEN location IS NOT NULL THEN '\n地点: ' || location ELSE '' END ||
                   CASE WHEN time_of_day IS NOT NULL THEN '\n时间: ' || time_of_day ELSE '' END ||
                   CASE WHEN atmosphere IS NOT NULL THEN '\n氛围: ' || atmosphere ELSE '' END
    """)
    
    # Set default empty array for characters
    op.execute("UPDATE movie_scenes SET characters = '[]'::json WHERE characters IS NULL")
    
    # Make scene NOT NULL after migration
    op.alter_column('movie_scenes', 'scene', nullable=False)
    
    # Drop old columns
    op.drop_column('movie_scenes', 'description')
    op.drop_column('movie_scenes', 'atmosphere')
    op.drop_column('movie_scenes', 'time_of_day')
    op.drop_column('movie_scenes', 'location')

    # 3. Modify movie_shots table
    # Add new columns
    op.add_column('movie_shots', sa.Column('characters', postgresql.JSON(astext_type=sa.Text()), nullable=True))
    op.add_column('movie_shots', sa.Column('keyframe_url', sa.String(length=500), nullable=True))
    
    # Migrate keyframe data: use first_frame_url as keyframe_url
    op.execute("UPDATE movie_shots SET keyframe_url = first_frame_url WHERE first_frame_url IS NOT NULL")
    
    # Set default empty array for characters
    op.execute("UPDATE movie_shots SET characters = '[]'::json WHERE characters IS NULL")
    
    # Drop old columns
    op.drop_column('movie_shots', 'performance_prompt')
    op.drop_column('movie_shots', 'first_frame_prompt')
    op.drop_column('movie_shots', 'last_frame_prompt')
    op.drop_column('movie_shots', 'first_frame_url')
    op.drop_column('movie_shots', 'last_frame_url')
    op.drop_column('movie_shots', 'video_url')
    op.drop_column('movie_shots', 'video_prompt')
    op.drop_column('movie_shots', 'video_task_id')
    op.drop_column('movie_shots', 'api_key_id')
    op.drop_column('movie_shots', 'status')
    op.drop_column('movie_shots', 'last_error')


def downgrade():
    # WARNING: This downgrade will lose data!
    
    # 1. Restore movie_shots columns
    op.add_column('movie_shots', sa.Column('last_error', sa.Text(), nullable=True))
    op.add_column('movie_shots', sa.Column('status', sa.String(length=20), nullable=True))
    op.add_column('movie_shots', sa.Column('api_key_id', sa.String(length=50), nullable=True))
    op.add_column('movie_shots', sa.Column('video_task_id', sa.String(length=100), nullable=True))
    op.add_column('movie_shots', sa.Column('video_prompt', sa.Text(), nullable=True))
    op.add_column('movie_shots', sa.Column('video_url', sa.String(length=500), nullable=True))
    op.add_column('movie_shots', sa.Column('last_frame_url', sa.String(length=500), nullable=True))
    op.add_column('movie_shots', sa.Column('last_frame_prompt', sa.Text(), nullable=True))
    op.add_column('movie_shots', sa.Column('first_frame_url', sa.String(length=500), nullable=True))
    op.add_column('movie_shots', sa.Column('first_frame_prompt', sa.Text(), nullable=True))
    op.add_column('movie_shots', sa.Column('performance_prompt', sa.Text(), nullable=True))
    
    # Restore first_frame_url from keyframe_url
    op.execute("UPDATE movie_shots SET first_frame_url = keyframe_url WHERE keyframe_url IS NOT NULL")
    
    op.drop_column('movie_shots', 'keyframe_url')
    op.drop_column('movie_shots', 'characters')

    # 2. Restore movie_scenes columns
    op.add_column('movie_scenes', sa.Column('location', sa.String(length=200), nullable=True))
    op.add_column('movie_scenes', sa.Column('time_of_day', sa.String(length=50), nullable=True))
    op.add_column('movie_scenes', sa.Column('atmosphere', sa.String(length=200), nullable=True))
    op.add_column('movie_scenes', sa.Column('description', sa.Text(), nullable=True))
    
    # Restore description from scene
    op.execute("UPDATE movie_scenes SET description = scene")
    
    op.drop_column('movie_scenes', 'characters')
    op.drop_column('movie_scenes', 'scene')

    # 3. Drop movie_shot_transitions table
    op.drop_index(op.f('ix_movie_shot_transitions_status'), table_name='movie_shot_transitions')
    op.drop_index(op.f('ix_movie_shot_transitions_to_shot_id'), table_name='movie_shot_transitions')
    op.drop_index(op.f('ix_movie_shot_transitions_from_shot_id'), table_name='movie_shot_transitions')
    op.drop_index(op.f('ix_movie_shot_transitions_script_id'), table_name='movie_shot_transitions')
    op.drop_table('movie_shot_transitions')
