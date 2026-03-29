# provider-test Specification

## Purpose
定义用户 Provider 连通性测试端点及其返回语义，保证前端可进行真实联通性验证。
## Requirements
### Requirement: Provider 连通性测试端点
系统 SHALL 提供 `POST /api/v1/providers/{provider_id}/test` 端点，使用 langchain-openai 测试提供商配置的可达性。

#### Scenario: 测试成功
- **WHEN** 用户对自己的 Provider 调用测试端点
- **THEN** 后端解密 config，实例化 ChatOpenAI 并发送测试消息
- **THEN** 返回 `{ success: true, message: "连接成功", latency_ms: <int> }`

#### Scenario: 测试失败（无效 API Key）
- **WHEN** API Key 无效或过期
- **THEN** 返回 `{ success: false, message: "<错误描述>", latency_ms: null }`，HTTP 200

#### Scenario: 无权测试他人 Provider
- **WHEN** 用户尝试测试不属于自己的 Provider
- **THEN** 返回 HTTP 404
