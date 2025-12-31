# AICG平台 - Docker部署指南

## 📋 目录

- [快速开始](#快速开始)
- [构建镜像](#构建镜像)
- [部署说明](#部署说明)
- [配置说明](#配置说明)
- [常见问题](#常见问题)
- [生产环境建议](#生产环境建议)

---

## 🚀 快速开始

### 前置要求

- Docker 20.10+
- Docker Compose 2.0+
- 至少 4GB 可用内存
- 至少 20GB 可用磁盘空间

### 一键部署

```bash
# 1. 克隆项目
git clone https://github.com/869413421/aicon2.git
cd aicon2

# 2. 配置环境变量
cp .env.production.example .env.production
# 编辑 .env.production 填写必要的配置

# 3. 构建并启动
docker-compose -f docker-compose.prod.yml up -d

# 4. 查看日志
docker-compose -f docker-compose.prod.yml logs -f

# 5. 访问应用
# 前端: http://localhost
# 后端API: http://localhost:8000
# API文档: http://localhost:8000/docs
# MinIO控制台: http://localhost:9001
```

---

## 🔨 构建镜像

### 方法1: 使用构建脚本(推荐)

**Linux/Mac:**
```bash
chmod +x build-docker.sh
./build-docker.sh
```

**Windows:**
```cmd
build-docker.bat
```

### 方法2: 手动构建

```bash
# 构建后端镜像
cd backend
docker build -t aicg/aicg-backend:latest .
cd ..

# 构建前端镜像
cd frontend
docker build -t aicg/aicg-frontend:latest .
cd ..
```

### 方法3: 使用docker-compose构建

```bash
docker-compose -f docker-compose.prod.yml build
```

### 自定义镜像标签

```bash
# 设置版本号
export VERSION=v1.0.0
export IMAGE_REGISTRY=your-registry.com

# 构建
./build-docker.sh

# 或手动指定
docker build -t your-registry.com/aicg-backend:v1.0.0 ./backend
docker build -t your-registry.com/aicg-frontend:v1.0.0 ./frontend
```

---

## 📦 部署说明

### 架构说明

生产环境包含以下服务:

| 服务 | 说明 | 端口 |
|------|------|------|
| **frontend** | Vue3前端 + Nginx | 80 |
| **backend** | FastAPI后端服务 | 8000 |
| **celery-worker** | 异步任务处理 | - |
| **celery-beat** | 定时任务调度 | - |
| **postgres** | PostgreSQL数据库 | 5432 |
| **redis** | 缓存和消息队列 | 6379 |
| **minio** | 对象存储 | 9000, 9001 |

### 部署步骤

#### 1. 准备环境变量

```bash
cp .env.production.example .env.production
```

编辑 `.env.production`,**必须修改**以下配置:

```env
# 数据库密码
POSTGRES_PASSWORD=your-strong-password

# Redis密码
REDIS_PASSWORD=your-redis-password

# MinIO密码
MINIO_ROOT_PASSWORD=your-minio-password

# 应用密钥(用于JWT等)
SECRET_KEY=your-random-secret-key-at-least-32-characters

# AI服务密钥
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=...
```

#### 2. 启动服务

```bash
# 启动所有服务
docker-compose -f docker-compose.prod.yml up -d

# 查看服务状态
docker-compose -f docker-compose.prod.yml ps

# 查看日志
docker-compose -f docker-compose.prod.yml logs -f backend
```

#### 3. 初始化数据库

数据库迁移会在后端服务启动时自动执行。如需手动执行:

```bash
docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head
```

#### 4. 验证部署

```bash
# 检查后端健康状态
curl http://localhost:8000/health

# 检查前端
curl http://localhost/

# 检查API文档
open http://localhost:8000/docs
```

### 停止和清理

```bash
# 停止服务
docker-compose -f docker-compose.prod.yml down

# 停止并删除数据卷(⚠️ 会删除所有数据)
docker-compose -f docker-compose.prod.yml down -v

# 清理未使用的镜像
docker image prune -a
```

---

## ⚙️ 配置说明

### 环境变量详解

#### 数据库配置

```env
POSTGRES_DB=aicg_platform          # 数据库名称
POSTGRES_USER=aicg_user            # 数据库用户
POSTGRES_PASSWORD=***              # 数据库密码(必须修改)
POSTGRES_PORT=5432                 # 数据库端口
```

#### Redis配置

```env
REDIS_PASSWORD=***                 # Redis密码(必须修改)
REDIS_PORT=6379                    # Redis端口
```

#### MinIO配置

```env
MINIO_ROOT_USER=minioadmin         # MinIO管理员用户名
MINIO_ROOT_PASSWORD=***            # MinIO密码(必须修改)
MINIO_BUCKET=aicg-platform         # 存储桶名称
MINIO_API_PORT=9000                # API端口
MINIO_CONSOLE_PORT=9001            # 控制台端口
```

#### 应用配置

```env
SECRET_KEY=***                     # JWT密钥(必须修改为随机字符串)
DEBUG=false                        # 调试模式(生产环境必须为false)
ENVIRONMENT=production             # 运行环境
```

#### 服务端口

```env
BACKEND_PORT=8000                  # 后端服务端口
FRONTEND_PORT=80                   # 前端服务端口
```

### 自定义配置

#### 修改Celery并发数

编辑 `docker-compose.prod.yml`:

```yaml
celery-worker:
  command: celery -A src.tasks.app worker --loglevel=info --concurrency=8
```

#### 修改Nginx配置

编辑 `frontend/nginx.conf`,然后重新构建前端镜像。

#### 使用外部数据库

如果使用外部数据库,可以移除postgres服务,并修改 `DATABASE_URL`:

```env
DATABASE_URL=postgresql+asyncpg://user:password@external-db-host:5432/dbname
```

---

## 🔍 常见问题

### 1. 端口冲突

**问题**: 端口已被占用

**解决**:
```bash
# 修改 .env.production 中的端口
FRONTEND_PORT=8080
BACKEND_PORT=8001
```

### 2. 内存不足

**问题**: 容器因内存不足被杀死

**解决**:
```bash
# 限制Celery并发数
celery-worker:
  command: celery -A src.tasks.app worker --concurrency=2
```

### 3. 数据库连接失败

**问题**: 后端无法连接数据库

**解决**:
```bash
# 检查postgres是否健康
docker-compose -f docker-compose.prod.yml ps postgres

# 查看postgres日志
docker-compose -f docker-compose.prod.yml logs postgres

# 确保depends_on配置正确
```

### 4. MinIO无法访问

**问题**: 文件上传失败

**解决**:
```bash
# 检查MinIO状态
docker-compose -f docker-compose.prod.yml logs minio

# 手动创建bucket
docker-compose -f docker-compose.prod.yml exec minio \
  mc alias set local http://localhost:9000 minioadmin minioadmin123
docker-compose -f docker-compose.prod.yml exec minio \
  mc mb local/aicg-platform
```

### 5. 前端无法访问后端API

**问题**: 前端调用API失败

**解决**:
检查 `frontend/nginx.conf` 中的代理配置:
```nginx
location /api/ {
    proxy_pass http://backend:8000;  # 确保服务名正确
}
```

---

## 🏭 生产环境建议

### 1. 安全加固

#### 使用HTTPS

```bash
# 使用Let's Encrypt获取证书
# 然后配置nginx支持HTTPS
```

#### 修改默认密码

```env
# 使用强密码
POSTGRES_PASSWORD=$(openssl rand -base64 32)
REDIS_PASSWORD=$(openssl rand -base64 32)
MINIO_ROOT_PASSWORD=$(openssl rand -base64 32)
SECRET_KEY=$(openssl rand -base64 48)
```

#### 限制网络访问

```yaml
# 只暴露必要的端口
ports:
  - "127.0.0.1:5432:5432"  # 数据库只允许本地访问
```

### 2. 性能优化

#### 使用生产级数据库

```bash
# 使用外部托管的PostgreSQL
# 如AWS RDS, Google Cloud SQL等
```

#### 配置资源限制

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G
```

#### 启用日志轮转

```yaml
services:
  backend:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### 3. 监控和备份

#### 数据备份

```bash
# 备份PostgreSQL
docker-compose -f docker-compose.prod.yml exec postgres \
  pg_dump -U aicg_user aicg_platform > backup.sql

# 备份MinIO数据
docker-compose -f docker-compose.prod.yml exec minio \
  mc mirror local/aicg-platform /backup/minio
```

#### 健康检查

```bash
# 定期检查服务健康状态
docker-compose -f docker-compose.prod.yml ps

# 设置监控告警(推荐使用Prometheus + Grafana)
```

### 4. 扩展性

#### 水平扩展Worker

```bash
# 增加Worker实例
docker-compose -f docker-compose.prod.yml up -d --scale celery-worker=4
```

#### 使用负载均衡

```yaml
# 使用nginx或Traefik作为负载均衡器
# 部署多个backend实例
```

### 5. 日志管理

```bash
# 查看实时日志
docker-compose -f docker-compose.prod.yml logs -f --tail=100

# 导出日志
docker-compose -f docker-compose.prod.yml logs > app.log

# 使用ELK或Loki进行日志聚合
```

---

## 📊 镜像大小优化

当前镜像大小:
- **backend**: ~500MB (使用slim基础镜像)
- **frontend**: ~50MB (使用nginx-alpine)

进一步优化建议:
1. 使用 `.dockerignore` 排除不必要的文件
2. 多阶段构建减少最终镜像大小
3. 使用alpine基础镜像
4. 清理apt缓存和临时文件

---

## 🔗 相关链接

- [Docker官方文档](https://docs.docker.com/)
- [Docker Compose文档](https://docs.docker.com/compose/)
- [项目GitHub](https://github.com/869413421/aicon2)

---

## 📞 支持

如有问题,请:
1. 查看[常见问题](#常见问题)
2. 提交[GitHub Issue](https://github.com/869413421/aicon2/issues)
3. 联系技术支持

---

**最后更新**: 2025-12-31
