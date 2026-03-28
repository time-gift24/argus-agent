---
paths:
  - "frontend/**/*.vue"
  - "frontend/**/*.ts"
  - "frontend/**/*.js"
  - "frontend/**/*.css"
---

# 编码风格

## 设计令牌一致性

使用 `style.css` 中定义的 `@theme` 令牌，而非原生 Tailwind 颜色：

```
// 伪代码
WRONG:  bg-white text-gray-500 border-gray-200
CORRECT: bg-surface text-text-secondary border-border
```

**可用令牌（定义于 `frontend/src/style.css`）：**

| 类别 | 令牌 |
|------|------|
| 背景 | `bg-background`, `bg-surface`, `bg-surface-2`, `bg-surface-3` |
| 文字 | `text-text`, `text-text-secondary`, `text-text-muted` |
| 边框 | `border-border`, `border-border-strong` |
| 语义 | `bg-success-bg`, `bg-warning-bg`, `bg-danger-bg`, `bg-info-bg` |
| 阴影 | `shadow-card`, `shadow-panel`, `shadow-float` |
| 圆角 | `rounded-sm`, `rounded-md`, `rounded-lg`, `rounded-xl`, `rounded-full` |

## SFC 顺序与结构

固定顺序：`<template>` → `<script setup>` → `<style scoped>`

```vue
<template>
  <!-- 模板内容 -->
</template>

<script setup>
// 脚本内容
</script>

<style scoped>
/* 组件样式 */
</style>
```

* `<style>` 必须使用 `scoped` 避免样式污染
* 无自定义样式时可省略 `<style>` 块

## 组件体积控制

* 单一职责：每个组件只做一件事
* 拆分触发条件：
  - 模板超过 200 行
  - 脚本超过 100 行
  - 存在 3 个以上独立 UI 区域
* 提取重复 UI 模式到 `components/`
* 提取重复逻辑到 `composables/`

## 命名约定

| 类型 | 约定 | 示例 |
|------|------|------|
| 视图组件 | `*View.vue` | `DashboardView.vue` |
| UI 组件 | PascalCase | `GlobalHeader.vue` |
| Composables | `use*.ts` | `useAgentStatus.ts` |
| Stores | 复数名词 | `agents.ts` |
| 布局 | `*Layout.vue` | `MainLayout.vue` |

## TypeScript 迁移

项目正在逐步引入 TypeScript：

* 新建 composables 使用 `.ts` 扩展名
* 新建 stores 可使用 `.ts` 扩展名
* 逐步迁移现有 `.js` 文件
* 迁移时添加类型注解，使用 `defineComponent` 包装

# 标准

## TinyVue 组件引入

按需引入，使用别名避免命名冲突：

```javascript
import { Grid as TinyGrid, Button as TinyButton } from '@opentiny/vue'
```

* 不全局注册 TinyVue 组件
* 别名格式：`Tiny` + 组件名

## 图标使用

使用 `lucide-vue-next` 图标库：

```javascript
import { Play, Pause, Settings } from 'lucide-vue-next'
```

* 在响应式数组中存储图标引用时，使用 `markRaw()` 包装：

```javascript
const navItems = [
  { icon: markRaw(Dashboard), label: 'Dashboard' }
]
```

## 路径别名

使用 `@/` 别名替代相对路径：

```javascript
// WRONG
import { useAgentsStore } from '../stores/agents'

// CORRECT
import { useAgentsStore } from '@/stores/agents'
```

别名配置于 `vite.config.js`：`@` → `/src`

## Tailwind CSS 4

设计令牌通过 `@theme` 定义，使用语义化类名：

```html
<!-- 推荐 -->
<div class="bg-surface shadow-card rounded-lg border border-border">

<!-- 避免 -->
<div class="bg-white shadow-md rounded-lg border border-gray-200">
```

## 参考

查看技能：
- `vue-best-practices` - Composition API、`<script setup>`、组件设计完整指南
- `create-adaptable-composable` - 创建可复用的 composable 函数
