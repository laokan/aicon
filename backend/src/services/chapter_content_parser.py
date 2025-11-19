"""
章节内容解析服务 - 专门用于章节的段落和句子解析

提供服务：
- 解析章节内容生成段落和句子统计数据
- 计算章节的统计信息（字数、段落数、句子数）
- 清理和标准化文本内容

设计原则：
- 使用现有的文本处理工具保持一致性
- 简洁的API，专注于章节统计计算
- 异步设计，支持服务层集成
"""

from typing import Dict, List, Tuple

from src.core.logging import get_logger
from src.models.paragraph import ParagraphAction
from src.models.sentence import SentenceStatus
from src.utils.text_utils import sentence_splitter

logger = get_logger(__name__)


class ChapterContentParser:
    """章节内容解析服务"""

    def __init__(self):
        """初始化章节内容解析服务"""
        logger.debug("ChapterContentParser 初始化完成")

    async def parse_content_with_structure(self, chapter_id: str, content: str) -> Tuple[Dict, List[Dict], List[Dict]]:
        """
        解析章节内容，生成统计信息和完整的段落句子结构数据

        Args:
            chapter_id: 章节ID
            content: 章节原始内容

        Returns:
            Tuple: (统计信息, 段落数据列表, 句子数据列表)
        """
        if not content:
            return {
                "word_count": 0,
                "paragraph_count": 0,
                "sentence_count": 0
            }, [], []

        # 清理文本：标准化换行符
        cleaned_content = content.replace('\r\n', '\n').replace('\r', '\n').strip()

        # 计算字数（简单的字符数统计，排除空格）
        word_count = len(cleaned_content.replace(' ', ''))

        # 分割段落（使用简单的换行分割，更适合中文文本）
        paragraphs = [p.strip() for p in cleaned_content.split('\n\n') if p.strip()]
        paragraph_count = len(paragraphs)

        # 生成段落和句子数据
        paragraphs_data = []
        sentences_data = []
        sentence_count = 0

        for para_idx, paragraph_text in enumerate(paragraphs):
            if not paragraph_text.strip():
                continue

            # 分割当前段落的句子
            paragraph_sentences = sentence_splitter.split_text(paragraph_text)
            para_sentence_count = len(paragraph_sentences)
            sentence_count += para_sentence_count

            # 生成段落数据
            paragraph_data = {
                "chapter_id": chapter_id,
                "content": paragraph_text.strip(),
                "order_index": para_idx + 1,
                "word_count": len(paragraph_text.replace(' ', '')),
                "sentence_count": para_sentence_count,
                "action": ParagraphAction.KEEP.value,
                "is_confirmed": False,
            }
            paragraphs_data.append(paragraph_data)

            # 生成句子数据
            for sent_idx, sentence_text in enumerate(paragraph_sentences):
                if not sentence_text.strip():
                    continue

                sentence_data = {
                    "paragraph_id": None,  # 将在段落创建后设置
                    "content": sentence_text.strip(),
                    "order_index": sent_idx + 1,
                    "word_count": len(sentence_text.replace(' ', '')),
                    "character_count": len(sentence_text),
                    "status": SentenceStatus.PENDING.value,
                    "retry_count": 0,
                    "is_manual_edited": False,
                }
                sentences_data.append(sentence_data)

        stats = {
            "word_count": word_count,
            "paragraph_count": paragraph_count,
            "sentence_count": sentence_count
        }

        logger.debug(f"内容结构解析完成: 字数={word_count}, 段落={paragraph_count}, 句子={sentence_count}")
        return stats, paragraphs_data, sentences_data


# 全局实例
chapter_content_parser = ChapterContentParser()

__all__ = [
    "ChapterContentParser",
    "chapter_content_parser"
]
