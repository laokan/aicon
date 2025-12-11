"""
仪表盘API响应模型
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ProjectStatistics(BaseModel):
    """项目统计"""
    total: int = Field(..., description="项目总数")
    by_status: Dict[str, int] = Field(..., description="按状态分组的项目数")
    uploaded: int = Field(0, description="已上传状态的项目数")
    parsing: int = Field(0, description="解析中的项目数")
    parsed: int = Field(0, description="已解析的项目数")
    generating: int = Field(0, description="生成中的项目数")
    completed: int = Field(0, description="已完成的项目数")
    failed: int = Field(0, description="失败的项目数")
    archived: int = Field(0, description="已归档的项目数")


class ContentStatistics(BaseModel):
    """内容统计"""
    total_chapters: int = Field(..., description="章节总数")
    total_paragraphs: int = Field(..., description="段落总数")
    total_sentences: int = Field(..., description="句子总数")


class GenerationStatistics(BaseModel):
    """生成统计"""
    generated_images: int = Field(..., description="已生成图片数")
    generated_audios: int = Field(..., description="已生成音频数")
    generated_videos: int = Field(..., description="已生成视频数")


class TaskStatistics(BaseModel):
    """任务统计"""
    running_tasks: int = Field(..., description="运行中的任务总数")
    project_tasks: int = Field(..., description="项目级任务数")
    chapter_tasks: int = Field(..., description="章节级任务数")


class CostEstimate(BaseModel):
    """成本估算"""
    total: float = Field(..., description="总成本(估算)")
    image_cost: float = Field(..., description="图片生成成本")
    audio_cost: float = Field(..., description="音频生成成本")
    prompt_cost: float = Field(..., description="提示词生成成本")
    currency: str = Field("CNY", description="货币单位")
    is_estimate: bool = Field(True, description="是否为估算值(非实际扣费)")
    generated_count: Dict[str, int] = Field(..., description="已生成数量明细")


class DashboardStatistics(BaseModel):
    """仪表盘综合统计"""
    projects: ProjectStatistics = Field(..., description="项目统计")
    content: ContentStatistics = Field(..., description="内容统计")
    generation: GenerationStatistics = Field(..., description="生成统计")
    tasks: TaskStatistics = Field(..., description="任务统计")
    cost: CostEstimate = Field(..., description="成本估算")
    last_updated: str = Field(..., description="最后更新时间")

    class Config:
        json_schema_extra = {
            "example": {
                "projects": {
                    "total": 10,
                    "by_status": {"uploaded": 2, "parsed": 5, "completed": 3},
                    "uploaded": 2,
                    "parsing": 0,
                    "parsed": 5,
                    "generating": 0,
                    "completed": 3,
                    "failed": 0,
                    "archived": 0
                },
                "content": {
                    "total_chapters": 50,
                    "total_paragraphs": 200,
                    "total_sentences": 1000
                },
                "generation": {
                    "generated_images": 800,
                    "generated_audios": 750,
                    "generated_videos": 30
                },
                "tasks": {
                    "running_tasks": 2,
                    "project_tasks": 1,
                    "chapter_tasks": 1
                },
                "cost": {
                    "total": 33.0,
                    "image_cost": 32.0,
                    "audio_cost": 15.0,
                    "prompt_cost": 1.0,
                    "currency": "CNY"
                },
                "last_updated": "2025-12-11T03:15:00"
            }
        }


class RecentProject(BaseModel):
    """最近项目"""
    id: str = Field(..., description="项目ID")
    title: str = Field(..., description="项目标题")
    status: str = Field(..., description="项目状态")
    updated_at: Optional[str] = Field(None, description="更新时间")
    chapter_count: int = Field(0, description="章节数量")
    word_count: int = Field(0, description="字数统计")


class RecentProjectsResponse(BaseModel):
    """最近项目列表响应"""
    projects: List[RecentProject] = Field(..., description="最近项目列表")
    total: int = Field(..., description="总数")


class RecentActivity(BaseModel):
    """最近活动"""
    id: str = Field(..., description="活动ID")
    type: str = Field(..., description="活动类型: project_created, chapter_confirmed, video_generated")
    description: str = Field(..., description="活动描述")
    timestamp: Optional[str] = Field(None, description="活动时间")
    related_id: str = Field(..., description="关联的资源ID")
    status: str = Field(..., description="资源状态")


class RecentActivitiesResponse(BaseModel):
    """最近活动列表响应"""
    activities: List[RecentActivity] = Field(..., description="最近活动列表")
    total: int = Field(..., description="总数")


class TaskQueueItem(BaseModel):
    """任务队列项"""
    id: str = Field(..., description="任务ID")
    type: str = Field(..., description="任务类型: project_processing, chapter_generating")
    title: str = Field(..., description="任务标题")
    status: str = Field(..., description="任务状态")
    progress: int = Field(0, description="任务进度 0-100")
    started_at: Optional[str] = Field(None, description="开始时间")


class TaskQueueStatus(BaseModel):
    """任务队列状态"""
    running_tasks: int = Field(..., description="运行中的任务数")
    tasks: List[TaskQueueItem] = Field(..., description="任务列表")


__all__ = [
    "ProjectStatistics",
    "ContentStatistics",
    "GenerationStatistics",
    "TaskStatistics",
    "CostEstimate",
    "DashboardStatistics",
    "RecentProject",
    "RecentProjectsResponse",
    "RecentActivity",
    "RecentActivitiesResponse",
    "TaskQueueItem",
    "TaskQueueStatus",
]
