<template>
  <div class="max-w-7xl mx-auto space-y-5">
    <div class="animate-fade-up">
      <h1 class="text-3xl font-headline font-bold tracking-tight text-on-surface">
        系统<span class="text-primary">设置</span>
      </h1>
      <p class="text-sm text-on-surface-variant mt-1">配置平台参数和访问策略。</p>
    </div>

    <div class="space-y-6">
      <!-- 通用配置 -->
      <div class="bg-surface-container-lowest rounded-[2rem] border border-outline-variant/30 shadow-sm p-6 animate-fade-up animate-delay-1">
        <h2 class="text-sm font-headline font-bold text-on-surface mb-5 pb-4 border-b border-outline-variant/20">通用配置</h2>
        <div class="space-y-0">
          <div v-for="(setting, i) in generalSettings" :key="i" class="flex items-center justify-between py-4" :class="i < generalSettings.length - 1 ? 'border-b border-outline-variant/10' : ''">
            <div>
              <p class="text-sm font-semibold text-on-surface">{{ setting.name }}</p>
              <p class="text-xs text-on-surface-variant mt-1">{{ setting.desc }}</p>
            </div>
            <tiny-button size="small" plain>编辑</tiny-button>
          </div>
        </div>
      </div>

      <!-- 安全与访问 -->
      <div class="bg-surface-container-lowest rounded-[2rem] border border-outline-variant/30 shadow-sm p-6 animate-fade-up animate-delay-2">
        <h2 class="text-sm font-headline font-bold text-on-surface mb-5 pb-4 border-b border-outline-variant/20">安全与访问</h2>
        <div class="space-y-0">
          <div v-for="(setting, i) in securitySettings" :key="i" class="flex items-center justify-between py-4" :class="i < securitySettings.length - 1 ? 'border-b border-outline-variant/10' : ''">
            <div>
              <p class="text-sm font-semibold text-on-surface">{{ setting.name }}</p>
              <p class="text-xs text-on-surface-variant mt-1">{{ setting.desc }}</p>
            </div>
            <tiny-button size="small" plain>编辑</tiny-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { Button as TinyButton } from '@opentiny/vue'

const generalSettings = [
  { name: '最大并发智能体', desc: '可同时运行的最大智能体数量。' },
  { name: '任务超时', desc: '智能体任务执行的默认超时时间（秒）。' },
  { name: '日志保留', desc: '系统日志归档前的保留天数。' },
]

const securitySettings = [
  { name: 'API 密钥轮换', desc: '智能体认证的自动 API 密钥轮换策略。' },
  { name: '访问控制', desc: '平台的基于角色的访问控制配置。' },
]
</script>
