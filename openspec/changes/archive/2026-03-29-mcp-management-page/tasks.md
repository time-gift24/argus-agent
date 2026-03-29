## 1. 路由与导航

- [x] 1.1 在 `router/index.js` 中新增 `/mcp` 路由，懒加载 `McpConfigsView` 组件
- [x] 1.2 在 `App.vue` 的 `navLinks` 中添加 "MCP 服务" 页签，位于 "提供商" 之后

## 2. MCP 配置页面骨架

- [x] 2.1 创建 `views/McpConfigsView.vue`，实现页面骨架（标题、空状态、加载状态）
- [x] 2.2 实现 `GET /api/v1/mcp-configs` 调用，展示配置卡片列表，区分 user/global 类型

## 3. 配置 CRUD

- [x] 3.1 实现创建配置模态框，支持 stdio/http/sse 三种 transport 类型，根据选择动态展示字段
- [x] 3.2 实现编辑配置模态框，预填当前值，调用 `PATCH` 更新
- [x] 3.3 实现删除确认弹窗，调用 `DELETE` 删除配置

## 4. 连接测试与工具浏览

- [x] 4.1 实现测试连接按钮，调用 `POST .../test`，展示成功/失败结果和工具列表
- [x] 4.2 实现查看缓存工具功能，调用 `GET .../tools`，展示工具名称、描述和参数 schema
