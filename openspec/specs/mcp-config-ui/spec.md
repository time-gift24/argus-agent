# mcp-config-ui Specification

## Purpose
定义 MCP 配置管理界面的导航、列表、创建编辑、测试与工具浏览行为。

## Requirements
### Requirement: MCP 服务导航入口
系统 SHALL 在顶部导航栏中提供 "MCP 服务" 页签，链接到 `/mcp` 路由。

#### Scenario: 导航栏显示 MCP 服务页签
- **WHEN** 用户加载任意页面
- **THEN** 顶部导航栏中显示 "MCP 服务" 页签，位于 "提供商" 之后
- **AND** 点击页签导航到 `/mcp`

### Requirement: MCP 配置列表展示
系统 SHALL 展示当前用户的个人配置和全局配置列表，每条配置显示名称、描述、transport 类型、kind（user/global）和创建时间。

#### Scenario: 成功加载配置列表
- **WHEN** 用户访问 `/mcp` 页面
- **THEN** 系统调用 `GET /api/v1/mcp-configs` 获取配置列表
- **AND** 以卡片形式展示所有配置，区分 user 和 global 类型

#### Scenario: 无配置时的空状态
- **WHEN** 用户访问 `/mcp` 页面且 API 返回空列表
- **THEN** 显示空状态提示文案，引导用户创建第一个配置

### Requirement: MCP 列表页统一 body 头部
系统 SHALL 在 `/mcp` 页面通过共享 body 页面模板展示固定位置的面包屑和页面级主操作。

#### Scenario: 访问 MCP 列表
- **WHEN** 用户导航到 `/mcp`
- **THEN** 页面头部显示当前页面包屑 "MCP 服务"
- **THEN** "新增配置" 作为页面级主操作显示在面包屑下方的独立区域

### Requirement: 创建 MCP 配置
系统 SHALL 提供 `/mcp/new` 独立页面用于创建 MCP 配置，支持 `stdio`、`http`、`sse` 三种 transport 类型，并根据 transport 动态展示对应字段；列表页不得再通过弹窗承载创建表单。

#### Scenario: 新建页面展示
- **WHEN** 用户导航到 `/mcp/new`
- **THEN** 页面显示包含面包屑 "MCP 服务 > 新增配置" 的完整表单页面
- **THEN** 表单根据当前 transport 动态展示 `command/args/env` 或 `url/headers` 字段

#### Scenario: 创建 http 类型配置
- **WHEN** 用户填写名称、选择 `http` transport、输入 URL 后提交
- **THEN** 系统调用 `POST /api/v1/mcp-configs` 创建配置
- **THEN** 创建成功后重定向到 `/mcp`

#### Scenario: 创建 stdio 类型配置
- **WHEN** 管理员用户填写名称、选择 `stdio` transport、输入 command 后提交
- **THEN** 系统调用 `POST /api/v1/mcp-configs` 创建配置
- **THEN** 创建成功后重定向到 `/mcp`

#### Scenario: 创建配置权限约束
- **WHEN** 非 admin 用户访问 `/mcp/new`
- **THEN** 页面将 `stdio` 选项标记为仅管理员可用并阻止选择

### Requirement: 新建 MCP 配置时测试未保存配置
系统 SHALL 在 `/mcp/new` 页面提供 "测试连接" 按钮，使用当前表单值测试未保存配置，并在页面内展示结果。

#### Scenario: 测试新建页表单
- **WHEN** 用户在 `/mcp/new` 页面填写表单并点击 "测试连接"
- **THEN** 系统调用 `POST /api/v1/mcp-configs/test-config`
- **THEN** 页面内联展示成功/失败状态和发现的工具数量

### Requirement: 编辑 MCP 配置
系统 SHALL 提供 `/mcp/:id/edit` 独立页面用于编辑已有配置；列表页上的编辑操作 MUST 导航到该页面，修改成功后自动清除该配置的工具缓存。

#### Scenario: 进入编辑页
- **WHEN** 用户点击某条 user 配置的编辑按钮，或直接访问 `/mcp/:id/edit`
- **THEN** 系统显示预填当前值的完整编辑页面，而不是打开编辑弹窗
- **THEN** `headers` 或 `env` 输入为空时表示保留当前已保存值

#### Scenario: 提交编辑
- **WHEN** 用户修改表单并点击 "保存"
- **THEN** 系统调用 `PATCH /api/v1/mcp-configs/{id}` 更新配置
- **THEN** 成功后重定向到 `/mcp`
- **THEN** 该配置的本地测试状态和工具缓存被清除

### Requirement: 删除 MCP 配置
系统 SHALL 允许用户删除配置，删除前需要确认。

#### Scenario: 删除用户配置
- **WHEN** 用户点击某条配置的删除按钮并确认
- **THEN** 系统调用 `DELETE /api/v1/mcp-configs/{id}` 删除配置
- **AND** 从列表中移除该配置

### Requirement: 测试 MCP 连接
系统 SHALL 提供测试连接按钮，触发后端测试端点，展示连通性结果和发现的工具列表。

#### Scenario: 测试连接成功
- **WHEN** 用户点击某条配置的 "测试连接" 按钮
- **THEN** 系统调用 `POST /api/v1/mcp-configs/{id}/test`
- **AND** 展示测试结果（成功/失败）和发现的工具列表

#### Scenario: 测试连接失败
- **WHEN** 测试端点返回 `success: false`
- **THEN** 展示错误原因提示

### Requirement: 查看缓存工具
系统 SHALL 展示每条配置已缓存的工具列表，包含工具名称、描述和参数 schema。

#### Scenario: 查看已有缓存工具
- **WHEN** 用户点击某条配置的工具查看按钮
- **THEN** 系统调用 `GET /api/v1/mcp-configs/{id}/tools` 获取缓存工具
- **AND** 展示工具列表（名称、描述、参数 schema）

#### Scenario: 缓存为空
- **WHEN** 配置尚无缓存工具
- **THEN** 展示空状态，提示用户先执行测试连接
