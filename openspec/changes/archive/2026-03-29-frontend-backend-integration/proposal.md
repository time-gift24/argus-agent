## Why

后端已完整实现 auth (DevMode/OIDC)、users (GET/PATCH /me)、providers (CRUD + internal) 三组 API，但前端全部使用硬编码 mock 数据，无 HTTP 客户端、无认证流程、无 Provider 管理 UI。前后端完全断裂，需要打通全链路让系统真正可用。

## What Changes

- **新建前端 API 服务层**：axios 实例 + JWT 拦截器 + 4 个 API 模块 (auth, users, providers)
- **新建认证流程 (DevMode)**：Login 弹窗 → X-Dev-User header → JWT → localStorage → axios 自动注入
- **新建 Pinia stores**：user store (认证态) + providers store (Provider CRUD)
- **改造 GlobalHeader**：硬编码 "管理员" 替换为真实用户信息 + Login/Logout 交互
- **改造 SettingsView**：嵌入 LLM Provider 管理区域（内部 providers 只读 + 用户 providers CRUD）
- **改造 Router**：添加 beforeEach 守卫处理认证态（DevMode 不强制跳转）
- **删除无用 UI**：App.vue 的 "Deploy Agent" 按钮 + 侧边栏 "Logout" 条目
- **配置 Vite proxy**：/api → localhost:8000

## Capabilities

### New Capabilities
- `dev-auth`: DevMode 认证流程 — Login 弹窗、JWT 获取与存储、axios 拦截器注入、Logout 清除
- `user-profile-ui`: 用户信息展示 — GlobalHeader 接入 user store，显示真实用户名与头像
- `provider-management-ui`: Provider 管理 UI — Settings 页面内的 Provider CRUD 区域（内部只读列表、用户 providers 增删、设为默认）

### Modified Capabilities

(无已有 capability 需要修改)

## Impact

- **前端文件变更**：App.vue, GlobalHeader.vue, SettingsView.vue, router/index.js, vite.config.js
- **新建文件**：src/api/ (4 files), src/stores/ (2 files)
- **依赖**：需安装 axios
- **后端无变更**：完全使用现有 API，无需改动
- **运行时依赖**：后端需以 DEV_MODE=true 启动
