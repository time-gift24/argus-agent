<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold tracking-tight text-text">仪表盘概览</h1>
        <p class="text-sm text-text-muted mt-0.5">实时监控智能体运行状态</p>
      </div>
      <div class="flex items-center gap-2">
        <div class="flex items-center gap-1.5 px-3 py-1.5 bg-surface rounded-lg border border-border">
          <div class="w-1.5 h-1.5 rounded-full bg-success animate-pulse"></div>
          <span class="text-[11px] font-semibold text-text-secondary">系统正常</span>
        </div>
      </div>
    </div>

    <!-- Stat Cards -->
    <div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
      <div
        v-for="(stat, i) in stats"
        :key="i"
        class="bg-surface rounded-xl border border-border shadow-card p-5 hover:shadow-panel transition-shadow cursor-pointer group"
      >
        <div class="flex items-start justify-between mb-4">
          <div
            class="w-10 h-10 rounded-lg flex items-center justify-center"
            :class="stat.bgClass"
          >
            <component :is="stat.icon" class="w-5 h-5" :class="stat.iconClass" :stroke-width="2" />
          </div>
          <span
            class="text-[11px] font-semibold px-2 py-0.5 rounded-full"
            :class="stat.badgeClass"
          >{{ stat.badge }}</span>
        </div>
        <p class="text-2xl font-bold font-mono text-text">{{ stat.value }}</p>
        <p class="text-xs font-medium text-text-muted mt-1">{{ stat.label }}</p>
        <div class="mt-3 h-1 bg-surface-3 rounded-full overflow-hidden">
          <div
            class="h-full rounded-full transition-all duration-500"
            :class="stat.barClass"
            :style="{ width: stat.percent + '%' }"
          ></div>
        </div>
      </div>
    </div>

    <!-- Activity & Quick Actions Row -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">
      <!-- Recent Activity -->
      <div class="lg:col-span-2 bg-surface rounded-xl border border-border shadow-card p-5">
        <h2 class="text-sm font-bold text-text mb-4">最近活动</h2>
        <div class="space-y-3">
          <div v-for="(activity, i) in activities" :key="i" class="flex items-start gap-3">
            <div class="w-2 h-2 rounded-full mt-1.5 shrink-0" :class="activity.dotClass"></div>
            <div class="flex-1 min-w-0">
              <p class="text-xs font-medium text-text">{{ activity.text }}</p>
              <p class="text-[10px] text-text-muted font-mono mt-0.5">{{ activity.time }}</p>
            </div>
            <span class="text-[10px] font-semibold shrink-0" :class="activity.tagClass">{{ activity.tag }}</span>
          </div>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="bg-surface rounded-xl border border-border shadow-card p-5">
        <h2 class="text-sm font-bold text-text mb-4">快捷操作</h2>
        <div class="space-y-2">
          <button
            v-for="action in quickActions"
            :key="action.label"
            class="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-left transition-colors hover:bg-surface-3 group"
          >
            <div class="w-7 h-7 rounded-md flex items-center justify-center bg-primary/10 text-primary group-hover:bg-primary group-hover:text-white transition-colors">
              <component :is="action.icon" class="w-3.5 h-3.5" :stroke-width="2.5" />
            </div>
            <div>
              <p class="text-xs font-semibold text-text">{{ action.label }}</p>
              <p class="text-[10px] text-text-muted">{{ action.sub }}</p>
            </div>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { markRaw } from 'vue'
import {
  Cpu,
  Zap,
  Clock,
  Activity,
  Plus,
  RefreshCw,
  Settings,
} from 'lucide-vue-next'

// @mock — 仪表盘统计数据、最近活动、快捷操作全部硬编码；替换为：GET /api/dashboard
const stats = [
  {
    label: '运行中的智能体',
    value: '12',
    badge: '+3 本周',
    badgeClass: 'bg-success/10 text-success',
    icon: markRaw(Cpu),
    bgClass: 'bg-primary/10',
    iconClass: 'text-primary',
    barClass: 'bg-primary',
    percent: 75,
  },
  {
    label: '总任务处理量',
    value: '8,241',
    badge: '+18%',
    badgeClass: 'bg-primary/10 text-primary',
    icon: markRaw(Zap),
    bgClass: 'bg-amber-50',
    iconClass: 'text-amber-500',
    barClass: 'bg-amber-400',
    percent: 82,
  },
  {
    label: '平均响应时间',
    value: '94ms',
    badge: '-12ms',
    badgeClass: 'bg-success/10 text-success',
    icon: markRaw(Activity),
    bgClass: 'bg-emerald-50',
    iconClass: 'text-emerald-500',
    barClass: 'bg-success',
    percent: 40,
  },
  {
    label: '系统运行时长',
    value: '14天',
    badge: '稳定',
    badgeClass: 'bg-success/10 text-success',
    icon: markRaw(Clock),
    bgClass: 'bg-indigo-50',
    iconClass: 'text-indigo-500',
    barClass: 'bg-indigo-400',
    percent: 92,
  },
]

const activities = [
  { text: 'Agent-003 成功处理任务 #2048', time: '2 分钟前', tag: '成功', tagClass: 'text-success bg-success/10 px-1.5 py-0.5 rounded', dotClass: 'bg-success' },
  { text: 'Agent-007 异常重启，已恢复', time: '11 分钟前', tag: '已恢复', tagClass: 'text-amber-500 bg-amber-50 px-1.5 py-0.5 rounded', dotClass: 'bg-amber-400' },
  { text: '新增工具插件 "网页抓取" 已注册', time: '38 分钟前', tag: '新插件', tagClass: 'text-primary bg-primary/10 px-1.5 py-0.5 rounded', dotClass: 'bg-primary' },
  { text: 'Agent-001 - Agent-005 批量更新完成', time: '2 小时前', tag: '完成', tagClass: 'text-text-muted bg-surface-3 px-1.5 py-0.5 rounded', dotClass: 'bg-text-muted' },
]

const quickActions = [
  { label: '创建新智能体', sub: '快速启动一个全新智能体', icon: markRaw(Plus) },
  { label: '批量刷新状态', sub: '更新所有智能体运行状态', icon: markRaw(RefreshCw) },
  { label: '系统设置', sub: '配置全局参数与权限', icon: markRaw(Settings) },
]
</script>
