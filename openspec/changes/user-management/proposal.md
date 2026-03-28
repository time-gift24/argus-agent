## Why

argus-agents 需要用户管理作为基础模块。所有 agent 和 LLM 调用都需按用户隔离计费、鉴权。通过 OAuth2/OIDC 登录，不存密码，降低安全风险。LLM Provider 抽象层（用户自定义 + 内部统一）支撑灵活的成本控制和模型路由。

## What Changes

- **User 模型**：id (UUID)、name、oauth_provider、oauth_subject、meta_data (JSONB)、created_at、updated_at；组合唯一索引 (oauth_provider, oauth_subject)
- **Provider 模型**：id (UUID)、name、kind (enum: user | internal)、config (AES-256-GCM 加密)、created_at、updated_at
- **UserProvider junction 表**：user_id、provider_id、is_default、created_at；仅用于 `kind=user` 的 provider；PK (user_id, provider_id)
- **认证流程**：OIDC login/callback，返回 HS256 JWT（user_id + name + exp）；支持 DEV_MODE header bypass
- **Provider CRUD API**：用户增删查自己的 user provider、设默认；internal provider 启动时 upsert，全局只读
- **加密基础设施**：AES_KEY 环境变量（32字节，base64），AES-256-GCM 加密 config；JWT_SECRET 环境变量；启动时 fail-fast 检查

## Capabilities

### New Capabilities

- `user-auth`: OAuth2/OIDC 认证，支持 dev 模式 bypass，JWT 签发与校验
- `user-profile`: 用户基本信息读写，meta_data 口袋字段
- `provider-management`: LLM Provider 的 CRUD（user provider 加密存储，internal provider 启动时 upsert）
- `user-provider-binding`: 用户与 user provider 的多对多关联，默认 provider 标记

### Modified Capabilities

（无，现有 specs 为空）

## Impact

- 新增 `backend/app/models/` SQLAlchemy 模型（user, provider, user_provider）
- 新增 `backend/app/auth/` OIDC 认证模块 + JWT 工具
- 新增 `backend/app/api/` REST API 路由（/auth/*, /me, /providers/*）
- 新增 `backend/app/core/crypto.py` AES 加密封装
- Alembic migration 文件（models 变更）
- 新增依赖：`python-jose`（JWT）、`cryptography`（AES-GCM）
- DEV_MODE=true 时，header `X-Dev-User: <name>` 跳过真实 OIDC 直接登录
