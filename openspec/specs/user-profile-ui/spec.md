# user-profile-ui Specification

## Purpose
定义前端用户信息展示与 user store 行为。

## Requirements
### Requirement: GlobalHeader 显示真实用户信息
系统 SHALL 在用户已登录时，在 GlobalHeader 右上角显示从 GET /api/v1/me 获取的真实用户名和头像。头像 SHALL 使用 dicebear API 基于 username 生成。

#### Scenario: 已登录态显示用户信息
- **WHEN** 用户已登录（token 存在于 localStorage）
- **THEN** 前端调用 GET /api/v1/me 获取用户 profile
- **THEN** GlobalHeader 右上角显示用户 name 和 dicebear 头像
- **THEN** 原 "超级权限" 文字不再显示

#### Scenario: 未登录态显示 Login 按钮
- **WHEN** 用户未登录（localStorage 无 token）
- **THEN** GlobalHeader 右上角显示 Login 按钮
- **THEN** 不显示用户名和头像

### Requirement: User Pinia Store
系统 SHALL 提供 user Pinia store，管理认证态和用户 profile。

#### Scenario: Store 初始化
- **WHEN** 应用启动时
- **THEN** store 从 localStorage 读取 token，若有 token 则标记为已登录态
- **THEN** 若有 token 则自动调用 GET /api/v1/me 获取 profile

#### Scenario: Store 登录
- **WHEN** store 的 login action 被调用（传入 token）
- **THEN** token 写入 localStorage
- **THEN** 自动调用 GET /api/v1/me 获取并存储 profile
- **THEN** isLoggedIn 状态变为 true

#### Scenario: Store 登出
- **WHEN** store 的 logout action 被调用
- **THEN** 清除 localStorage 中的 token
- **THEN** 清除 profile 数据
- **THEN** isLoggedIn 状态变为 false
