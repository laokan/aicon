"""
电影角色相关API路由
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, File, Form, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from src.core.logging import get_logger
from src.models.user import User
from src.api.dependencies import get_current_user_required
from src.services.movie_character_service import MovieCharacterService
from src.api.schemas.movie import (
    MovieCharacterBase,
    CharacterExtractRequest,
    CharacterUpdateRequest,
    CharacterGenerateRequest,
    BatchGenerateAvatarsRequest
)

logger = get_logger(__name__)
router = APIRouter()

@router.post("/chapters/{chapter_id}/extract-characters", summary="从章节提取角色")
async def extract_characters(
    chapter_id: str, 
    req: CharacterExtractRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_required)
):
    """从章节内容中提取角色（异步任务）"""
    from src.tasks.movie import movie_extract_characters
    task = movie_extract_characters.delay(chapter_id, req.api_key_id, req.model)
    return {"task_id": task.id, "message": "角色提取任务已提交"}

@router.get("/projects/{project_id}/characters")
async def list_characters(
    project_id: str, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_required)
):
    """列出项目下的所有电影角色"""
    from src.services.movie import MovieService
    from src.api.schemas.movie import MovieCharacterBase
    
    movie_service = MovieService(db)
    chars = await movie_service.list_characters(project_id)
    
    # 使用schema的from_orm_with_signed_urls方法
    result = [MovieCharacterBase.from_orm_with_signed_urls(char) for char in chars]
    
    # 返回统一格式：{ characters: [...] }
    return {"characters": [r.model_dump() for r in result]}

@router.put("/characters/{character_id}", response_model=MovieCharacterBase)
async def update_character(
    character_id: str,
    req: CharacterUpdateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_required)
):
    """更新角色信息（头像、参考图）"""
    from src.services.movie import MovieService
    movie_service = MovieService(db)
    updated_char = await movie_service.update_character(character_id, req.dict(exclude_unset=True))
    if not updated_char:
        raise HTTPException(status_code=404, detail="Character not found")
    return updated_char

@router.delete("/characters/{character_id}", summary="删除角色")
async def delete_character(
    character_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_required)
):
    """删除角色"""
    from src.services.movie import MovieService
    movie_service = MovieService(db)
    success = await movie_service.delete_character(character_id)
    if not success:
        raise HTTPException(status_code=404, detail="Character not found")
    return {"success": True, "message": "角色已删除"}

@router.post("/characters/{character_id}/generate", summary="生成角色头像")
async def generate_character_avatar(
    character_id: str,
    api_key_id: str = Form(...),
    model: Optional[str] = Form(None),
    prompt: Optional[str] = Form(None),
    style: Optional[str] = Form("cinematic"),
    selected_reference_indices: Optional[str] = Form(None, description="选中的参考图索引，逗号分隔，如'0,1,2'"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_required)
):
    """提交角色头像生成任务到 Celery"""
    from src.tasks.movie import movie_generate_character_avatar
    
    # 解析选中的参考图索引
    reference_indices = []
    if selected_reference_indices:
        try:
            reference_indices = [int(idx.strip()) for idx in selected_reference_indices.split(',') if idx.strip()]
        except ValueError:
            raise HTTPException(status_code=400, detail="参考图索引格式错误")
    
    task = movie_generate_character_avatar.delay(
        character_id, 
        api_key_id, 
        model, 
        prompt, 
        style,
        reference_indices
    )
    return {"task_id": task.id, "message": "角色头像生成任务已提交"}

@router.post("/projects/{project_id}/characters/batch-generate", summary="批量生成角色定妆照")
async def batch_generate_avatars(
    project_id: str,
    req: BatchGenerateAvatarsRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_required)
):
    """批量为所有未生成定妆照的角色生成头像"""
    from src.tasks.movie import movie_batch_generate_avatars
    task = movie_batch_generate_avatars.delay(project_id, req.api_key_id, req.model)
    return {"task_id": task.id, "message": "批量生成定妆照任务已提交"}

@router.post("/characters/{character_id}/reference-images", summary="上传角色参考图")
async def upload_reference_image(
    character_id: str,
    file: UploadFile = File(..., description="参考图片"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_required)
):
    """上传角色参考图"""
    from src.services.movie import MovieService
    from src.models.movie import MovieCharacter
    from src.models.project import Project
    from src.utils.image_utils import extract_and_upload_image
    
    # 验证文件类型
    if not file.content_type or not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="只能上传图片文件")
    
    # 获取角色
    char = await db.get(MovieCharacter, character_id)
    if not char:
        raise HTTPException(status_code=404, detail="角色不存在")
    
    # 获取项目
    project = await db.get(Project, char.project_id)
    
    # 直接上传到 MinIO
    from src.utils.storage import get_storage_client
    storage_client = await get_storage_client()
    
    upload_result = await storage_client.upload_file(
        user_id=str(project.owner_id),
        file=file,
        metadata={"character_id": str(char.id), "type": "reference_image"}
    )
    object_key = upload_result["object_key"]
    
    # 添加到参考图列表
    refs = list(char.reference_images) if char.reference_images else []
    if object_key not in refs:
        refs.append(object_key)
        char.reference_images = refs
        await db.commit()
    
    return {"success": True, "reference_image_url": object_key, "message": "参考图上传成功"}

@router.delete("/characters/{character_id}/reference-images/{image_index}", summary="删除角色参考图")
async def delete_reference_image(
    character_id: str,
    image_index: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_required)
):
    """删除指定索引的参考图"""
    from src.models.movie import MovieCharacter
    from src.utils.storage import get_storage_client
    
    # 获取角色
    char = await db.get(MovieCharacter, character_id)
    if not char:
        raise HTTPException(status_code=404, detail="角色不存在")
    
    # 检查索引
    refs = list(char.reference_images) if char.reference_images else []
    if image_index < 0 or image_index >= len(refs):
        raise HTTPException(status_code=400, detail="无效的图片索引")
    
    # 删除 MinIO 中的文件
    image_url = refs[image_index]
    try:
        storage_client = get_storage_client()
        storage_client.delete_object(image_url)
    except Exception as e:
        logger.error(f"删除MinIO文件失败: {e}")
        # 继续删除数据库记录
    
    # 从列表中移除
    refs.pop(image_index)
    char.reference_images = refs
    await db.commit()
    
    return {"success": True, "message": "参考图删除成功"}
