## Context

当前后端启动依赖 `.env` 文件存放密钥（AES_KEY、JWT_SECRET 等），但 `.env` 被 gitignore 排除且没有模板文件。新开发者无法知道需要哪些变量，也无法一键启动开发环境。Makefile 中也没有 `dev` 目标。

## Goals / Non-Goals

**Goals:**
- `make dev` 一行命令启动开发服务器，零配置
- `.env.dev` 提交到仓库，包含开发安全的默认密钥
- `.env.example` 作为生产部署参考模板
- 环境变量始终能覆盖文件中的默认值

**Non-Goals:**
- 不做生产环境配置管理（生产用真实环境变量）
- 不引入新的配置管理库（继续用 pydantic-settings）
- 不修改已有的 config.py 参数结构

## Decisions

### 1. `.env.dev` 而非 `.env`

**选择**: 创建 `.env.dev` 提交到仓库，`config.py` 通过 `env_file=".env.dev"` 加载。

**理由**: `.env` 已被 gitignore 排除且是业界惯例的本地覆盖文件。使用 `.env.dev` 明确表达"这是开发默认配置"，不会与个人本地 `.env` 冲突。pydantic-settings 原生支持 `env_file` 参数，无需额外代码。

**备选方案**: 用 `.env.example` 让开发者手动 `cp .env.example .env` → 多一步手动操作，且 `.env` 容易误提交。

### 2. `make dev` 实现

**选择**: Makefile 中新增 `dev` 目标，调用 `uvicorn` 并自动加载 `.env.dev`。

**理由**: 与项目现有 `uv run` 模式一致，无需额外工具。

### 3. `.env.example` 保留

**选择**: 同时维护 `.env.example` 作为文档，列出所有变量及说明，不含实际值。

**理由**: 生产部署人员需要知道需要哪些环境变量，`.env.example` 是通用实践。

## Risks / Trade-offs

- **`.env.dev` 包含默认密钥** → 仅用于开发，AES_KEY 和 JWT_SECRET 为随机生成的固定值，标注了 `# 仅用于本地开发`，生产必须覆盖
- **pydantic-settings 的 `env_file` 优先级** → 环境变量 > `.env.dev` 文件，符合预期
