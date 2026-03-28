---
paths:
  - "frontend/**/*.vue"
  - "frontend/**/*.ts"
  - "frontend/**/*.js"
---

# 常见模式

## 可组合函数（Composables）

提取重复逻辑到 `src/composables/useXxx.ts`：

* 一个 composable 只做一件事
* 返回响应式状态和方法
* 接受 `MaybeRef` / `MaybeRefOrGetter` 参数以支持灵活调用

**示例：状态映射**

```
// 伪代码
DUPLICATED: translateStatus() 在 AgentListView.vue 和 AgentDetailsView.vue 中重复
EXTRACTED:  src/composables/useAgentStatus.ts 导出 translateStatus, statusDotClass, statusTextClass
```

## 布局统一

* `App.vue` 是应用唯一根布局
* 不创建平行的重复布局组件
* 需要多布局时，提取共享部分为子组件（如 `Sidebar.vue`、`Header.vue`）

## API 数据层

数据流方向：`API` → `Store` → `Component`

* API 调用封装在 `src/api/` 模块
* Store 消费 API 层，处理缓存和状态
* 组件只从 Store 获取数据，不直接调用 API

## 状态管理

使用 Pinia setup stores：

```javascript
export const useAgentsStore = defineStore('agents', () => {
  const agents = ref([])
  const activeCount = computed(() => agents.value.filter(a => a.status === 'running').length)

  async function fetchAgents() { /* ... */ }

  return { agents, activeCount, fetchAgents }
})
```

* 使用 `storeToRefs` 解构响应式状态
* Store 不包含 UI 逻辑（无 DOM 引用、无路由跳转）

# Vue 模式

## 路由懒加载

除默认路由外，懒加载所有视图：

```javascript
const routes = [
  { path: '/', component: () => import('@/views/DashboardView.vue') },
  { path: '/agents', component: () => import('@/views/AgentListView.vue') }
]
```

## 列表与过滤模式

* 过滤状态使用 `ref`
* 过滤结果使用 `computed`
* 过滤选项定义为常量

```javascript
const STATUS_OPTIONS = ['all', 'running', 'stopped', 'error'] as const

const filter = ref('all')
const filteredAgents = computed(() =>
  filter.value === 'all'
    ? agents.value
    : agents.value.filter(a => a.status === filter.value)
)
```

## 组件通信

* **父 → 子**：props
* **子 → 父**：emits
* **深层依赖**：provide/inject
* **全局状态**：Pinia store

```vue
<!-- 父组件 -->
<AgentCard :agent="agent" @update="handleUpdate" />

<!-- 子组件 -->
<script setup>
const props = defineProps({ agent: Object })
const emit = defineEmits(['update'])
</script>
```

## 参考

查看技能：
- `vue-best-practices` - Composition API、组件设计、响应式模式
- `vue-pinia-best-practices` - Pinia store 模式与最佳实践
- `vue-router-best-practices` - 路由配置、导航守卫、懒加载
- `create-adaptable-composable` - 创建可复用的 composable 函数
