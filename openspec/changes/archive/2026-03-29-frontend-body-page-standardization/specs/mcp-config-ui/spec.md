## ADDED Requirements

### Requirement: MCP 列表页统一 body 头部
`/mcp` 页面 SHALL 在内容区左上角显示面包屑、页面标题、页面说明和主操作区。

#### Scenario: 访问 MCP 列表
- **WHEN** 用户导航到 `/mcp`
- **THEN** 页面头部显示当前页面包屑 "MCP 服务"
- **THEN** "新增配置" 作为页面级主操作显示在头部区域，并导航到 `/mcp/new`

### Requirement: 新建 MCP 配置时测试未保存配置
系统 SHALL 在 `/mcp/new` 页面提供 "测试连接" 按钮，使用当前表单值测试未保存配置，并在页面内展示结果。

#### Scenario: 测试新建页表单
- **WHEN** 用户在 `/mcp/new` 页面填写表单并点击 "测试连接"
- **THEN** 系统调用 `POST /api/v1/mcp-configs/test-config`
- **THEN** 页面内联展示成功/失败状态和发现的工具数量

## MODIFIED Requirements

### Requirement: 创建 MCP 配置
系统 SHALL 提供 `/mcp/new` 独立页面用于创建 MCP 配置，支持 `stdio`、`http`、`sse` 三种 transport 类型，并根据选择动态展示对应字段；列表页不得再通过弹窗承载创建表单。

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
