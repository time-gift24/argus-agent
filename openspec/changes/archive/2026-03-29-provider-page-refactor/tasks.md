## 1. 路由与导航

- [x] 1.1 在 `router/index.js` 添加 `/providers`、`/providers/new`、`/providers/:id/edit` 三个路由
- [x] 1.2 在 `App.vue` sidebarItems 中将 "API 密钥" 替换为 "LLM 提供商"（path: /providers，更新图标）
- [x] 1.3 在 `App.vue` navLinks 中添加 "提供商" 导航项

## 2. Provider 列表页

- [x] 2.1 创建 `ProvidersView.vue` — 卡片化展示内部提供商和用户提供商
- [x] 2.2 内部提供商卡片只读展示（名称）
- [x] 2.3 用户提供商卡片展示名称、默认标记、API Key 脱敏、操作按钮（设为默认/编辑/测试/删除）
- [x] 2.4 "测试连接" 按钮 — 调用 `POST /api/v1/providers/{id}/test`，404 时提示 "功能开发中"
- [x] 2.5 删除确认交互

## 3. Provider 编辑页

- [x] 3.1 创建 `ProviderEditView.vue` — 面包屑导航 + 表单（名称、API Key、Base URL、Model）
- [x] 3.2 新增模式（/providers/new）— 空表单，提交调用 `POST /api/v1/providers`
- [x] 3.3 编辑模式（/providers/:id/edit）— 预填充表单，提交调用 `PATCH /api/v1/providers/{id}`

## 4. 清理

- [x] 4.1 从 `SettingsView.vue` 移除 LLM Providers section
- [x] 4.2 确认构建通过
