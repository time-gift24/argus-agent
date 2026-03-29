<!-- @mock — agent 详情、metrics 趋势值/百分比、运行日志、配置信息均为硬编码；替换为：GET /api/agents/:id + WebSocket 实时日志 -->
<template>
  <div class="max-w-7xl mx-auto space-y-6">
    <!-- Breadcrumbs -->
    <div class="flex items-center gap-2 text-sm animate-fade-up">
      <router-link to="/agents" class="text-on-surface-variant hover:text-primary transition-colors">智能体管理</router-link>
      <svg class="w-4 h-4 text-on-surface-variant" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="9 18 15 12 9 6"/>
      </svg>
      <span class="font-bold text-on-surface font-headline">{{ agent?.name || '加载中...' }}</span>
    </div>

    <!-- Agent Header -->
    <div class="bg-surface-container-lowest p-6 rounded-[2rem] border border-outline-variant/30 shadow-sm flex items-center justify-between animate-fade-up animate-delay-1">
      <div class="flex items-center gap-4">
        <div class="w-16 h-16 rounded-2xl bg-primary-fixed flex items-center justify-center text-primary">
          <svg class="w-8 h-8" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="4" y="4" width="16" height="16" rx="2"/>
            <path d="M9 9h.01M15 9h.01M9 15h.01M15 15h.01"/>
          </svg>
        </div>
        <div>
          <h1 class="text-2xl font-headline font-bold tracking-tight text-on-surface">{{ agent?.name }}</h1>
          <div class="flex items-center gap-3 mt-1">
            <div class="flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[10px] font-bold" :class="statusBadgeClass(agent?.status)">
              <div class="w-1.5 h-1.5 rounded-full" :class="statusDotClass(agent?.status)"></div>
              <span class="uppercase tracking-wider">{{ agent?.status }}</span>
            </div>
            <span class="text-xs text-on-surface-variant font-mono">ID: {{ agent?.id }}</span>
          </div>
        </div>
      </div>

      <div class="flex items-center gap-2">
        <tiny-button type="primary">
          <span class="flex items-center gap-1">
            <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="5 3 19 12 5 21 5 3"/></svg>
            启动
          </span>
        </tiny-button>
        <tiny-button plain>
          <span class="flex items-center gap-1">
            <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect x="6" y="4" width="4" height="16"/><rect x="14" y="4" width="4" height="16"/></svg>
            停止
          </span>
        </tiny-button>
        <tiny-button plain>
          <span class="flex items-center gap-1">
            <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 4 12 14.01 9 11.01"/><path d="M22 12A10 10 0 1 1 12 2"/></svg>
            重启
          </span>
        </tiny-button>
        <div class="w-px h-8 bg-outline-variant/30 mx-2"></div>
        <tiny-button type="danger" ghost>
          <span class="flex items-center gap-1">
            <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2"/></svg>
            删除
          </span>
        </tiny-button>
      </div>
    </div>

    <!-- Metrics Grid -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6 animate-fade-up animate-delay-2">
      <div v-for="metric in metrics" :key="metric.title" class="bg-surface-container-lowest p-5 rounded-[2rem] border border-outline-variant/30 shadow-sm">
        <div class="flex items-center justify-between mb-3">
          <span class="text-[10px] font-bold text-on-surface-variant uppercase tracking-widest">{{ metric.title }}</span>
          <div class="w-8 h-8 rounded-lg bg-primary-fixed flex items-center justify-center text-primary">
            <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" v-html="metric.iconPath"></svg>
          </div>
        </div>
        <div class="flex items-end gap-2">
          <span class="text-2xl font-headline font-bold text-on-surface">{{ metric.value }}</span>
          <span class="text-xs font-bold text-success mb-1">{{ metric.trend }}</span>
        </div>
        <div class="mt-4 h-1.5 w-full bg-surface-container rounded-full overflow-hidden">
          <div class="h-full bg-primary rounded-full" :style="{ width: metric.percent + '%' }"></div>
        </div>
      </div>
    </div>

    <!-- Tabs Content -->
    <div class="bg-surface-container-lowest rounded-[2rem] border border-outline-variant/30 shadow-sm overflow-hidden animate-fade-up animate-delay-3">
      <tiny-tabs v-model="activeTab" class="details-tabs">
        <tiny-tab-item title="性能" name="perf">
          <div class="p-8 text-center py-20">
            <div class="w-16 h-16 bg-surface-container rounded-full flex items-center justify-center mx-auto mb-4 text-on-surface-variant">
              <svg class="w-8 h-8" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/>
              </svg>
            </div>
            <p class="text-on-surface-variant">实时性能图表即将上线...</p>
          </div>
        </tiny-tab-item>

        <tiny-tab-item title="运行日志" name="logs">
          <div class="bg-inverse-surface p-4 font-mono text-xs text-success min-h-[400px]">
            <div v-for="i in 10" :key="i" class="mb-1">
              <span class="text-on-surface-variant">[2026-03-27 10:0{{i}}:00]</span>
              <span class="text-primary-fixed"> INFO:</span>
              <span class="text-inverse-on-surface"> Agent {{ agent?.name }} processed task #{{ 1000 + i }}</span>
            </div>
            <div class="animate-pulse">_</div>
          </div>
        </tiny-tab-item>

        <tiny-tab-item title="配置" name="config">
          <div class="p-6 space-y-6">
            <div v-for="i in 3" :key="i" class="flex items-center justify-between py-4 border-b border-outline-variant/20 last:border-0">
              <div>
                <p class="text-sm font-bold text-on-surface">配置参数 {{ i }}</p>
                <p class="text-xs text-on-surface-variant mt-1">控制智能体的核心运行时行为。</p>
              </div>
              <tiny-button size="small" plain>编辑</tiny-button>
            </div>
          </div>
        </tiny-tab-item>
      </tiny-tabs>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import {
  Tabs as TinyTabs, TabItem as TinyTabItem,
  Button as TinyButton
} from '@opentiny/vue'
import { useAgentStore } from '../stores/agents'

const route = useRoute()
const agentStore = useAgentStore()

const activeTab = ref('perf')
const agent = computed(() => agentStore.agents.find(a => a.id === route.params.id))

const statusBadgeClass = (status) => {
  return {
    Active: 'bg-success/10 text-success',
    Idle: 'bg-surface-container text-on-surface-variant',
    Error: 'bg-danger/10 text-danger'
  }[status] || 'bg-surface-container text-on-surface-variant'
}

const statusDotClass = (status) => {
  return {
    Active: 'bg-success',
    Idle: 'bg-on-surface-variant',
    Error: 'bg-danger'
  }[status] || 'bg-on-surface-variant'
}

const metrics = computed(() => [
  { title: 'CPU 使用率', value: (agent.value?.cpu || 0) + '%', trend: '+2.4%', percent: agent.value?.cpu || 0, iconPath: '<line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/>' },
  { title: '内存', value: (agent.value?.memory || 0) + ' MB', trend: '-0.5%', percent: 45, iconPath: '<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/>' },
  { title: '平均响应', value: '124ms', trend: '+12ms', percent: 65, iconPath: '<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>' },
  { title: '运行时间', value: '14d 2h', trend: 'Stable', percent: 92, iconPath: '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>' },
])
</script>

<style scoped>
:deep(.details-tabs .tiny-tabs__header) {
  padding: 0 1.5rem;
  border-bottom: 1px solid rgba(195, 197, 217, 0.3);
}
:deep(.details-tabs .tiny-tabs__item) {
  font-family: "Space Grotesk", sans-serif;
  font-weight: 600;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  padding: 1rem 0;
}
</style>
