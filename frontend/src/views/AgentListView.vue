<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <h1 class="text-3xl font-bold tracking-tight">Agents</h1>
      <div class="flex items-center gap-3">
        <tiny-button type="primary" :icon="icons.Plus">Create Agent</tiny-button>
        <tiny-button :icon="icons.RefreshCw">Refresh</tiny-button>
      </div>
    </div>

    <!-- Filters & Bulk Actions -->
    <div class="bg-white p-4 rounded-xl border border-gray-200 shadow-sm flex items-center justify-between">
      <div class="flex items-center gap-4">
        <div class="flex items-center gap-2 px-3 py-1.5 bg-gray-50 rounded-lg border border-gray-100">
          <span class="text-xs font-bold text-gray-400 uppercase tracking-wider">Status:</span>
          <div class="flex gap-1">
            <button 
              v-for="status in ['All', 'Active', 'Idle', 'Error']" 
              :key="status"
              class="px-3 py-0.5 text-xs font-bold rounded-md transition-all"
              :class="[filter === status ? 'bg-primary text-white shadow-sm' : 'text-gray-500 hover:bg-gray-200']"
              @click="filter = status"
            >
              {{ status }}
            </button>
          </div>
        </div>
      </div>
      
      <div class="flex items-center gap-2">
        <tiny-button size="small" :icon="icons.Play">Start</tiny-button>
        <tiny-button size="small" :icon="icons.Square">Stop</tiny-button>
        <tiny-button size="small" type="danger" :icon="icons.Trash2">Delete</tiny-button>
      </div>
    </div>

    <!-- Agent Grid/Table -->
    <div class="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
      <tiny-grid :data="filteredAgents" border resizable auto-resize height="500">
        <tiny-grid-column type="selection" width="50"></tiny-grid-column>
        <tiny-grid-column field="name" title="Agent Name" sortable>
          <template #default="data">
            <div class="flex items-center gap-3">
              <div class="w-8 h-8 rounded-lg bg-gray-50 border border-gray-100 flex items-center justify-center">
                <component :is="icons.Cpu" class="w-4 h-4 text-primary" />
              </div>
              <router-link :to="`/agents/${data.row.id}`" class="font-bold text-primary hover:underline">
                {{ data.row.name }}
              </router-link>
            </div>
          </template>
        </tiny-grid-column>
        <tiny-grid-column field="status" title="Status" width="120" sortable>
          <template #default="data">
            <div class="flex items-center gap-2">
              <div class="w-2 h-2 rounded-full" :class="statusColor(data.row.status)"></div>
              <span class="text-xs font-bold uppercase tracking-tight">{{ data.row.status }}</span>
            </div>
          </template>
        </tiny-grid-column>
        <tiny-grid-column field="cpu" title="CPU %" width="100" sortable align="center">
          <template #default="data">
            <span class="font-mono text-xs font-bold">{{ data.row.cpu }}%</span>
          </template>
        </tiny-grid-column>
        <tiny-grid-column field="memory" title="MEM (MB)" width="120" sortable align="center">
          <template #default="data">
            <span class="font-mono text-xs font-bold">{{ data.row.memory }} MB</span>
          </template>
        </tiny-grid-column>
        <tiny-grid-column field="lastSeen" title="Last Activity" width="200" sortable>
          <template #default="data">
            <span class="text-xs text-gray-500 font-mono">{{ data.row.lastSeen }}</span>
          </template>
        </tiny-grid-column>
        <tiny-grid-column title="Actions" width="120" align="center">
          <template #default="data">
            <div class="flex items-center justify-center gap-2">
              <button class="p-1.5 hover:bg-gray-100 rounded-md text-gray-400 hover:text-primary transition-colors">
                <component :is="icons.ExternalLink" class="w-4 h-4" />
              </button>
              <button class="p-1.5 hover:bg-gray-100 rounded-md text-gray-400 hover:text-rose-500 transition-colors">
                <component :is="icons.Settings" class="w-4 h-4" />
              </button>
            </div>
          </template>
        </tiny-grid-column>
      </tiny-grid>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { 
  Plus, RefreshCw, Cpu, Play, Square, Trash2, 
  ExternalLink, Settings 
} from 'lucide-vue-next'
import { Grid as TinyGrid, GridColumn as TinyGridColumn, Button as TinyButton } from '@opentiny/vue'
import { useAgentStore } from '../stores/agents'
import { storeToRefs } from 'pinia'

const icons = { Plus, RefreshCw, Cpu, Play, Square, Trash2, ExternalLink, Settings }
const agentStore = useAgentStore()
const { agents } = storeToRefs(agentStore)

const filter = ref('All')

const filteredAgents = computed(() => {
  if (filter.value === 'All') return agents.value
  return agents.value.filter(a => a.status === statusMap[filter.value] || a.status === filter.value)
})

const statusMap = {
  'Active': 'Active',
  'Idle': 'Idle',
  'Error': 'Error'
}

const statusColor = (status) => {
  switch (status) {
    case 'Active': return 'bg-emerald-500'
    case 'Idle': return 'bg-gray-300'
    case 'Error': return 'bg-rose-500'
    default: return 'bg-gray-400'
  }
}
</script>
