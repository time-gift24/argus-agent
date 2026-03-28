## Why

后端开发环境缺少标准启动入口（无 `make dev`），且配置文件没有 dev/prod 分离——开发者必须手动创建 `.env` 并填入密钥才能启动服务，新人上手成本高，也容易误提交敏感信息。

## What Changes

- 新增 `make dev` 目标，一行命令启动开发服务器
- 创建 `.env.dev`（开发默认配置，可提交）替代 `.env`（已被 gitignore）
- `config.py` 开发模式下自动加载 `.env.dev`，环境变量仍可覆盖
- 新增 `.env.example` 作为模板文档，列出所有必需/可选变量及说明

## Capabilities

### New Capabilities
- `dev-env-setup`: 开发环境一键启动，包含 `make dev` 命令、`.env.dev` 默认配置、`.env.example` 模板

### Modified Capabilities

（无已有 spec 需修改）

## Impact

- `backend/Makefile`：新增 `dev` 目标
- `backend/.env.dev`：新增，包含开发模式默认密钥
- `backend/.env.example`：新增，环境变量模板文档
- `backend/app/core/config.py`：修改 `.env` 加载逻辑，支持 `.env.dev` 优先级
