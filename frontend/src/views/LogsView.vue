<template>
  <div class="space-y-5">
    <div>
      <h1 class="text-2xl font-bold tracking-tight text-text">系统日志</h1>
      <p class="text-sm text-text-muted mt-0.5">查看平台运行日志与事件记录</p>
    </div>

    <!-- Logs Table -->
    <div class="bg-surface rounded-xl border border-border shadow-card overflow-hidden">
      <div class="p-4 border-b border-border flex items-center justify-between">
        <div class="flex items-center gap-3">
          <div class="flex items-center gap-1.5 px-2.5 py-1 bg-surface-3 rounded-md border border-border">
            <span class="text-[10px] font-semibold text-text-muted uppercase tracking-widest">日志级别:</span>
            <button
              v-for="level in ['全部', '信息', '警告', '错误']"
              :key="level"
              class="px-2 py-0.5 text-[10px] font-semibold rounded transition-colors cursor-pointer"
              :class="activeLevel === level ? 'bg-primary text-white' : 'text-text-secondary hover:bg-surface-2'"
              @click="activeLevel = level"
            >
              {{ level }}
            </button>
          </div>
        </div>
        <button class="inline-flex items-center gap-1.5 px-3 py-1.5 text-[11px] font-semibold text-text-secondary border border-border bg-surface rounded-lg hover:bg-surface-3 transition-colors cursor-pointer">
          <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
            <polyline points="7 10 12 15 17 10"/>
            <line x1="12" y1="15" x2="12" y2="3"/>
          </svg>
          导出日志
        </button>
      </div>

      <!-- Log Entries -->
      <div class="font-mono text-xs divide-y divide-border">
        <div v-for="(log, i) in filteredLogs" :key="i" class="flex items-start gap-3 px-4 py-2.5 hover:bg-surface-3 transition-colors">
          <span class="text-[10px] text-text-muted shrink-0 w-36">{{ log.time }}</span>
          <span class="text-[10px] font-semibold px-1.5 py-0.5 rounded shrink-0" :class="log.levelClass">{{ log.level }}</span>
          <span class="text-text-secondary">{{ log.message }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const activeLevel = ref('全部')

// @mock — 8 条硬编码日志；替换为：GET /api/logs
const logs = [
  { time: '2026-03-27 14:32:01', level: '信息', levelClass: 'text-primary bg-primary/10', message: 'Agent-003 成功处理任务 #2048' },
  { time: '2026-03-27 14:28:45', level: '警告', levelClass: 'text-amber-500 bg-amber-50', message: 'Agent-007 CPU 使用率超过 85%' },
  { time: '2026-03-27 14:21:10', level: '信息', levelClass: 'text-primary bg-primary/10', message: '系统完成自动备份，耗时 23 秒' },
  { time: '2026-03-27 14:15:33', level: '错误', levelClass: 'text-danger bg-danger/10', message: 'Agent-005 连接超时，已自动重试' },
  { time: '2026-03-27 14:10:00', level: '信息', levelClass: 'text-primary bg-primary/10', message: '新增工具插件 "网页抓取" 已注册' },
  { time: '2026-03-27 14:02:18', level: '信息', levelClass: 'text-primary bg-primary/10', message: 'Agent-001 - Agent-005 批量更新完成' },
  { time: '2026-03-27 13:55:42', level: '警告', levelClass: 'text-amber-500 bg-amber-50', message: '内存使用率达到 78%，建议扩容' },
  { time: '2026-03-27 13:44:00', level: '信息', levelClass: 'text-primary bg-primary/10', message: '用户 "admin" 登录系统' },
]

const levelMap = { '全部': null, '信息': '信息', '警告': '警告', '错误': '错误' }
const filteredLogs = computed(() => {
  const l = levelMap[activeLevel.value]
  return l ? logs.filter(log => log.level === l) : logs
})
</script>
