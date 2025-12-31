# 镜像构建和发布指南

## 前置要求

1. Docker 已安装
2. Docker Hub 账号: `qingshui869413421`
3. 已登录 Docker Hub

## 登录 Docker Hub

```bash
docker login
# 输入用户名: qingshui869413421
# 输入密码: [你的密码]
```

## 构建和推送镜像

### Windows (PowerShell)

```powershell
# 推送最新版本
.\scripts\build-and-push.ps1

# 推送指定版本
.\scripts\build-and-push.ps1 -Version "v1.0.0"
```

### Linux/Mac (Bash)

```bash
# 添加执行权限
chmod +x scripts/build-and-push.sh

# 推送最新版本
./scripts/build-and-push.sh

# 推送指定版本
./scripts/build-and-push.sh v1.0.0
```

## 推送的镜像

脚本会自动构建并推送以下镜像:

- `qingshui869413421/aicon-backend:latest`
- `qingshui869413421/aicon-backend:[version]`
- `qingshui869413421/aicon-frontend:latest`
- `qingshui869413421/aicon-frontend:[version]`

## 验证镜像

推送成功后,可以在 Docker Hub 查看:
- https://hub.docker.com/r/qingshui869413421/aicon-backend
- https://hub.docker.com/r/qingshui869413421/aicon-frontend

## 注意事项

1. 每次代码更新后,需要重新构建和推送镜像
2. 建议使用语义化版本号,如 `v1.0.0`, `v1.1.0`
3. `latest` 标签会自动更新为最新版本
