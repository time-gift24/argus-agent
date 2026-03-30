<script setup>
import { ref, watch } from 'vue'
import * as api from '../api/providers'

import { getApiErrorMessage } from '../api/client'

const props = defineProps({
  providerId: { type: String, required: true },
})
const emit = defineEmits(['change'])

const models = ref([])
const loading = ref(false)
const newModelName = ref('')
const addingModel = ref(false)
const error = ref('')

// Per-model test state
const testStates = ref(new Map()) // modelId → { loading, result }

async function fetchModels() {
  loading.value = true
  error.value = ''
  try {
    const { data } = await api.listModels(props.providerId)
    models.value = data
    emit('change', data)
  } catch {
    error.value = '加载模型列表失败'
  } finally {
    loading.value = false
  }
}

async function handleAddModel() {
  const name = newModelName.value.trim()
  if (!name) return

  addingModel.value = true
  error.value = ''
  try {
    const { data } = await api.addModel(props.providerId, name)
    models.value.push(data)
    emit('change', models.value)
    newModelName.value = ''
  } catch (e) {
    error.value = getApiErrorMessage(e, '添加模型失败')
  } finally {
    addingModel.value = false
  }
}

async function handleDeleteModel(modelId) {
  error.value = ''
  try {
    await api.deleteModel(props.providerId, modelId)
    testStates.value.delete(modelId)
    await fetchModels()
  } catch (e) {
    error.value = getApiErrorMessage(e, '删除模型失败')
  }
}

async function handleSetDefault(modelId) {
  error.value = ''
  try {
    await api.setDefaultModel(props.providerId, modelId)
    models.value = models.value.map(m => ({
      ...m,
      is_default: m.id === modelId,
    }))
    emit('change', models.value)
  } catch (e) {
    error.value = getApiErrorMessage(e, '设置默认失败')
  }
}

async function handleTestModel(modelId) {
  const prev = testStates.value.get(modelId) || {}
  testStates.value.set(modelId, { ...prev, loading: true, result: null })
  try {
    const { data } = await api.testModel(props.providerId, modelId)
    testStates.value.set(modelId, { loading: false, result: data })
  } catch (e) {
    testStates.value.set(modelId, {
      loading: false,
      result: { success: false, message: getApiErrorMessage(e, '测试失败') },
    })
  }
}

watch(() => props.providerId, (id) => {
  if (id) fetchModels()
}, { immediate: true })
</script>

<template>
  <section class="rounded-2xl border border-outline-variant/20 bg-surface-container-lowest p-5 shadow-sm">
    <div class="mb-4">
      <p class="text-[10px] font-bold uppercase tracking-[0.24em] text-on-surface-variant">模型配置</p>
      <p class="mt-1 text-xs text-on-surface-variant">为该提供商添加一个或多个模型标识，独立测试每个模型的连通性。</p>
    </div>

    <!-- Add model -->
    <div class="flex gap-2">
      <input
        v-model="newModelName"
        class="flex-1 rounded-xl border border-outline-variant/30 bg-surface-container px-4 py-2 text-sm font-mono transition-colors focus:border-primary focus:outline-none"
        placeholder="gpt-4o、claude-3-sonnet"
        @keydown.enter="handleAddModel"
      />
      <button
        type="button"
        class="rounded-xl border border-outline-variant/30 px-4 py-2 text-sm font-bold text-on-surface-variant transition-colors hover:bg-surface-container disabled:cursor-not-allowed disabled:opacity-50"
        :disabled="addingModel || !newModelName.trim()"
        @click="handleAddModel"
      >
        {{ addingModel ? '添加中...' : '添加模型' }}
      </button>
    </div>

    <p v-if="error" class="mt-2 text-xs text-danger">{{ error }}</p>

    <!-- Model list -->
    <div v-if="loading" class="mt-3 text-xs text-on-surface-variant">加载中...</div>
    <div v-else-if="models.length === 0" class="mt-3 text-xs text-on-surface-variant">尚未添加模型</div>
    <div v-else class="mt-3 space-y-2">
      <div
        v-for="model in models"
        :key="model.id"
        class="flex items-center gap-3 rounded-xl bg-surface-container px-4 py-2.5"
      >
        <span class="font-mono text-sm">{{ model.name }}</span>
        <span
          v-if="model.is_default"
          class="flex items-center gap-1 text-[10px] font-bold text-primary"
        >
          <span class="h-1.5 w-1.5 rounded-full bg-primary"></span>
          默认
        </span>

        <div class="ml-auto flex items-center gap-1">
          <button
            v-if="!model.is_default"
            type="button"
            class="p-1.5 rounded-lg hover:bg-surface-container-high text-on-surface-variant hover:text-primary transition-colors cursor-pointer"
            title="设为默认"
            @click="handleSetDefault(model.id)"
          >
            <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" /></svg>
          </button>
          <button
            type="button"
            class="p-1.5 rounded-lg hover:bg-surface-container-high text-on-surface-variant hover:text-tertiary-fixed-dim transition-colors cursor-pointer"
            title="测试连通性"
            :disabled="testStates.get(model.id)?.loading"
            @click="handleTestModel(model.id)"
          >
            <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" /><polyline points="22 4 12 14.01 9 11.01" /></svg>
          </button>
          <button
            type="button"
            class="p-1.5 rounded-lg hover:bg-surface-container-high text-on-surface-variant hover:text-danger transition-colors cursor-pointer"
            title="删除模型"
            @click="handleDeleteModel(model.id)"
          >
            <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6" /><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" /></svg>
          </button>
        </div>

        <!-- Inline test result -->
        <div
          v-if="testStates.get(model.id)?.result"
          class="w-full mt-1 rounded-lg bg-surface-container-low px-3 py-1.5 text-[11px]"
        >
          <div v-if="testStates.get(model.id).result.success" class="flex items-center gap-1.5">
            <span class="h-1.5 w-1.5 shrink-0 rounded-full bg-success"></span>
            <span class="font-semibold text-success">连接成功</span>
            <span v-if="testStates.get(model.id).result.latency_ms != null" class="font-mono text-on-surface-variant">
              {{ testStates.get(model.id).result.latency_ms }}ms
            </span>
          </div>
          <div v-else class="flex items-start gap-1.5">
            <span class="mt-0.5 h-1.5 w-1.5 shrink-0 rounded-full bg-danger"></span>
            <span class="text-danger">{{ testStates.get(model.id).result.message }}</span>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
