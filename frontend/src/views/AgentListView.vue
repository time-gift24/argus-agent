<!-- @mock — agent 列表数据来自 stores/agents.js 的硬编码数组；替换为：GET /api/agents -->
<template>
  <div class="max-w-7xl mx-auto space-y-5">
    <!-- Page Header -->
    <div class="flex items-center justify-between animate-fade-up">
      <div>
        <h1 class="text-3xl font-headline font-bold tracking-tight text-on-surface">Agent <span class="text-primary">Management</span></h1>
        <p class="text-sm text-on-surface-variant mt-1">Monitor and manage all registered agents</p>
      </div>
      <div class="flex items-center gap-2">
        <tiny-button type="primary">
          <span class="flex items-center gap-1.5">
            <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <line x1="12" y1="5" x2="12" y2="19"/>
              <line x1="5" y1="12" x2="19" y2="12"/>
            </svg>
            Create Agent
          </span>
        </tiny-button>
        <tiny-button plain>
          <span class="flex items-center gap-1.5">
            <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M23 4l-6 6M17 4h6v6M1 20l6-6M7 20H1v-6"/>
            </svg>
            Refresh
          </span>
        </tiny-button>
      </div>
    </div>

    <!-- Filters -->
    <div class="bg-surface-container-lowest p-4 rounded-[2rem] border border-outline-variant/30 shadow-sm flex items-center justify-between gap-4 flex-wrap animate-fade-up animate-delay-1">
      <div class="flex items-center gap-3">
        <span class="text-[10px] font-bold text-on-surface-variant uppercase tracking-widest">Status:</span>
        <div class="flex gap-1">
          <button
            v-for="status in filterOptions"
            :key="status.key"
            class="px-3 py-1 text-[11px] font-semibold rounded-lg transition-all duration-150 cursor-pointer"
            :class="filter === status.key
              ? 'bg-primary text-on-primary shadow-sm'
              : 'text-on-surface-variant hover:bg-surface-container'"
            @click="filter = status.key"
          >
            {{ status.label }}
          </button>
        </div>
      </div>

      <!-- Bulk Actions -->
      <div class="flex items-center gap-2">
        <button class="inline-flex items-center gap-1.5 px-2.5 py-1.5 text-[11px] font-semibold text-success border border-success/20 bg-success/10 rounded-lg hover:bg-success hover:text-white transition-colors cursor-pointer">
          <svg class="w-3 h-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <polygon points="5 3 19 12 5 21 5 3"/>
          </svg>
          Start
        </button>
        <button class="inline-flex items-center gap-1.5 px-2.5 py-1.5 text-[11px] font-semibold text-warning border border-warning/20 bg-warning/10 rounded-lg hover:bg-warning hover:text-white transition-colors cursor-pointer">
          <svg class="w-3 h-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <rect x="6" y="4" width="4" height="16"/>
            <rect x="14" y="4" width="4" height="16"/>
          </svg>
          Stop
        </button>
        <button class="inline-flex items-center gap-1.5 px-2.5 py-1.5 text-[11px] font-semibold text-danger border border-danger/20 bg-danger/10 rounded-lg hover:bg-danger hover:text-white transition-colors cursor-pointer">
          <svg class="w-3 h-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="3 6 5 6 21 6"/>
            <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2"/>
          </svg>
          Delete
        </button>
      </div>
    </div>

    <!-- Agent Table -->
    <div class="bg-surface-container-lowest rounded-[2rem] border border-outline-variant/30 shadow-sm overflow-hidden animate-fade-up animate-delay-2">
      <tiny-grid :data="filteredAgents" border resizable auto-resize height="460">
        <tiny-grid-column type="selection" width="44"></tiny-grid-column>

        <tiny-grid-column field="name" title="Agent" sortable>
          <template #default="data">
            <div class="flex items-center gap-2.5">
              <div class="w-8 h-8 rounded-lg bg-primary-fixed flex items-center justify-center text-primary shrink-0">
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

        <tiny-grid-column field="status" title="Status" width="110" sortable>
          <template #default="data">
            <div class="flex items-center gap-2">
              <div class="w-2 h-2 rounded-full shrink-0" :class="statusDotClass(data.row.status)"></div>
              <span class="text-[11px] font-bold uppercase tracking-wide" :class="statusTextClass(data.row.status)">
                {{ data.row.status }}
              </span>
            </div>
          </template>
        </tiny-grid-column>

        <tiny-grid-column field="cpu" title="CPU" width="90" sortable align="center">
          <template #default="data">
            <div class="flex items-center justify-center gap-1.5">
              <div class="w-10 h-1.5 bg-surface-container rounded-full overflow-hidden">
                <div
                  class="h-full rounded-full"
                  :class="cpuBarClass(data.row.cpu)"
                  :style="{ width: data.row.cpu + '%' }"
                ></div>
              </div>
              <span class="text-[11px] font-mono font-semibold text-on-surface-variant w-8">{{ data.row.cpu }}%</span>
            </div>
          </template>
        </tiny-grid-column>

        <tiny-grid-column field="memory" title="Memory" width="100" sortable align="center">
          <template #default="data">
            <span class="text-[11px] font-mono font-semibold text-on-surface-variant">{{ data.row.memory }} MB</span>
          </template>
        </tiny-grid-column>

        <tiny-grid-column field="lastSeen" title="Last Active" width="150" sortable>
          <template #default="data">
            <span class="text-[11px] text-on-surface-variant font-mono">{{ data.row.lastSeen }}</span>
          </template>
        </tiny-grid-column>

        <tiny-grid-column title="Actions" width="100" align="center">
          <template #default="data">
            <div class="flex items-center justify-center gap-1">
              <button class="p-1.5 rounded-lg hover:bg-surface-container text-on-surface-variant hover:text-primary transition-colors cursor-pointer" title="View">
                <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>
                  <polyline points="15 3 21 3 21 9"/>
                  <line x1="10" y1="14" x2="21" y2="3"/>
                </svg>
              </button>
              <button class="p-1.5 rounded-lg hover:bg-surface-container text-on-surface-variant hover:text-on-surface transition-colors cursor-pointer" title="Settings">
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
import { Grid as TinyGrid, GridColumn as TinyGridColumn, Button as TinyButton } from '@opentiny/vue'
import { useAgentStore } from '../stores/agents'
import { storeToRefs } from 'pinia'

const agentStore = useAgentStore()
const { agents } = storeToRefs(agentStore)

const filterOptions = [
  { key: 'All', label: 'All' },
  { key: 'Active', label: 'Active' },
  { key: 'Idle', label: 'Idle' },
  { key: 'Error', label: 'Error' },
]
const filter = ref('All')

const filteredAgents = computed(() => {
  if (filter.value === 'All') return agents.value
  return agents.value.filter(a => a.status === filter.value)
})

const statusDotClass = (status) => {
  return { Active: 'bg-success', Idle: 'bg-on-surface-variant', Error: 'bg-danger' }[status] || 'bg-on-surface-variant'
}

const statusTextClass = (status) => {
  return { Active: 'text-success', Idle: 'text-on-surface-variant', Error: 'text-danger' }[status] || 'text-on-surface-variant'
}

const cpuBarClass = (cpu) => {
  if (cpu >= 80) return 'bg-danger'
  if (cpu >= 50) return 'bg-amber-400'
  return 'bg-success'
}
</script>
