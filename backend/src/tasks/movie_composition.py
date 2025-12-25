"""
电影合成 Celery 任务 - 从过渡视频合成完整电影
"""

from src.tasks.app import celery_app
from src.tasks.base import async_task_decorator
from src.core.logging import get_logger
from sqlalchemy.ext.asyncio import AsyncSession

logger = get_logger(__name__)


@celery_app.task(
    bind=True,
    max_retries=0,
    name="movie.compose_video"
)
@async_task_decorator
async def movie_compose_video(db_session: AsyncSession, self, task_id: str):
    """
    电影合成任务 - 将过渡视频合成为完整电影
    
    Args:
        db_session: 数据库会话（由 async_task_decorator 注入）
        self: Celery task 实例
        task_id: 视频任务ID
        
    工作流程:
    1. 获取章节的所有过渡视频
    2. 验证视频完整性
    3. 并发下载过渡视频
    4. 使用 FFmpeg 拼接视频
    5. 可选：添加 BGM
    6. 上传最终视频到 MinIO
    7. 更新任务状态
    """
    from src.services.movie_video_service import MovieVideoService
    
    logger.info(f"🎬 Celery任务开始: movie_compose_video (task_id={task_id})")
    
    service = MovieVideoService(db_session)
    result = await service.synthesize_movie_from_transitions(task_id)
    
    logger.info(f"🎉 Celery任务成功: movie_compose_video (task_id={task_id})")
    return result


__all__ = ["movie_compose_video"]
