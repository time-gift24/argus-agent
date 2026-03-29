## Why

当前 Provider 的 config 中只有一个 `model` 字符串，但实际上一个供应商（如 OpenAI）支持多个模型（gpt-4o、gpt-4o-mini 等），每个模型有不同的属性（context_window、max_tokens 等）。用户需要在 Provider 下管理多个模型配置，并对每个模型单独测试连通性。

## What Changes

- **BREAKING**: 新建 `ProviderModel` 数据库表（provider_id, name, context_window, max_tokens, is_default 等），替代 config 中的单一 `model` 字段
- 后端：ProviderModel CRUD 端点，连通性测试端点改为针对单个 model
- 前端：Provider 编辑页增加模型列表管理（增删改），每个模型可单独测试

## Capabilities

### New Capabilities
- `provider-model-management`: Provider 下的多模型管理 — CRUD + 每模型连通性测试

### Modified Capabilities

## Impact

- **数据库**: 新增 `provider_models` 表 + Alembic 迁移
- **后端**: 新增 ORM 模型、Schema、CRUD 端点、测试端点改造
- **前端**: ProviderEditView 大幅改造（模型列表 + 内联测试）
- **兼容性**: 现有 Provider 的 `config.model` 字段需迁移到新表
