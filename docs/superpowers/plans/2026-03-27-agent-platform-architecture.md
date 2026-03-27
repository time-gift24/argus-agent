# Agent 管理平台 - Web 服务架构搭建计划

> **For agentic workers:** 使用 superpowers:subagent-driven-development 执行本计划。

**Goal:** 搭建 Web 服务层（FastAPI + SQLAlchemy），实现 Agent、PromptTemplate、Tool 的配置管理 CRUD API。

**Architecture:** 分层架构，API 层 → Service 层 → 数据层。

**Tech Stack:** FastAPI 0.135.1 · SQLAlchemy 2.0.48 · Pydantic v2 · Alembic

---

## Chunk 1: 依赖配置

**Files:**
- Modify: `backend/pyproject.toml`

- [ ] **Step 1: 更新 pyproject.toml**

```toml
[project]
name = "argus-agents"
version = "0.1.0"
description = "Agent Management Platform"
readme = "README.md"
requires-python = ">=3.12"

dependencies = [
    "fastapi==0.135.1",
    "uvicorn[standard]==0.41.0",
    "sqlalchemy==2.0.48",
    "pydantic==2.12.5",
    "pydantic-settings==2.13.1",
    "alembic==1.18.1",
    "python-multipart>=0.0.22",
]

[tool.uv]
dev-dependencies = [
    "pytest>=8.3.0",
    "pytest-asyncio>=0.25.0",
    "httpx>=0.28.1",
]
```

- [ ] **Step 2: 安装依赖**

Run: `cd /Users/wanyaozhong/Projects/argus-agents/backend && uv sync`

- [ ] **Step 3: 提交**

```bash
git add backend/pyproject.toml
git commit -m "feat: add web service dependencies"
```

---

## Chunk 2: 核心配置

**Files:**
- Create: `backend/app/core/config.py`
- Create: `backend/app/core/__init__.py`

- [ ] **Step 1: 创建 config.py**

```python
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "argus-agents"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    DATABASE_URL: str = "sqlite:///./argus_agents.db"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
```

- [ ] **Step 2: 提交**

```bash
git add app/core/
git commit -m "feat: add core config"
```

---

## Chunk 3: 数据库层

**Files:**
- Create: `backend/app/db/models.py`
- Create: `backend/app/db/__init__.py`

**数据模型:**

- `LLMProvider` — LLM Provider 配置（名称、API Base URL、模型列表、API Key 等）

- [ ] **Step 1: 创建 base_class.py**

```python
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import DateTime, func


class Base(DeclarativeBase):
    pass


class TimestampMixin:
    created_at: datetime = datetime
    updated_at: datetime = datetime
```

- [ ] **Step 2: 创建 models.py**

```python
import uuid
from sqlalchemy import Column, String, Text, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID
from app.db.base_class import Base, TimestampMixin


class LLMProvider(Base, TimestampMixin):
    __tablename__ = "llm_providers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(128), unique=True, nullable=False, index=True)
    api_base = Column(String(512), nullable=True)
    api_key = Column(String(512), nullable=True)
    models = Column(JSON, default=list)
    is_active = Column(Boolean, default=True)
```

- [ ] **Step 3: 创建 session.py**

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False}, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

- [ ] **Step 4: 提交**

```bash
git add app/db/
git commit -m "feat: add database models and session"
```

---

## Chunk 4: Pydantic Schemas

**Files:**
- Create: `backend/app/schemas/llm_provider.py`
- Create: `backend/app/schemas/__init__.py`

**数据模型:**

- `LLMProvider` — LLM Provider 配置

- [ ] **Step 1: 创建 schemas (agent.py, prompt.py, tool.py)**

标准 CRUD Schema：Base / Create / Update / Read

- [ ] **Step 2: 提交**

```bash
git add app/schemas/
git commit -m "feat: add pydantic schemas"
```

---

## Chunk 5: Service 层

**Files:**
- Create: `backend/app/services/llm_provider_service.py`
- Create: `backend/app/services/__init__.py`

标准 CRUD Service

- [ ] **Step 1: 提交**

```bash
git add app/services/
git commit -m "feat: add service layer"
```

---

## Chunk 6: API 路由层

**Files:**
- Create: `backend/app/api/endpoints/llm_providers.py`
- Create: `backend/app/api/router.py`
- Create: `backend/app/api/deps.py`
- Create: `backend/app/api/__init__.py`
- Create: `backend/app/api/endpoints/__init__.py`

标准 REST CRUD 端点

- [ ] **Step 1: 提交**

```bash
git add app/api/
git commit -m "feat: add api routes"
```

---

## Chunk 7: FastAPI 入口

**Files:**
- Create: `backend/app/main.py`
- Create: `backend/app/__init__.py`

- [ ] **Step 1: 提交**

```bash
git add app/main.py
git commit -m "feat: add fastapi entry point"
```

---

## 目录结构

```
backend/
├── app/
│   ├── api/
│   │   ├── endpoints/       # llm_providers.py
│   │   ├── deps.py         # get_db
│   │   └── router.py       # 路由汇总
│   ├── core/
│   │   └── config.py       # Settings
│   ├── db/
│   │   ├── models.py       # LLMProvider
│   │   └── session.py      # engine, SessionLocal
│   ├── schemas/            # Pydantic schemas
│   ├── services/           # 业务逻辑
│   └── main.py             # FastAPI 入口
├── agents/                 # (暂不搭建)
├── alembic/                 # (暂不搭建)
└── tests/
```
