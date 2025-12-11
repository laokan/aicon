"""
仪表盘API端点 - 提供用户统计和概览数据
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.dependencies import get_current_user_required
from src.api.schemas.dashboard import (
    DashboardStatistics,
    RecentActivitiesResponse,
    RecentProjectsResponse,
    TaskQueueStatus
)
from src.core.database import get_db
from src.core.logging import get_logger
from src.models.user import User
from src.services.dashboard import DashboardService

logger = get_logger(__name__)

router = APIRouter()


@router.get("/statistics", response_model=DashboardStatistics)
async def get_dashboard_statistics(
        *,
        current_user: User = Depends(get_current_user_required),
        db: AsyncSession = Depends(get_db)
):
    """
    获取用户仪表盘统计数据
    
    包括:
    - 项目统计(总数、各状态分布)
    - 内容统计(章节、段落、句子数)
    - 生成统计(图片、音频、视频数)
    - 任务统计(运行中的任务)
    - 成本估算
    """
    dashboard_service = DashboardService(db)
    statistics = await dashboard_service.get_user_statistics(str(current_user.id))
    
    return DashboardStatistics(**statistics)


@router.get("/recent-projects", response_model=RecentProjectsResponse)
async def get_recent_projects(
        *,
        current_user: User = Depends(get_current_user_required),
        db: AsyncSession = Depends(get_db),
        limit: int = 5
):
    """
    获取最近的项目列表
    
    Args:
        limit: 返回数量限制，默认5个
    """
    dashboard_service = DashboardService(db)
    projects = await dashboard_service.get_recent_projects(
        str(current_user.id),
        limit=limit
    )
    
    return RecentProjectsResponse(
        projects=projects,
        total=len(projects)
    )


@router.get("/recent-activities", response_model=RecentActivitiesResponse)
async def get_recent_activities(
        *,
        current_user: User = Depends(get_current_user_required),
        db: AsyncSession = Depends(get_db),
        limit: int = 10
):
    """
    获取最近的活动记录
    
    包括:
    - 项目创建
    - 章节确认
    - 视频生成
    
    Args:
        limit: 返回数量限制，默认10个
    """
    dashboard_service = DashboardService(db)
    activities = await dashboard_service.get_recent_activities(
        str(current_user.id),
        limit=limit
    )
    
    return RecentActivitiesResponse(
        activities=activities,
        total=len(activities)
    )


@router.get("/task-queue", response_model=TaskQueueStatus)
async def get_task_queue_status(
        *,
        current_user: User = Depends(get_current_user_required),
        db: AsyncSession = Depends(get_db)
):
    """
    获取任务队列状态
    
    包括:
    - 运行中的项目处理任务
    - 运行中的章节生成任务
    """
    dashboard_service = DashboardService(db)
    queue_status = await dashboard_service.get_task_queue_status(
        str(current_user.id)
    )
    
    return TaskQueueStatus(**queue_status)


__all__ = ["router"]
