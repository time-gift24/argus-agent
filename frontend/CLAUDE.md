# Frontend Development Guide

## Design System: Axiom Azure (Material Design 3)

### Typography

| Token | Font | Usage |
|-------|------|-------|
| `.font-headline` | Space Grotesk | 标题(h1-h4)、品牌名、卡片标题、统计数字 |
| `--font-body` (默认) | Manrope | 正文、描述、标签、按钮 |
| `.font-mono` | JetBrains Mono | ID、时间戳、CPU/内存数值 |

标题模式：`text-3xl font-headline font-bold tracking-tight text-on-surface`，强调词用 `text-primary`。

### Color Tokens

**主色**：
- `primary` (#003ec7) — 强调文字、主按钮、进度条
- `primary-fixed` (#dde1ff) — 图标背景、头像底色
- `primary-fixed-dim` (#b7c4ff) — 图表柱状条
- `primary-container` (#0052ff) — 渐变端点

**表面层级**（从亮到暗）：
- `surface-container-lowest` (#ffffff) — 卡片/面板背景（白）
- `surface-container-low` (#f3f4f5) — 顶栏/侧边栏/搜索框
- `surface-container` (#edeeef) — hover 背景、进度条轨道
- `surface-container-high` (#e7e8e9) — 次级 hover

**文字层级**：
- `on-surface` (#191c1d) — 主文字、标题
- `on-surface-variant` (#434656) — 次要描述、标签、时间戳

**语义色**：
- `success` / `danger` / `warning` — 状态指示（Active/Error/Idle）

**边框**：`text-on-surface`
**边框**：统一使用 `border-outline-variant/30`，分隔线用 `/10` 或 `/20`。

**语义色**：`success`(#10B981) / `warning`(#F59E0B) / `danger`(#EF4444) / `error`(#ba1a1a)

**第三色**：
- `tertiary-fixed` (#9cf0ff) — 状态 badge（STABLE、Success）
- `tertiary-fixed-dim` (#00daf3) — Active 状态指示点

### Border Radius

| 值 | 用途 |
|----|------|
| `rounded-[2rem]` | 所有卡片/面板/表格容器（核心圆角） |
| `rounded-xl` | 按钮、"New Module" 按钮 |
| `rounded-lg` | 筛选按钮、侧栏 nav 项、表格内头像 |
| `rounded-full` | 状态点、搜索框 pill、头像圆、badge |

### Shadow

- 卡片默认：`shadow-sm`
- 卡片 hover：`hover:shadow-xl transition-all duration-300`
- FAB：`shadow-2xl`
- 系统健康卡（强调）：`shadow-lg`

### Animation

- 入场动画：`animate-fade-up`，配合 `animate-delay-1` 到 `animate-delay-5` 做交错
- 页面路由切换：Vue `<Transition name="fade">`
- 侧栏折叠：`sidebar-transition` (0.3s cubic-bezier)
- hover 统一：`transition-colors` 或 `transition-all duration-300`

### Special Effects

- `.glass-panel` — 毛玻璃面板（rgba 白 + blur 16px）
- `.architectural-grid` — 40px 网格背景
- `.glow-pulse` — 发光脉冲（box-shadow cyan）

## Layout Patterns

### Page Container

所有页面：`max-w-7xl mx-auto`

### Body Page Template

- body 页面顶部使用统一公共模板，面包屑始终位于内容区左上角固定位置
- 面包屑容器固定使用 `max-w-7xl mx-auto`，不跟随具体页面内容宽度变化
- 共享 header 保持轻量：不做 sticky、不做悬浮卡片、不额外包毛玻璃面板
- 页面级操作按钮放在面包屑下方的独立一行，不得挤占或改变面包屑位置
- 如页面已有面包屑，不再在 body 内重复渲染大标题；需要语义标题时使用页面模板统一提供

### Dialog Usage

- 优先使用页面内布局和内联反馈，尽可能减少业务弹窗
- 弹窗主要用于防呆场景：删除确认、危险操作确认、登录补救
- 新建/编辑流程默认使用独立页面，不使用大表单弹窗

### Form Density

- 表单以紧凑优先，控制在 `space-y-4` 到 `space-y-5`
- 分组卡片只保留 micro label，不再重复渲染粗大标题
- 新建页标题已经表达上下文时，表单 section 不再重复写“新增 XXX”
- 分组卡片推荐：`rounded-2xl border border-outline-variant/20 bg-surface-container-lowest p-5 shadow-sm`
- 提交区与测试结果保持内联，优先在当前页面就地反馈

### 间距规范

| 场景 | 值 |
|------|-----|
| 页面区块间 | `space-y-5` 或 `space-y-6` |
| 网格 gap | `gap-6` |
| 按钮组 | `gap-2` |
| 图标+文字 | `gap-1.5` |
| 状态点+文字 | `gap-1` |

### Grid

- Bento 12 列：`grid grid-cols-12` + `col-span-12 lg:col-span-8/4`
- 卡片网格：`grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6`
- 内部双列：`grid grid-cols-2 gap-4`

## Component Usage (OpenTiny)

### TinyGrid

```vue
import { Grid as TinyGrid, GridColumn as TinyGridColumn } from '@opentiny/vue'

<tiny-grid :data="data" border resizable auto-resize>
  <tiny-grid-column field="name" title="Name" sortable>
    <template #default="{ row }">...</template>
  </tiny-grid-column>
</tiny-grid>
```

### TinyButton

```vue
import { Button as TinyButton } from '@opentiny/vue'

<tiny-button type="primary">主操作</tiny-button>
<tiny-button plain>次操作</tiny-button>
<tiny-button type="text">链接操作</tiny-button>
```

### TinyTabs

```vue
import { Tabs as TinyTabs, TabItem as TinyTabItem } from '@opentiny/vue'

<tiny-tabs v-model="activeTab">
  <tiny-tab-item title="Tab" name="tab">...</tiny-tab-item>
</tiny-tabs>
```

## Common Patterns

### Card

```
bg-surface-container-lowest rounded-[2rem] p-6 shadow-sm border border-outline-variant/30
  [+ hover:shadow-xl transition-all duration-300 group]
```

### Body Page Header

```html
<div class="mx-auto max-w-7xl animate-fade-up">
  <div class="min-h-5 flex items-center">
    <nav class="flex items-center gap-2 text-xs font-semibold text-on-surface-variant">
      ...
    </nav>
  </div>
  <div class="mt-3 flex items-center gap-2">
    ...
  </div>
</div>
```

### Status Badge

```html
<span class="flex items-center gap-1 text-[10px] font-bold" :class="colorClass">
  <span class="w-2 h-2 rounded-full" :class="dotClass"></span>
  STATUS
</span>
```

### Micro Label

```html
<span class="text-[10px] font-bold tracking-widest uppercase text-on-surface-variant">LABEL</span>
```

### Icon Button

```html
<button class="p-1.5 rounded-lg hover:bg-surface-container text-on-surface-variant hover:text-primary transition-colors cursor-pointer">
  <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">...</svg>
</button>
```

### Inline SVG Icon

统一属性：`viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"`

尺寸：`w-3 h-3` / `w-3.5 h-3.5` / `w-4 h-4` / `w-5 h-5` / `w-6 h-6`

## App Layout Structure

```
+--[TopNav h-16 fixed, glass blur]------------------+
| Menu | Axiom Azure | Dashboard Agents ... | Search | Deploy |
+-----+--------------------------------------------+
|Side | Main Content (pt-24 px-8 pb-12)            |
|w-64 | ml-64 (or ml-20 collapsed)                 |
|     | <router-view> with fade transition          |
+-----+--------------------------------------------+
                                    [FAB fixed bottom-8 right-8]
```
