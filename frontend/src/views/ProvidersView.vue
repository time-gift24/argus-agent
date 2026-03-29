<template>
  <PageBodyShell
    :breadcrumbs="['LLM 提供商']"
    description="管理大语言模型供应商及其配置"
    title="LLM 提供商"
  >
    <template #actions>
      <router-link
        v-if="userStore.isLoggedIn"
        to="/providers/new"
        class="flex items-center gap-2 px-4 py-2.5 bg-primary text-on-primary rounded-xl text-sm font-bold transition-colors hover:opacity-90"
      >
        <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <line x1="12" y1="5" x2="12" y2="19"/>
          <line x1="5" y1="12" x2="19" y2="12"/>
        </svg>
        新增提供商
      </router-link>
    </template>

    <!-- Not logged in -->
    <div v-if="!userStore.isLoggedIn" class="text-center py-20 animate-fade-up">
      <p class="text-on-surface-variant text-lg">请先登录以查看提供商配置</p>
    </div>

    <!-- Logged in content -->
    <template v-else>
      <!-- Internal Providers -->
      <div v-if="providersStore.internalProviders.length" class="mb-8 animate-fade-up animate-delay-1">
        <h2 class="text-sm font-bold tracking-widest uppercase text-on-surface-variant mb-4">内置提供商</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
          <div
            v-for="p in providersStore.internalProviders"
            :key="p.id"
            class="bg-surface-container-lowest rounded-[2rem] p-6 shadow-sm border border-outline-variant/30"
          >
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 rounded-xl bg-primary-fixed flex items-center justify-center">
                <svg class="w-5 h-5 text-primary" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="2" y="2" width="20" height="8" rx="2" ry="2"/>
                  <rect x="2" y="14" width="20" height="8" rx="2" ry="2"/>
                  <line x1="6" y1="6" x2="6.01" y2="6"/>
                  <line x1="6" y1="18" x2="6.01" y2="18"/>
                </svg>
              </div>
              <div>
                <h3 class="font-headline font-bold text-sm text-on-surface">{{ p.name }}</h3>
                <span class="text-[10px] font-bold tracking-widest uppercase text-on-surface-variant">系统内置</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- User Providers -->
      <div class="animate-fade-up animate-delay-2">
        <h2 class="text-sm font-bold tracking-widest uppercase text-on-surface-variant mb-4">我的提供商</h2>
        <div v-if="providersStore.userProviders.length" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
          <div
            v-for="p in providersStore.userProviders"
            :key="p.id"
            class="bg-surface-container-lowest rounded-[2rem] p-6 shadow-sm border border-outline-variant/30 hover:shadow-xl transition-all duration-300 group"
          >
            <!-- Card header -->
            <div class="flex items-start justify-between mb-4">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-xl bg-primary-fixed flex items-center justify-center">
                  <svg class="w-5 h-5 text-primary" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="2" y="2" width="20" height="8" rx="2" ry="2"/>
                    <rect x="2" y="14" width="20" height="8" rx="2" ry="2"/>
                    <line x1="6" y1="6" x2="6.01" y2="6"/>
                    <line x1="6" y1="18" x2="6.01" y2="18"/>
                  </svg>
                </div>
                <div>
                  <h3 class="font-headline font-bold text-sm text-on-surface">{{ p.name }}</h3>
                  <div class="flex items-center gap-2 mt-0.5">
                    <span v-if="p.is_default" class="text-[10px] font-bold text-primary">★ 默认</span>
                    <span class="text-[10px] text-on-surface-variant font-mono">{{ p.model_count || 0 }} models</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Config info -->
            <div class="space-y-1.5 mb-4 text-xs text-on-surface-variant">
              <div v-if="p.default_model_name" class="flex items-center gap-1.5">
                <span class="text-[10px] font-bold tracking-widest uppercase">默认模型</span>
                <span class="font-mono">{{ p.default_model_name }}</span>
              </div>
              <div class="flex items-center gap-1.5">
                <span class="text-[10px] font-bold tracking-widest uppercase">模型数</span>
                <span class="font-mono">{{ p.model_count || 0 }}</span>
              </div>
              <div v-if="!p.default_model_name" class="text-[11px] leading-relaxed text-on-surface-variant">
                尚未设置默认模型，请先进入编辑页添加模型并设置默认值。
              </div>
            </div>

            <!-- Inline test result -->
            <div v-if="testResults.has(p.id)" class="mb-3 px-3 py-2 rounded-xl bg-surface-container text-xs">
              <div v-if="testResults.get(p.id).success" class="flex items-center gap-2">
                <span class="w-2 h-2 rounded-full bg-success shrink-0"></span>
                <span class="text-success font-semibold">连接成功</span>
                <span v-if="p.default_model_name" class="text-on-surface-variant font-mono">({{ p.default_model_name }})</span>
                <span v-if="testResults.get(p.id).latency_ms != null" class="text-on-surface-variant font-mono">{{ testResults.get(p.id).latency_ms }}ms</span>
              </div>
              <div v-else class="flex items-start gap-2">
                <span class="w-2 h-2 rounded-full bg-danger mt-0.5 shrink-0"></span>
                <span class="text-danger">
                  <template v-if="p.default_model_name">默认模型 {{ p.default_model_name }}：</template>{{ testResults.get(p.id).message }}
                </span>
              </div>
            </div>

            <!-- Actions -->
            <div class="flex items-center gap-2 pt-3 border-t border-outline-variant/10">
              <button
                v-if="!p.is_default"
                class="px-3 py-1.5 text-[10px] font-bold tracking-widest uppercase text-on-surface-variant hover:text-primary rounded-lg hover:bg-surface-container transition-colors cursor-pointer"
                @click="handleSetDefault(p.id)"
              >
                设为默认
              </button>
              <router-link
                :to="`/providers/${p.id}/edit`"
                class="px-3 py-1.5 text-[10px] font-bold tracking-widest uppercase text-on-surface-variant hover:text-primary rounded-lg hover:bg-surface-container transition-colors"
              >
                编辑
              </router-link>
              <button
                class="px-3 py-1.5 text-[10px] font-bold tracking-widest uppercase text-on-surface-variant hover:text-tertiary-fixed-dim rounded-lg hover:bg-surface-container transition-colors cursor-pointer disabled:opacity-50 disabled:cursor-wait"
                :disabled="testingIds.has(p.id) || !p.default_model_name"
                @click="handleTest(p)"
              >
                <template v-if="testingIds.has(p.id)">测试中...</template>
                <template v-else>{{ p.default_model_name ? '测试默认模型' : '先配置模型' }}</template>
              </button>
              <button
                class="px-3 py-1.5 text-[10px] font-bold tracking-widest uppercase text-on-surface-variant hover:text-danger rounded-lg hover:bg-surface-container transition-colors cursor-pointer ml-auto"
                @click="confirmDelete(p)"
              >
                删除
              </button>
            </div>
          </div>
        </div>
        <div v-else class="text-center py-12 text-on-surface-variant">
          <p class="text-sm">暂无自定义提供商</p>
          <router-link to="/providers/new" class="text-primary text-sm font-semibold mt-2 inline-block hover:underline">添加第一个提供商</router-link>
        </div>
      </div>
    </template>

    <!-- Delete confirmation dialog -->
    <tiny-dialog-box
      v-model:visible="showDeleteDialog"
      append-to-body
      title="确认删除"
      width="400px"
    >
      <p class="text-sm text-on-surface-variant">确定要删除提供商「{{ deleteTarget?.name }}」吗？此操作不可撤销。</p>
      <template #footer>
        <tiny-button @click="showDeleteDialog = false">取消</tiny-button>
        <tiny-button type="danger" :loading="deleteLoading" @click="handleDelete">删除</tiny-button>
      </template>
    </tiny-dialog-box>
  </PageBodyShell>
</template>

<script setup>
import { ref, reactive, watch } from 'vue'
import { useUserStore } from '../stores/user'
import { useProvidersStore } from '../stores/providers'
import { Button as TinyButton, DialogBox as TinyDialogBox } from '@opentiny/vue'
import PageBodyShell from '../components/PageBodyShell.vue'
import client, { getApiErrorMessage } from '../api/client'

const userStore = useUserStore()
const providersStore = useProvidersStore()

// Delete
const showDeleteDialog = ref(false)
const deleteTarget = ref(null)
const deleteLoading = ref(false)

function confirmDelete(provider) {
  deleteTarget.value = provider
  showDeleteDialog.value = true
}

async function handleDelete() {
  deleteLoading.value = true
  try {
    await providersStore.deleteProvider(deleteTarget.value.id)
    testResults.delete(deleteTarget.value.id)
    showDeleteDialog.value = false
  } finally {
    deleteLoading.value = false
  }
}

async function handleSetDefault(id) {
  await providersStore.setDefaultProvider(id)
}

// Test (inline per-card)
const testResults = reactive(new Map()) // provider.id -> { success, message, latency_ms }
const testingIds = reactive(new Set()) // provider.id set while loading

async function handleTest(provider) {
  testingIds.add(provider.id)
  testResults.delete(provider.id)
  try {
    const { data } = await client.post(`/providers/${provider.id}/test`)
    testResults.set(provider.id, data)
  } catch (e) {
    testResults.set(provider.id, { success: false, message: getApiErrorMessage(e, '连接测试失败') })
  } finally {
    testingIds.delete(provider.id)
  }
}

// Fetch providers when logged in
watch(() => userStore.isLoggedIn, (val) => {
  if (val) providersStore.fetchProviders()
}, { immediate: true })
</script>
