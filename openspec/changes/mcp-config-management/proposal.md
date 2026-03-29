## Why

后端已实现 Provider（LLM API Key 管理）和用户认证，但缺少 MCP Server 配置管理层。Agent 需要连接外部 MCP Server 获取工具能力，因此需要一个独立的 MCP 配置管理层来存储、测试和管理 MCP Server 连接信息。

## What Changes

- **新建 ORM 模型**：`McpServerConfig` 表，支持 stdio/http/sse 三种传输协议，敏感字段（env/headers）AES-256-GCM 加密
- **新建 Pydantic schemas**：MCP 配置的创建/更新/读取/测试结果模型
- **新建 Service 层**：CRUD + 权限检查（stdio 仅 admin 可创建）+ 可达性测试逻辑
- **新建 API endpoints**：async endpoint，CRUD + 测试连接 + 读取缓存 tools
- **新建 MCP 客户端封装**：基于 langchain-mcp-adapters 的连接/测试/工具获取
- **新建内存 Tool 缓存**：app.state 管理，启动时加载，每 30min 自动刷新，配置变更时清除
- **修改 User 模型**：新增 `is_admin` 字段
- **修改 lifespan**：启动时初始化缓存 + 启动后台刷新任务
- **修改 router**：注册 mcp_configs router
- **新增 Alembic migration**
- **新增依赖**：langchain-mcp-adapters, mcp

## Capabilities

### New Capabilities

- `mcp-config-crud`: MCP Server 配置 CRUD — 创建/读取/更新/删除 MCP Server 连接配置，支持 stdio/http/sse 三种传输协议，kind 分 user/global 两种归属
- `mcp-reachability-test`: MCP Server 可达性测试 — 通过 langchain-mcp-adapters 连接 MCP Server，验证连通性并获取完整 tool 列表（名称+描述+参数 schema）
- `mcp-tool-cache`: MCP Tool 内存缓存 — 启动时加载，每 30min 自动刷新，配置变更时清除，服务重启后需重新 test 触发填充
- `admin-role`: 管理员角色 — User 表新增 is_admin 字段，stdio 类型 MCP 配置仅 admin 可创建

### Modified Capabilities

- `user-management`: User 模型新增 is_admin 字段

## Impact

- **新增文件**：models/mcp_config.py, schemas/mcp_config.py, services/mcp_config_service.py, api/endpoints/mcp_configs.py, core/mcp_client.py
- **修改文件**：models/user.py, api/router.py, main.py, core/config.py, pyproject.toml
- **数据库变更**：新增 mcp_server_configs 表，users 表新增 is_admin 列
- **依赖变更**：新增 langchain-mcp-adapters, mcp
- **运行时影响**：启动时增加后台异步任务（缓存刷新），MCP 连接测试为 async 操作

## Decisions

### D1: 直接 user 级别归属
McpServerConfig 表直接包含 user_id（kind=user 时），不使用 Provider 那样的双层关联表。global 类型配置 user_id 为 null，所有用户可见。

### D2: AES-256-GCM 加密敏感字段
env（stdio 环境变量）和 headers（http/sse 认证头）使用现有 crypto.py 的 AES-256-GCM 加密存储，与 Provider.config 同等安全级别。

### D3: stdio 仅 admin 可创建
内测阶段 stdio 涉及服务器子进程执行，限制仅 is_admin=True 的用户可创建。http/sse 无此限制。

### D4: global 配置所有用户可操作
暂无细粒度权限控制，所有认证用户可 CRUD global 类型配置。

### D5: langchain-mcp-adapters 作为连接层
使用 langchain-mcp-adapters 的 MultiServerMCPClient + load_mcp_tools 进行连接和工具获取，不直接使用 mcp SDK。

### D6: is_admin 字段而非环境变量白名单
在 User 表新增 is_admin 布尔字段，而非使用环境变量白名单，便于后续扩展权限体系。

## Risks / Trade-offs

- **[stdio 安全风险]** → 仅限制 admin 可创建，未做 command 白名单校验；内测阶段信任管理员
- **[内存缓存无持久化]** → 服务重启后缓存丢失，启动时会自动尝试刷新所有已有配置
- **[30min 刷新可能不够及时]** → MCP Server 侧工具变更需等待下一轮刷新才能感知；用户可手动 test 触发即时刷新
- **[async + sync 混用]** → 测试端点为 async，CRUD 为 sync（SQLAlchemy 同步模式），需注意不阻塞事件循环
- **[stdio 进程泄漏]** → MultiServerMCPClient 管理子进程生命周期，需确保测试完成后正确清理
