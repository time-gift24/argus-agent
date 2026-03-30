# Backend CLAUDE.md

本目录是 FastAPI 后端实现，目标是提供稳定的认证、Provider、MCP 配置与 Tool 管理能力。

## 先看这些文件

- `main.py`: 当前运行入口（`make dev` 使用 `uvicorn main:app`）
- `app/api/router.py`: 已挂载路由清单（当前实际生效接口）
- `app/core/config.py`: 环境变量与配置优先级
- `app/models/`: 数据模型（`user.py` / `mcp_config.py` / `tool.py`）
- `tests/`: 回归测试基线

## 实际技术栈（以代码为准）

- FastAPI
- SQLAlchemy 2.x（同步 Session）
- Alembic
- uv（依赖与运行）
- pytest / pytest-cov
- SQLite（默认开发库，可由 `DATABASE_URL` 切换）

## 运行与测试

```bash
cd backend
make install-dev
make dev
```

```bash
cd backend
make test
make test-cov
```

## 路由与模块约束

- 新增/修改接口时，必须同步检查 `app/api/router.py` 是否已挂载对应 endpoint。
- `app/api/endpoints/llm_providers.py` 当前未在 `router.py` 挂载；若需要启用，必须明确评估并补测试后再接入。
- 认证依赖统一复用 `app/auth/deps.py`，禁止在 endpoint 重复造鉴权逻辑。

## 数据与安全约束

- Provider 配置与 MCP 敏感字段使用 AES-256-GCM 加密存储，禁止明文入库。
- 所有密钥类配置只来自环境变量（见 `app/core/config.py`），禁止硬编码。
- 默认开发流程使用 `DEV_MODE=true`，生产模式必须走 OIDC 正常链路。

## 变更清单（提交前自检）

1. 接口变更已覆盖 schema、service、endpoint、测试，不留半改状态。
2. `api/openapi.yaml` 与实际行为保持一致（至少同步新增/删改路径与字段）。
3. 新逻辑在 `tests/` 有对应回归测试。
4. 遵守仓库规则：KISS / YAGNI / DRY，不为“将来可能”提前设计复杂抽象。

## 代码风格

- 遵守根目录规则：`../rules/python/`
- 优先保持小函数、清晰命名、单一职责
- 错误处理优先返回明确 HTTP 状态与可诊断信息
