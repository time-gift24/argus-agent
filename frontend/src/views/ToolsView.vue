<template>
  <div>
    <h1 class="text-3xl font-bold mb-6">工具箱</h1>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="i in 6" :key="i" class="bg-white p-6 rounded-xl border border-gray-200 shadow-sm hover:border-primary transition-colors cursor-pointer group">
        <div class="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center text-primary mb-4 group-hover:bg-primary group-hover:text-white transition-colors">
          <WrenchIcon class="w-6 h-6" />
        </div>
        <h3 class="text-lg font-bold mb-2">实用工具 {{ i }}</h3>
        <p class="text-sm text-gray-500">这里是工具的简短描述，提供智能体辅助功能。</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { Wrench as WrenchIcon } from 'lucide-vue-next'
</script>
