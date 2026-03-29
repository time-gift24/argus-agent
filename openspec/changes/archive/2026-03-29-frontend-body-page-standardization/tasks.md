## 1. Shared page body shell

- [x] 1.1 Create a shared body page shell component for breadcrumb, title, description, and page-level actions
- [x] 1.2 Update the main content layout so the body header can stay sticky below the global top nav without overlapping page content
- [x] 1.3 Define a consistent breadcrumb data shape that top-level pages and nested edit pages can both render

## 2. Concrete page body migration

- [x] 2.1 Refactor concrete route pages (`DashboardView`, `AgentListView`, `AgentDetailsView`, `ToolsView`, `ShellView`, `LogsView`, `SettingsView`) to use the shared body shell
- [x] 2.2 Refactor `ProvidersView` to use the shared body shell and expose its primary action in the page header
- [x] 2.3 Refactor `McpConfigsView` list page to use the shared body shell and keep destructive actions in confirmation dialogs only

## 3. Provider editor polish

- [x] 3.1 Rework `ProviderEditView` to use the shared body shell with fixed breadcrumb placement
- [x] 3.2 Split the provider form into clear page sections for basic configuration, connection testing, and submit actions
- [x] 3.3 Verify provider create/edit navigation and inline test feedback still work after the page layout refactor

## 4. MCP create and edit pages

- [x] 4.1 Add dedicated `/mcp/new` and `/mcp/:id/edit` routes and extract a reusable full-page MCP form view
- [x] 4.2 Replace MCP list-page create/edit dialogs with route navigation while keeping delete confirmation as a guardrail dialog
- [x] 4.3 Preserve MCP transport-specific fields, admin-only stdio restrictions, and secret-field retention semantics on the new pages
- [x] 4.4 Surface unsaved-config connection testing on the MCP create page using the existing `test-config` endpoint

## 5. Verification

- [x] 5.1 Run frontend build and fix any regressions introduced by the route and layout changes
- [x] 5.2 Manually verify breadcrumb placement, sticky body headers, and create/edit flows for Provider and MCP pages on desktop
