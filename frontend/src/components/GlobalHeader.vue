<template>
  <div class="flex-1 flex items-center justify-between min-w-0">
    <!-- System Status Pill (desktop only) -->
    <div class="hidden xl:flex items-center gap-5 ml-1">
      <div class="flex items-center gap-2 px-3 py-1.5 bg-surface-3 rounded-full border border-border">
        <span class="text-[10px] font-bold text-text-muted uppercase tracking-widest">系统健康度</span>
        <div class="flex items-center gap-4 ml-1">
          <div class="flex items-center gap-1.5">
            <div class="w-1.5 h-1.5 rounded-full bg-primary"></div>
            <span class="text-[10px] font-semibold font-mono text-text-secondary">{{ summary.total }} 总数</span>
          </div>
          <div class="w-px h-3 bg-border"></div>
          <div class="flex items-center gap-1.5">
            <div class="w-1.5 h-1.5 rounded-full bg-success animate-pulse"></div>
            <span class="text-[10px] font-semibold font-mono text-text-secondary">{{ summary.active }} 运行中</span>
          </div>
          <div class="w-px h-3 bg-border"></div>
          <div class="flex items-center gap-1.5">
            <div class="w-1.5 h-1.5 rounded-full bg-danger"></div>
            <span class="text-[10px] font-semibold font-mono text-text-secondary">{{ summary.error }} 异常</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Right Actions -->
    <div class="flex items-center gap-2 sm:gap-3 ml-auto">
      <!-- Notification Bell -->
      <button class="relative p-2 text-text-muted hover:text-text hover:bg-surface-3 rounded-lg transition-colors cursor-pointer" title="通知">
        <svg class="w-[18px] h-[18px]" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
          <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/>
          <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
        </svg>
        <!-- Notification Dot -->
        <span class="absolute top-1.5 right-1.5 w-1.5 h-1.5 bg-danger rounded-full border border-surface"></span>
      </button>

      <div class="w-px h-5 bg-border hidden sm:block"></div>

      <!-- User Avatar -->
      <div class="flex items-center gap-2.5 cursor-pointer group">
        <div class="text-right hidden sm:block">
          <p class="text-xs font-semibold text-text group-hover:text-primary transition-colors leading-none">管理员</p>
          <p class="text-[9px] text-text-muted font-mono mt-0.5 uppercase tracking-wide">超级权限</p>
        </div>
        <div class="w-8 h-8 sm:w-9 sm:h-9 rounded-full border-2 border-border group-hover:border-primary transition-colors overflow-hidden shadow-sm">
          <img
            src="https://api.dicebear.com/7.x/avataaars/svg?seed=Argus"
            alt="用户头像"
            class="w-full h-full object-cover"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useAgentStore } from '../stores/agents'
import { storeToRefs } from 'pinia'

const agentStore = useAgentStore()
const { summary } = storeToRefs(agentStore)
</script>
