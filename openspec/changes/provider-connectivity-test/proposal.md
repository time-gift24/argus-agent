## Why

前端 Provider 卡片已有 "测试连接" 按钮，但后端缺少对应接口。需要实现一个连通性测试端点，使用 `langchain-openai` 向 LLM 发送简单请求以验证 API Key + Base URL + Model 是否可达。

## What Changes

- **新增** `langchain-openai` 依赖
- **新增** `POST /api/v1/providers/{provider_id}/test` 端点
- **新增** `ProviderTestResult` 响应 schema（success, message, latency_ms）
- **新增** 服务层函数 `test_provider_connectivity(provider)` 解密 config 并调用 LLM
- **前端** 测试按钮已有，调用该接口并展示结果即可

## Capabilities

### New Capabilities
- `provider-test`: Provider 连通性测试 — 使用 langchain-openai 验证 API 配置可用性

### Modified Capabilities

(无)
