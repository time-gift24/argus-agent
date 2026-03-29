<template>
  <div class="max-w-7xl mx-auto">
    <!-- Page Header -->
    <div class="flex items-center justify-between mb-8 animate-fade-up">
      <div>
        <h1 class="text-3xl font-headline font-bold tracking-tight text-on-surface">
          MCP <span class="text-primary">服务</span>
        </h1>
        <p class="text-sm text-on-surface-variant mt-1">管理 MCP Server 连接配置</p>
      </div>
      <button
        v-if="userStore.isLoggedIn"
        class="flex items-center gap-2 px-4 py-2.5 bg-primary text-on-primary rounded-xl text-sm font-bold transition-colors hover:opacity-90 cursor-pointer"
        @click="openCreateDialog"
      >
        <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <line x1="12" y1="5" x2="12" y2="19"/>
          <line x1="5" y1="12" x2="19" y2="12"/>
        </svg>
        新增配置
      </button>
    </div>

    <!-- Not logged in -->
    <div v-if="!userStore.isLoggedIn" class="text-center py-20 animate-fade-up">
      <p class="text-on-surface-variant text-lg">请先登录以查看 MCP 配置</p>
    </div>

    <!-- Loading -->
    <div v-else-if="loading" class="text-center py-20 text-on-surface-variant">加载中...</div>

    <!-- Logged in content -->
    <template v-else>
      <!-- Global configs -->
      <div v-if="globalConfigs.length" class="mb-8 animate-fade-up animate-delay-1">
        <h2 class="text-sm font-bold tracking-widest uppercase text-on-surface-variant mb-4">全局配置</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
          <div
            v-for="c in globalConfigs"
            :key="c.id"
            class="bg-surface-container-lowest rounded-[2rem] p-6 shadow-sm border border-outline-variant/30 hover:shadow-xl transition-all duration-300 group"
          >
            <McpConfigCard
              :config="c"
              :testing="testingIds.has(c.id)"
              :test-result="testResults.get(c.id)"
              :tools="toolsCache.get(c.id)"
              :tools-loading="toolsLoadingIds.has(c.id)"
              @test="handleTest(c.id)"
              @tools="toggleTools(c.id)"
              @edit="openEditDialog(c)"
              @delete="confirmDelete(c)"
            />
          </div>
        </div>
      </div>

      <!-- User configs -->
      <div class="animate-fade-up animate-delay-2">
        <h2 class="text-sm font-bold tracking-widest uppercase text-on-surface-variant mb-4">我的配置</h2>
        <div v-if="userConfigs.length" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
          <div
            v-for="c in userConfigs"
            :key="c.id"
            class="bg-surface-container-lowest rounded-[2rem] p-6 shadow-sm border border-outline-variant/30 hover:shadow-xl transition-all duration-300 group"
          >
            <McpConfigCard
              :config="c"
              :testing="testingIds.has(c.id)"
              :test-result="testResults.get(c.id)"
              :tools="toolsCache.get(c.id)"
              :tools-loading="toolsLoadingIds.has(c.id)"
              @test="handleTest(c.id)"
              @tools="toggleTools(c.id)"
              @edit="openEditDialog(c)"
              @delete="confirmDelete(c)"
            />
          </div>
        </div>
        <div v-else-if="!globalConfigs.length" class="text-center py-12 text-on-surface-variant">
          <p class="text-sm">暂无 MCP 配置</p>
          <button class="text-primary text-sm font-semibold mt-2 inline-block hover:underline cursor-pointer" @click="openCreateDialog">添加第一个配置</button>
        </div>
      </div>
    </template>

    <!-- Create / Edit dialog -->
    <tiny-dialog-box
      v-model:visible="showFormDialog"
      append-to-body
      :title="isEditing ? '编辑配置' : '新增配置'"
      width="520px"
    >
      <div class="space-y-4 py-2">
        <div>
          <label class="text-[10px] font-bold tracking-widest uppercase text-on-surface-variant">名称 *</label>
          <input
            v-model="form.name"
            class="mt-1 w-full px-3 py-2 text-sm bg-surface-container rounded-lg border border-outline-variant/30 focus:border-primary focus:outline-none transition-colors"
            placeholder="配置名称"
          />
        </div>
        <div>
          <label class="text-[10px] font-bold tracking-widest uppercase text-on-surface-variant">描述</label>
          <input
            v-model="form.description"
            class="mt-1 w-full px-3 py-2 text-sm bg-surface-container rounded-lg border border-outline-variant/30 focus:border-primary focus:outline-none transition-colors"
            placeholder="可选描述"
          />
        </div>
        <div>
          <label class="text-[10px] font-bold tracking-widest uppercase text-on-surface-variant">传输类型</label>
          <select
            v-model="form.transport"
            :disabled="isEditing"
            class="mt-1 w-full px-3 py-2 text-sm bg-surface-container rounded-lg border border-outline-variant/30 focus:border-primary focus:outline-none transition-colors"
          >
            <option value="http">HTTP</option>
            <option value="sse">SSE</option>
            <option value="stdio" :disabled="!canManageStdio">STDIO（仅管理员）</option>
          </select>
          <p v-if="!canManageStdio" class="mt-1 text-xs text-on-surface-variant">STDIO 配置仅管理员可创建或修改。</p>
        </div>

        <!-- stdio fields -->
        <template v-if="form.transport === 'stdio'">
          <div>
            <label class="text-[10px] font-bold tracking-widest uppercase text-on-surface-variant">Command *</label>
            <input
              v-model="form.command"
              class="mt-1 w-full px-3 py-2 text-sm bg-surface-container rounded-lg border border-outline-variant/30 focus:border-primary focus:outline-none transition-colors font-mono"
              placeholder="e.g. npx -y @modelcontextprotocol/server-filesystem"
            />
          </div>
          <div>
            <label class="text-[10px] font-bold tracking-widest uppercase text-on-surface-variant">Args (JSON Array)</label>
            <textarea
              v-model="form.argsStr"
              class="mt-1 w-full px-3 py-2 text-sm bg-surface-container rounded-lg border border-outline-variant/30 focus:border-primary focus:outline-none transition-colors font-mono"
              rows="3"
              placeholder='["/path/to/dir", "--verbose"]'
            />
            <p class="mt-1 text-xs text-on-surface-variant">使用 JSON 数组可以保留包含空格的参数。</p>
          </div>
          <div>
            <label class="text-[10px] font-bold tracking-widest uppercase text-on-surface-variant">环境变量 (JSON)</label>
            <textarea
              v-model="form.envStr"
              class="mt-1 w-full px-3 py-2 text-sm bg-surface-container rounded-lg border border-outline-variant/30 focus:border-primary focus:outline-none transition-colors font-mono"
              rows="3"
              placeholder='{"KEY": "value"}'
            />
            <p class="mt-1 text-xs text-on-surface-variant">编辑已有配置时，留空表示保持现有环境变量。</p>
          </div>
        </template>

        <!-- http/sse fields -->
        <template v-if="form.transport === 'http' || form.transport === 'sse'">
          <div>
            <label class="text-[10px] font-bold tracking-widest uppercase text-on-surface-variant">URL *</label>
            <input
              v-model="form.url"
              class="mt-1 w-full px-3 py-2 text-sm bg-surface-container rounded-lg border border-outline-variant/30 focus:border-primary focus:outline-none transition-colors font-mono"
              placeholder="https://example.com/mcp"
            />
          </div>
          <div>
            <label class="text-[10px] font-bold tracking-widest uppercase text-on-surface-variant">Headers (JSON)</label>
            <textarea
              v-model="form.headersStr"
              class="mt-1 w-full px-3 py-2 text-sm bg-surface-container rounded-lg border border-outline-variant/30 focus:border-primary focus:outline-none transition-colors font-mono"
              rows="3"
              placeholder='{"Authorization": "Bearer xxx"}'
            />
            <p class="mt-1 text-xs text-on-surface-variant">编辑已有配置时，留空表示保持现有请求头。</p>
          </div>
        </template>

        <p v-if="formError" class="text-xs text-danger">{{ formError }}</p>

        <div v-if="!isEditing && formTestResult" class="px-4 py-2.5 rounded-xl bg-surface-container text-xs">
          <div v-if="formTestResult.success" class="flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-success shrink-0"></span>
            <span class="text-success font-semibold">连接成功</span>
            <span v-if="formTestResult.tools?.length" class="text-on-surface-variant">{{ formTestResult.tools.length }} 个工具</span>
          </div>
          <div v-else class="flex items-start gap-2">
            <span class="w-2 h-2 rounded-full bg-danger mt-0.5 shrink-0"></span>
            <span class="text-danger">{{ formTestResult.message }}</span>
          </div>
        </div>
      </div>
      <template #footer>
        <tiny-button @click="showFormDialog = false">取消</tiny-button>
        <tiny-button v-if="!isEditing" :loading="formTestLoading" @click="handleTestConfig">测试连接</tiny-button>
        <tiny-button type="primary" :loading="formLoading" @click="handleSubmit">{{ isEditing ? '保存' : '创建' }}</tiny-button>
      </template>
    </tiny-dialog-box>

    <!-- Delete confirmation dialog -->
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
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch } from 'vue'
import { useUserStore } from '../stores/user'
import { Button as TinyButton, DialogBox as TinyDialogBox } from '@opentiny/vue'
import client, { getApiErrorMessage } from '../api/client'
import McpConfigCard from '../components/McpConfigCard.vue'
import { buildMcpConfigPayload, formatArgsForEditor } from '../utils/mcpConfigForm'

const userStore = useUserStore()
const canManageStdio = computed(() => userStore.isAdmin)

// Config list state
const configs = ref([])
const loading = ref(false)

const globalConfigs = computed(() => configs.value.filter(c => c.kind === 'global'))
const userConfigs = computed(() => configs.value.filter(c => c.kind === 'user'))

async function fetchConfigs() {
  loading.value = true
  try {
    const { data } = await client.get('/mcp-configs')
    configs.value = data
    pruneTransientState()
  } finally {
    loading.value = false
  }
}

function setConfigTools(id, tools) {
  const config = configs.value.find(item => item.id === id)
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
  const validIds = new Set(configs.value.map(config => config.id))

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

// Test connection
const testResults = reactive(new Map())
const testingIds = reactive(new Set())

async function handleTest(id) {
  testingIds.add(id)
  testResults.delete(id)
  try {
    const { data } = await client.post(`/mcp-configs/${id}/test`)
    testResults.set(id, data)
    setConfigTools(id, data.tools || [])
    if (toolsCache.has(id)) {
      toolsCache.set(id, data.tools || [])
    }
  } catch (e) {
    clearConfigState(id)
    testResults.set(id, { success: false, message: e.response?.data?.detail || '连接测试失败' })
  } finally {
    testingIds.delete(id)
  }
}

// Tools cache
const toolsCache = reactive(new Map())
const toolsLoadingIds = reactive(new Set())

async function fetchTools(id) {
  toolsLoadingIds.add(id)
  try {
    const { data } = await client.get(`/mcp-configs/${id}/tools`)
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

// Create / Edit form
const showFormDialog = ref(false)
const isEditing = ref(false)
const editingId = ref(null)
const formLoading = ref(false)
const formTestLoading = ref(false)
const formError = ref('')
const formTestResult = ref(null)
const form = reactive({
  name: '',
  description: '',
  transport: 'http',
  command: '',
  argsStr: '',
  envStr: '',
  url: '',
  headersStr: '',
})

function resetForm() {
  form.name = ''
  form.description = ''
  form.transport = 'http'
  form.command = ''
  form.argsStr = ''
  form.envStr = ''
  form.url = ''
  form.headersStr = ''
  formError.value = ''
  formTestResult.value = null
}

function openCreateDialog() {
  resetForm()
  isEditing.value = false
  editingId.value = null
  showFormDialog.value = true
}

function openEditDialog(config) {
  resetForm()
  isEditing.value = true
  editingId.value = config.id
  form.name = config.name
  form.description = config.description || ''
  form.transport = config.transport
  form.command = config.command || ''
  form.argsStr = formatArgsForEditor(config.args)
  form.envStr = ''
  form.url = config.url || ''
  form.headersStr = ''
  showFormDialog.value = true
}

async function handleSubmit() {
  formError.value = ''
  let payload
  try {
    payload = buildMcpConfigPayload(form)
  } catch (e) {
    formError.value = e.message
    return
  }
  formLoading.value = true
  try {
    if (isEditing.value) {
      await client.patch(`/mcp-configs/${editingId.value}`, payload)
      clearConfigState(editingId.value)
    } else {
      await client.post('/mcp-configs', payload)
    }
    showFormDialog.value = false
    await fetchConfigs()
  } catch (e) {
    formError.value = e.response?.data?.detail || '操作失败'
  } finally {
    formLoading.value = false
  }
}

async function handleTestConfig() {
  formError.value = ''
  formTestResult.value = null

  let payload
  try {
    payload = buildMcpConfigPayload(form)
  } catch (e) {
    formError.value = e.message
    return
  }

  formTestLoading.value = true
  try {
    const { data } = await client.post('/mcp-configs/test-config', payload)
    formTestResult.value = data
  } catch (e) {
    formTestResult.value = {
      success: false,
      message: getApiErrorMessage(e, '连接测试失败'),
    }
  } finally {
    formTestLoading.value = false
  }
}

// Delete
const showDeleteDialog = ref(false)
const deleteTarget = ref(null)
const deleteLoading = ref(false)

function confirmDelete(config) {
  deleteTarget.value = config
  showDeleteDialog.value = true
}

async function handleDelete() {
  deleteLoading.value = true
  try {
    await client.delete(`/mcp-configs/${deleteTarget.value.id}`)
    clearConfigState(deleteTarget.value.id)
    showDeleteDialog.value = false
    await fetchConfigs()
  } finally {
    deleteLoading.value = false
  }
}

// Fetch on login
watch(() => userStore.isLoggedIn, (val) => {
  if (val) fetchConfigs()
}, { immediate: true })
</script>
