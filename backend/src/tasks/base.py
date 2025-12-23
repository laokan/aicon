"""
任务基础工具模块 - 提供异步任务运行和数据库会话管理
"""
import asyncio
import functools
from typing import Any, Callable, Coroutine, TypeVar

from src.core.database import get_async_db, close_database_connections
from src.core.logging import get_logger

logger = get_logger(__name__)

T = TypeVar("T")

# 全局事件循环容器（针对 Prefork 模式，每个 worker 进程一个）
_worker_loop = None

def get_worker_loop():
    """获取或创建一个在该 worker 进程中持续存在的事件循环"""
    global _worker_loop
    try:
        if _worker_loop is None or _worker_loop.is_closed():
            _worker_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(_worker_loop)
    except RuntimeError:
        # 如果当前线程没有循环（如在某些 worker 模式下），创建一个
        _worker_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(_worker_loop)
    return _worker_loop

def run_async_task(coro: Coroutine[Any, Any, T]) -> T:
    """
    在同步环境中运行异步协程的辅助函数。
    使用持续存在的事件循环，避免频繁创建/关闭造成的开销和数据库连接池失效。
    """
    loop = get_worker_loop()
    return loop.run_until_complete(coro)

def async_task_decorator(func: Callable[..., Coroutine[Any, Any, T]]) -> Callable[..., T]:
    """
    将异步函数包装为同步 Celery 任务的装饰器。
    自动注入数据库会话并处理异步运行。
    
    使用此装饰器的函数定义应为：
    @async_task_decorator
    async def my_task(db_session, *args, **kwargs):
        ...
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        async def _run():
            # 获取异步数据库会话
            async with get_async_db() as db:
                # 将 db_session 注入第一个参数
                return await func(db, *args, **kwargs)
        
        return run_async_task(_run())
    
    return wrapper
