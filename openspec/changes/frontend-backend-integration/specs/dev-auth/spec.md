## ADDED Requirements

### Requirement: DevMode 登录弹窗
系统 SHALL 在 GlobalHeader 右上角显示 Login 按钮（未登录态）。点击后弹出 TinyDialog，包含用户名输入框和确认按钮。确认后前端 SHALL 发送 GET /api/v1/auth/login 请求，携带 X-Dev-User header。

#### Scenario: 成功登录
- **WHEN** 用户在弹窗输入用户名 "alice" 并点击确认
- **THEN** 前端发送 GET /api/v1/auth/login (Header: X-Dev-User: alice)
- **THEN** 收到 JWT token 后存入 localStorage
- **THEN** 关闭弹窗，GlobalHeader 显示用户信息
- **THEN** axios 默认注入 Authorization: Bearer <token>

#### Scenario: 登录失败（空用户名）
- **WHEN** 用户未输入用户名直接点击确认
- **THEN** 弹窗不关闭，输入框显示校验提示

#### Scenario: 登录失败（后端错误）
- **WHEN** 后端返回非 200 响应
- **THEN** 弹窗显示错误提示，不存储 token

### Requirement: JWT 自动注入
axios 实例 SHALL 通过 request interceptor 在每个请求的 Authorization header 中注入 `Bearer <token>`（从 localStorage 读取）。

#### Scenario: 已登录态发起请求
- **WHEN** 用户已登录，token 存在于 localStorage
- **THEN** 所有 API 请求自动携带 Authorization: Bearer <token>

#### Scenario: Token 不存在
- **WHEN** localStorage 中无 token
- **THEN** 请求不携带 Authorization header

### Requirement: 401 响应处理
axios response interceptor SHALL 监听 401 状态码，自动清除 localStorage 中的 token 和 user profile，触发 UI 更新为未登录态。

#### Scenario: 收到 401
- **WHEN** 任一 API 请求返回 401
- **THEN** 清除 localStorage 中的 token 和 user profile
- **THEN** Pinia user store 重置为未登录态
- **THEN** GlobalHeader 显示 Login 按钮

### Requirement: Logout
系统 SHALL 在已登录态的 GlobalHeader 用户区域提供 Logout 操作。Logout 后 SHALL 清除 localStorage 中的 token 和 user profile，Pinia user store 重置为未登录态。

#### Scenario: 点击 Logout
- **WHEN** 已登录用户点击 Logout
- **THEN** 清除 localStorage 中的 token 和 profile 数据
- **THEN** Pinia user store 重置为未登录态
- **THEN** GlobalHeader 切换为 Login 按钮

### Requirement: Vite 开发代理
vite.config.js SHALL 配置 devServer proxy，将 `/api` 前缀的请求代理到 `http://localhost:8000`。

#### Scenario: 开发环境 API 调用
- **WHEN** 前端发起 `/api/v1/auth/login` 请求
- **THEN** Vite devServer 将请求代理到 `http://localhost:8000/api/v1/auth/login`
