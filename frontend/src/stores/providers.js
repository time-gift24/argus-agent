import { ref } from 'vue'
import { defineStore } from 'pinia'
import * as api from '../api/providers'

export const useProvidersStore = defineStore('providers', () => {
  const internalProviders = ref([])
  const userProviders = ref([])
  const loading = ref(false)

  async function fetchProviders() {
    loading.value = true
    try {
      const [internal, user] = await Promise.all([
        api.listInternal(),
        api.list(),
      ])
      internalProviders.value = internal.data
      userProviders.value = user.data
    } catch {
      // If unauthenticated, user providers will fail — leave empty
      internalProviders.value = []
      userProviders.value = []
    } finally {
      loading.value = false
    }
  }

  async function createProvider(data) {
    await api.create(data)
    await fetchProviders()
  }

  async function deleteProvider(id) {
    await api.remove(id)
    await fetchProviders()
  }

  async function setDefaultProvider(id) {
    await api.setDefault(id)
    await fetchProviders()
  }

  return {
    internalProviders, userProviders, loading,
    fetchProviders, createProvider, deleteProvider, setDefaultProvider,
  }
})
