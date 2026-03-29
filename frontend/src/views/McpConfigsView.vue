<script setup>
import { computed, reactive, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { Button as TinyButton, DialogBox as TinyDialogBox } from '@opentiny/vue'
import { getApiErrorMessage } from '../api/client'
import * as api from '../api/mcpConfigs'
import PageBodyShell from '../components/PageBodyShell.vue'
import McpConfigCard from '../components/McpConfigCard.vue'
import { useUserStore } from '../stores/user'

const router = useRouter()
const userStore = useUserStore()

const configs = ref([])
const loading = ref(false)
const globalConfigs = computed(() => configs.value.filter((config) => config.kind === 'global'))
const userConfigs = computed(() => configs.value.filter((config) => config.kind === 'user'))

const testResults = reactive(new Map())
const testingIds = reactive(new Set())
const toolsCache = reactive(new Map())
const toolsLoadingIds = reactive(new Set())

const showDeleteDialog = ref(false)
const deleteTarget = ref(null)
const deleteLoading = ref(false)

function setConfigTools(id, tools) {
  const config = configs.value.find((item) => item.id === id)
  if (config) {
    config.tools = tools
  }
}

function clearConfigState(id) {
  testResults.delete(id)
  toolsCache.delete(id)
  testingIds.delete(id)
  toolsLoadingIds.delete(id)
  setConfigTools(id, undefined)
}

function pruneTransientState() {
  const validIds = new Set(configs.value.map((config) => config.id))

  for (const id of [...testResults.keys()]) {
    if (!validIds.has(id)) testResults.delete(id)
  }
  for (const id of [...toolsCache.keys()]) {
    if (!validIds.has(id)) toolsCache.delete(id)
  }
  for (const id of [...testingIds]) {
    if (!validIds.has(id)) testingIds.delete(id)
  }
  for (const id of [...toolsLoadingIds]) {
    if (!validIds.has(id)) toolsLoadingIds.delete(id)
  }
}

async function fetchConfigs() {
  loading.value = true
  try {
    const { data } = await api.list()
    configs.value = data
    pruneTransientState()
  } finally {
    loading.value = false
  }
}

async function handleTest(id) {
  testingIds.add(id)
  testResults.delete(id)

  try {
    const { data } = await api.testSaved(id)
    testResults.set(id, data)
    setConfigTools(id, data.tools || [])
    if (toolsCache.has(id)) {
      toolsCache.set(id, data.tools || [])
    }
  } catch (error) {
    clearConfigState(id)
    testResults.set(id, {
      success: false,
      message: getApiErrorMessage(error, '连接测试失败'),
    })
  } finally {
    testingIds.delete(id)
  }
}

async function fetchTools(id) {
  toolsLoadingIds.add(id)
  try {
    const { data } = await api.getTools(id)
    toolsCache.set(id, data)
    setConfigTools(id, data)
  } catch {
    toolsCache.set(id, [])
    setConfigTools(id, [])
  } finally {
    toolsLoadingIds.delete(id)
  }
}

function toggleTools(id) {
  if (toolsLoadingIds.has(id)) return
  if (toolsCache.has(id)) {
    toolsCache.delete(id)
    return
  }
  fetchTools(id)
}

function openEditPage(id) {
  router.push(`/mcp/${id}/edit`)
}

function confirmDelete(config) {
  deleteTarget.value = config
  showDeleteDialog.value = true
}

async function handleDelete() {
  deleteLoading.value = true
  try {
    await api.remove(deleteTarget.value.id)
    clearConfigState(deleteTarget.value.id)
    showDeleteDialog.value = false
    await fetchConfigs()
  } finally {
    deleteLoading.value = false
  }
}

watch(
  () => userStore.isLoggedIn,
  (isLoggedIn) => {
    if (isLoggedIn) {
      fetchConfigs()
      return
    }

    configs.value = []
    pruneTransientState()
  },
  { immediate: true }
)
</script>

<template>
  <PageBodyShell
    :breadcrumbs="['MCP 服务']"
    description="管理 MCP Server 连接配置"
    title="MCP 服务"
  >
    <template #actions>
      <router-link
        v-if="userStore.isLoggedIn"
        to="/mcp/new"
        class="flex items-center gap-2 rounded-xl bg-primary px-4 py-2.5 text-sm font-bold text-on-primary transition-colors hover:opacity-90"
      >
        <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <line x1="12" y1="5" x2="12" y2="19" />
          <line x1="5" y1="12" x2="19" y2="12" />
        </svg>
        新增配置
      </router-link>
    </template>

    <div v-if="!userStore.isLoggedIn" class="py-20 text-center animate-fade-up">
      <p class="text-lg text-on-surface-variant">请先登录以查看 MCP 配置</p>
    </div>

    <div v-else-if="loading" class="py-20 text-center text-on-surface-variant">加载中...</div>

    <template v-else>
      <div v-if="globalConfigs.length" class="mb-8 animate-fade-up animate-delay-1">
        <h2 class="mb-4 text-sm font-bold uppercase tracking-widest text-on-surface-variant">全局配置</h2>
        <div class="grid grid-cols-1 gap-6 md:grid-cols-2 xl:grid-cols-3">
          <div
            v-for="config in globalConfigs"
            :key="config.id"
            class="rounded-[2rem] border border-outline-variant/30 bg-surface-container-lowest p-6 shadow-sm transition-all duration-300 hover:shadow-xl"
          >
            <McpConfigCard
              :config="config"
              :test-result="testResults.get(config.id)"
              :testing="testingIds.has(config.id)"
              :tools="toolsCache.get(config.id)"
              :tools-loading="toolsLoadingIds.has(config.id)"
              @delete="confirmDelete(config)"
              @edit="openEditPage(config.id)"
              @test="handleTest(config.id)"
              @tools="toggleTools(config.id)"
            />
          </div>
        </div>
      </div>

      <div class="animate-fade-up animate-delay-2">
        <h2 class="mb-4 text-sm font-bold uppercase tracking-widest text-on-surface-variant">我的配置</h2>

        <div v-if="userConfigs.length" class="grid grid-cols-1 gap-6 md:grid-cols-2 xl:grid-cols-3">
          <div
            v-for="config in userConfigs"
            :key="config.id"
            class="rounded-[2rem] border border-outline-variant/30 bg-surface-container-lowest p-6 shadow-sm transition-all duration-300 hover:shadow-xl"
          >
            <McpConfigCard
              :config="config"
              :test-result="testResults.get(config.id)"
              :testing="testingIds.has(config.id)"
              :tools="toolsCache.get(config.id)"
              :tools-loading="toolsLoadingIds.has(config.id)"
              @delete="confirmDelete(config)"
              @edit="openEditPage(config.id)"
              @test="handleTest(config.id)"
              @tools="toggleTools(config.id)"
            />
          </div>
        </div>

        <div v-else-if="!globalConfigs.length" class="py-12 text-center text-on-surface-variant">
          <p class="text-sm">暂无 MCP 配置</p>
          <router-link to="/mcp/new" class="mt-2 inline-block text-sm font-semibold text-primary hover:underline">
            添加第一个配置
          </router-link>
        </div>
      </div>
    </template>

    <tiny-dialog-box
      v-model:visible="showDeleteDialog"
      append-to-body
      title="确认删除"
      width="400px"
    >
      <p class="text-sm text-on-surface-variant">确定要删除配置「{{ deleteTarget?.name }}」吗？此操作不可撤销。</p>
      <template #footer>
        <tiny-button @click="showDeleteDialog = false">取消</tiny-button>
        <tiny-button type="danger" :loading="deleteLoading" @click="handleDelete">删除</tiny-button>
      </template>
    </tiny-dialog-box>
  </PageBodyShell>
</template>
