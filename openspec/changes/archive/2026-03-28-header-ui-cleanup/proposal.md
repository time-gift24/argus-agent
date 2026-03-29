## Why

当前 GlobalHeader 和 App.vue 存在多处无效 UI 元素和布局问题：
- 搜索框位置不对（应在左侧）
- 侧边栏"帮助中心"无实际功能
- 通知铃铛按钮无实际功能
- 顶部导航栏右侧同时出现通知铃铛和用户区域，Login 按钮不够突出

需要清理这些装饰性元素，让 Header 聚焦于实际可用的功能。

## What Changes

- **删除** App.vue 侧边栏 footerItems 中的"帮助中心"条目
- **删除** GlobalHeader.vue 中的通知铃铛按钮及其分隔线
- **移动** 搜索框到 GlobalHeader 左侧（系统健康度 pill 区域之前）
- **保留** Login/用户头像区域在右侧

## Capabilities

### New Capabilities
- `header-layout-cleanup`: Header 布局清理 — 搜索框左对齐、删除通知铃铛和帮助中心、Login 按钮突出显示

### Modified Capabilities

(无)

## Impact

- **前端文件变更**：App.vue, GlobalHeader.vue
- **无后端变更**
- **无新增依赖**
