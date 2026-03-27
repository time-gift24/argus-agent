<template>
  <div class="flex-1 flex items-center justify-between min-w-0">
    <div class="hidden sm:flex items-center gap-6">
      <div class="flex items-center gap-2 px-3 py-1 bg-gray-50 rounded-full border border-gray-100">
        <span class="text-[10px] font-bold text-gray-400 tracking-widest uppercase">HEALTH</span>
        <div class="flex items-center gap-3 ml-2">
          <div class="flex items-center gap-1.5">
            <div class="w-1.5 h-1.5 rounded-full bg-blue-500"></div>
            <span class="text-[10px] font-mono font-bold">{{ summary.total }}</span>
          </div>
          <div class="flex items-center gap-1.5">
            <div class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></div>
            <span class="text-[10px] font-mono font-bold">{{ summary.active }}</span>
          </div>
          <div class="flex items-center gap-1.5">
            <div class="w-1.5 h-1.5 rounded-full bg-rose-500"></div>
            <span class="text-[10px] font-mono font-bold">{{ summary.error }}</span>
          </div>
        </div>
      </div>
    </div>

    <div class="flex items-center gap-2 sm:gap-4 ml-auto">
      <button class="p-2 text-gray-400 hover:text-primary transition-colors">
        <component :is="icons.Bell" class="w-5 h-5" />
      </button>
      <div class="w-px h-6 bg-gray-200 mx-1"></div>
      <div class="flex items-center gap-2 sm:gap-3 cursor-pointer group">
        <div class="text-right hidden sm:block">
          <p class="text-xs font-bold text-text group-hover:text-primary transition-colors leading-none">Admin</p>
          <p class="text-[9px] text-gray-400 font-mono mt-1 uppercase">ROOT</p>
        </div>
        <div class="w-8 h-8 sm:w-10 sm:h-10 rounded-full bg-secondary flex items-center justify-center text-primary font-bold border-2 border-white shadow-sm overflow-hidden">
          <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Argus" alt="Avatar" class="w-full h-full object-cover" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { Bell } from 'lucide-vue-next'
import { useAgentStore } from '../stores/agents'
import { storeToRefs } from 'pinia'

const icons = { Bell }
const agentStore = useAgentStore()
const { summary } = storeToRefs(agentStore)
</script>
