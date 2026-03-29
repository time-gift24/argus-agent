# provider-editor Specification

## Purpose
定义 Provider 新增与编辑页面的路由、表单和面包屑行为。

## Requirements
### Requirement: Provider 新增页面
系统 SHALL 提供 `/providers/new` 路由用于新增 LLM 提供商，并以独立 body 页面承载完整表单而非弹窗。

#### Scenario: 新增页面展示
- **WHEN** 用户导航到 `/providers/new`
- **THEN** 显示 ProviderEditView 页面，包含固定在内容区左上角的面包屑 "LLM 提供商 > 新增提供商"
- **THEN** 表单字段包含：名称（必填）、API Key（必填）、Base URL（选填）、Model（选填）
- **THEN** 页面内同时展示测试连接与提交操作区

#### Scenario: 提交新增
- **WHEN** 用户填写表单并点击 "创建" 按钮
- **THEN** 调用 `POST /api/v1/providers` 创建提供商
- **THEN** 成功后重定向到 `/providers`

### Requirement: Provider 编辑页面
系统 SHALL 提供 `/providers/:id/edit` 路由用于编辑已有提供商，并以独立 body 页面承载完整表单和测试反馈。

#### Scenario: 编辑页面展示
- **WHEN** 用户导航到 `/providers/:id/edit`
- **THEN** 显示 ProviderEditView 页面，包含固定在内容区左上角的面包屑 "LLM 提供商 > 编辑 - {name}"
- **THEN** 表单预填充该提供商的当前配置
- **THEN** 测试连接结果和保存操作在页面内联展示，而不是通过弹窗反馈

#### Scenario: 提交编辑
- **WHEN** 用户修改表单并点击 "保存" 按钮
- **THEN** 调用 `PATCH /api/v1/providers/{id}` 更新提供商
- **THEN** 成功后重定向到 `/providers`

### Requirement: 面包屑导航
编辑/新增页面 SHALL 在 body 顶部左侧显示统一模板渲染的面包屑导航。

#### Scenario: 面包屑交互
- **WHEN** 用户在编辑/新增页面
- **THEN** 面包屑 "LLM 提供商" 可点击，导航回 `/providers`
- **THEN** 当前页面名称不可点击（面包屑末尾）
