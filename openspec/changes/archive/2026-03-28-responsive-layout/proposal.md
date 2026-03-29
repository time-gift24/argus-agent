## Why

当前 App.vue 使用固定定位 + margin-left 偏移实现侧边栏布局，存在以下问题：
- 侧边栏占据文档流空间而非悬浮，导致主内容区宽度被挤压
- 布局未利用 Vue 组件库的标准布局方案，维护成本高
- 页面不具备真正的响应式能力（移动端适配差）

需要重构为悬浮可收缩侧边栏 + 自适应主内容区的标准布局模式。

## What Changes

- **重构** App.vue 布局结构：侧边栏改为悬浮（fixed overlay）模式，不占据文档流
- **重构** 主内容区为上下结构（顶部导航 + 下方内容），宽度 100% 自适应
- **保留** 侧边栏收缩/展开动画，使用 CSS transition
- **删除** 主内容区的 margin-left 偏移逻辑（因为侧边栏悬浮不再挤压内容）

## Capabilities

### New Capabilities
- `floating-sidebar-layout`: 悬浮侧边栏布局 — 侧边栏 fixed overlay、主内容区自适应宽度、收缩/展开动画

### Modified Capabilities

(无)

## Impact

- **前端文件变更**：App.vue
- **无后端变更**
- **无新增依赖**
