# provider-management-ui Specification

## Purpose
定义早期 Settings 页面中的 Provider 管理界面行为。

## Requirements
### Requirement: 内部 Providers 只读列表
Settings 页面 LLM Providers 区域 SHALL 展示 GET /api/v1/internal-providers 返回的内部 providers 列表。内部 providers 只读，不可编辑或删除。

#### Scenario: 显示内部 providers
- **WHEN** 用户进入 Settings 页面且已登录
- **THEN** 前端调用 GET /api/v1/internal-providers
- **THEN** 显示内部 provider 名称列表，标记为 INTERNAL 类型

#### Scenario: 未登录态
- **WHEN** 用户未登录进入 Settings 页面
- **THEN** Provider 区域显示 "请先登录" 提示

### Requirement: 用户 Providers 列表
Settings 页面 SHALL 展示 GET /api/v1/providers 返回的当前用户关联的 providers 列表，显示名称、是否默认（★ 标记），以及操作按钮（设为默认、删除）。

#### Scenario: 显示用户 providers
- **WHEN** 已登录用户进入 Settings 页面
- **THEN** 前端调用 GET /api/v1/providers 获取用户 providers
- **THEN** 列表显示每个 provider 的名称、★ Default 标记（仅默认 provider）、Set Default 按钮（非默认 provider）、Delete 按钮

#### Scenario: 无用户 providers
- **WHEN** 已登录用户无任何 provider
- **THEN** 列表区域显示空状态提示

### Requirement: 添加 Provider
Settings 页面 SHALL 提供 "Add Provider" 按钮，点击后弹出表单（TinyDialog），包含字段：Name（必填）、API Key（必填）、Base URL（可选）、Model（可选）。确认后 POST /api/v1/providers。

#### Scenario: 成功添加 Provider
- **WHEN** 用户填写 Name="My OpenAI"、API Key="sk-xxx" 并确认
- **THEN** 前端发送 POST /api/v1/providers，body: {name, config: {api_key, base_url, model}}
- **THEN** 创建成功后刷新 provider 列表
- **THEN** 关闭弹窗

#### Scenario: 首个 Provider 自动设为默认
- **WHEN** 用户添加第一个 provider
- **THEN** 后端自动设置 is_default=true
- **THEN** 刷新后列表中该 provider 显示 ★ Default 标记

#### Scenario: 添加失败
- **WHEN** 后端返回 400/422/500
- **THEN** 弹窗显示错误信息，不关闭

#### Scenario: 表单校验
- **WHEN** 用户未填写必填字段（Name 或 API Key）点击确认
- **THEN** 表单显示校验提示，不发送请求

### Requirement: 删除 Provider
用户 providers 列表中每项 SHALL 提供 Delete 按钮。点击后弹出确认提示（window.confirm 或 TinyDialog），确认后 DELETE /api/v1/providers/{id}。

#### Scenario: 成功删除非默认 Provider
- **WHEN** 用户删除一个非默认 provider 并确认
- **THEN** 前端发送 DELETE /api/v1/providers/{id}
- **THEN** 刷新 provider 列表，该 provider 不再显示

#### Scenario: 删除默认 Provider 自动转移
- **WHEN** 用户删除默认 provider 并确认
- **THEN** 后端自动将下一个 provider 设为默认
- **THEN** 刷新后列表显示新的默认 provider 带 ★ 标记

### Requirement: 设为默认 Provider
非默认 provider 的操作区 SHALL 提供 "Set Default" 按钮。点击后 PUT /api/v1/providers/{id}/default。

#### Scenario: 成功设为默认
- **WHEN** 用户点击某 provider 的 "Set Default"
- **THEN** 前端发送 PUT /api/v1/providers/{id}/default
- **THEN** 刷新后仅该 provider 显示 ★ Default 标记

### Requirement: Providers Pinia Store
系统 SHALL 提供 providers Pinia store，管理 provider 数据和 CRUD 操作。

#### Scenario: Store 初始化（已登录）
- **WHEN** store fetchProviders action 被调用
- **THEN** 并行调用 GET /api/v1/internal-providers 和 GET /api/v1/providers
- **THEN** 分别存储 internalProviders 和 userProviders

#### Scenario: Store CRUD 操作后自动刷新
- **WHEN** createProvider / deleteProvider / setDefault action 完成
- **THEN** 自动重新调用 fetchProviders 刷新列表
