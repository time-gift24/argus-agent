# Backend

Python 后端，基于 FastAPI + SQLAlchemy + SQLite。

## 技术栈

| 类别 | 技术 |
|------|------|
| 框架 | FastAPI |
| ORM | SQLAlchemy 2.x (同步) |
| 数据库 | SQLite (dev/test) / 可换 PostgreSQL |
| 迁移 | Alembic |
| 包管理 | uv |
| 认证 | OIDC (生产) / Dev bypass (开发) |
| 加密 | AES-256-GCM (provider config) |
| JWT | python-jose HS256 |

## 目录结构

```
backend/
├── main.py                  # FastAPI app 入口，lifespan seed
├── Makefile                 # make test / lint / fmt
├── alembic/                 # 数据库迁移
├── app/
│   ├── api/
│   │   ├── router.py        # 路由聚合 (auth, users, providers)
│   │   └── endpoints/       # 各端点模块
│   │       ├── auth.py      #   /auth/login, /auth/callback
│   │       ├── users.py     #   /me (GET/PATCH)
│   │       └── providers.py #   /providers, /internal-providers
│   ├── auth/
│   │   ├── deps.py          # get_current_user_id, get_current_user 依赖
│   │   ├── jwt.py           # JWT 签发/验证
│   │   └── oidc.py          # OIDC 抽象 (ProdOIDCProvider / DevOIDCProvider)
│   ├── core/
│   │   ├── config.py        # Settings (pydantic-settings, 环境变量)
│   │   ├── crypto.py        # AES-256-GCM encrypt/decrypt
│   │   └── providers.py     # InternalProvider 定义 + seed
│   ├── db/
│   │   ├── base_class.py    # DeclarativeBase + TimestampMixin
│   │   └── session.py       # engine, SessionLocal, get_db
│   ├── models/
│   │   └── user.py          # User, Provider, UserProvider ORM
│   └── schemas/
│       └── user.py          # Pydantic 请求/响应 schema
└── tests/
    ├── conftest.py          # 测试 fixtures (内存 SQLite, monkeypatch)
    ├── test_auth.py         # 登录流程集成测试
    ├── test_auth_deps.py    # 认证依赖单元测试
    ├── test_crypto.py       # 加解密单元测试
    ├── test_jwt.py          # JWT 单元测试
    ├── test_providers.py    # Provider CRUD 集成测试
    └── test_users.py        # 用户 profile 集成测试
```

## 核心数据流

```
Request → CORS → Auth Deps (JWT → user_id) → Endpoint → SQLAlchemy → SQLite
```

### 认证流程

- **开发模式** (`DEV_MODE=true`): `X-Dev-User` header 直接构造用户，跳过 OIDC
- **生产模式**: `/auth/login` → OIDC Provider → `/auth/callback` → 换 token → upsert User → 签发 JWT

### Provider 加密存储

所有 Provider 的 config 字段用 AES-256-GCM 加密后存 DB，API 响应中永不含 config。

## 测试

```bash
make test           # 跑全部测试 (32 个)
make test-cov       # 跑覆盖率 (最低 80%)
make test-cov-open  # 生成 HTML 覆盖率报告
```

### 测试基础设施

- **DB**: `sqlite:///:memory:` + `StaticPool`，每个测试函数独立回滚
- **配置**: conftest.py 在 import 前注入测试环境变量 (`AES_KEY`, `JWT_SECRET`, `DEV_MODE=true`)
- **隔离**: monkeypatch `get_db` 和 lifespan 均走测试内存 DB，不碰生产数据
- **认证**: 测试通过 `X-Dev-User` header 获取 JWT，无需真实 OIDC

### 测试分类

| 测试文件 | 类型 | 覆盖范围 |
|----------|------|----------|
| test_crypto.py | 单元 | encrypt/decrypt roundtrip, 篡改检测 |
| test_jwt.py | 单元 | JWT 签发/验证/过期/篡改 |
| test_auth_deps.py | 单元 | get_current_user_id 依赖 + request.state |
| test_auth.py | 集成 | Dev 登录流程, upsert, JWT 可访问 /me |
| test_providers.py | 集成 | Provider CRUD, default 重分配, config 不泄露 |
| test_users.py | 集成 | PATCH /me, 忽略无关字段 |

## 环境变量

| 变量 | 必填 | 说明 |
|------|------|------|
| `AES_KEY` | 是 | AES-256 密钥 (base64, 32 字节) |
| `JWT_SECRET` | 是 | JWT 签名密钥 |
| `DEV_MODE` | 否 | `true` 启用开发模式 bypass |
| `OIDC_ISSUER` | 否 | OIDC Provider issuer URL |
| `OIDC_CLIENT_ID` | 否 | OAuth2 Client ID |
| `OIDC_CLIENT_SECRET` | 否 | OAuth2 Client Secret |
| `OIDC_REDIRECT_URI` | 否 | OAuth2 回调地址 |
| `DATABASE_URL` | 否 | 默认 `sqlite:///./argus_agents.db` |
