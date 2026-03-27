<template>
  <div class="h-full flex flex-col space-y-4">
    <!-- Page Header -->
    <div class="flex items-center justify-between shrink-0">
      <div>
        <h1 class="text-2xl font-bold tracking-tight text-text">交互控制台</h1>
        <p class="text-sm text-text-muted mt-0.5">通过命令行与智能体交互</p>
      </div>
      <div class="flex items-center gap-2">
        <button
          class="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold text-text-secondary border border-border bg-surface rounded-lg hover:bg-surface-3 transition-colors cursor-pointer"
          @click="clearHistory"
        >
          <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="3 6 5 6 21 6"/>
            <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2"/>
          </svg>
          清空
        </button>
        <button class="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold text-text-secondary border border-border bg-surface rounded-lg hover:bg-surface-3 transition-colors cursor-pointer">
          <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
            <polyline points="7 10 12 15 17 10"/>
            <line x1="12" y1="15" x2="12" y2="3"/>
          </svg>
          导出日志
        </button>
      </div>
    </div>

    <!-- Terminal Window -->
    <div class="flex-1 bg-[#0F172A] rounded-xl border border-[#1E293B] shadow-float flex flex-col overflow-hidden font-mono text-sm min-h-0">

      <!-- Title Bar -->
      <div class="bg-[#1E293B] px-4 py-2.5 border-b border-[#334155] flex items-center justify-between shrink-0">
        <div class="flex items-center gap-3">
          <!-- Traffic lights -->
          <div class="flex gap-1.5">
            <div class="w-3 h-3 rounded-full bg-[#FF5F56]"></div>
            <div class="w-3 h-3 rounded-full bg-[#FFBD2E]"></div>
            <div class="w-3 h-3 rounded-full bg-[#27C93F]"></div>
          </div>
          <span class="text-[10px] text-slate-400 font-semibold uppercase tracking-widest">Argus 控制台</span>
        </div>
        <div class="flex items-center gap-1.5">
          <span class="text-[10px] text-slate-500 font-mono">bash</span>
          <svg class="w-3.5 h-3.5 text-slate-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="4 17 10 11 4 5"/>
            <line x1="12" y1="19" x2="20" y2="19"/>
          </svg>
        </div>
      </div>

      <!-- Terminal Body -->
      <div
        ref="terminalBody"
        class="flex-1 p-5 overflow-y-auto space-y-1"
        @click="terminalInput?.focus()"
      >
        <!-- Welcome Banner -->
        <div class="text-emerald-400 font-semibold mb-5 select-none">
          <div class="mb-1">
            <span class="text-slate-200">╔══════════════════════════════════════╗</span>
          </div>
          <div class="text-center">Argus 智能体管理系统 [版本 0.1.0-alpha]</div>
          <div class="text-slate-500 text-[11px] text-center">(c) 2026 Argus Corp. 保留所有权利。</div>
          <div class="mt-2 mb-1">
            <span class="text-slate-200">╚══════════════════════════════════════╝</span>
          </div>
          <div class="text-slate-400 text-xs">输入 <span class="text-primary">help</span> 获取可用命令列表。</div>
        </div>

        <!-- History Entries -->
        <div v-for="(entry, index) in history" :key="index" class="space-y-0.5">
          <!-- Command -->
          <div class="flex items-start gap-2">
            <!-- Prompt Arrow SVG -->
            <svg class="w-4 h-4 text-primary mt-0.5 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M5 12h14M12 5l7 7-7 7"/>
            </svg>
            <span class="text-slate-100 font-semibold leading-snug">{{ entry.command }}</span>
          </div>
          <!-- Output -->
          <div class="pl-6 text-slate-400 whitespace-pre-wrap leading-relaxed text-[13px]">{{ entry.output }}</div>
        </div>

        <!-- Active Input Line -->
        <div class="flex items-center gap-2 mt-1 group/input">
          <!-- Prompt Arrow SVG -->
          <svg class="w-4 h-4 text-primary shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <path d="M5 12h14M12 5l7 7-7 7"/>
          </svg>
          <span class="text-slate-400 font-semibold">$</span>
          <input
            v-model="input"
            ref="terminalInput"
            type="text"
            class="flex-1 bg-transparent border-none outline-none text-slate-100 placeholder-slate-600 focus:ring-0 p-0 font-mono text-[13px]"
            placeholder="输入命令..."
            @keydown.enter="executeCommand"
            @keydown.up.prevent="navigateHistory('up')"
            @keydown.down.prevent="navigateHistory('down')"
          />
          <!-- Blinking cursor -->
          <span class="w-2 h-4 bg-primary animate-pulse rounded-sm"></span>
        </div>
      </div>

      <!-- Status Bar -->
      <div class="bg-[#1E293B] px-4 py-1.5 border-t border-[#334155] flex items-center justify-between shrink-0">
        <div class="flex items-center gap-4">
          <span class="text-[10px] text-slate-500 font-mono">{{ history.length }} 条记录</span>
          <span class="text-[10px] text-slate-500 font-mono">输入 help 查看命令</span>
        </div>
        <div class="flex items-center gap-1.5">
          <div class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></div>
          <span class="text-[10px] text-emerald-400 font-semibold">就绪</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'

const input = ref('')
const terminalBody = ref(null)
const terminalInput = ref(null)
const history = ref([])
const commandList = ref([])
const historyPointer = ref(-1)

const executeCommand = async () => {
  const cmd = input.value.trim()
  if (!cmd) return

  commandList.value.unshift(cmd)
  historyPointer.value = -1

  let output = ''
  switch (cmd.toLowerCase()) {
    case 'help':
      output = `可用命令:
  help     显示此帮助信息
  clear    清空终端历史
  list     列出所有已注册的智能体
  status   显示系统运行状态
  version  显示系统版本`
      break
    case 'clear':
      history.value = []
      input.value = ''
      return
    case 'list':
      output = `ID   名称           状态
  1   Agent-001      运行中
  2   Agent-002      运行中
  3   Agent-003      异常
  4   Agent-004      空闲`
      break
    case 'status':
      output = `系统健康度: 良好
运行中的智能体: 2
异常数量: 1
响应延迟: 124ms`
      break
    case 'version':
      output = 'Argus CLI v0.1.0-alpha (darwin-arm64)'
      break
    default:
      output = `未找到命令: ${cmd}。输入 'help' 获取帮助。`
  }

  history.value.push({ command: cmd, output })
  input.value = ''

  await nextTick()
  if (terminalBody.value) {
    terminalBody.value.scrollTop = terminalBody.value.scrollHeight
  }
}

const navigateHistory = (direction) => {
  if (commandList.value.length === 0) return

  if (direction === 'up') {
    if (historyPointer.value < commandList.value.length - 1) {
      historyPointer.value++
      input.value = commandList.value[historyPointer.value]
    }
  } else {
    if (historyPointer.value > 0) {
      historyPointer.value--
      input.value = commandList.value[historyPointer.value]
    } else {
      historyPointer.value = -1
      input.value = ''
    }
  }
}

const clearHistory = () => {
  history.value = []
}
</script>
