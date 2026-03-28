## Context

argus-agents 是多租户 AI Agent 平台，需要用户认证和 LLM Provider 抽象。系统从零构建，backend 使用 FastAPI + SQLAlchemy + Alembic + PostgreSQL。设计原则：YAGNI / KISS / DRY。

## Goals / Non-Goals

**Goals:**
- 通过 OAuth2/OIDC 实现无密码登录
- JWT 保护所有需要认证的 API
- 支持 user-defined provider（API key 加密存储）和 internal provider（硬编码）
- dev 模式绕过真实 OIDC，便于本地开发

**Non-Goals:**
- 不实现 OAuth2 之外的登录方式（无 password login、无 magic link）
- 不实现用户注册流程（首次 OIDC callback 时自动 upsert）
- 不实现 OAuth2 token 的 refresh token 存储（JWT 短期过期即可）
- 不实现权限 RBAC（user / admin 暂不区分）
- 不实现 provider 使用量计费

## Decisions

### D1: 主键使用 UUID string，不使用整型自增

**决定**：User、Provider 使用 `uuid` 类型作为主键，JWT sub 直接使用 UUID string。

**理由**：
- 抗爬取，不暴露合并 DB 时的顺序
- 多实例部署天然无冲突
- JWT payload 直接引用，无需额外映射

**替代考虑**：
- 整型自增：实现更简单，但暴露业务规模，不选

---

### D2: config 字段使用 AES-256-GCM 加密

**决定**：Provider.config 整体加密（包含 api_key、base_url 等），格式为 `base64(iv || ciphertext || tag)`。

**理由**：
- GCM 模式提供认证加密（保密 + 防篡改）
- 每次加密随机 IV，无需担心 ECB 模式问题
- 整体加密比只加密 api_key 更简洁

**替代考虑**：
- 只加密 api_key 字段：需要拆分 schema，且加密后长度不一致
- 不加密：user provider 含明文 API key，不选

---

### D3: AES key 存储在环境变量，启动 fail-fast

**决定**：应用启动时读取 `AES_KEY`（32 字节，base64 编码），缺失则抛出 `RuntimeError`。

**理由**：
- 12-factor app 标准
- 零运维复杂度
- fail-fast 防止生产环境密钥缺失导致加密数据损坏

---

### D4: JWT 使用 HS256，payload 含 user_id 和 name

**决定**：JWT 签发 HS256，payload = `{sub: user_id, name: user_name, exp, iat}`，环境变量 `JWT_SECRET`。

**理由**：
- 实现最简，无需公钥基础设施
- sub 字段标准映射到 user_id
- name 减少 `/me` 调用次数

**替代考虑**：
- RS256：需要 key pair 管理和公钥分发，过重，不选

---

### D5: Dev 模式使用 header bypass

**决定**：`DEV_MODE=true` 时，请求带 `X-Dev-User: <name>` header 直接构造 FakeUserInfo，跳过真实 OIDC 流程。

**理由**：
- 无需额外部署 mock OIDC server
- 前端本地 dev 轻松切换用户
- header 天然不出生产，零安全风险

---

### D6: OIDC 使用 duck typing，dev 实现保底

**决定**：定义 `OIDCProvider` protocol，具体实现注入（ProdOIDC / DevOIDC）。

**理由**：
- dev 实现简单（直接返回 FakeUserInfo）
- prod 实现完整 OIDC discovery + token exchange
- 切换 provider 只需注入不同实现，不改业务逻辑

---

### D7: internal provider 启动时 upsert

**决定**：`Kind.INTERNAL` 的 provider 定义为 Python dataclass，启动时查询 DB，不存在则 insert。

**理由**：
- 配置即代码，git 可追踪
- 一处定义，不依赖 migration seed
- 修改后重启生效，行为可预测

---

### D8: Database 使用 PostgreSQL，dev 可切换 SQLite

**决定**：生产 PostgreSQL + JSONB；SQLAlchemy 支持 dialect 切换，dev 可用 SQLite。

**理由**：
- `meta_data: JSONB` 需要 PostgreSQL 的 JSONB 索引能力
- 迁移脚本 `alembic revision --autogenerate` 兼容 SQLite
- Alembic 支持多 dialect，无需改迁移代码

---

### D9: UserProvider junction 仅用于 kind=user

**决定**：`kind=internal` 的 provider 不走 UserProvider 关联表，agents 调用时直接用 `provider_id` 引用，全局共享。

**理由**：
- internal provider 无需每个用户单独关联
- agents 调用链路更短

---

## Risks / Trade-offs

- **[Risk]** AES key rotation：轮换 `AES_KEY` 后旧加密数据无法解密
  - **Mitigation**：加密数据加版本前缀 `v1:base64(...)`，解密时按前缀选择 key；当前版本不加前缀保持兼容；后续 key rotation 时实现 migration 脚本

- **[Risk]** JWT 过期无 refresh token：用户被迫重新登录
  - **Mitigation**：JWT 过期时间设为 24h（合理平衡安全与体验）；后续可加 `/auth/token/refresh` endpoint

- **[Risk]** dev header bypass 误入生产
  - **Mitigation**：`DEV_MODE` 默认为 `false`；生产环境不设置该 env var 即可；代码中显式检查 `DEV_MODE == "true"` 字符串

- **[Risk]** OIDC provider 不可用时用户无法登录
  - **Mitigation**：dev 模式不依赖外部服务；生产建议 OIDC provider 高可用 + 监控

## Migration Plan

1. **新增 Model**：定义 SQLAlchemy Model（User、Provider、UserProvider），不破坏现有代码
2. **生成 Migration**：`alembic revision --autogenerate -m "add user management tables"`
3. **实现认证层**：OIDC 协议、JWT 工具、依赖注入
4. **实现 API 层**：/auth/*、/me、/providers/*
5. **配置 internal provider**：启动时 upsert
6. **添加 JWT 中间件**：保护其他 API（后续模块）

**Rollback**：Alembic `alembic downgrade -1` 回退 migration；代码层无状态，rollback 即回退 schema。

## Open Questions

（无，所有技术决策已在探索阶段确认。）
