## Context

后端 MCP 配置管理 API 已完成（PR #12），提供 6 个端点用于 MCP Server 配置的 CRUD、连接测试和工具缓存查询。前端目前有 Providers 页面作为类似的配置管理模式可参考。导航栏和侧边栏均定义在 `App.vue` 中，路由在 `router/index.js` 中注册。

## Goals / Non-Goals

**Goals:**
- 在导航栏新增 MCP 服务入口，提供配置管理的完整 UI
- 复用 Providers 页面的 UI 模式，保持一致的视觉语言
- 支持 stdio/http/sse 三种 transport 类型的配置创建和编辑
- 支持连接测试和工具浏览的交互反馈

**Non-Goals:**
- 不实现 MCP 工具的在线调用/执行（仅展示工具列表）
- 不实现全局配置的创建 UI（全局配置由 admin 通过 API 管理，页面仅展示）
- 不实现 admin 角色判断的前端逻辑（后端已做权限校验，前端透传错误即可）

## Decisions

### 1. 单页面模式（非列表+详情分离）

**选择**：一个 `McpConfigsView.vue` 页面，通过模态框/抽屉处理创建和编辑。

**替代方案**：像 Providers 一样拆分为列表页 + 编辑页（两个路由）。

**理由**：MCP 配置的编辑频率低于 Provider，单页面 + 弹窗更轻量，减少路由和组件数量。

### 2. 复用 Providers 的 API 调用模式

**选择**：直接在组件内使用 `fetch` 调用后端 API，与 ProvidersView 保持一致。

**替代方案**：抽取共享的 API composable 或 Pinia store。

**理由**：YAGNI 原则，当前只有 MCP 配置一个领域需要这些 API 调用，过早抽象增加复杂度。

### 3. 仅添加到顶部导航栏

**选择**：只在 `navLinks` 中添加 "MCP 服务" 入口。

**替代方案**：同时在侧边栏添加。

**理由**：MCP 配置属于基础设施管理，与 Providers 同层级，放入顶部导航栏即可。

## Risks / Trade-offs

- [stdio 配置创建可能被后端拒绝] → 前端不隐藏入口，透传后端 403 错误信息给用户
- [工具缓存可能为空] → 展示空状态提示，引导用户先执行测试连接
