<template>
  <div class="min-h-screen bg-surface architectural-grid font-body text-on-surface">

    <!-- Top Navigation Bar -->
    <nav class="fixed top-0 w-full h-16 flex items-center justify-between px-6 bg-surface-container-low/70 backdrop-blur-xl z-50 shadow-sm border-b border-outline-variant/30">
      <div class="flex items-center gap-4 min-w-[200px]">
        <button
          class="text-on-surface-variant hover:text-primary transition-colors p-1 cursor-pointer"
          @click="toggleSidebar"
        >
          <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="3" y1="6" x2="21" y2="6"/>
            <line x1="3" y1="12" x2="21" y2="12"/>
            <line x1="3" y1="18" x2="21" y2="18"/>
          </svg>
        </button>
        <span class="text-xl font-bold text-primary font-headline tracking-tight">Axiom Azure</span>
      </div>

      <div class="hidden md:flex items-center gap-8 justify-center flex-1">
        <router-link
          v-for="link in navLinks"
          :key="link.path"
          :to="link.path"
          class="font-headline tracking-tight transition-colors duration-200 text-sm"
          :class="[isActiveRoute(link.path)
            ? 'text-primary border-b-2 border-primary font-semibold'
            : 'text-on-surface-variant hover:text-primary']"
        >
          {{ link.name }}
        </router-link>
      </div>

      <div class="flex items-center gap-4 min-w-[200px] justify-end">
        <div class="hidden sm:flex items-center bg-surface-container-low px-3 py-1.5 rounded-full gap-2 text-on-surface-variant border border-outline-variant/30">
          <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="11" r="8"/>
            <line x1="21" y1="21" x2="16.65" y2="16.65"/>
          </svg>
          <input
            class="bg-transparent border-none focus:outline-none text-sm w-32 xl:w-48 font-label"
            placeholder="Search..."
            type="text"
          />
        </div>

        <button class="relative text-on-surface-variant hover:text-primary transition-colors cursor-pointer">
          <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/>
            <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
          </svg>
          <span class="absolute -top-0.5 -right-0.5 w-2 h-2 bg-error rounded-full"></span>
        </button>

        <tiny-button type="primary" round>
          <span class="font-headline font-semibold">Deploy Agent</span>
        </tiny-button>
      </div>
    </nav>

    <!-- Sidebar -->
    <aside
      class="fixed left-0 top-0 h-screen p-4 flex flex-col justify-between bg-surface-container-low border-r border-outline-variant/30 z-[60] sidebar-transition overflow-hidden"
      :class="isCollapsed ? 'w-20' : 'w-64'"
    >
      <div class="space-y-6">
        <div
          class="flex items-center gap-3 px-2 h-16 mb-2"
          :class="isCollapsed ? 'justify-center' : ''"
        >
          <div class="w-10 h-10 min-w-[40px] rounded-lg bg-primary flex items-center justify-center text-on-primary">
            <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect x="4" y="4" width="16" height="16" rx="2"/>
              <path d="M9 9h.01M15 9h.01M9 15h.01M15 15h.01"/>
            </svg>
          </div>
          <div v-if="!isCollapsed" class="overflow-hidden">
            <h3 class="font-headline font-bold text-sm leading-tight whitespace-nowrap">Core Engine</h3>
            <p class="text-[10px] text-on-surface-variant tracking-wider uppercase">v2.4.0 Active</p>
          </div>
        </div>

        <nav class="space-y-1">
          <router-link
            v-for="item in sidebarItems"
            :key="item.path"
            :to="item.path"
            class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-300 overflow-hidden"
            :class="[
              isCollapsed ? 'justify-center' : '',
              isActiveRoute(item.path)
                ? 'bg-white text-primary shadow-sm'
                : 'text-on-surface-variant hover:bg-surface-container'
            ]"
          >
            <component :is="item.icon" class="w-5 h-5 min-w-[20px]" />
            <span v-if="!isCollapsed" class="whitespace-nowrap">{{ item.name }}</span>
          </router-link>
        </nav>

        <div v-if="!isCollapsed" class="pt-4 flex justify-center">
          <button class="w-full py-3 border-2 border-dashed border-outline-variant text-outline hover:border-primary hover:text-primary rounded-xl text-xs font-bold transition-colors uppercase tracking-widest flex items-center justify-center gap-2 cursor-pointer">
            <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <line x1="12" y1="5" x2="12" y2="19"/>
              <line x1="5" y1="12" x2="19" y2="12"/>
            </svg>
            <span class="whitespace-nowrap">New Module</span>
          </button>
        </div>
      </div>

      <div class="space-y-1 border-t border-outline-variant/30 pt-4">
        <a
          v-for="f in footerItems"
          :key="f.name"
          class="flex items-center gap-3 px-3 py-2 text-on-surface-variant text-sm font-medium transition-colors overflow-hidden cursor-pointer"
          :class="[isCollapsed ? 'justify-center' : '', f.class]"
        >
          <component :is="f.icon" class="w-5 h-5 min-w-[20px]" />
          <span v-if="!isCollapsed" class="whitespace-nowrap">{{ f.name }}</span>
        </a>
      </div>
    </aside>

    <!-- Main Content -->
    <main
      class="pt-24 px-8 pb-12 main-transition min-h-screen"
      :class="isCollapsed ? 'ml-20' : 'ml-64'"
    >
      <router-view v-slot="{ Component }">
        <Transition name="fade" mode="out-in">
          <component :is="Component" />
        </Transition>
      </router-view>
    </main>

  </div>
</template>

<script setup>
import { ref, markRaw } from 'vue'
import { useRoute } from 'vue-router'
import { Button as TinyButton } from '@opentiny/vue'

const route = useRoute()
const isCollapsed = ref(false)

const toggleSidebar = () => {
  isCollapsed.value = !isCollapsed.value
}

const isActiveRoute = (path) => {
  if (path === '/') return route.path === '/'
  return route.path.startsWith(path)
}

const navLinks = [
  { name: 'Dashboard', path: '/dashboard' },
  { name: 'Agents', path: '/agents' },
  { name: 'Workflows', path: '/tools' },
  { name: 'Analytics', path: '/logs' },
]

const sidebarItems = [
  {
    name: 'Fleet Overview',
    path: '/dashboard',
    icon: markRaw({
      template: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>`
    })
  },
  {
    name: 'Logic Designer',
    path: '/tools',
    icon: markRaw({
      template: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="5" r="3"/><circle cx="5" cy="19" r="3"/><circle cx="19" cy="19" r="3"/><line x1="12" y1="8" x2="5" y2="16"/><line x1="12" y1="8" x2="19" y2="16"/></svg>`
    })
  },
  {
    name: 'Memory Vault',
    path: '/shell',
    icon: markRaw({
      template: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/></svg>`
    })
  },
  {
    name: 'API Keys',
    path: '/agents',
    icon: markRaw({
      template: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 2l-2 2m-7.61 7.61a5.5 5.5 0 1 1-7.778 7.778 5.5 5.5 0 0 1 7.777-7.777zm0 0L15.5 7.5m0 0l3 3L22 7l-3-3m-3.5 3.5L19 4"/></svg>`
    })
  },
  {
    name: 'System Logs',
    path: '/logs',
    icon: markRaw({
      template: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="4 17 10 11 4 5"/><line x1="12" y1="19" x2="20" y2="19"/></svg>`
    })
  },
]

const footerItems = [
  {
    name: 'Help Center',
    class: 'hover:text-primary',
    icon: markRaw({
      template: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>`
    })
  },
  {
    name: 'Logout',
    class: 'hover:text-error',
    icon: markRaw({
      template: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>`
    })
  },
]
</script>
