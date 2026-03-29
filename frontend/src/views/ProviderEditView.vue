<template>
  <div class="max-w-3xl mx-auto">
    <!-- Breadcrumb -->
    <nav class="flex items-center gap-2 text-sm mb-8 animate-fade-up">
      <router-link to="/providers" class="text-on-surface-variant hover:text-primary transition-colors">LLM 提供商</router-link>
      <svg class="w-3.5 h-3.5 text-on-surface-variant" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="9 18 15 12 9 6"/>
      </svg>
      <span class="text-on-surface font-semibold">{{ isEdit ? `编辑 - ${form.name || '...'}` : '新增提供商' }}</span>
    </nav>

    <!-- Form Card -->
    <div class="bg-surface-container-lowest rounded-[2rem] p-8 shadow-sm border border-outline-variant/30 animate-fade-up animate-delay-1">
      <h2 class="text-xl font-headline font-bold tracking-tight text-on-surface mb-6">
        {{ isEdit ? '编辑提供商' : '新增提供商' }}
      </h2>

      <form @submit.prevent="handleSubmit" class="space-y-6">
        <!-- Name -->
        <div>
          <label class="text-[10px] font-bold tracking-widest uppercase text-on-surface-variant block mb-1.5">名称 *</label>
          <input
            v-model="form.name"
            class="w-full px-4 py-2.5 text-sm bg-surface-container rounded-xl border border-outline-variant/30 focus:border-primary focus:outline-none transition-colors"
            placeholder="例如：OpenAI、Anthropic"
            required
          />
        </div>

        <!-- API Key -->
        <div>
          <label class="text-[10px] font-bold tracking-widest uppercase text-on-surface-variant block mb-1.5">API Key *</label>
          <input
            v-model="form.api_key"
            type="password"
            class="w-full px-4 py-2.5 text-sm bg-surface-container rounded-xl border border-outline-variant/30 focus:border-primary focus:outline-none transition-colors font-mono"
            placeholder="sk-..."
            required
          />
        </div>

        <!-- Base URL -->
        <div>
          <label class="text-[10px] font-bold tracking-widest uppercase text-on-surface-variant block mb-1.5">Base URL</label>
          <input
            v-model="form.base_url"
            class="w-full px-4 py-2.5 text-sm bg-surface-container rounded-xl border border-outline-variant/30 focus:border-primary focus:outline-none transition-colors font-mono"
            placeholder="https://api.openai.com/v1"
          />
        </div>

        <!-- Model -->
        <div>
          <label class="text-[10px] font-bold tracking-widest uppercase text-on-surface-variant block mb-1.5">模型</label>
          <input
            v-model="form.model"
            class="w-full px-4 py-2.5 text-sm bg-surface-container rounded-xl border border-outline-variant/30 focus:border-primary focus:outline-none transition-colors font-mono"
            placeholder="gpt-4o、claude-3-sonnet"
          />
        </div>

        <!-- Error -->
        <p v-if="error" class="text-sm text-danger">{{ error }}</p>

        <!-- Test result -->
        <div v-if="testResult" class="px-4 py-2.5 rounded-xl bg-surface-container text-xs">
          <div v-if="testResult.success" class="flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-success shrink-0"></span>
            <span class="text-success font-semibold">连接成功</span>
            <span v-if="testResult.latency_ms != null" class="text-on-surface-variant font-mono">{{ testResult.latency_ms }}ms</span>
          </div>
          <div v-else class="flex items-start gap-2">
            <span class="w-2 h-2 rounded-full bg-danger mt-0.5 shrink-0"></span>
            <span class="text-danger">{{ testResult.message }}</span>
          </div>
        </div>

        <!-- Actions -->
        <div class="flex items-center gap-3 pt-4 border-t border-outline-variant/10">
          <button
            type="submit"
            class="px-6 py-2.5 bg-primary text-on-primary rounded-xl text-sm font-bold transition-colors hover:opacity-90 cursor-pointer"
            :disabled="loading"
          >
            {{ isEdit ? '保存' : '创建' }}
          </button>
          <button
            type="button"
            class="px-6 py-2.5 text-on-surface-variant rounded-xl text-sm font-bold border border-outline-variant/30 hover:bg-surface-container transition-colors cursor-pointer disabled:opacity-50"
            :disabled="testLoading || !form.api_key.trim()"
            @click="handleTestConfig"
          >
            {{ testLoading ? '测试中...' : '测试连接' }}
          </button>
          <router-link
            to="/providers"
            class="px-6 py-2.5 text-on-surface-variant rounded-xl text-sm font-medium hover:bg-surface-container transition-colors"
          >
            取消
          </router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import * as api from '../api/providers'
import client, { getApiErrorMessage } from '../api/client'

const route = useRoute()
const router = useRouter()

const isEdit = computed(() => route.name !== undefined ? route.path.includes('/edit') : !!route.params.id)
const providerId = computed(() => route.params.id)

const form = ref({
  name: '',
  api_key: '',
  base_url: '',
  model: '',
})

const loading = ref(false)
const error = ref('')

// Test config
const testLoading = ref(false)
const testResult = ref(null) // { success, message, latency_ms }

async function handleTestConfig() {
  if (!form.value.api_key.trim()) {
    testResult.value = { success: false, message: '请先填写 API Key' }
    return
  }
  testLoading.value = true
  testResult.value = null
  try {
    const { data } = await client.post('/providers/test-config', {
      api_key: form.value.api_key.trim(),
      base_url: form.value.base_url.trim() || null,
      model: form.value.model.trim() || null,
    })
    testResult.value = data
  } catch (e) {
    testResult.value = { success: false, message: getApiErrorMessage(e, '连接测试失败') }
  } finally {
    testLoading.value = false
  }
}

onMounted(async () => {
  if (providerId.value) {
    try {
      const { data } = await api.get(providerId.value)
      form.value = {
        name: data.name || '',
        api_key: data.config?.api_key || '',
        base_url: data.config?.base_url || '',
        model: data.config?.model || '',
      }
    } catch (e) {
      error.value = '加载提供商信息失败'
    }
  }
})

async function handleSubmit() {
  if (!form.value.name.trim() || !form.value.api_key.trim()) {
    error.value = '名称和 API Key 为必填项'
    return
  }

  loading.value = true
  error.value = ''

  const payload = {
    name: form.value.name.trim(),
    config: {
      api_key: form.value.api_key.trim(),
      base_url: form.value.base_url.trim() || null,
      model: form.value.model.trim() || null,
    }
  }

  try {
    if (providerId.value) {
      await api.update(providerId.value, payload)
    } else {
      await api.create(payload)
    }
    router.push('/providers')
  } catch (e) {
    error.value = getApiErrorMessage(e, '操作失败')
  } finally {
    loading.value = false
  }
}
</script>
