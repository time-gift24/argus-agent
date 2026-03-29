## Context

后端 FastAPI 已实现完整的 user management 模块（auth + users + providers），包含 9 个 REST endpoint、JWT 认证、AES-256-GCM 加密、OIDC/DevMode 双模式。前端 Vue 3 应用目前 7 个 View 全部硬编码 mock 数据，无 HTTP 客户端、无认证流程、无 API 调用层。

前端技术栈：Vue 3 + Vite 6 + Pinia 3 + Vue Router 4 + TinyVue + Tailwind v4。未安装 axios。

后端运行在 `localhost:8000`，API 前缀 `/api/v1`。

## Goals / Non-Goals

**Goals:**
- 建立前端 API 服务层，打通后端已实现的全部 provider/user 端点
- 实现 DevMode 认证流程（用户名输入 → JWT → 自动注入）
- Settings 页面内实现 Provider 完整 CRUD（列表、添加、删除、设为默认）
- GlobalHeader 显示真实用户信息

**Non-Goals:**
- OIDC 正式认证流程（后续迭代）
- Provider config 修改（后端无 update endpoint）
- 其他 mock 页面（Dashboard/Agents/Tools/Logs/Shell）的真实化
- Token 刷新机制（当前 JWT 24h 有效，足够 DevMode 使用）

## Decisions

### D1: axios 作为 HTTP 客户端
选择 axios 而非 fetch，因为需要拦截器（request interceptor 注入 JWT、response interceptor 处理 401）。fetch 的拦截需要 wrapper 代码，axios 原生支持。

### D2: JWT 存 localStorage
DevMode 下无 XSS 风险（本地开发），localStorage 比 sessionStorage 跨 tab 共享更方便。生产环境切 OIDC 时应考虑 HttpOnly cookie。

### D3: Vite devServer proxy
前端开发时通过 `vite.config.js` 的 `server.proxy` 将 `/api` 代理到 `localhost:8000`，避免 CORS 问题。生产部署时通过反向代理（nginx）处理。

### D4: 路由守卫策略 — 不强制跳转
DevMode 下不拦截未认证用户的页面浏览。未登录时 Login 按钮始终可见于 GlobalHeader，Settings 页面的 Provider 区域在未登录时隐藏或显示 Login 提示。

### D5: Provider 管理嵌入 Settings 页面
在 General Configuration 和 Security & Access 之间新增 LLM Providers 区域。不新建独立页面或路由，减少路由复杂度。

### D6: 登录交互 — GlobalHeader 内 TinyDialog
Login 按钮放在右上角（原 "Deploy Agent" / 硬编码用户头像位置）。点击弹出 TinyDialog 输入用户名，POST /auth/login 携带 X-Dev-User header。

## Risks / Trade-offs

- **[JWT 过期无自动刷新]** → DevMode 下用户可重新登录获取新 token，24h 有效期内足够
- **[localStorage XSS 风险]** → 仅 DevMode 使用，生产环境切 OIDC + HttpOnly cookie
- **[无 Provider config 编辑]** → 后端未提供 update endpoint，用户需删除后重新创建
- **[全局布局组件需改认证态]** → App.vue 是所有页面的壳，认证逻辑通过 Pinia store 注入，响应式更新
