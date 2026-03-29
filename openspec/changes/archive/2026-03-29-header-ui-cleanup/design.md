## Context

GlobalHeader 和 App.vue 是所有页面的公共壳。当前有多处装饰性 UI 元素（通知铃铛、帮助中心）无后端支持，属于噪音。搜索框目前在 App.vue 的 TopNav 右侧，应移到 GlobalHeader 左侧与内容区对齐。

## Goals / Non-Goals

**Goals:**
- 清理 Header 中无功能绑定的装饰元素
- 搜索框左对齐，贴近内容区
- Login 按钮在右侧更醒目

**Non-Goals:**
- 搜索功能实现（保持占位，后续接入）
- 通知系统实现
- 用户下拉菜单功能扩展

## Decisions

### D1: 搜索框从 App.vue 移到 GlobalHeader 左侧
搜索框应贴近主内容区，而非固定在顶部导航栏右侧。移到 GlobalHeader 的系统健康度 pill 之前。

### D2: 删除通知铃铛
无后端通知 API，铃铛上的红点是硬编码的，产生误导。直接删除。

### D3: 删除帮助中心
侧边栏 footer 的"帮助中心"无实际页面。删除减少噪音。

## Risks / Trade-offs

- **[搜索框位置变动]** → 用户习惯可能需要适应，但左对齐更符合常见布局模式
