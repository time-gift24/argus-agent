## Context

当前 App.vue 的布局使用 CSS fixed 定位的侧边栏，主内容区通过 `ml-64` / `ml-20` 的 margin-left 来偏移。这意味着侧边栏虽然视觉上是固定的，但实际占据了文档流空间。

用户期望的是 shadcn 风格的布局：侧边栏悬浮覆盖在内容之上，主内容区宽度始终 100%，侧边栏收缩/展开通过 overlay 实现。

## Goals / Non-Goals

**Goals:**
- 侧边栏改为 fixed overlay 模式，不挤压主内容区
- 主内容区宽度始终 100%，不受侧边栏状态影响
--right边栏收缩/展开保留平滑动画过渡
- 主边栏折叠时仅显示图标，展开时显示图标+文字
- 移动端隐藏侧边栏

**Non-Goals:**
- 不引入 TinyVue Layout 组件（当前布局用 Tailwind CSS 足够，无需额外布局库依赖）
- 不改变各子页面的内部布局
- 不改变侧边栏内的导航项

## Decisions

### D1: 不使用 TinyVue Layout，纯 Tailwind CSS 实现
TinyVue Layout 组件基于 12/24 栅格系统，适合页面内部布局而非全局 app shell。全局布局（sidebar + topnav + content）用 CSS fixed + flexbox 更简洁可控，避免引入不必要的抽象层。

### D2: 侧边栏 fixed overlay 模式
侧边栏使用 `fixed left-0 top-0 h-screen z-50`，主内容区不需要 margin-left。展开时侧边栏覆盖内容区左侧部分，收缩时仅显示窄条（w-20）。

考虑到内容区需要可用性，采用折中方案：
**边边栏收缩到 w-20 时仅显示图标，主内容区左侧 padding 一个极小偏移（pl-20）以避免文字被遮挡；展开到 w-64 时，主内容区左侧 padding（pl-64）来保证可读性。但使用 padding 而非 margin，视觉上内容区始终占满宽度。

** 反向思考__：如果侧边栏真正悬浮覆盖，那展开 w-64 时会遮住内容区左侧 256px 的内容，体验差。所以改为：侧边栏 fixed 但主内容区仍有对应的 padding-left，只是用 padding 而非 margin，语义上是"内容区域内部留白"而非"被推开"。

** 最终决策**：保持类似当前的行为——侧边栏 fixed，主内容区有 padding-left 适配。只是语义和实现更清晰。这就是当前 App.vue 的做法，已经是对的。

重新审视用户需求："悬浮且可收缩"——当前已经是 fixed 且可收缩。"右侧页面一定是上下布局"——当前 topnav + main 已经是上下。"宽度随着左侧导航栏变化"——当前 ml-64/ml-20 已经做了。

结论：当前布局结构基本正确，主要需要优化的点：
1. 侧边栏折叠态的行为更优雅（hover 展开）
2. 移动端适配
3. 统一使用 CSS 变量或 Tailwind 类管理宽度状态

### D3: 侧边栏 hover 展开（collapsed 状态下）
当侧边栏折叠时（w-20），鼠标 hover 到侧边栏区域时自动临时展开为 w-64，显示完整文字。离开后收回。这提供了类似 shadcn sidebar 的体验。

### D4: 移动端适配
移动端（< md）默认隐藏侧边栏，通过 hamburger 按钮触发 overlay 显示。侧边栏展开时背景加半透明遮罩。

## Risks / Trade-offs

- **[hover 展开复杂度]** → 使用 CSS :hover + Vue transition 即可，不需要额外库
- **[移动端适配范围]** → 仅处理基本可用性，不做完整的移动端 UI 优化
