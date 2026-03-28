<!-- @mock — 3 行占位配置，无真实设置数据；替换为：GET /api/settings -->
<template>
  <div class="max-w-7xl mx-auto space-y-5">
    <div class="animate-fade-up">
      <h1 class="text-3xl font-headline font-bold tracking-tight text-on-surface">
        System <span class="text-primary">Settings</span>
      </h1>
      <p class="text-sm text-on-surface-variant mt-1">Configure platform parameters and access policies.</p>
    </div>

    <!-- Settings Groups -->
    <div class="space-y-6">
      <div class="bg-surface-container-lowest rounded-[2rem] border border-outline-variant/30 shadow-sm p-6 animate-fade-up animate-delay-1">
        <h2 class="text-sm font-headline font-bold text-on-surface mb-5 pb-4 border-b border-outline-variant/20">General Configuration</h2>
        <div class="space-y-0">
          <div v-for="(setting, i) in generalSettings" :key="i" class="flex items-center justify-between py-4" :class="i < generalSettings.length - 1 ? 'border-b border-outline-variant/10' : ''">
            <div>
              <p class="text-sm font-semibold text-on-surface">{{ setting.name }}</p>
              <p class="text-xs text-on-surface-variant mt-1">{{ setting.desc }}</p>
            </div>
            <tiny-button size="small" plain>Edit</tiny-button>
          </div>
        </div>
      </div>

      <div class="bg-surface-container-lowest rounded-[2rem] border border-outline-variant/30 shadow-sm p-6 animate-fade-up animate-delay-2">
        <h2 class="text-sm font-headline font-bold text-on-surface mb-5 pb-4 border-b border-outline-variant/20">Security & Access</h2>
        <div class="space-y-0">
          <div v-for="(setting, i) in securitySettings" :key="i" class="flex items-center justify-between py-4" :class="i < securitySettings.length - 1 ? 'border-b border-outline-variant/10' : ''">
            <div>
              <p class="text-sm font-semibold text-on-surface">{{ setting.name }}</p>
              <p class="text-xs text-on-surface-variant mt-1">{{ setting.desc }}</p>
            </div>
            <tiny-button size="small" plain>Edit</tiny-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { Button as TinyButton } from '@opentiny/vue'

const generalSettings = [
  { name: 'Max Concurrent Agents', desc: 'Maximum number of agents that can run simultaneously.' },
  { name: 'Task Timeout', desc: 'Default timeout for agent task execution in seconds.' },
  { name: 'Log Retention', desc: 'Number of days to retain system logs before archiving.' },
]

const securitySettings = [
  { name: 'API Key Rotation', desc: 'Automatic API key rotation policy for agent authentication.' },
  { name: 'Access Control', desc: 'Role-based access control configuration for the platform.' },
]
</script>
