<script setup>
import { ref } from 'vue'

import { addProviderModelDraft, removeProviderModelDraft } from '../utils/providerModelDrafts'

const form = defineModel({ type: Object, required: true })

defineProps({
  isEdit: { type: Boolean, default: false },
  loading: { type: Boolean, default: false },
  error: { type: String, default: '' },
  testLoading: { type: Boolean, default: false },
  testResult: { type: Object, default: null },
})

defineEmits(['submit', 'test'])

const modelDraftName = ref('')
const modelDraftError = ref('')

function handleAddModelDraft() {
  const result = addProviderModelDraft(form.value.models ?? [], modelDraftName.value)
  form.value.models = result.models
  modelDraftError.value = result.error
  if (!result.error) {
    modelDraftName.value = ''
  }
}

function handleRemoveModelDraft(name) {
  form.value.models = removeProviderModelDraft(form.value.models ?? [], name)
  modelDraftError.value = ''
}
</script>

<template>
  <form class="space-y-4" @submit.prevent="$emit('submit')">
    <section class="rounded-2xl border border-outline-variant/20 bg-surface-container-lowest p-5 shadow-sm">
      <div class="mb-4">
        <p class="text-[10px] font-bold uppercase tracking-[0.24em] text-on-surface-variant">基础配置</p>
      </div>

      <div class="grid gap-4 md:grid-cols-2">
        <div class="md:col-span-2">
          <label class="block text-[10px] font-bold uppercase tracking-widest text-on-surface-variant">名称 *</label>
          <input
            v-model="form.name"
            class="mt-1.5 w-full rounded-xl border border-outline-variant/30 bg-surface-container px-4 py-2.5 text-sm transition-colors focus:border-primary focus:outline-none"
            placeholder="例如：OpenAI、Anthropic"
            required
          />
        </div>

        <div class="md:col-span-2">
          <label class="block text-[10px] font-bold uppercase tracking-widest text-on-surface-variant">API Key *</label>
          <input
            v-model="form.api_key"
            type="password"
            class="mt-1.5 w-full rounded-xl border border-outline-variant/30 bg-surface-container px-4 py-2.5 text-sm font-mono transition-colors focus:border-primary focus:outline-none"
            placeholder="sk-..."
            required
          />
        </div>
      </div>
    </section>

    <section class="rounded-2xl border border-outline-variant/20 bg-surface-container-lowest p-5 shadow-sm">
      <div class="mb-4">
        <p class="text-[10px] font-bold uppercase tracking-[0.24em] text-on-surface-variant">Endpoint</p>
      </div>

      <div>
        <label class="block text-[10px] font-bold uppercase tracking-widest text-on-surface-variant">Base URL</label>
        <input
          v-model="form.base_url"
          class="mt-1.5 w-full rounded-xl border border-outline-variant/30 bg-surface-container px-4 py-2.5 text-sm font-mono transition-colors focus:border-primary focus:outline-none"
          placeholder="https://api.openai.com/v1"
        />
      </div>
    </section>

    <section
      v-if="!isEdit"
      class="rounded-2xl border border-outline-variant/20 bg-surface-container-lowest p-5 shadow-sm"
    >
      <div class="mb-4">
        <p class="text-[10px] font-bold uppercase tracking-[0.24em] text-on-surface-variant">初始模型</p>
        <p class="mt-2 text-sm leading-relaxed text-on-surface-variant">
          创建时可直接添加一个或多个模型名称，首个模型会自动设为默认模型。
        </p>
      </div>

      <div class="flex flex-col gap-2 sm:flex-row">
        <input
          v-model="modelDraftName"
          class="flex-1 rounded-xl border border-outline-variant/30 bg-surface-container px-4 py-2.5 text-sm font-mono transition-colors focus:border-primary focus:outline-none"
          placeholder="gpt-4o、claude-3-7-sonnet"
          @keydown.enter.prevent="handleAddModelDraft"
        />
        <button
          type="button"
          class="rounded-xl border border-outline-variant/30 px-5 py-2.5 text-sm font-bold text-on-surface-variant transition-colors hover:bg-surface-container disabled:cursor-not-allowed disabled:opacity-50"
          :disabled="!modelDraftName.trim()"
          @click="handleAddModelDraft"
        >
          添加模型
        </button>
      </div>

      <p v-if="modelDraftError" class="mt-3 text-sm text-danger">{{ modelDraftError }}</p>

      <div v-if="form.models?.length" class="mt-4 flex flex-wrap gap-2">
        <span
          v-for="modelName in form.models"
          :key="modelName"
          class="inline-flex items-center gap-2 rounded-full bg-surface-container px-3 py-1.5 text-sm text-on-surface"
        >
          <span class="font-mono">{{ modelName }}</span>
          <button
            type="button"
            class="rounded-full px-1 text-xs text-on-surface-variant transition-colors hover:text-danger"
            @click="handleRemoveModelDraft(modelName)"
          >
            移除
          </button>
        </span>
      </div>
    </section>

    <section class="rounded-2xl border border-outline-variant/20 bg-surface-container-lowest p-5 shadow-sm">
      <div class="flex flex-col gap-3 md:flex-row md:items-start md:justify-between">
        <div>
          <p class="text-[10px] font-bold uppercase tracking-[0.24em] text-on-surface-variant">连接验证</p>
          <p class="mt-2 text-sm leading-relaxed text-on-surface-variant">在保存前验证 API Key 和 Base URL 是否可用。</p>
        </div>

        <button
          type="button"
          class="rounded-xl border border-outline-variant/30 px-5 py-2.5 text-sm font-bold text-on-surface-variant transition-colors hover:bg-surface-container disabled:cursor-not-allowed disabled:opacity-50"
          :disabled="testLoading || !form.api_key.trim()"
          @click="$emit('test')"
        >
          {{ testLoading ? '测试中...' : '测试连接' }}
        </button>
      </div>

      <div v-if="testResult" class="mt-4 rounded-xl bg-surface-container px-4 py-3 text-xs">
        <div v-if="testResult.success" class="flex items-center gap-2">
          <span class="h-2 w-2 shrink-0 rounded-full bg-success"></span>
          <span class="font-semibold text-success">连接成功</span>
          <span v-if="testResult.latency_ms != null" class="font-mono text-on-surface-variant">{{ testResult.latency_ms }}ms</span>
        </div>
        <div v-else class="flex items-start gap-2">
          <span class="mt-0.5 h-2 w-2 shrink-0 rounded-full bg-danger"></span>
          <span class="text-danger">{{ testResult.message }}</span>
        </div>
      </div>
    </section>

    <p v-if="error" class="text-sm text-danger">{{ error }}</p>

    <section class="flex flex-wrap items-center gap-3 rounded-2xl border border-outline-variant/20 bg-surface-container-lowest px-5 py-4 shadow-sm">
      <button
        type="submit"
        class="rounded-xl bg-primary px-6 py-2.5 text-sm font-bold text-on-primary transition-colors hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-60"
        :disabled="loading"
      >
        {{ isEdit ? '保存' : '创建' }}
      </button>
      <router-link
        to="/providers"
        class="rounded-xl px-5 py-2.5 text-sm font-medium text-on-surface-variant transition-colors hover:bg-surface-container"
      >
        返回列表
      </router-link>
    </section>
  </form>
</template>
