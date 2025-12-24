"""
电影场景相关API路由
"""

from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from src.core.logging import get_logger
from src.models.user import User
from src.api.dependencies import get_current_user_required
from src.api.schemas.movie import MovieScriptResponse, ScriptGenerateRequest

logger = get_logger(__name__)
router = APIRouter()

@router.post("/chapters/{chapter_id}/scenes", summary="从章节提取场景")
async def extract_scenes(
    chapter_id: str, 
    req: ScriptGenerateRequest,
    current_user: User = Depends(get_current_user_required),
    db: AsyncSession = Depends(get_db)
):
    """
    从章节提取场景（生成剧本）
    注意：这里只提取场景，不提取分镜
    """
    from src.tasks.movie import movie_extract_scenes
    task = movie_extract_scenes.delay(chapter_id, req.api_key_id, req.model)
    return {"task_id": task.id, "message": "场景提取任务已提交"}

@router.get("/chapters/{chapter_id}/script", response_model=Optional[MovieScriptResponse])
async def get_script(
    chapter_id: str, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_required)
):
    """获取章节关联的剧本详情"""
    from src.services.movie import MovieService
    movie_service = MovieService(db)
    script = await movie_service.get_script(chapter_id)
    return script
