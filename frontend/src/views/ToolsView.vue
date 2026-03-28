<!-- @mock — 6 张占位卡片，无真实工具数据；替换为：GET /api/tools -->
<template>
  <div class="max-w-7xl mx-auto space-y-6">
    <div class="animate-fade-up">
      <h1 class="text-3xl font-headline font-bold tracking-tight text-on-surface mb-1">
        Tool <span class="text-primary">Arsenal</span>
      </h1>
      <p class="text-sm text-on-surface-variant">Modular capabilities available for your agents.</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
      <div
        v-for="(tool, i) in tools"
        :key="i"
        class="bg-surface-container-lowest p-6 rounded-[2rem] shadow-sm border border-outline-variant/30 hover:shadow-xl transition-all duration-300 group cursor-pointer animate-fade-up"
        :class="`animate-delay-${i + 1}`"
      >
        <div class="absolute top-6 right-6" v-if="tool.elite">
          <span class="flex items-center gap-1 text-[10px] font-bold text-primary">
            <svg class="w-3 h-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M12 2L9 9l-7 1 5 5-1.5 7L12 18.5 18.5 22 17 15l5-5-7-1z"/>
            </svg>
            ELITE
          </span>
        </div>

        <div class="w-14 h-14 rounded-2xl flex items-center justify-center mb-5 transition-colors"
          :class="tool.bgClass"
        >
          <svg class="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" :class="tool.iconClass" v-html="tool.iconPath"></svg>
        </div>
        <h3 class="font-headline font-bold text-lg text-on-surface mb-2">{{ tool.name }}</h3>
        <p class="text-xs text-on-surface-variant leading-relaxed">{{ tool.desc }}</p>

        <div class="mt-5 pt-4 border-t border-outline-variant/20 flex items-center justify-between">
          <span class="text-[10px] font-bold uppercase tracking-widest" :class="tool.statusClass">{{ tool.status }}</span>
          <div class="flex items-center gap-1 text-on-surface-variant group-hover:text-primary transition-colors">
            <span class="text-[10px] font-bold">Open</span>
            <svg class="w-3 h-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <line x1="7" y1="17" x2="17" y2="7"/><polyline points="7 7 17 7 17 17"/>
            </svg>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const tools = [
  {
    name: 'Web Scraper',
    desc: 'Extract structured data from any web page with intelligent parsing and rate limiting.',
    status: 'Active',
    statusClass: 'text-success',
    elite: true,
    bgClass: 'bg-primary-fixed group-hover:bg-primary',
    iconClass: 'text-primary group-hover:text-on-primary',
    iconPath: '<circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>',
  },
  {
    name: 'Code Executor',
    desc: 'Sandboxed runtime environment for executing agent-generated code safely.',
    status: 'Active',
    statusClass: 'text-success',
    elite: false,
    bgClass: 'bg-tertiary-fixed group-hover:bg-tertiary',
    iconClass: 'text-tertiary group-hover:text-on-tertiary',
    iconPath: '<polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/>',
  },
  {
    name: 'Sentiment Engine',
    desc: 'Natural language processing pipeline for market sentiment analysis.',
    status: 'Active',
    statusClass: 'text-success',
    elite: false,
    bgClass: 'bg-secondary-fixed group-hover:bg-secondary',
    iconClass: 'text-secondary group-hover:text-on-secondary',
    iconPath: '<path d="M12 2a8 8 0 0 1 8 8v4a8 8 0 0 1-16 0v-4a8 8 0 0 1 8-8z"/><path d="M9 12h.01M15 12h.01"/>',
  },
  {
    name: 'Data Pipeline',
    desc: 'Orchestrate complex data flows between agents and external services.',
    status: 'Beta',
    statusClass: 'text-primary',
    elite: false,
    bgClass: 'bg-primary-fixed group-hover:bg-primary',
    iconClass: 'text-primary group-hover:text-on-primary',
    iconPath: '<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/>',
  },
  {
    name: 'Threat Scanner',
    desc: 'Real-time security analysis and vulnerability detection engine.',
    status: 'Active',
    statusClass: 'text-success',
    elite: true,
    bgClass: 'bg-error-container/20 group-hover:bg-error-container',
    iconClass: 'text-error group-hover:text-on-error',
    iconPath: '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',
  },
  {
    name: 'Memory Indexer',
    desc: 'Persistent memory management with vector-based semantic retrieval.',
    status: 'Coming Soon',
    statusClass: 'text-on-surface-variant',
    elite: false,
    bgClass: 'bg-surface-container group-hover:bg-outline-variant',
    iconClass: 'text-on-surface-variant group-hover:text-on-surface',
    iconPath: '<rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/>',
  },
]
</script>
