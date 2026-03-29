<template>
  <div>
    <!-- Card header -->
    <div class="flex items-start justify-between mb-4">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-xl bg-primary-fixed flex items-center justify-center">
          <svg class="w-5 h-5 text-primary" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 2L2 7l10 5 10-5-10-5z"/>
            <path d="M2 17l10 5 10-5"/>
            <path d="M2 12l10 5 10-5"/>
          </svg>
        </div>
        <div>
          <h3 class="font-headline font-bold text-sm text-on-surface">{{ config.name }}</h3>
          <div class="flex items-center gap-2 mt-0.5">
            <span class="text-[10px] font-bold tracking-widest uppercase px-1.5 py-0.5 rounded-full"
              :class="config.transport === 'stdio' ? 'bg-warning/20 text-warning' : config.transport === 'sse' ? 'bg-tertiary-fixed text-on-surface' : 'bg-primary-fixed text-primary'"
            >{{ config.transport.toUpperCase() }}</span>
            <span v-if="config.kind === 'global'" class="text-[10px] font-bold text-on-surface-variant">全局</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Config info -->
    <div class="space-y-1.5 mb-4 text-xs text-on-surface-variant">
      <p v-if="config.description" class="truncate">{{ config.description }}</p>
      <div v-if="config.url" class="flex items-center gap-1.5">
        <span class="text-[10px] font-bold tracking-widest uppercase">URL</span>
        <span class="font-mono truncate">{{ config.url }}</span>
      </div>
      <div v-if="config.command" class="flex items-center gap-1.5">
        <span class="text-[10px] font-bold tracking-widest uppercase">CMD</span>
        <span class="font-mono truncate">{{ config.command }}</span>
      </div>
      <div v-if="config.tools?.length" class="flex items-center gap-1.5">
        <span class="text-[10px] font-bold tracking-widest uppercase">工具</span>
        <span class="font-mono">{{ config.tools.length }} 个</span>
      </div>
    </div>

    <!-- Test result -->
    <div v-if="testResult" class="mb-3 px-3 py-2 rounded-xl bg-surface-container text-xs">
      <div v-if="testResult.success" class="flex items-center gap-2">
        <span class="w-2 h-2 rounded-full bg-success shrink-0"></span>
        <span class="text-success font-semibold">连接成功</span>
        <span v-if="testResult.tools?.length" class="text-on-surface-variant">{{ testResult.tools.length }} 个工具</span>
      </div>
      <div v-else class="flex items-start gap-2">
        <span class="w-2 h-2 rounded-full bg-danger mt-0.5 shrink-0"></span>
        <span class="text-danger">{{ testResult.message || '连接失败' }}</span>
      </div>
    </div>

    <!-- Tools list -->
    <div v-if="tools !== undefined" class="mb-3 px-3 py-2 rounded-xl bg-surface-container text-xs space-y-1.5 max-h-48 overflow-y-auto">
      <p v-if="toolsLoading" class="text-on-surface-variant">加载中...</p>
      <p v-else-if="!tools.length" class="text-on-surface-variant">暂无缓存工具，请先测试连接</p>
      <template v-else>
        <div v-for="t in tools" :key="t.name" class="py-1">
          <p class="font-mono font-semibold text-on-surface">{{ t.name }}</p>
          <p v-if="t.description" class="text-on-surface-variant mt-0.5">{{ t.description }}</p>
        </div>
      </template>
    </div>

    <!-- Actions -->
    <div class="flex items-center gap-2 pt-3 border-t border-outline-variant/10">
      <button
        class="px-3 py-1.5 text-[10px] font-bold tracking-widest uppercase text-on-surface-variant hover:text-tertiary-fixed-dim rounded-lg hover:bg-surface-container transition-colors cursor-pointer disabled:opacity-50 disabled:cursor-wait"
        :disabled="testing"
        @click="$emit('test')"
      >
        <template v-if="testing">测试中...</template>
        <template v-else>测试连接</template>
      </button>
      <button
        class="px-3 py-1.5 text-[10px] font-bold tracking-widest uppercase text-on-surface-variant hover:text-primary rounded-lg hover:bg-surface-container transition-colors cursor-pointer"
        @click="$emit('tools')"
      >
        {{ tools !== undefined ? '收起工具' : '查看工具' }}
      </button>
      <button
        v-if="config.kind === 'user'"
        class="px-3 py-1.5 text-[10px] font-bold tracking-widest uppercase text-on-surface-variant hover:text-primary rounded-lg hover:bg-surface-container transition-colors cursor-pointer"
        @click="$emit('edit')"
      >
        编辑
      </button>
      <button
        v-if="config.kind === 'user'"
        class="px-3 py-1.5 text-[10px] font-bold tracking-widest uppercase text-on-surface-variant hover:text-danger rounded-lg hover:bg-surface-container transition-colors cursor-pointer ml-auto"
        @click="$emit('delete')"
      >
        删除
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  config: { type: Object, required: true },
  testing: { type: Boolean, default: false },
  testResult: { type: Object, default: undefined },
  tools: { type: Array, default: undefined },
  toolsLoading: { type: Boolean, default: false },
})

defineEmits(['test', 'tools', 'edit', 'delete'])
</script>
