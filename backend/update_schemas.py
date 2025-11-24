"""
批量更新 schema 文件以支持 UUID 类型
"""
import re
from pathlib import Path

# Schema 文件和需要更新的字段映射
SCHEMA_FILES = {
    "chapter.py": {
        "response_class": "ChapterResponse",
        "uuid_fields": ["id", "project_id"]
    },
    "paragraph.py": {
        "response_class": "ParagraphResponse",
        "uuid_fields": ["id", "chapter_id"]
    },
    "sentence.py": {
        "response_class": "SentenceResponse",
        "uuid_fields": ["id", "paragraph_id"]
    },
    "api_key.py": {
        "response_class": "APIKeyResponse",
        "uuid_fields": ["id", "user_id"]
    },
    "user.py": {
        "response_class": "UserResponse",
        "uuid_fields": ["id"]
    }
}

def update_schema_file(file_path: Path, response_class: str, uuid_fields: list):
    """更新单个 schema 文件"""
    print(f"Processing {file_path.name}...")
    
    content = file_path.read_text(encoding='utf-8')
    
    # 1. 添加 UUID 导入
    if "from uuid import UUID" not in content:
        content = content.replace(
            "from typing import",
            "from typing import"
        )
        # 在 typing 导入后添加 UUID 导入
        content = re.sub(
            r'(from typing import [^\n]+\n)',
            r'\1from uuid import UUID\n',
            content,
            count=1
        )
    
    # 2. 添加 UUIDMixin 导入
    if "UUIDMixin" not in content:
        content = content.replace(
            "from .base import PaginatedResponse",
            "from .base import PaginatedResponse, UUIDMixin"
        )
    
    # 3. 修改响应类继承
    content = re.sub(
        rf'class {response_class}\(BaseModel\):',
        f'class {response_class}(UUIDMixin):',
        content
    )
    
    # 4. 更新 UUID 字段类型
    for field in uuid_fields:
        # 匹配字段定义并替换类型
        content = re.sub(
            rf'{field}:\s*str\s*=\s*Field',
            f'{field}: UUID = Field',
            content
        )
    
    file_path.write_text(content, encoding='utf-8')
    print(f"✓ Updated {file_path.name}")

def main():
    """主函数"""
    schemas_dir = Path(r"d:\go\src\github.com\869413421\aicon2\backend\src\api\schemas")
    
    for filename, config in SCHEMA_FILES.items():
        file_path = schemas_dir / filename
        if file_path.exists():
            try:
                update_schema_file(
                    file_path,
                    config["response_class"],
                    config["uuid_fields"]
                )
            except Exception as e:
                print(f"✗ Error updating {filename}: {e}")
        else:
            print(f"✗ File not found: {filename}")
    
    print("\n✓ All schema files updated!")

if __name__ == "__main__":
    main()
