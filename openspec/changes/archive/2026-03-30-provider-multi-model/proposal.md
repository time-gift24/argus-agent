## Why

当前 Provider 的加密 config 中 `model` 是单一字符串（如 `gpt-4o`），但一个供应商（OpenAI、Anthropic）实际支持多个模型。用户需要：
- 在同一 Provider 下配置多个模型（gpt-4o、gpt-4o-mini 等）
- 对每个模型独立测试连通性
- 设置默认模型供 Agent 调用

## What Changes

- **BREAKING**: 新建 `ProviderModel` 数据库表（provider_id, name, is_default），将 `model` 从加密 config 中提取出来
- 后端：`config` 收窄为 `{api_key, base_url}`，新增 ProviderModel CRUD 端点，测试端点改为针对单个 model
- 前端：`ProviderConfigForm` 的单一 model 输入替换为模型列表管理（增/删/设默认/逐个测试）
- 数据迁移：Alembic 迁移将现有 `config.model` 提取到新表

## Capabilities

### New Capabilities
- `provider-model-management`: Provider 下的多模型管理 — CRUD + 每模型连通性测试 + 默认模型

### Modified Capabilities
- `provider-management`: Provider config 结构变更（移除 model 字段）
- `provider-connectivity-test`: 测试目标从 Provider 整体变为单个模型

## Impact

- **数据库**: 新增 `provider_models` 表 + Alembic 迁移（含数据迁移）
- **后端**: 新增 ORM/Schema/CRUD 端点，改造测试端点
- **前端**: ProviderConfigForm 重构（模型列表替代单输入框）
- **兼容性**: 现有 Provider 的 `config.model` 需迁移到新表，config 结构从三字段变为两字段
