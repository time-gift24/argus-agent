<template>
  <PageBodyShell
    :breadcrumbs="breadcrumbs"
    :description="pageDescription"
    :title="pageTitle"
    width-class="max-w-5xl"
  >
    <ProviderConfigForm
      v-model="form"
      :error="error"
      :is-edit="isEdit"
      :loading="loading"
      :test-loading="testLoading"
      :test-result="testResult"
      @submit="handleSubmit"
      @test="handleTestConfig"
    />

    <ProviderModelList
      v-if="isEdit && providerId"
      :provider-id="providerId"
    />
  </PageBodyShell>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import * as api from '../api/providers'
import client, { getApiErrorMessage } from '../api/client'
import PageBodyShell from '../components/PageBodyShell.vue'
import ProviderConfigForm from '../components/ProviderConfigForm.vue'
import ProviderModelList from '../components/ProviderModelList.vue'
import { buildProviderPayload } from '../utils/providerModelDrafts'
import { breadcrumb } from '../utils/pageShell'

const route = useRoute()
const router = useRouter()

const isEdit = computed(() => route.name === 'provider-edit')
const providerId = computed(() => route.params.id)
const form = ref({
  name: '',
  api_key: '',
  base_url: '',
  models: [],
})
const pageTitle = computed(() => (isEdit.value ? '编辑提供商' : '新增提供商'))
const pageDescription = computed(() => (
  isEdit.value
    ? '调整当前 Provider 的名称、凭据和连接参数，并在保存前完成连接验证。'
    : '创建新的 LLM Provider，并可同时添加初始模型。'
))
const breadcrumbs = computed(() => [
  breadcrumb('LLM 提供商', '/providers'),
  breadcrumb(isEdit.value ? `编辑 - ${form.value.name || '...'}` : '新增提供商'),
])

const loading = ref(false)
const error = ref('')

// Test config
const testLoading = ref(false)
const testResult = ref(null)

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
      model: null,
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
        models: [],
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

  const payload = buildProviderPayload(form.value, { includeModels: !providerId.value })

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
