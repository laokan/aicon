"""
电影过渡视频相关API路由
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from src.core.logging import get_logger
from src.models.user import User
from src.api.dependencies import get_current_user_required
from src.api.schemas.movie import TransitionGenerateRequest

logger = get_logger(__name__)
router = APIRouter()

@router.post("/scripts/{script_id}/create-transitions", summary="创建过渡视频记录")
async def create_transitions(
    script_id: str,
    req: TransitionGenerateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_required)
):
    """
    为剧本的所有连续分镜创建过渡视频记录
    包含视频提示词生成
    """
    from src.tasks.movie import movie_create_transitions
    task = movie_create_transitions.delay(script_id, req.api_key_id, req.model)
    return {"task_id": task.id, "message": "过渡视频创建任务已提交"}

@router.post("/scripts/{script_id}/generate-transition-videos", summary="批量生成过渡视频")
async def generate_transition_videos(
    script_id: str,
    req: TransitionGenerateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_required)
):
    """批量生成剧本所有过渡视频"""
    from src.tasks.movie import movie_generate_transition_videos
    task = movie_generate_transition_videos.delay(script_id, req.api_key_id, req.video_model)
    return {"task_id": task.id, "message": "过渡视频生成任务已提交"}

@router.post("/transitions/{transition_id}/generate-video", summary="生成单个过渡视频")
async def generate_single_transition_video(
    transition_id: str,
    req: TransitionGenerateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_required)
):
    """生成单个过渡视频"""
    from src.tasks.movie import movie_generate_single_transition
    task = movie_generate_single_transition.delay(transition_id, req.api_key_id, req.video_model)
    return {"task_id": task.id, "message": "过渡视频生成任务已提交"}
