<template>
  <div class="space-y-5">
    <div>
      <h1 class="text-2xl font-bold tracking-tight text-text">系统设置</h1>
      <p class="text-sm text-text-muted mt-0.5">配置平台全局参数与权限策略</p>
    </div>

    <!-- Settings Groups -->
    <div class="space-y-4">
      <div class="bg-surface rounded-xl border border-border shadow-card p-5">
        <h2 class="text-sm font-bold text-text mb-4 pb-3 border-b border-border">通用设置</h2>
        <div class="space-y-4">
          <div v-for="i in 3" :key="i" class="flex items-center justify-between py-2">
            <div>
              <p class="text-xs font-semibold text-text">配置参数 {{ i }}</p>
              <p class="text-[11px] text-text-muted mt-0.5">该设置项控制智能体的核心运行行为。</p>
            </div>
            <button class="px-3 py-1.5 text-[11px] font-semibold text-primary border border-primary/30 bg-primary/10 rounded-lg hover:bg-primary hover:text-white transition-colors cursor-pointer">
              编辑
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
