## Context

Provider 的 config 存储为 AES-256-GCM 加密的 JSON，包含 `api_key`、`base_url`、`model` 三个字段。后端已有加解密工具（`app/core/security.py`）。

当前依赖中无 LLM SDK，需要新增 `langchain-openai`。

## Goals / Non-Goals

**Goals:**
- 后端实现 `POST /providers/{id}/test` 端点
- 使用 `langchain-openai` 的 `ChatOpenAI` 发送简单 ping 请求
- 返回成功/失败状态、延迟毫秒数、错误信息

**Non-Goals:**
- 不实现流式响应
- 不实现模型列表获取
- 不支持非 OpenAI 兼容 API

## Decisions

### D1: 使用 langchain-openai ChatOpenAI
`ChatOpenAI` 支持 `openai_api_base`（自定义 base_url）和 `model_name`，直接兼容 OpenAI API 格式。

### D2: 实现流程
1. 根据 provider_id + 当前用户查询 UserProvider
2. 解密 config 获取 api_key、base_url、model
3. 实例化 ChatOpenAI，发送 invoke([HumanMessage("Hi")])
4. 计时返回 `{ success, message, latency_ms }`

### D3: 响应 schema
```python
class ProviderTestResult(BaseModel):
    success: bool
    message: str
    latency_ms: int | None = None
```

## Risks / Trade-offs

- **[超时]** → 设置 request_timeout=10
- **[API Key 泄露]** → 日志不记录 API Key
