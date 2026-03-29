## Why

当前前端各个路由页面的 body 结构不一致：有的页面没有固定面包屑，有的页面把核心创建/编辑流程放在弹窗里，导致导航层级不清、页面信息密度不稳定，也让复杂表单在弹窗里变得局促。现在需要先统一页面 body 的设计约束，再把 LLM 和 MCP 的编辑体验收敛到同一套页面模式。

## What Changes

- 新增统一的 route body 页面规范：页面左上角固定展示面包屑，页面标题、说明和主操作区采用一致的头部结构。
- 将具体业务页面按统一 body 规范整改，覆盖已有的仪表盘、智能体、工具、Shell、日志、设置、Provider、MCP 等 route 页面。
- 将“创建/编辑”这类高信息密度流程从业务弹窗迁移到独立页面；弹窗主要保留给删除确认、登录拦截等防呆或保护性场景。
- 完善 LLM Provider 编辑页，使新增/编辑页在布局、测试连接反馈和操作区结构上符合新的 body 规范。
- 完善 MCP 配置管理页，新增独立的创建页和编辑页，并将列表页上的新增/编辑入口改为页面导航而非表单弹窗。

## Capabilities

### New Capabilities
- `app-body-layout`: 统一 route body 页面结构，定义固定在页面左上角的面包屑区域、页面头部信息区以及尽量以内联页面替代业务弹窗的交互约束

### Modified Capabilities
- `provider-list-page`: `/providers` 列表页增加统一 body 头部与面包屑要求，并保持新增入口跳转到独立编辑页
- `provider-editor`: `/providers/new` 与 `/providers/:id/edit` 按统一页面骨架重构编辑体验，明确测试连接、保存和返回操作的布局要求
- `mcp-config-ui`: `/mcp` 列表页改为跳转到独立的新建/编辑页，限制业务弹窗使用范围，并补充 MCP 编辑页能力

## Impact

- **前端文件变更**：`frontend/src/App.vue`、`frontend/src/router/index.js`、多个 `frontend/src/views/*.vue` 页面，以及新增共享页面壳/面包屑组件
- **无后端 API 变更预期**：复用现有 Provider 与 MCP CRUD / test 接口
- **无新增外部依赖预期**：主要为前端路由、视图结构与交互调整
