## Why

LLM 提供商管理当前嵌在 SettingsView.vue 的一个 tab section 中，UI 受限且缺乏扩展性。随着 Provider 功能（模型配置、连通性测试）的增强，需要一个独立的页面来承载更丰富的交互。

## What Changes

- **新增** 独立的 `/providers` 路由和 `ProvidersView.vue` 页面
- **新增** 侧边栏 "LLM 提供商" 导航项（替换原 sidebar "API 密钥" 或新增独立入口）
- **重构** Provider 列表为卡片布局（每张卡片展示名称、默认标记、测试按钮）
- **新增** `/providers/new` 和 `/providers/:id/edit` 路由，使用面包屑导航
- **新增** Provider 编辑/新增页面，包含表单字段：名称、API Key、Base URL、Model
- **新增** 测试按钮 UI（调用后端连通性测试接口，后端尚未实现，前端先占位）
- **移除** SettingsView.vue 中的 LLM Providers section

## Capabilities

### New Capabilities
- `provider-list-page`: Provider 独立页面 — 卡片化列表、默认标记、测试按钮
- `provider-editor`: Provider 编辑/新增页面 — 面包屑导航、表单、连通性测试占位

### Modified Capabilities

(无)
