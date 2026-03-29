<template>
  <PageBodyShell
    :breadcrumbs="['系统日志']"
    content-class="space-y-5"
    description="平台运行日志和事件记录。"
    title="系统日志"
  >
    <template #actions>
      <tiny-button plain>
        <span class="flex items-center gap-1.5">
          <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
            <polyline points="7 10 12 15 17 10"/>
            <line x1="12" y1="15" x2="12" y2="3"/>
          </svg>
          导出
        </span>
      </tiny-button>
    </template>

    <!-- Logs Panel -->
    <div class="bg-surface-container-lowest rounded-[2rem] border border-outline-variant/30 shadow-sm overflow-hidden animate-fade-up animate-delay-1">
      <!-- Toolbar -->
      <div class="p-5 border-b border-outline-variant/20">
        <div class="flex items-center gap-3">
          <span class="text-[10px] font-bold text-on-surface-variant uppercase tracking-widest">级别:</span>
          <div class="flex gap-1">
            <button
              v-for="level in levels"
              :key="level"
              class="px-3 py-1 text-[11px] font-semibold rounded-lg transition-all cursor-pointer"
              :class="activeLevel === level
                ? 'bg-primary text-on-primary shadow-sm'
                : 'text-on-surface-variant hover:bg-surface-container'"
              @click="activeLevel = level"
            >
              {{ level }}
            </button>
          </div>
        </div>
      </div>

      <!-- Log Entries -->
      <div class="font-mono text-xs divide-y divide-outline-variant/10">
        <div v-for="(log, i) in filteredLogs" :key="i" class="flex items-start gap-3 px-5 py-3 hover:bg-surface-container-low transition-colors">
          <span class="text-[10px] text-on-surface-variant shrink-0 w-36">{{ log.time }}</span>
          <span class="text-[10px] font-bold px-2 py-0.5 rounded shrink-0" :class="log.levelClass">{{ log.level }}</span>
          <span class="text-on-surface-variant">{{ log.message }}</span>
        </div>
      </div>
    </div>
  </PageBodyShell>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Button as TinyButton } from '@opentiny/vue'
import PageBodyShell from '../components/PageBodyShell.vue'

const levels = ['全部', '信息', '警告', '异常']
const activeLevel = ref('全部')

// @mock — 8 条硬编码日志；替换为：GET /api/logs
const logs = [
  { time: '2026-03-27 14:32:01', level: '信息', levelClass: 'bg-primary-fixed text-primary', message: 'Agent-003 成功处理任务 #2048' },
  { time: '2026-03-27 14:28:45', level: '警告', levelClass: 'bg-warning/10 text-warning', message: 'Agent-007 CPU 使用率超过 85%' },
  { time: '2026-03-27 14:21:10', level: '信息', levelClass: 'bg-primary-fixed text-primary', message: '系统自动备份完成，耗时 23 秒' },
  { time: '2026-03-27 14:15:33', level: '异常', levelClass: 'bg-danger/10 text-danger', message: 'Agent-005 连接超时，已自动重试' },
  { time: '2026-03-27 14:10:00', level: '信息', levelClass: 'bg-primary-fixed text-primary', message: '新工具插件 "网页抓取器" 已注册' },
  { time: '2026-03-27 14:02:18', level: '信息', levelClass: 'bg-primary-fixed text-primary', message: 'Agent-001 至 Agent-005 批量更新完成' },
  { time: '2026-03-27 13:55:42', level: '警告', levelClass: 'bg-warning/10 text-warning', message: '内存使用率 78%，建议扩容' },
  { time: '2026-03-27 13:44:00', level: '信息', levelClass: 'bg-primary-fixed text-primary', message: '用户 "admin" 已登录' },
]

const levelMap = { '全部': null, '信息': '信息', '警告': '警告', '异常': '异常' }
const filteredLogs = computed(() => {
  const l = levelMap[activeLevel.value]
  return l ? logs.filter(log => log.level === l) : logs
})
</script>
