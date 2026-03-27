import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAgentStore = defineStore('agents', () => {
  const agents = ref([
    { id: '1', name: 'Agent-001', status: 'Active', cpu: 12, memory: 128, lastSeen: '2026-03-27 10:00:00' },
    { id: '2', name: 'Agent-002', status: 'Active', cpu: 45, memory: 256, lastSeen: '2026-03-27 10:01:00' },
    { id: '3', name: 'Agent-003', status: 'Error', cpu: 0, memory: 0, lastSeen: '2026-03-27 09:55:00' },
    { id: '4', name: 'Agent-004', status: 'Idle', cpu: 2, memory: 64, lastSeen: '2026-03-27 10:02:00' },
  ])

  const summary = computed(() => {
    return {
      total: agents.value.length,
      active: agents.value.filter(a => a.status === 'Active').length,
      error: agents.value.filter(a => a.status === 'Error').length,
    }
  })

  return { agents, summary }
})
