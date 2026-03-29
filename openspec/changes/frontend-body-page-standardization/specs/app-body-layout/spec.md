## ADDED Requirements

### Requirement: 统一的 route body 页面骨架
系统 SHALL 为具体业务 route 页面提供统一的 body 页面骨架，包含位于内容区左上角的面包屑区、页面标题/说明区和页面级操作区。

#### Scenario: 访问具体业务页面
- **WHEN** 用户访问 `/dashboard`、`/agents`、`/agents/:id`、`/tools`、`/shell`、`/logs`、`/settings`、`/providers`、`/providers/new`、`/providers/:id/edit`、`/mcp`、`/mcp/new` 或 `/mcp/:id/edit`
- **THEN** 页面 body 顶部显示一致的头部骨架，并与内容区左边界对齐
- **THEN** 面包屑位于标题和说明之前

### Requirement: 面包屑在页面滚动时保持可见
系统 SHALL 让 body 页面的面包屑区在内容区滚动时保持固定可见，并位于全局 top nav 之下。

#### Scenario: 长页面滚动
- **WHEN** 用户在内容超过一屏的具体业务页面内向下滚动
- **THEN** 面包屑区仍固定显示在内容区左上角
- **THEN** 页面正文在其下方滚动，不遮挡面包屑文字

### Requirement: 复杂业务录入流程使用独立页面
系统 SHALL 将复杂的创建/编辑流程放在独立路由页面中，而不是通过业务表单弹窗承载；弹窗仅保留给防呆和保护性场景。

#### Scenario: 从列表页发起创建或编辑
- **WHEN** 用户从 Provider 或 MCP 列表页发起创建或编辑操作
- **THEN** 系统导航到对应的独立页面路由完成录入
- **THEN** 系统不打开包含完整业务表单的弹窗

#### Scenario: 保留防呆弹窗
- **WHEN** 用户执行登录拦截或删除确认这类短链路保护性操作
- **THEN** 系统仍可使用弹窗进行确认或提醒
