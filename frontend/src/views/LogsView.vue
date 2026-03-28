<template>
  <div class="max-w-7xl mx-auto space-y-5">
    <div class="animate-fade-up">
      <h1 class="text-3xl font-headline font-bold tracking-tight text-on-surface">
        System <span class="text-primary">Logs</span>
      </h1>
      <p class="text-sm text-on-surface-variant mt-1">Platform runtime logs and event records.</p>
    </div>

    <!-- Logs Panel -->
    <div class="bg-surface-container-lowest rounded-[2rem] border border-outline-variant/30 shadow-sm overflow-hidden animate-fade-up animate-delay-1">
      <!-- Toolbar -->
      <div class="p-5 border-b border-outline-variant/20 flex items-center justify-between">
        <div class="flex items-center gap-3">
          <span class="text-[10px] font-bold text-on-surface-variant uppercase tracking-widest">Level:</span>
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
        <tiny-button plain>
          <span class="flex items-center gap-1.5">
            <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
              <polyline points="7 10 12 15 17 10"/>
              <line x1="12" y1="15" x2="12" y2="3"/>
            </svg>
            Export
          </span>
        </tiny-button>
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
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Button as TinyButton } from '@opentiny/vue'

const levels = ['All', 'Info', 'Warning', 'Error']
const activeLevel = ref('All')

// @mock — 8 条硬编码日志；替换为：GET /api/logs
const logs = [
  { time: '2026-03-27 14:32:01', level: 'Info', levelClass: 'bg-primary-fixed text-primary', message: 'Agent-003 successfully processed task #2048' },
  { time: '2026-03-27 14:28:45', level: 'Warning', levelClass: 'bg-warning/10 text-warning', message: 'Agent-007 CPU usage exceeded 85%' },
  { time: '2026-03-27 14:21:10', level: 'Info', levelClass: 'bg-primary-fixed text-primary', message: 'System auto-backup completed in 23 seconds' },
  { time: '2026-03-27 14:15:33', level: 'Error', levelClass: 'bg-danger/10 text-danger', message: 'Agent-005 connection timeout, auto-retry initiated' },
  { time: '2026-03-27 14:10:00', level: 'Info', levelClass: 'bg-primary-fixed text-primary', message: 'New tool plugin "Web Scraper" registered' },
  { time: '2026-03-27 14:02:18', level: 'Info', levelClass: 'bg-primary-fixed text-primary', message: 'Agent-001 through Agent-005 batch update completed' },
  { time: '2026-03-27 13:55:42', level: 'Warning', levelClass: 'bg-warning/10 text-warning', message: 'Memory usage at 78%, scaling recommended' },
  { time: '2026-03-27 13:44:00', level: 'Info', levelClass: 'bg-primary-fixed text-primary', message: 'User "admin" logged in' },
]

const levelMap = { 'All': null, 'Info': 'Info', 'Warning': 'Warning', 'Error': 'Error' }
const filteredLogs = computed(() => {
  const l = levelMap[activeLevel.value]
  return l ? logs.filter(log => log.level === l) : logs
})
</script>
