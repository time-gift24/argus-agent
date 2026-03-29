## Context

当前 Provider 管理嵌在 SettingsView.vue 中，使用简单的表格 + TinyDialog 弹窗新增。用户需要更直观的卡片式列表和独立的编辑页面来管理 LLM 提供商。

已有基础设施：
- `stores/providers.js` — internalProviders / userProviders / fetchProviders / createProvider / deleteProvider / setDefaultProvider
- `api/providers.js` — listInternal / list / create / remove / setDefault
- 路由系统在 `router/index.js`，侧边栏导航在 `App.vue` 的 `sidebarItems` 和 `navLinks`

## Goals / Non-Goals

**Goals:**
- Provider 拥有独立页面 `/providers`，卡片化展示
- 新增/编辑 Provider 通过独立路由页面 + 面包屑导航
- 测试按钮占位（前端 UI 就绪，后端接口预留）
- 从 SettingsView 中移除 Provider section

**Non-Goals:**
- 后端测试接口实现（仅前端占位）
- Provider 高级配置（rate limit、token limit 等）
- Provider 分组/标签功能

## Decisions

### D1: 路由设计
```
/providers          → ProvidersView.vue（卡片列表）
/providers/new      → ProviderEditView.vue（新增）
/providers/:id/edit → ProviderEditView.vue（编辑）
```
使用同一个 ProviderEditView 组件，通过 route params 区分新增/编辑模式。

### D2: 卡片布局
每张卡片展示：
- Provider 名称 + 默认标记（★）
- API Key 脱敏显示（sk-***xxx）
- Base URL / Model 信息
- 操作按钮：设为默认 / 编辑 / 测试 / 删除

卡片使用项目设计系统：`bg-surface-container-lowest rounded-[2rem] p-6 shadow-sm`

### D3: 面包屑导航
编辑/新增页面顶部显示面包屑：
```
LLM 提供商 > 新增提供商
LLM 提供商 > 编辑 - {name}
```
点击 "LLM 提供商" 返回列表页。

### D4: 测试按钮占位
卡片上显示 "测试连接" 按钮，点击后调用 `POST /api/v1/providers/{id}/test`（后端未实现，前端 try/catch 捕获 404 并提示"功能开发中"）。

### D5: 侧边栏导航
将 sidebarItems 中的 "API 密钥"（path: /agents）改为 "LLM 提供商"（path: /providers），更新图标。在 navLinks 中也增加 "提供商" 顶部导航项。

## Risks / Trade-offs

- **[测试按钮无后端]** → 前端 graceful fallback，提示"功能开发中"，不影响其他功能
- **[SettingsView 移除 Provider 后可能显得空]** → 保留通用设置和安全设置 section，后续可扩展
