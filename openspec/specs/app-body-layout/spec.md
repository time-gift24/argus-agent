# app-body-layout Specification

## Purpose
定义统一的业务 body 页面模板、固定面包屑位置和页面级操作布局规则。

## Requirements
### Requirement: 统一的 body 页面模板
系统 SHALL 为业务 route 页面提供统一的 body 页面模板，并由共享组件负责渲染页面顶部结构。

#### Scenario: 访问业务页面
- **WHEN** 用户访问 `/dashboard`、`/agents`、`/agents/:id`、`/tools`、`/shell`、`/logs`、`/settings`、`/providers`、`/providers/new`、`/providers/:id/edit`、`/mcp`、`/mcp/new` 或 `/mcp/:id/edit`
- **THEN** 页面 body 顶部使用一致的公共模板
- **THEN** 该模板为页面提供语义标题和可复用的顶部结构

### Requirement: 面包屑位置统一
body 页面模板 SHALL 在内容区左上角使用固定宽度容器渲染面包屑，且该位置不随具体页面内容宽度变化。

#### Scenario: 窄表单页与宽列表页切换
- **WHEN** 用户在窄内容页面与宽内容页面之间切换
- **THEN** 面包屑都显示在统一的左上起点
- **THEN** 面包屑容器不跟随页面内容区宽度收窄或放大

### Requirement: 页面级操作与面包屑分层
body 页面模板 SHALL 将页面级操作放在面包屑下方的独立区域，而不是改变面包屑所在行的布局。

#### Scenario: 页面存在主操作
- **WHEN** 页面提供如“新增提供商”或“新增配置”这类主操作
- **THEN** 面包屑仍保持在固定位置
- **THEN** 操作按钮显示在其下方的独立操作区

### Requirement: 复杂录入流程使用独立页面
系统 SHALL 将复杂的创建与编辑流程放在独立路由页面中，而不是使用业务大表单弹窗；弹窗仅用于防呆与保护性场景。

#### Scenario: 从列表页发起创建或编辑
- **WHEN** 用户从 Provider 或 MCP 列表页发起创建或编辑操作
- **THEN** 系统导航到对应的独立页面路由完成录入
- **THEN** 系统不打开承载完整业务表单的弹窗

#### Scenario: 保留保护性弹窗
- **WHEN** 用户执行删除确认或登录补救这类短链路保护性操作
- **THEN** 系统仍可使用弹窗进行确认或提醒
