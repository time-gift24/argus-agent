## 1. 基础设施

- [x] 1.1 安装 axios 依赖 (`npm install axios`)
- [x] 1.2 创建 `src/api/client.js` — axios 实例 + request interceptor (JWT 注入) + response interceptor (401 清除)
- [x] 1.3 配置 `vite.config.js` — 添加 server.proxy 将 `/api` 代理到 `http://localhost:8000`

## 2. API 模块

- [x] 2.1 创建 `src/api/auth.js` — devLogin(username): GET /api/v1/auth/login with X-Dev-User header
- [x] 2.2 创建 `src/api/users.js` — getProfile(): GET /api/v1/me, updateProfile(data): PATCH /api/v1/me
- [x] 2.3 创建 `src/api/providers.js` — listInternal(): GET /api/v1/internal-providers, list(): GET /api/v1/providers, create(data): POST /api/v1/providers, remove(id): DELETE /api/v1/providers/{id}, setDefault(id): PUT /api/v1/providers/{id}/default

## 3. Pinia Stores

- [x] 3.1 创建 `src/stores/user.js` — state: token/profile/isLoggedIn, actions: login(token)/fetchProfile/logout, 初始化时从 localStorage 恢复 token
- [x] 3.2 创建 `src/stores/providers.js` — state: internalProviders/userProviders/loading, actions: fetchProviders/createProvider/deleteProvider/setDefaultProvider

## 4. 认证 UI

- [x] 4.1 改造 `GlobalHeader.vue` — 未登录态显示 Login 按钮，已登录态显示真实用户名+dicebear头像+Logout 下拉
- [x] 4.2 GlobalHeader 内实现 DevMode 登录弹窗 (TinyDialog) — 用户名输入 → 调用 auth.js → 存 token → 刷新 profile
- [x] 4.3 改造 `App.vue` — 删除 "Deploy Agent" 按钮，删除侧边栏 footerItems 中的 "Logout" 条目

## 5. Provider 管理 UI

- [x] 5.1 改造 `SettingsView.vue` — 在 General Configuration 和 Security & Access 之间新增 LLM Providers 区域
- [x] 5.2 实现内部 Providers 只读列表
- [x] 5.3 实现用户 Providers 列表（名称 + ★ Default 标记 + Set Default 按钮 + Delete 按钮）
- [x] 5.4 实现 Add Provider 弹窗 (TinyDialog) — Name + API Key + Base URL + Model 表单
- [x] 5.5 实现 Delete Provider 确认交互 + 设为默认操作
- [x] 5.6 未登录态 Provider 区域显示 "请先登录" 提示

## 6. 路由守卫

- [x] 6.1 `router/index.js` — 添加 beforeEach 守卫，DevMode 下不强制跳转，仅确保 user store 初始化

## 7. 清理

- [x] 7.1 移除 GlobalHeader.vue 中的硬编码 "管理员" / "超级权限" 及相关 @mock 注释
- [x] 7.2 验证全链路：Login → 查看 Profile → Settings 管理 Providers → Logout
