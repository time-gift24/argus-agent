## ADDED Requirements

### Requirement: Test-config endpoint for unsaved provider config
系统 SHALL 提供 `POST /api/v1/providers/test-config` 端点，接受原始 `{ api_key, base_url?, model? }` 直接测试连通性。

#### Scenario: Successful test with raw config
- **WHEN** 用户传入有效的 `{ api_key, base_url }` 调用 `POST /providers/test-config`
- **THEN** 系统返回 `{ "success": true, "latency_ms": <毫秒数>, "message": "连接成功" }`

#### Scenario: Invalid API Key
- **WHEN** 用户传入无效的 api_key
- **THEN** 系统返回 `{ "success": false, "message": "<错误详情>" }`

#### Scenario: Missing api_key
- **WHEN** 请求体缺少 api_key
- **THEN** 系统返回 HTTP 422 验证错误

#### Scenario: Unreachable base_url
- **WHEN** base_url 无法连接
- **THEN** 系统返回 `{ "success": false, "message": "连接失败: <错误详情>" }`

### Requirement: Inline test result on provider list cards
列表页每张 Provider 卡片 SHALL 内联展示测试结果，不使用弹窗。

#### Scenario: Click test button on card
- **WHEN** 用户点击卡片上的「测试连接」按钮
- **THEN** 按钮变为 loading 态（禁用 + 加载指示），同时卡片内出现测试状态区域

#### Scenario: Test succeeds inline
- **WHEN** 后端返回 `success: true`
- **THEN** 按钮恢复，卡片内显示绿色状态点 + "连接成功" + 延迟毫秒数

#### Scenario: Test fails inline
- **WHEN** 后端返回 `success: false`
- **THEN** 按钮恢复，卡片内显示红色状态点 + 错误信息

#### Scenario: Multiple cards test independently
- **WHEN** 用户在多张卡片上依次点击测试
- **THEN** 每张卡片的测试状态独立，互不影响

### Requirement: Test button on create/edit form
新增/编辑页 SHALL 在表单底部提供「测试连接」按钮。

#### Scenario: Test with form values
- **WHEN** 用户填写 api_key 和可选的 base_url/model 后点击「测试连接」
- **THEN** 调用 `POST /providers/test-config`，结果展示在按钮下方

#### Scenario: Test succeeds in form
- **WHEN** 测试成功
- **THEN** 按钮下方显示绿色状态点 + "连接成功" + 延迟

#### Scenario: Test fails in form
- **WHEN** 测试失败
- **THEN** 按钮下方显示红色状态点 + 错误信息

#### Scenario: Missing required fields
- **WHEN** api_key 为空时点击测试
- **THEN** 不发起请求，前端提示"请先填写 API Key"
