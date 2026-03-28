<!-- @mock — agent 列表数据来自 stores/agents.js 的硬编码数组；替换为：GET /api/agents -->
<template>
  <div class="space-y-5">
    <!-- Page Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold tracking-tight text-text">智能体管理</h1>
        <p class="text-sm text-text-muted mt-0.5">查看和管理所有已注册的智能体</p>
      </div>
      <div class="flex items-center gap-2">
        <button class="inline-flex items-center gap-1.5 px-3.5 py-2 text-xs font-semibold text-primary border border-primary/30 bg-primary/10 rounded-lg hover:bg-primary hover:text-white transition-colors cursor-pointer">
          <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 5v14M5 12h14"/>
          </svg>
          创建智能体
        </button>
        <button class="inline-flex items-center gap-1.5 px-3.5 py-2 text-xs font-semibold text-text-secondary border border-border bg-surface rounded-lg hover:bg-surface-3 transition-colors cursor-pointer">
          <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M23 4l-6 6M17 4h6v6M1 20l6-6M7 20H1v-6"/>
          </svg>
          刷新
        </button>
      </div>
    </div>

    <!-- Filters -->
    <div class="bg-surface p-4 rounded-xl border border-border shadow-card flex items-center justify-between gap-4 flex-wrap">
      <div class="flex items-center gap-3">
        <span class="text-[11px] font-semibold text-text-muted uppercase tracking-widest">状态:</span>
        <div class="flex gap-1">
          <button
            v-for="status in filterOptions"
            :key="status.key"
            class="px-3 py-1 text-[11px] font-semibold rounded-md transition-all duration-150 cursor-pointer"
            :class="filter === status.key
              ? 'bg-primary text-white shadow-sm'
              : 'text-text-secondary hover:bg-surface-3'"
            @click="filter = status.key"
          >
            {{ status.label }}
          </button>
        </div>
      </div>

      <!-- Bulk Actions -->
      <div class="flex items-center gap-2">
        <button class="inline-flex items-center gap-1.5 px-2.5 py-1.5 text-[11px] font-semibold text-success border border-success/20 bg-success/10 rounded-md hover:bg-success hover:text-white transition-colors cursor-pointer">
          <svg class="w-3 h-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <polygon points="5 3 19 12 5 21 5 3"/>
          </svg>
          启动
        </button>
        <button class="inline-flex items-center gap-1.5 px-2.5 py-1.5 text-[11px] font-semibold text-amber-500 border border-amber-200 bg-amber-50 rounded-md hover:bg-amber-500 hover:text-white transition-colors cursor-pointer">
          <svg class="w-3 h-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <rect x="6" y="4" width="4" height="16"/>
            <rect x="14" y="4" width="4" height="16"/>
          </svg>
          停止
        </button>
        <button class="inline-flex items-center gap-1.5 px-2.5 py-1.5 text-[11px] font-semibold text-danger border border-danger/20 bg-danger/10 rounded-md hover:bg-danger hover:text-white transition-colors cursor-pointer">
          <svg class="w-3 h-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="3 6 5 6 21 6"/>
            <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2"/>
          </svg>
          删除
        </button>
      </div>
    </div>

    <!-- Agent Table -->
    <div class="bg-surface rounded-xl border border-border shadow-card overflow-hidden">
      <tiny-grid :data="filteredAgents" border resizable auto-resize height="460">
        <!-- Checkbox -->
        <tiny-grid-column type="selection" width="44"></tiny-grid-column>

        <!-- Name -->
        <tiny-grid-column field="name" title="名称" sortable>
          <template #default="data">
            <div class="flex items-center gap-2.5">
              <div class="w-8 h-8 rounded-lg bg-primary/10 border border-primary/20 flex items-center justify-center text-primary shrink-0">
                <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="4" y="4" width="16" height="16" rx="2"/>
                  <path d="M9 9h.01M15 9h.01M9 15h.01M15 15h.01"/>
                </svg>
              </div>
              <router-link
                :to="`/agents/${data.row.id}`"
                class="text-sm font-semibold text-primary hover:underline cursor-pointer"
              >
                {{ data.row.name }}
              </router-link>
            </div>
          </template>
        </tiny-grid-column>

        <!-- Status -->
        <tiny-grid-column field="status" title="状态" width="110" sortable>
          <template #default="data">
            <div class="flex items-center gap-2">
              <div class="w-2 h-2 rounded-full shrink-0" :class="statusDotClass(data.row.status)"></div>
              <span class="text-[11px] font-bold uppercase tracking-wide" :class="statusTextClass(data.row.status)">
                {{ translateStatus(data.row.status) }}
              </span>
            </div>
          </template>
        </tiny-grid-column>

        <!-- CPU -->
        <tiny-grid-column field="cpu" title="CPU" width="90" sortable align="center">
          <template #default="data">
            <div class="flex items-center justify-center gap-1.5">
              <div class="w-10 h-1.5 bg-surface-3 rounded-full overflow-hidden">
                <div
                  class="h-full rounded-full"
                  :class="cpuBarClass(data.row.cpu)"
                  :style="{ width: data.row.cpu + '%' }"
                ></div>
              </div>
              <span class="text-[11px] font-mono font-semibold text-text-secondary w-8">{{ data.row.cpu }}%</span>
            </div>
          </template>
        </tiny-grid-column>

        <!-- Memory -->
        <tiny-grid-column field="memory" title="内存" width="100" sortable align="center">
          <template #default="data">
            <span class="text-[11px] font-mono font-semibold text-text-secondary">{{ data.row.memory }} MB</span>
          </template>
        </tiny-grid-column>

        <!-- Last Seen -->
        <tiny-grid-column field="lastSeen" title="最后活跃" width="150" sortable>
          <template #default="data">
            <span class="text-[11px] text-text-muted font-mono">{{ data.row.lastSeen }}</span>
          </template>
        </tiny-grid-column>

        <!-- Actions -->
        <tiny-grid-column title="操作" width="100" align="center">
          <template #default="data">
            <div class="flex items-center justify-center gap-1">
              <!-- View -->
              <button class="p-1.5 rounded-md hover:bg-surface-3 text-text-muted hover:text-primary transition-colors cursor-pointer" title="查看详情">
                <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>
                  <polyline points="15 3 21 3 21 9"/>
                  <line x1="10" y1="14" x2="21" y2="3"/>
                </svg>
              </button>
              <!-- Settings -->
              <button class="p-1.5 rounded-md hover:bg-surface-3 text-text-muted hover:text-text transition-colors cursor-pointer" title="设置">
                <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="12" r="3"/>
                  <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/>
                </svg>
              </button>
            </div>
          </template>
        </tiny-grid-column>
      </tiny-grid>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Grid as TinyGrid, GridColumn as TinyGridColumn } from '@opentiny/vue'
import { useAgentStore } from '../stores/agents'
import { storeToRefs } from 'pinia'

const agentStore = useAgentStore()
const { agents } = storeToRefs(agentStore)

const filterOptions = [
  { key: '全部', label: '全部' },
  { key: '运行中', label: '运行中' },
  { key: '空闲', label: '空闲' },
  { key: '异常', label: '异常' },
]
const filter = ref('全部')

const statusMap = {
  '运行中': 'Active',
  '空闲': 'Idle',
  '异常': 'Error',
}

const translateStatus = (status) => {
  const map = { Active: '运行中', Idle: '空闲', Error: '异常' }
  return map[status] || status
}

const filteredAgents = computed(() => {
  if (filter.value === '全部') return agents.value
  return agents.value.filter(a => a.status === statusMap[filter.value])
})

const statusDotClass = (status) => {
  return { Active: 'bg-success', Idle: 'bg-text-muted', Error: 'bg-danger' }[status] || 'bg-text-muted'
}

const statusTextClass = (status) => {
  return { Active: 'text-success', Idle: 'text-text-muted', Error: 'text-danger' }[status] || 'text-text-muted'
}

const cpuBarClass = (cpu) => {
  if (cpu >= 80) return 'bg-danger'
  if (cpu >= 50) return 'bg-amber-400'
  return 'bg-success'
}
</script>
