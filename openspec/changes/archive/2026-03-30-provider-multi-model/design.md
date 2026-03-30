## Context

当前 Provider 的加密 config 存储三个字段：`{api_key, base_url, model}`。其中 `api_key` 和 `base_url` 是供应商级别的共享凭据，而 `model` 是具体的模型标识。一个供应商（如 OpenAI）支持多个模型，当前单 model 字段无法表达这种一对多关系。

后端已有完整的 Provider CRUD（含 GET by ID / PATCH），config 通过 AES-256-GCM 加密存储。前端 `ProviderConfigForm` 是独立组件，包含单一 model 输入框。连通性测试已有两套：`test_config_connectivity`（表单测试）和 `test_provider_connectivity`（已保存 Provider 测试）。

## Goals / Non-Goals

**Goals:**
- Provider 支持多个模型配置，每个模型可独立测试连通性
- 用户可指定默认模型（供 Agent 调用使用）
- 现有数据平滑迁移

**Non-Goals:**
- 模型级别的参数配置（context_window、max_tokens 等）— 后续按需添加
- 模型的启用/禁用状态 — 当前所有添加的模型均可用
- 模型分组或分类功能

## Decisions

### D1: ProviderModel 独立表 vs 保留在 config 中

**选择**: 新建 `provider_models` 表，model 从 config 中移出。

**理由**: model 是结构化数据（需要 CRUD、设置默认、独立测试），放在加密的 config Text 字段中无法被后端直接查询和操作。独立表使得 model 的增删改不需要重新加密整个 config。

**替代方案**: 将 models 数组保留在加密 config 中 — 不可行，因为无法对加密数据做 SQL 查询，且每次操作 model 都需要解密→修改→重新加密整个 config。

### D2: ProviderModel schema（极简）

```python
class ProviderModel(Base):
    __tablename__ = "provider_models"

    id: String(36) PK
    provider_id: String(36) FK(providers.id, CASCADE)
    name: String(128) NOT NULL        # 模型标识，如 "gpt-4o"
    is_default: Boolean NOT NULL False
    created_at: DateTime
    updated_at: DateTime

    UniqueConstraint(provider_id, name)  # 同一 Provider 下模型名唯一
```

**不包含 context_window / max_tokens 的理由**: YAGNI — 当前没有消费这些字段的代码，等有实际需求时再扩展。

### D3: Config 收窄

`ProviderConfigInput` 从 `{api_key, base_url, model}` 变为 `{api_key, base_url}`。`model` 字段从 schema 中移除。

**理由**: api_key 和 base_url 是供应商级别的共享凭据（同一供应商的多个模型共用），model 已独立建表。

### D4: API 设计

在现有 `/providers/{provider_id}/` 下挂载子资源：

| Method | Path | 说明 |
|--------|------|------|
| GET | `/providers/{provider_id}/models` | 列出 Provider 下所有模型 |
| POST | `/providers/{provider_id}/models` | 添加模型 |
| DELETE | `/providers/{provider_id}/models/{model_id}` | 删除模型 |
| PUT | `/providers/{provider_id}/models/{model_id}/default` | 设为默认 |
| POST | `/providers/{provider_id}/models/{model_id}/test` | 测试单个模型 |

现有 `POST /providers/test-config` 调整：body 增加 `model: str` 字段（原在 config 内，现独立传入）。

现有 `POST /providers/{provider_id}/test` 保留但语义变为测试该 Provider 的默认模型。

### D5: 数据迁移策略

Alembic 迁移步骤：
1. 创建 `provider_models` 表
2. 遍历所有 Provider，解密 config → 提取 `model` 字段 → 插入 `provider_models` 行（is_default=True）→ 从 config JSON 中移除 `model` → 重新加密写回
3. 无 model 的 Provider 跳过（config 中 model 原本就是可选的）

## Risks / Trade-offs

- **[迁移风险]** 解密→重加密所有 Provider config 可能因 key 变更或数据损坏失败 → 迁移中 catch 异常并 log warning，跳过有问题的 Provider，不阻塞整体迁移
- **[空模型列表]** 迁移后如果 Provider 无任何模型（原本就没配 model），测试端点需给出明确提示 → 返回 "该 Provider 尚未配置模型"
- **[默认模型约束]** 同一 Provider 下只能有一个默认模型 → 创建第一个模型自动设为默认，删除默认模型时自动将最近添加的模型设为默认（与 Provider 的 default 逻辑一致）
