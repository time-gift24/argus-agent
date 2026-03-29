<template>
  <div class="max-w-7xl mx-auto">
    <!-- Page Header -->
    <div class="flex items-center justify-between mb-8 animate-fade-up">
      <div>
        <h1 class="text-3xl font-headline font-bold tracking-tight text-on-surface">
          工具 <span class="text-primary">库</span>
        </h1>
        <p class="text-sm text-on-surface-variant mt-1">智能体可用的模块化能力</p>
      </div>
    </div>

    <div
      v-if="!userStore.isLoggedIn"
      class="mb-8 rounded-[2rem] border border-outline-variant/30 bg-surface-container-low px-6 py-4 text-sm text-on-surface-variant animate-fade-up animate-delay-1"
    >
      当前可浏览全部工具，登录后可新增或删除自定义工具。
    </div>

    <!-- Loading -->
    <div v-if="toolsStore.loading" class="text-center py-12 text-on-surface-variant text-sm">加载中...</div>

    <template v-else>
      <div v-if="!hasTools" class="text-center py-12 text-on-surface-variant">
        <p class="text-sm">暂无工具</p>
      </div>

      <!-- Builtin Tools -->
      <div v-if="toolsStore.builtinTools.length" class="mb-8 animate-fade-up animate-delay-1">
        <h2 class="text-sm font-bold tracking-widest uppercase text-on-surface-variant mb-4">内置工具</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
          <div
            v-for="tool in toolsStore.builtinTools"
            :key="tool.id"
            class="bg-surface-container-lowest rounded-[2rem] p-6 shadow-sm border border-outline-variant/30"
          >
            <div class="flex items-center gap-3 mb-3">
              <div class="w-10 h-10 rounded-xl bg-primary-fixed flex items-center justify-center">
                <svg class="w-5 h-5 text-primary" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>
                </svg>
              </div>
              <div>
                <h3 class="font-headline font-bold text-sm text-on-surface">{{ tool.name }}</h3>
                <span class="text-[10px] font-bold tracking-widest uppercase text-primary">BUILTIN</span>
              </div>
            </div>
            <p class="text-xs text-on-surface-variant leading-relaxed">{{ tool.description }}</p>
          </div>
        </div>
      </div>

      <!-- Custom Tools -->
      <div v-if="userStore.isLoggedIn || toolsStore.customTools.length" class="animate-fade-up animate-delay-2">
        <h2 class="text-sm font-bold tracking-widest uppercase text-on-surface-variant mb-4">自定义工具</h2>
        <div v-if="toolsStore.customTools.length" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
          <div
            v-for="tool in toolsStore.customTools"
            :key="tool.id"
            class="bg-surface-container-lowest rounded-[2rem] p-6 shadow-sm border border-outline-variant/30 hover:shadow-xl transition-all duration-300 group"
          >
            <div class="flex items-center gap-3 mb-3">
              <div class="w-10 h-10 rounded-xl bg-tertiary-fixed flex items-center justify-center">
                <svg class="w-5 h-5 text-tertiary" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
                </svg>
              </div>
              <div>
                <h3 class="font-headline font-bold text-sm text-on-surface">{{ tool.name }}</h3>
                <span class="text-[10px] font-bold tracking-widest uppercase text-tertiary-fixed-dim">CUSTOM</span>
              </div>
            </div>
            <p class="text-xs text-on-surface-variant leading-relaxed">{{ tool.description }}</p>
            <div class="flex items-center gap-2 pt-3 mt-4 border-t border-outline-variant/10">
              <button
                v-if="userStore.isLoggedIn"
                class="px-3 py-1.5 text-[10px] font-bold tracking-widest uppercase text-on-surface-variant hover:text-danger rounded-lg hover:bg-surface-container transition-colors cursor-pointer ml-auto"
                @click="confirmDelete(tool)"
              >
                删除
              </button>
            </div>
          </div>
        </div>
        <div v-else class="text-center py-12 text-on-surface-variant">
          <p class="text-sm">暂无自定义工具</p>
        </div>
      </div>
    </template>

    <!-- Delete Dialog -->
    <tiny-dialog-box v-model:visible="showDeleteDialog" append-to-body title="确认删除" width="400px">
      <p class="text-sm text-on-surface-variant">确定要删除工具「{{ deleteTarget?.name }}」吗？此操作不可撤销。</p>
      <template #footer>
        <tiny-button @click="showDeleteDialog = false">取消</tiny-button>
        <tiny-button type="danger" :loading="deleteLoading" @click="handleDelete">删除</tiny-button>
      </template>
    </tiny-dialog-box>
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { useUserStore } from '../stores/user'
import { useToolsStore } from '../stores/tools'
import { Button as TinyButton, DialogBox as TinyDialogBox } from '@opentiny/vue'

const userStore = useUserStore()
const toolsStore = useToolsStore()
const hasTools = computed(() => toolsStore.builtinTools.length + toolsStore.customTools.length > 0)

// Keep the public tool catalog fresh on initial load and auth changes.
watch(() => userStore.isLoggedIn, () => {
  toolsStore.fetchTools()
}, { immediate: true })

// Delete
const showDeleteDialog = ref(false)
const deleteTarget = ref(null)
const deleteLoading = ref(false)

function confirmDelete(tool) {
  deleteTarget.value = tool
  showDeleteDialog.value = true
}

async function handleDelete() {
  deleteLoading.value = true
  try {
    await toolsStore.deleteTool(deleteTarget.value.id)
    showDeleteDialog.value = false
  } finally {
    deleteLoading.value = false
  }
}
</script>
