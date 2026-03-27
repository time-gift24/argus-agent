<template>
  <div class="flex h-screen bg-background overflow-hidden relative">
    <!-- Mobile Sidebar Backdrop -->
    <div 
      v-if="isSidebarOpen" 
      class="fixed inset-0 bg-text/40 z-40 lg:hidden backdrop-blur-sm transition-opacity duration-300"
      @click="isSidebarOpen = false"
    ></div>

    <!-- Sidebar -->
    <aside 
      class="fixed inset-y-0 left-0 w-64 bg-white border-r border-gray-200 flex flex-col z-50 transition-transform duration-300 transform lg:relative lg:translate-x-0"
      :class="[isSidebarOpen ? 'translate-x-0 shadow-2xl' : '-translate-x-full']"
    >
      <div class="p-6 flex items-center justify-between border-b border-gray-200">
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 bg-primary rounded-lg flex items-center justify-center text-white">
            <component :is="icons.Cpu" class="w-5 h-5" />
          </div>
          <span class="text-xl font-bold tracking-tight text-text">Argus 智能体</span>
        </div>
        <button @click="isSidebarOpen = false" class="lg:hidden p-1 text-gray-400">
          <component :is="icons.X" class="w-5 h-5" />
        </button>
      </div>
      
      <nav class="flex-1 p-4 space-y-2 overflow-y-auto">
        <router-link 
          v-for="item in menuItems" 
          :key="item.path"
          :to="item.path"
          class="flex items-center gap-3 px-4 py-2.5 rounded-lg transition-all duration-200"
          :class="[$route.path === item.path ? 'bg-primary/10 text-primary' : 'text-gray-600 hover:bg-gray-100']"
          @click="isSidebarOpen = false"
        >
          <component :is="item.icon" class="w-5 h-5" />
          <span class="font-bold text-sm">{{ item.name }}</span>
        </router-link>
      </nav>
      
      <div class="p-4 border-t border-gray-200">
        <div class="flex items-center gap-3 px-4 py-2 text-gray-500 text-xs italic">
          版本 v0.1.0-alpha
        </div>
      </div>
    </aside>

    <!-- Main Content Area -->
    <div class="flex-1 flex flex-col overflow-hidden min-w-0">
      <!-- Header with Mobile Toggle -->
      <header class="h-16 bg-white border-b border-gray-200 flex items-center justify-between px-4 lg:px-8 shrink-0">
        <div class="flex items-center gap-4 flex-1">
          <button @click="isSidebarOpen = true" class="lg:hidden p-2 -ml-2 text-gray-400 hover:text-primary transition-colors">
            <component :is="icons.Menu" class="w-6 h-6" />
          </button>
          <GlobalHeader />
        </div>
      </header>

      <!-- Main Scrollable Area -->
      <main class="flex-1 overflow-y-auto p-4 lg:p-8">
        <router-view v-slot="{ Component }">
          <transition 
            name="fade" 
            mode="out-in"
            enter-active-class="transition duration-200 ease-out"
            enter-from-class="opacity-0 translate-y-2"
            enter-to-class="opacity-100 translate-y-0"
            leave-active-class="transition duration-150 ease-in"
            leave-from-class="opacity-100 translate-y-0"
            leave-to-class="opacity-0 -translate-y-2"
          >
            <component :is="Component" />
          </transition>
        </router-view>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { 
  Cpu, Wrench, Menu, X 
} from 'lucide-vue-next'
import GlobalHeader from '../components/GlobalHeader.vue'

const icons = { Cpu, Menu, X }
const isSidebarOpen = ref(false)

const menuItems = [
  { name: '智能体管理', path: '/agents', icon: Cpu },
  { name: '工具箱', path: '/tools', icon: Wrench },
]
</script>

<style>
/* Global styles for OpenTiny components to follow Fira fonts */
.tiny-grid, .tiny-tabs, .tiny-button {
  font-family: "Fira Sans", ui-sans-serif, system-ui, sans-serif !important;
}

.font-mono {
  font-family: "Fira Code", ui-monospace, SFMono-Regular, monospace !important;
}
</style>
