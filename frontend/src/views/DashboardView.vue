<template>
  <div>
    <h1 class="text-3xl font-bold mb-6">Dashboard Overview</h1>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div v-for="i in 3" :key="i" class="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
        <div class="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center text-primary mb-4">
          <LayoutIcon class="w-6 h-6" />
        </div>
        <h3 class="text-lg font-bold mb-2">Stat Metric {{ i }}</h3>
        <p class="text-3xl font-bold text-primary font-mono">1,234</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { Layout as LayoutIcon } from 'lucide-vue-next'
</script>
