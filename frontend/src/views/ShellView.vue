<template>
  <div class="max-w-7xl mx-auto h-full flex flex-col space-y-4">
    <!-- Page Header -->
    <div class="flex items-center justify-between shrink-0 animate-fade-up">
      <div>
        <h1 class="text-3xl font-headline font-bold tracking-tight text-on-surface">
          交互式 <span class="text-primary">控制台</span>
        </h1>
        <p class="text-sm text-on-surface-variant mt-1">直接与智能体交互的命令行界面</p>
      </div>
      <div class="flex items-center gap-2">
        <tiny-button plain @click="clearHistory">
          <span class="flex items-center gap-1.5">
            <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="3 6 5 6 21 6"/>
              <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2"/>
            </svg>
            清空
          </span>
        </tiny-button>
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
      </div>
    </div>

    <!-- Terminal Window -->
    <div class="flex-1 bg-inverse-surface rounded-[2rem] border border-outline-variant/30 shadow-lg flex flex-col overflow-hidden font-mono text-sm min-h-0 animate-fade-up animate-delay-1">

      <!-- Title Bar -->
      <div class="bg-inverse-surface/80 px-5 py-3 border-b border-outline-variant/20 flex items-center justify-between shrink-0">
        <div class="flex items-center gap-3">
          <div class="flex gap-1.5">
            <div class="w-3 h-3 rounded-full bg-danger"></div>
            <div class="w-3 h-3 rounded-full bg-warning"></div>
            <div class="w-3 h-3 rounded-full bg-success"></div>
          </div>
          <span class="text-[10px] text-inverse-on-surface/50 font-semibold uppercase tracking-widest font-headline">Axiom 控制台</span>
        </div>
        <div class="flex items-center gap-1.5">
          <span class="text-[10px] text-inverse-on-surface/30 font-mono">bash</span>
          <svg class="w-3.5 h-3.5 text-inverse-on-surface/30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
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
        <div class="text-success font-semibold mb-5 select-none">
          <div class="mb-1">
            <span class="text-inverse-on-surface/60">+======================================+</span>
          </div>
          <div class="text-center">Axiom Azure 智能体系统 [v2.4.0]</div>
          <div class="text-inverse-on-surface/30 text-[11px] text-center">(c) 2026 Axiom Corp. 保留所有权利。</div>
          <div class="mt-2 mb-1">
            <span class="text-inverse-on-surface/60">+======================================+</span>
          </div>
          <div class="text-inverse-on-surface/50 text-xs">输入 <span class="text-primary-fixed">help</span> 查看可用命令。</div>
        </div>

        <!-- History Entries -->
        <div v-for="(entry, index) in history" :key="index" class="space-y-0.5">
          <div class="flex items-start gap-2">
            <svg class="w-4 h-4 text-primary mt-0.5 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M5 12h14M12 5l7 7-7 7"/>
            </svg>
            <span class="text-inverse-on-surface font-semibold leading-snug">{{ entry.command }}</span>
          </div>
          <div class="pl-6 text-inverse-on-surface/50 whitespace-pre-wrap leading-relaxed text-[13px]">{{ entry.output }}</div>
        </div>

        <!-- Active Input -->
        <div class="flex items-center gap-2 mt-1">
          <svg class="w-4 h-4 text-primary shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <path d="M5 12h14M12 5l7 7-7 7"/>
          </svg>
          <span class="text-inverse-on-surface/50 font-semibold">$</span>
          <input
            v-model="input"
            ref="terminalInput"
            type="text"
            class="flex-1 bg-transparent border-none outline-none text-inverse-on-surface placeholder-inverse-on-surface/20 focus:ring-0 p-0 font-mono text-[13px]"
            placeholder="输入命令..."
            @keydown.enter="executeCommand"
            @keydown.up.prevent="navigateHistory('up')"
            @keydown.down.prevent="navigateHistory('down')"
          />
          <span class="w-2 h-4 bg-primary animate-pulse rounded-sm"></span>
        </div>
      </div>

      <!-- Status Bar -->
      <div class="bg-inverse-surface/80 px-5 py-2 border-t border-outline-variant/20 flex items-center justify-between shrink-0">
        <div class="flex items-center gap-4">
          <span class="text-[10px] text-inverse-on-surface/30 font-mono">{{ history.length }} 条记录</span>
          <span class="text-[10px] text-inverse-on-surface/30 font-mono">输入 help 查看命令</span>
        </div>
        <div class="flex items-center gap-1.5">
          <div class="w-1.5 h-1.5 rounded-full bg-success animate-pulse"></div>
          <span class="text-[10px] text-success font-semibold">就绪</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import { Button as TinyButton } from '@opentiny/vue'

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
  help     显示帮助信息
  clear    清空终端历史
  list     列出所有已注册智能体
  status   显示系统状态
  version  显示系统版本`
      break
    case 'clear':
      history.value = []
      input.value = ''
      return
    // @mock — list/status 命令返回硬编码数据；替换为：调用后端 API 或 WebSocket
    case 'list':
      output = `ID   名称            状态
  1   Agent-001       Active
  2   Agent-002       Active
  3   Agent-003       Error
  4   Agent-004       Idle`
      break
    case 'status':
      output = `系统健康: 良好
运行中智能体: 2
异常数: 1
平均延迟: 124ms`
      break
    case 'version':
      output = 'Axiom Azure CLI v2.4.0 (darwin-arm64)'
      break
    default:
      output = `命令未找到: ${cmd}。输入 'help' 查看可用命令。`
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
