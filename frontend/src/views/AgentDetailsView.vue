<template>
  <div class="space-y-6">
    <!-- Breadcrumbs/Back -->
    <div class="flex items-center gap-2 text-sm text-gray-500">
      <router-link to="/agents" class="hover:text-primary transition-colors">智能体管理</router-link>
      <component :is="icons.ChevronRight" class="w-4 h-4" />
      <span class="font-bold text-text">{{ agent?.name || '加载中...' }}</span>
    </div>

    <!-- Agent Header -->
    <div class="bg-white p-6 rounded-xl border border-gray-200 shadow-sm flex items-center justify-between">
      <div class="flex items-center gap-4">
        <div class="w-16 h-16 rounded-2xl bg-primary/10 flex items-center justify-center text-primary">
          <component :is="icons.Cpu" class="w-8 h-8" />
        </div>
        <div>
          <h1 class="text-2xl font-bold tracking-tight">{{ agent?.name }}</h1>
          <div class="flex items-center gap-3 mt-1">
            <div class="flex items-center gap-1.5 px-2 py-0.5 bg-emerald-50 text-emerald-600 rounded-md border border-emerald-100">
              <div class="w-1.5 h-1.5 rounded-full bg-emerald-500"></div>
              <span class="text-[10px] font-bold uppercase tracking-wider">{{ translateStatus(agent?.status) }}</span>
            </div>
            <span class="text-xs text-gray-400 font-mono">ID: {{ agent?.id }}</span>
          </div>
        </div>
      </div>
      
      <div class="flex items-center gap-2">
        <tiny-button :icon="icons.Play" type="primary">启动</tiny-button>
        <tiny-button :icon="icons.Square">停止</tiny-button>
        <tiny-button :icon="icons.RefreshCw">重启</tiny-button>
        <div class="w-px h-8 bg-gray-200 mx-2"></div>
        <tiny-button :icon="icons.Trash2" type="danger" ghost>删除</tiny-button>
      </div>
    </div>

    <!-- Metrics Grid -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
      <div v-for="metric in metrics" :key="metric.title" class="bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
        <div class="flex items-center justify-between mb-3">
          <span class="text-xs font-bold text-gray-400 uppercase tracking-wider">{{ metric.title }}</span>
          <component :is="metric.icon" class="w-4 h-4 text-gray-300" />
        </div>
        <div class="flex items-end gap-2">
          <span class="text-2xl font-bold font-mono text-text">{{ metric.value }}</span>
          <span class="text-xs font-bold text-emerald-500 mb-1">{{ metric.trend }}</span>
        </div>
        <div class="mt-4 h-1.5 w-full bg-gray-100 rounded-full overflow-hidden">
          <div class="h-full bg-primary rounded-full" :style="{ width: metric.percent + '%' }"></div>
        </div>
      </div>
    </div>

    <!-- Tabs Content -->
    <div class="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
      <tiny-tabs v-model="activeTab" class="details-tabs">
        <tiny-tab-item title="性能监控" name="perf">
          <div class="p-8 text-center py-20">
            <div class="w-16 h-16 bg-gray-50 rounded-full flex items-center justify-center mx-auto mb-4 text-gray-300">
              <component :is="icons.BarChart3" class="w-8 h-8" />
            </div>
            <p class="text-gray-400 italic">实时性能图表开发中...</p>
          </div>
        </tiny-tab-item>
        
        <tiny-tab-item title="运行日志" name="logs">
          <div class="bg-[#1E1E1E] p-4 font-mono text-xs text-emerald-400 min-h-[400px]">
            <div v-for="i in 10" :key="i" class="mb-1">
              <span class="text-gray-500">[2026-03-27 10:0{{i}}:00]</span>
              <span class="text-blue-400"> 信息:</span>
              <span class="text-white"> 智能体 {{ agent?.name }} 成功处理任务 #{{ 1000 + i }}</span>
            </div>
            <div class="animate-pulse">_</div>
          </div>
        </tiny-tab-item>

        <tiny-tab-item title="配置信息" name="config">
          <div class="p-6 space-y-6">
            <div v-for="i in 3" :key="i" class="flex items-center justify-between py-4 border-b border-gray-100 last:border-0">
              <div>
                <p class="text-sm font-bold text-text">配置参数 {{ i }}</p>
                <p class="text-xs text-gray-400 mt-1">该设置项控制智能体的核心运行行为。</p>
              </div>
              <tiny-button size="small">编辑</tiny-button>
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
  ChevronRight, Cpu, Play, Square, RefreshCw, Trash2,
  Activity, Zap, Database, Clock, BarChart3
} from 'lucide-vue-next'
import { 
  Tabs as TinyTabs, TabItem as TinyTabItem, 
  Button as TinyButton 
} from '@opentiny/vue'
import { useAgentStore } from '../stores/agents'

const route = useRoute()
const agentStore = useAgentStore()
const icons = { ChevronRight, Cpu, Play, Square, RefreshCw, Trash2, BarChart3 }

const activeTab = ref('perf')
const agent = computed(() => agentStore.agents.find(a => a.id === route.params.id))

const translateStatus = (status) => {
  const translations = {
    'Active': '运行中',
    'Idle': '空闲',
    'Error': '异常'
  }
  return translations[status] || status
}

const metrics = computed(() => [
  { title: 'CPU 使用率', value: (agent.value?.cpu || 0) + '%', icon: Activity, trend: '+2.4%', percent: agent.value?.cpu || 0 },
  { title: '内存占用', value: (agent.value?.memory || 0) + ' MB', icon: Database, trend: '-0.5%', percent: 45 },
  { title: '平均响应时间', value: '124ms', icon: Zap, trend: '+12ms', percent: 65 },
  { title: '运行时间', value: '14天 2小时', icon: Clock, trend: '稳定', percent: 92 },
])
</script>

<style scoped>
:deep(.details-tabs .tiny-tabs__header) {
  padding: 0 1.5rem;
  border-bottom: 1px solid #E2E8F0;
}
:deep(.details-tabs .tiny-tabs__item) {
  font-weight: 600;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  padding: 1rem 0;
}
</style>
