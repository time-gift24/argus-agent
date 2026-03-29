# provider-list-page Specification

## Purpose
定义 Provider 列表页的共享头部、卡片动作与内联测试反馈。

## Requirements
### Requirement: Provider 列表页统一 body 头部
系统 SHALL 在 `/providers` 页面通过共享 body 页面模板展示固定位置的面包屑和页面级主操作。

#### Scenario: 访问 Provider 列表
- **WHEN** 用户导航到 `/providers`
- **THEN** 显示 ProvidersView 页面，包含位于内容区左上角的面包屑 "LLM 提供商"
- **THEN** "新增提供商" 作为页面级主操作显示在面包屑下方的独立区域

#### Scenario: 未登录态
- **WHEN** 用户未登录且访问 `/providers`
- **THEN** 页面显示 "请先登录" 提示，不展示提供商列表

### Requirement: Provider 卡片布局
每个提供商 SHALL 以卡片形式展示，包含名称、配置摘要和操作按钮。

#### Scenario: 内部提供商卡片
- **WHEN** 系统展示内部提供商列表
- **THEN** 每张卡片显示提供商名称
- **THEN** 卡片无删除/编辑按钮（只读）

#### Scenario: 用户提供商卡片
- **WHEN** 系统展示用户创建的提供商列表
- **THEN** 每张卡片显示：名称、默认标记（★）、API Key 脱敏、操作按钮
- **THEN** 操作按钮包含：设为默认、编辑、测试连接、删除

### Requirement: Provider 列表页内联测试反馈
每张用户提供商卡片 SHALL 提供真实可用的 "测试连接" 按钮，并在卡片内联显示测试结果。

#### Scenario: 点击测试连接
- **WHEN** 用户点击 "测试连接" 按钮
- **THEN** 前端调用 `POST /api/v1/providers/{id}/test`
- **THEN** 成功或失败结果以内联状态块显示在当前卡片中

### Requirement: 侧边栏导航入口
侧边栏 SHALL 包含 "LLM 提供商" 导航项，指向 `/providers`。

#### Scenario: 侧边栏导航
- **WHEN** 侧边栏展开
- **THEN** 显示 "LLM 提供商" 导航项，图标为服务器/云图标
- **THEN** 点击后导航到 `/providers`
