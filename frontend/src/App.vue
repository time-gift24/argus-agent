<template>
  <div class="flex h-screen bg-background overflow-hidden relative">

    <!-- Mobile Sidebar Backdrop -->
    <Transition name="backdrop">
      <div
        v-if="isSidebarOpen"
        class="fixed inset-0 bg-[#0F172A]/50 z-40 lg:hidden backdrop-blur-sm"
        @click="isSidebarOpen = false"
      ></div>
    </Transition>

    <!-- Sidebar -->
    <aside
      class="fixed inset-y-0 left-0 w-[248px] flex flex-col z-50 transition-transform duration-300 transform lg:relative lg:translate-x-0 bg-surface border-r border-border"
      :class="[isSidebarOpen ? 'translate-x-0 shadow-[8px_0_24px_rgba(0,0,0,0.12)]' : '-translate-x-full']"
    >
      <!-- Logo Area -->
      <div class="px-5 py-5 flex items-center justify-between border-b border-border">
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 bg-primary rounded-[8px] flex items-center justify-center text-white shadow-sm shadow-primary/30">
            <svg class="w-[18px] h-[18px]" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect x="4" y="4" width="16" height="16" rx="2"/>
              <path d="M9 9h.01M15 9h.01M9 15h.01M15 15h.01"/>
            </svg>
          </div>
          <div class="leading-tight">
            <span class="text-[15px] font-bold tracking-tight text-text">Argus</span>
            <span class="block text-[10px] font-medium text-text-muted -mt-0.5">智能体平台</span>
          </div>
        </div>
        <button @click="isSidebarOpen = false" class="hidden lg:block p-1 text-text-muted hover:text-text transition-colors rounded-md hover:bg-surface-3">
          <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M18 6L6 18M6 6l12 12"/>
          </svg>
        </button>
      </div>

      <!-- Section Label -->
      <div class="px-5 pt-5 pb-2">
        <span class="text-[10px] font-semibold text-text-muted uppercase tracking-widest">导航</span>
      </div>

      <nav class="px-3 flex-1 space-y-0.5 overflow-y-auto">
        <router-link
          v-for="item in menuItems"
          :key="item.path"
          :to="item.path"
          class="flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all duration-150 group relative"
          :class="[$route.path.startsWith(item.path) ? 'bg-primary/10 text-primary' : 'text-text-secondary hover:bg-surface-3 hover:text-text']"
          @click="isSidebarOpen = false"
        >
          <!-- Active indicator -->
          <div
            v-if="$route.path.startsWith(item.path)"
            class="absolute left-0 top-1/2 -translate-y-1/2 w-0.5 h-5 bg-primary rounded-r-full"
          ></div>

          <component :is="item.icon" class="w-[18px] h-[18px] shrink-0" :stroke-width="$route.path.startsWith(item.path) ? 2.5 : 2" />

          <span class="text-[13px] font-semibold">{{ item.name }}</span>

          <!-- Active dot -->
          <div
            v-if="$route.path.startsWith(item.path)"
            class="ml-auto w-1.5 h-1.5 rounded-full bg-primary"
          ></div>
        </router-link>
      </nav>

      <!-- Footer -->
      <div class="p-4 border-t border-border">
        <div class="flex items-center justify-between px-3 py-2">
          <span class="text-[11px] font-medium text-text-muted">v0.1.0-alpha</span>
          <div class="flex items-center gap-1">
            <div class="w-1.5 h-1.5 rounded-full bg-success animate-pulse"></div>
            <span class="text-[11px] font-medium text-success">运行中</span>
          </div>
        </div>
      </div>
    </aside>

    <!-- Main Content Area -->
    <div class="flex-1 flex flex-col overflow-hidden min-w-0">

      <!-- Header -->
      <header class="h-14 bg-surface border-b border-border flex items-center justify-between px-5 lg:px-8 shrink-0">
        <div class="flex items-center gap-4 flex-1">
          <button
            @click="isSidebarOpen = true"
            class="lg:hidden p-1.5 -ml-1.5 text-text-muted hover:text-text hover:bg-surface-3 rounded-md transition-colors"
          >
            <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="3" y1="6" x2="21" y2="6"/>
              <line x1="3" y1="12" x2="21" y2="12"/>
              <line x1="3" y1="18" x2="21" y2="18"/>
            </svg>
          </button>
          <GlobalHeader />
        </div>
      </header>

      <!-- Main Scrollable Area -->
      <main class="flex-1 overflow-y-auto p-5 lg:p-8">
        <router-view v-slot="{ Component }">
          <Transition name="fade" mode="out-in">
            <component :is="Component" />
          </Transition>
        </router-view>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, markRaw } from 'vue'
import {
  Cpu,
  Wrench,
  Terminal,
  FileText,
  Settings,
} from 'lucide-vue-next'
import GlobalHeader from './components/GlobalHeader.vue'

const isSidebarOpen = ref(false)

const menuItems = [
  { name: '智能体管理', path: '/agents', icon: markRaw(Cpu) },
  { name: '工具箱',     path: '/tools', icon: markRaw(Wrench) },
  { name: '交互控制台', path: '/shell', icon: markRaw(Terminal) },
  { name: '系统日志',   path: '/logs', icon: markRaw(FileText) },
  { name: '系统设置',   path: '/settings', icon: markRaw(Settings) },
]
</script>

<style scoped>
.backdrop-enter-active,
.backdrop-leave-active {
  transition: opacity 200ms ease;
}
.backdrop-enter-from,
.backdrop-leave-to {
  opacity: 0;
}
</style>
