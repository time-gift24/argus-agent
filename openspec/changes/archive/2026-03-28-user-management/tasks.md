## 1. 基础设施搭建

- [x] 1.1 安装依赖：`python-jose[cryptography]`（JWT）、`cryptography`（AES-GCM）
- [x] 1.2 创建目录结构：`app/models/`、`app/auth/`、`app/api/`、`app/core/`
- [x] 1.3 配置环境变量校验：启动时检查 `AES_KEY`、`JWT_SECRET` 是否存在，缺失则 `RuntimeError`

## 2. 数据库模型

- [x] 2.1 定义 `User` Model（id UUID PK、name、oauth_provider、oauth_subject、meta_data JSONB、created_at、updated_at；组合唯一索引）
- [x] 2.2 定义 `Provider` Model（id UUID PK、name、kind 枚举、config 加密字符串、created_at、updated_at）
- [x] 2.3 定义 `UserProvider` Model（user_id FK、provider_id FK、is_default bool、created_at；联合主键）
- [x] 2.4 运行 `alembic revision --autogenerate -m "add user management tables"` 生成迁移
- [x] 2.5 运行 `alembic upgrade head` 应用迁移到本地 DB

## 3. 加密模块

- [x] 3.1 实现 `app/core/crypto.py`：AES-256-GCM 加密函数 `encrypt(plaintext: str, key: bytes) -> str`（输出 `base64(iv || ciphertext || tag)`）
- [x] 3.2 实现 `decrypt(encrypted: str, key: bytes) -> str`：解析 version prefix，支持 `v1:` 前缀回退解密
- [x] 3.3 实现 key 加载函数：从 `AES_KEY` env var 解析 32 字节 base64 key

## 4. 认证模块

- [x] 4.1 定义 `OIDCProvider` Protocol（方法：`get_authorization_url(state) -> str`、`exchange_code(code) -> TokenResponse`、`get_userinfo(token) -> UserInfo`）
- [x] 4.2 实现 `DevOIDCProvider`：忽略 OIDC，构造 FakeUserInfo；构造函数接受 `X-Dev-User` header 值
- [x] 4.3 实现 `ProdOIDCProvider`：完整 OIDC discovery → auth → token → userinfo 流程
- [x] 4.4 实现 JWT 工具（`app/auth/jwt.py`）：`create_token(user_id, name) -> str`、`verify_token(token) -> dict`；使用 HS256 + `JWT_SECRET`
- [x] 4.5 实现 FastAPI `CurrentUser` 依赖（`app/auth/deps.py`）：从 `Authorization: Bearer` header 解析 JWT，注入 `user_id` 到 `request.state`
- [x] 4.6 实现 `AuthMiddleware` 或 dependency：`requires_auth` 保护端点

## 5. API 路由

- [x] 5.1 实现 `GET /auth/login`：生产模式重定向到 OIDC Provider；dev 模式直接 redirect 到 `/auth/callback?code=dev&state=dev`
- [x] 5.2 实现 `GET /auth/callback`：dev 模式检查 `X-Dev-User` header；生产模式交换 code；upsert User；签发 JWT 并返回 `{token, token_type}`
- [x] 5.3 实现 `GET /me`（需认证）：返回当前用户信息，config 永不出现在响应中
- [x] 5.4 实现 `PATCH /me`（需认证）：仅允许更新 `name` 字段
- [x] 5.5 实现 `GET /internal-providers`（需认证）：返回所有 kind=internal 的 provider，config 不返回
- [x] 5.6 实现 `GET /providers`（需认证）：返回当前用户的 provider 关联列表（join Provider），config 不返回
- [x] 5.7 实现 `POST /providers`（需认证）：解密 config 后用 AES 加密存入 DB；第一个 provider 自动设 `is_default=true`
- [x] 5.8 实现 `DELETE /providers/{provider_id}`（需认证）：删除 UserProvider 行；internal provider 返回 403；不属于该用户的 provider 返回 404
- [x] 5.9 实现 `PUT /providers/{provider_id}/default`（需认证）：将该 provider 设为 default，其他设为 false；不属于则返回 404
- [x] 5.10 统一返回格式：`config` 字段从所有响应中排除

## 6. 启动 Seed

- [x] 6.1 在 `app/core/providers.py` 中用 dataclass 定义 `InternalProvider`（name、config）；当前版本 config 可为空 dict `{}`
- [x] 6.2 实现 `seed_internal_providers()` 函数：启动时调用，upsert 所有定义的 internal provider
- [x] 6.3 在 `main.py` 或 lifespan 中注册启动事件，调用 `seed_internal_providers()`

## 7. 测试

- [x] 7.1 单元测试：`test_encrypt_decrypt_roundtrip`：加密后解密结果一致
- [x] 7.2 单元测试：`test_decrypt_detects_tampering`：篡改密文后解密抛出异常
- [x] 7.3 单元测试：`test_jwt_sign_and_verify`：签发后验证通过；过期 JWT 抛出异常
- [x] 7.4 集成测试：`test_dev_login_flow`：带 `X-Dev-User` header 登录，返回有效 JWT，可访问 `/me`
- [x] 7.5 集成测试：`test_provider_crud`：创建 → 列表 → 设默认 → 删除
- [x] 7.6 集成测试：`test_config_never_exposed`：创建 provider 后，列表响应中无 config 字段
- [x] 7.7 集成测试：`test_default_provider_reassignment`：删除默认 provider 后，自动升起另一个为默认
