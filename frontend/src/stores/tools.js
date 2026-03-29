import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import * as api from '../api/tools'

export const useToolsStore = defineStore('tools', () => {
  const tools = ref([])
  const loading = ref(false)

  const builtinTools = computed(() => tools.value.filter(t => t.is_builtin))
  const customTools = computed(() => tools.value.filter(t => !t.is_builtin))

  async function fetchTools() {
    loading.value = true
    try {
      const { data } = await api.list()
      tools.value = data.data
    } catch {
      tools.value = []
    } finally {
      loading.value = false
    }
  }

  async function deleteTool(id) {
    await api.remove(id)
    await fetchTools()
  }

  return {
    tools, loading, builtinTools, customTools,
    fetchTools, deleteTool,
  }
})
