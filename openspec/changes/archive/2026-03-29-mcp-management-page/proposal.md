## Why

后端 MCP Server 配置管理 API 已就绪（PR #12），但缺少前端界面。用户需要一个可视化页面来创建、管理和测试 MCP Server 连接配置，而非直接调用 API。

## What Changes

- 在顶部导航栏 `navLinks` 中新增 "MCP 服务" 页签，路由 `/mcp`
- 新增 `McpConfigsView.vue` 页面，承载 MCP 配置的完整管理功能：
  - 配置列表：展示用户的 + 全局的 MCP 配置，区分 transport 类型（stdio/http/sse）和 kind（user/global）
  - 新增配置：表单支持三种 transport，stdio 类型仅 admin 可创建
  - 编辑配置：修改已有配置，变更后自动清除工具缓存
  - 删除配置：删除确认，stdio 类型仅 admin 可删除
  - 测试连接：触发后端 test 端点，展示连通性结果和发现的工具列表
  - 查看工具：展示已缓存的工具列表（名称、描述、参数 schema）
- 新增路由 `/mcp` 注册到 router
- 复用现有 Providers 页面的 UI 模式（卡片列表 + 编辑表单）

## Capabilities

### New Capabilities

- `mcp-config-ui`: MCP 配置管理前端页面，包含配置 CRUD、连接测试、工具浏览的完整交互流程

### Modified Capabilities

（无现有 spec 需要修改）

## Impact

- **前端文件**：`App.vue`（导航）、`router/index.js`（路由）、新增 `views/McpConfigsView.vue`
- **API 依赖**：后端 6 个 MCP 配置端点（PR #12 已实现）
- **样式**：复用现有 design token（surface-container、primary、on-surface 等）
