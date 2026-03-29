<script setup>
import { computed, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import { getApiErrorMessage } from '../api/client'
import * as api from '../api/mcpConfigs'
import PageBodyShell from '../components/PageBodyShell.vue'
import McpConfigForm from '../components/McpConfigForm.vue'
import { buildMcpConfigPayload } from '../utils/mcpConfigForm'
import {
  createEmptyMcpConfigForm,
  getMcpConfigPageMeta,
  populateMcpConfigForm,
} from '../utils/mcpConfigEditor'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const isEdit = computed(() => route.name === 'mcp-config-edit')
const editingId = computed(() => route.params.id)
const pageMeta = computed(() => getMcpConfigPageMeta({
  isEdit: isEdit.value,
  name: form.value.name,
}))

const form = ref(createEmptyMcpConfigForm())
const pageLoading = ref(false)
const submitLoading = ref(false)
const testLoading = ref(false)
const loadError = ref('')
const formError = ref('')
const testResult = ref(null)

function resetCreatePage() {
  form.value = createEmptyMcpConfigForm()
  loadError.value = ''
  formError.value = ''
  testResult.value = null
}

async function loadPage() {
  if (!isEdit.value) {
    resetCreatePage()
    return
  }

  pageLoading.value = true
  loadError.value = ''
  formError.value = ''
  testResult.value = null

  try {
    const { data } = await api.list()
    const config = data.find((item) => item.id === editingId.value)

    if (!config || config.kind !== 'user') {
      loadError.value = '未找到可编辑的 MCP 配置'
      return
    }

    form.value = populateMcpConfigForm(config)
  } catch (error) {
    loadError.value = getApiErrorMessage(error, '加载 MCP 配置失败')
  } finally {
    pageLoading.value = false
  }
}

async function handleSubmit() {
  formError.value = ''

  let payload
  try {
    payload = buildMcpConfigPayload(form.value)
  } catch (error) {
    formError.value = error.message
    return
  }

  submitLoading.value = true
  try {
    if (isEdit.value) {
      await api.update(editingId.value, payload)
    } else {
      await api.create(payload)
    }

    router.push('/mcp')
  } catch (error) {
    formError.value = getApiErrorMessage(error, '操作失败')
  } finally {
    submitLoading.value = false
  }
}

async function handleTestConfig() {
  formError.value = ''
  testResult.value = null

  let payload
  try {
    payload = buildMcpConfigPayload(form.value)
  } catch (error) {
    formError.value = error.message
    return
  }

  testLoading.value = true
  try {
    const { data } = await api.testConfig(payload)
    testResult.value = data
  } catch (error) {
    testResult.value = {
      success: false,
      message: getApiErrorMessage(error, '连接测试失败'),
    }
  } finally {
    testLoading.value = false
  }
}

watch(
  () => [route.name, route.params.id],
  () => {
    loadPage()
  },
  { immediate: true }
)

watch(
  form,
  () => {
    if (testResult.value) {
      testResult.value = null
    }
  },
  { deep: true }
)
</script>

<template>
  <PageBodyShell
    :breadcrumbs="pageMeta.breadcrumbs"
    :description="pageMeta.description"
    :title="pageMeta.title"
    width-class="max-w-5xl"
  >
    <div v-if="pageLoading" class="rounded-[2rem] border border-outline-variant/30 bg-surface-container-lowest px-6 py-12 text-center text-sm text-on-surface-variant shadow-sm">
      加载中...
    </div>

    <div v-else-if="loadError" class="rounded-[2rem] border border-danger/20 bg-danger/5 px-6 py-5 text-sm text-danger shadow-sm">
      {{ loadError }}
    </div>

    <McpConfigForm
      v-else
      v-model="form"
      :can-manage-stdio="userStore.isAdmin"
      :form-error="formError"
      :is-edit="isEdit"
      :loading="submitLoading"
      :test-loading="testLoading"
      :test-result="testResult"
      @submit="handleSubmit"
      @test="handleTestConfig"
    />
  </PageBodyShell>
</template>
