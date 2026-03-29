<script setup>
const form = defineModel({ type: Object, required: true })

defineProps({
  isEdit: { type: Boolean, default: false },
  loading: { type: Boolean, default: false },
  formError: { type: String, default: '' },
  canManageStdio: { type: Boolean, default: false },
  testLoading: { type: Boolean, default: false },
  testResult: { type: Object, default: null },
})

defineEmits(['submit', 'test'])
</script>

<template>
  <form class="space-y-4" @submit.prevent="$emit('submit')">
    <section class="rounded-2xl border border-outline-variant/20 bg-surface-container-lowest p-5 shadow-sm">
      <div class="mb-4">
        <p class="text-[10px] font-bold uppercase tracking-[0.24em] text-on-surface-variant">基础信息</p>
      </div>

      <div class="grid gap-4 md:grid-cols-2">
        <div>
          <label class="block text-[10px] font-bold uppercase tracking-widest text-on-surface-variant">名称 *</label>
          <input
            v-model="form.name"
            class="mt-1.5 w-full rounded-xl border border-outline-variant/30 bg-surface-container px-4 py-2.5 text-sm transition-colors focus:border-primary focus:outline-none"
            placeholder="配置名称"
            required
          />
        </div>

        <div>
          <label class="block text-[10px] font-bold uppercase tracking-widest text-on-surface-variant">描述</label>
          <input
            v-model="form.description"
            class="mt-1.5 w-full rounded-xl border border-outline-variant/30 bg-surface-container px-4 py-2.5 text-sm transition-colors focus:border-primary focus:outline-none"
            placeholder="可选描述"
          />
        </div>
      </div>
    </section>

    <section class="rounded-2xl border border-outline-variant/20 bg-surface-container-lowest p-5 shadow-sm">
      <div class="mb-4">
        <p class="text-[10px] font-bold uppercase tracking-[0.24em] text-on-surface-variant">传输与连接</p>
      </div>

      <div class="space-y-4">
        <div>
          <label class="block text-[10px] font-bold uppercase tracking-widest text-on-surface-variant">传输类型</label>
          <select
            v-model="form.transport"
            :disabled="isEdit"
            class="mt-1.5 w-full rounded-xl border border-outline-variant/30 bg-surface-container px-4 py-2.5 text-sm transition-colors focus:border-primary focus:outline-none disabled:cursor-not-allowed disabled:opacity-70"
          >
            <option value="http">HTTP</option>
            <option value="sse">SSE</option>
            <option value="stdio" :disabled="!canManageStdio">STDIO（仅管理员）</option>
          </select>
          <p v-if="!canManageStdio" class="mt-1.5 text-xs text-on-surface-variant">STDIO 配置仅管理员可创建或修改。</p>
        </div>

        <template v-if="form.transport === 'stdio'">
          <div>
            <label class="block text-[10px] font-bold uppercase tracking-widest text-on-surface-variant">Command *</label>
            <input
              v-model="form.command"
              class="mt-1.5 w-full rounded-xl border border-outline-variant/30 bg-surface-container px-4 py-2.5 text-sm font-mono transition-colors focus:border-primary focus:outline-none"
              placeholder="e.g. npx -y @modelcontextprotocol/server-filesystem"
            />
          </div>
          <div>
            <label class="block text-[10px] font-bold uppercase tracking-widest text-on-surface-variant">Args (JSON Array)</label>
            <textarea
              v-model="form.argsStr"
              class="mt-1.5 w-full rounded-xl border border-outline-variant/30 bg-surface-container px-4 py-2.5 text-sm font-mono transition-colors focus:border-primary focus:outline-none"
              rows="4"
              placeholder='["/path/to/dir", "--verbose"]'
            />
            <p class="mt-1.5 text-xs text-on-surface-variant">使用 JSON 数组可以保留包含空格的参数。</p>
          </div>
          <div>
            <label class="block text-[10px] font-bold uppercase tracking-widest text-on-surface-variant">环境变量 (JSON)</label>
            <textarea
              v-model="form.envStr"
              class="mt-1.5 w-full rounded-xl border border-outline-variant/30 bg-surface-container px-4 py-2.5 text-sm font-mono transition-colors focus:border-primary focus:outline-none"
              rows="4"
              placeholder='{"KEY": "value"}'
            />
            <p class="mt-1.5 text-xs text-on-surface-variant">
              {{ isEdit ? '留空表示保留现有环境变量。' : '可选，使用 JSON 对象输入环境变量。' }}
            </p>
          </div>
        </template>

        <template v-else>
          <div>
            <label class="block text-[10px] font-bold uppercase tracking-widest text-on-surface-variant">URL *</label>
            <input
              v-model="form.url"
              class="mt-1.5 w-full rounded-xl border border-outline-variant/30 bg-surface-container px-4 py-2.5 text-sm font-mono transition-colors focus:border-primary focus:outline-none"
              placeholder="https://example.com/mcp"
            />
          </div>
          <div>
            <label class="block text-[10px] font-bold uppercase tracking-widest text-on-surface-variant">Headers (JSON)</label>
            <textarea
              v-model="form.headersStr"
              class="mt-1.5 w-full rounded-xl border border-outline-variant/30 bg-surface-container px-4 py-2.5 text-sm font-mono transition-colors focus:border-primary focus:outline-none"
              rows="4"
              placeholder='{"Authorization": "Bearer xxx"}'
            />
            <p class="mt-1.5 text-xs text-on-surface-variant">
              {{ isEdit ? '留空表示保留现有请求头。' : '可选，使用 JSON 对象输入请求头。' }}
            </p>
          </div>
        </template>
      </div>
    </section>

    <section class="rounded-2xl border border-outline-variant/20 bg-surface-container-lowest p-5 shadow-sm">
      <div v-if="!isEdit" class="flex flex-col gap-3 md:flex-row md:items-start md:justify-between">
        <div>
          <p class="text-[10px] font-bold uppercase tracking-[0.24em] text-on-surface-variant">连接验证</p>
          <p class="mt-2 text-sm leading-relaxed text-on-surface-variant">在创建前验证当前表单中的 transport、URL 或 command 参数是否可用。</p>
        </div>

        <button
          type="button"
          class="rounded-xl border border-outline-variant/30 px-5 py-2.5 text-sm font-bold text-on-surface-variant transition-colors hover:bg-surface-container disabled:cursor-not-allowed disabled:opacity-50"
          :disabled="testLoading"
          @click="$emit('test')"
        >
          {{ testLoading ? '测试中...' : '测试连接' }}
        </button>
      </div>

      <div v-else>
        <p class="text-[10px] font-bold uppercase tracking-[0.24em] text-on-surface-variant">编辑提示</p>
        <p class="mt-2 text-sm leading-relaxed text-on-surface-variant">编辑页不会回填已保存的 `headers` 和 `env` 明文；保持为空表示继续沿用后端已保存的值。保存完成后可以回到列表页使用“测试连接”验证最终配置。</p>
      </div>

      <div v-if="testResult" class="mt-4 rounded-xl bg-surface-container px-4 py-3 text-xs">
        <div v-if="testResult.success" class="flex items-center gap-2">
          <span class="h-2 w-2 shrink-0 rounded-full bg-success"></span>
          <span class="font-semibold text-success">连接成功</span>
          <span v-if="testResult.tools?.length" class="text-on-surface-variant">{{ testResult.tools.length }} 个工具</span>
        </div>
        <div v-else class="flex items-start gap-2">
          <span class="mt-0.5 h-2 w-2 shrink-0 rounded-full bg-danger"></span>
          <span class="text-danger">{{ testResult.message }}</span>
        </div>
      </div>
    </section>

    <p v-if="formError" class="text-sm text-danger">{{ formError }}</p>

    <section class="flex flex-wrap items-center gap-3 rounded-2xl border border-outline-variant/20 bg-surface-container-lowest px-5 py-4 shadow-sm">
      <button
        type="submit"
        class="rounded-xl bg-primary px-6 py-2.5 text-sm font-bold text-on-primary transition-colors hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-60"
        :disabled="loading"
      >
        {{ isEdit ? '保存' : '创建' }}
      </button>
      <router-link
        to="/mcp"
        class="rounded-xl px-5 py-2.5 text-sm font-medium text-on-surface-variant transition-colors hover:bg-surface-container"
      >
        返回列表
      </router-link>
    </section>
  </form>
</template>
