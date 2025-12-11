# Fast-Whisper / CTranslate2 GPU 加速配置说明（Linux/WSL）

为了让 fast-whisper 在 GPU 上运行，需确保 CUDA 相关动态库（`libcublas.so.12`、`libcudnn.so` 等）能被运行时正确加载。使用 pip/uv 安装的 CUDA wheel（如 `nvidia-cublas-cu12`、`nvidia-cudnn-cu12`）会将库文件放在虚拟环境的 `site-packages` 中，因此需要手动将其加入 `LD_LIBRARY_PATH`。

## 1. 激活虚拟环境

```bash
source .venv/bin/activate
```

## 2. 设置 CUDA 动态库路径

```bash
export LD_LIBRARY_PATH="<PROJECT_PATH>/.venv/lib/python3.12/site-packages/nvidia/cublas/lib:<PROJECT_PATH>/.venv/lib/python3.12/site-packages/nvidia/cudnn/lib:$LD_LIBRARY_PATH"
```

（将 `<PROJECT_PATH>` 替换为实际工程根目录）

## 3. 自动加载（可选）

将下面内容追加到 `.venv/bin/activate`，之后每次激活 venv 将自动启用 GPU 依赖库：

```bash
export LD_LIBRARY_PATH="<PROJECT_PATH>/.venv/lib/python3.12/site-packages/nvidia/cublas/lib:<PROJECT_PATH>/.venv/lib/python3.12/site-packages/nvidia/cudnn/lib:$LD_LIBRARY_PATH"
```

## 4. 修改代码

`backend\src\services\faster_whisper_service.py`
``` python
class WhisperTranscriptionService:
    def __init__(self, model_size="small", device="cuda", compute_type="float32"):
        """
        初始化语音识别服务（可复用模型，不需要每次都加载）
        """
        logger.info(f"🔄 正在加载 Whisper 模型: {model_size} ...")
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type)
        self.cc = OpenCC("t2s")  # 繁→简转换
        logger.info(f"✅ 模型加载完成")
```

将 `device` 修改为cuda，`model_size`也可以修改为适合你显卡的尺寸。