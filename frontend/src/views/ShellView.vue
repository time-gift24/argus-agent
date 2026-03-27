<template>
  <div class="h-full flex flex-col space-y-6">
    <div class="flex items-center justify-between">
      <h1 class="text-3xl font-bold tracking-tight">Interaction Shell</h1>
      <div class="flex items-center gap-2">
        <tiny-button size="small" :icon="icons.Trash2" @click="clearHistory">Clear</tiny-button>
        <tiny-button size="small" :icon="icons.Download">Export Logs</tiny-button>
      </div>
    </div>

    <!-- Terminal Container -->
    <div class="flex-1 bg-[#0D0D0D] rounded-xl border border-gray-800 shadow-2xl flex flex-col overflow-hidden font-mono text-sm">
      <!-- Terminal Header -->
      <div class="bg-[#1A1A1A] px-4 py-2 border-b border-gray-800 flex items-center justify-between">
        <div class="flex items-center gap-2">
          <div class="flex gap-1.5">
            <div class="w-3 h-3 rounded-full bg-[#FF5F56]"></div>
            <div class="w-3 h-3 rounded-full bg-[#FFBD2E]"></div>
            <div class="w-3 h-3 rounded-full bg-[#27C93F]"></div>
          </div>
          <span class="text-[10px] text-gray-500 font-bold ml-2 uppercase tracking-widest">Argus-Shell-Session — 80×24</span>
        </div>
        <component :is="icons.Terminal" class="w-4 h-4 text-gray-600" />
      </div>

      <!-- Terminal Body -->
      <div ref="terminalBody" class="flex-1 p-6 overflow-y-auto space-y-2 text-gray-300">
        <div class="text-emerald-500 font-bold mb-4">
          Argus Agents Management System [Version 0.1.0-alpha]<br>
          (c) 2026 Argus Corp. All rights reserved.<br><br>
          Type 'help' for a list of available commands.
        </div>

        <div v-for="(entry, index) in history" :key="index" class="space-y-1">
          <div class="flex gap-2">
            <span class="text-primary font-bold">➜</span>
            <span class="text-white font-bold">{{ entry.command }}</span>
          </div>
          <div class="pl-5 text-gray-400 whitespace-pre-wrap mb-4">{{ entry.output }}</div>
        </div>

        <!-- Input Line -->
        <div class="flex gap-2 items-center group">
          <span class="text-primary font-bold">➜</span>
          <input 
            v-model="input" 
            ref="terminalInput"
            type="text" 
            class="flex-1 bg-transparent border-none outline-none text-white focus:ring-0 p-0"
            placeholder="Type a command..."
            @keydown.enter="executeCommand"
            @keydown.up.prevent="navigateHistory('up')"
            @keydown.down.prevent="navigateHistory('down')"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import { Terminal, Trash2, Download } from 'lucide-vue-next'
import { Button as TinyButton } from '@opentiny/vue'

const icons = { Terminal, Trash2, Download }
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
      output = 'Available commands:\n  help     - Show this help message\n  clear    - Clear terminal history\n  list     - List all registered agents\n  status   - Show system health status\n  version  - Show system version'
      break
    case 'clear':
      history.value = []
      input.value = ''
      return
    case 'list':
      output = 'ID      NAME            STATUS\n1       Agent-001       ACTIVE\n2       Agent-002       ACTIVE\n3       Agent-003       ERROR\n4       Agent-004       IDLE'
      break
    case 'status':
      output = 'SYSTEM HEALTH: OK\nACTIVE AGENTS: 2\nERRORS: 1\nLATENCY: 124ms'
      break
    case 'version':
      output = 'Argus CLI v0.1.0-alpha (darwin-arm64)'
      break
    default:
      output = `Command not found: ${cmd}. Type 'help' for assistance.`
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

<style scoped>
input::placeholder {
  @apply text-gray-700 italic;
}
</style>
