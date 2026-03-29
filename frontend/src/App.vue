<template>
  <div class="min-h-screen bg-surface architectural-grid font-body text-on-surface">

    <!-- Sidebar (fixed overlay) -->
    <aside
      class="fixed left-0 top-0 h-screen flex flex-col justify-between bg-surface-container-low border-r border-outline-variant/30 z-[60] sidebar-transition overflow-hidden"
      :class="[
        (isCollapsed && !mobileOpen) ? 'w-16' : 'w-64',
        { 'hidden md:flex': !mobileOpen },
        { 'flex': mobileOpen }
      ]"
    >
      <div :class="sidebarShowsText ? 'space-y-6' : 'space-y-3'">
        <div
          class="flex items-center gap-3 px-2 h-16 mb-2"
          :class="sidebarShowsText ? '' : 'justify-center'"
        >
          <div class="w-10 h-10 min-w-[40px] rounded-lg bg-primary flex items-center justify-center text-on-primary">
            <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect x="4" y="4" width="16" height="16" rx="2"/>
              <path d="M9 9h.01M15 9h.01M9 15h.01M15 15h.01"/>
            </svg>
          </div>
          <div v-if="sidebarShowsText" class="overflow-hidden">
            <h3 class="font-headline font-bold text-sm leading-tight whitespace-nowrap">核心引擎</h3>
            <p class="text-[10px] text-on-surface-variant tracking-wider uppercase">v2.4.0 运行中</p>
          </div>
        </div>

        <nav class="space-y-1">
          <router-link
            v-for="item in sidebarItems"
            :key="item.path"
            :to="item.path"
            class="flex items-center gap-3 text-sm font-medium transition-all duration-300 overflow-hidden"
            :class="[
              sidebarShowsText
                ? 'mx-2 px-3 py-2.5 rounded-lg'
                : 'mx-auto h-9 w-9 justify-center rounded-lg p-0 gap-0',
              isActiveRoute(item.path)
                ? (sidebarShowsText
                    ? 'bg-surface-container text-primary shadow-sm'
                    : 'bg-primary/10 text-primary')
                : 'text-on-surface-variant hover:bg-surface-container'
            ]"
            @click="mobileOpen = false"
          >
            <component :is="item.icon" class="h-5 w-5 min-w-[20px] shrink-0" />
            <span v-if="sidebarShowsText" class="whitespace-nowrap">{{ item.name }}</span>
          </router-link>
        </nav>
      </div>

      <div class="space-y-1 border-t border-outline-variant/30 pt-4">
        <a
          v-for="f in footerItems"
          :key="f.name"
          class="flex items-center gap-3 px-3 py-2 text-on-surface-variant text-sm font-medium transition-colors overflow-hidden cursor-pointer"
          :class="[sidebarShowsText ? '' : 'justify-center', f.class]"
        >
          <component :is="f.icon" class="w-5 h-5 min-w-[20px]" />
          <span v-if="sidebarShowsText" class="whitespace-nowrap">{{ f.name }}</span>
        </a>
      </div>
    </aside>

    <!-- Mobile overlay backdrop -->
    <div
      v-if="mobileOpen"
      class="fixed inset-0 bg-black/40 z-[55] md:hidden"
      @click="mobileOpen = false"
    />

    <!-- Right side: top-bottom layout -->
    <div
      class="min-h-screen flex flex-col sidebar-transition"
      :class="contentPaddingClass"
    >
      <!-- Top Navigation Bar -->
      <nav class="sticky top-0 w-full h-16 flex items-center justify-between px-6 bg-surface-container-low/70 backdrop-blur-xl z-40 shadow-sm border-b border-outline-variant/30">
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

        <div class="hidden md:flex items-center gap-8 flex-1">
          <div class="hidden sm:flex items-center bg-surface-container-low px-3 py-1.5 rounded-full gap-2 text-on-surface-variant border border-outline-variant/30">
            <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="11" cy="11" r="8"/>
              <line x1="21" y1="21" x2="16.65" y2="16.65"/>
            </svg>
            <input
              class="bg-transparent border-none focus:outline-none text-sm w-32 xl:w-48 font-label"
              placeholder="搜索..."
              type="text"
            />
          </div>

          <div class="flex items-center gap-8">
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
        </div>

        <div class="flex items-center gap-4 min-w-[200px] justify-end">
          <!-- Not logged in: Login button -->
          <button
            v-if="!userStore.isLoggedIn"
            class="flex items-center gap-1.5 px-3 py-1.5 text-xs font-headline font-semibold text-on-surface-variant hover:text-primary bg-surface-container-low rounded-lg border border-outline-variant/30 transition-colors cursor-pointer"
            @click="showLoginDialog = true"
          >
            <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/>
              <polyline points="10 17 15 12 10 7"/>
              <line x1="15" y1="12" x2="3" y2="12"/>
            </svg>
            登录
          </button>

          <!-- Logged in: User info + Logout -->
          <div v-else class="flex items-center gap-2.5">
            <div class="text-right hidden sm:block">
              <p class="text-xs font-semibold text-on-surface leading-none">{{ userStore.userName }}</p>
              <p class="text-[9px] text-on-surface-variant font-mono mt-0.5 uppercase tracking-wide">开发模式</p>
            </div>
            <div class="relative user-menu-container">
              <button
                class="w-8 h-8 sm:w-9 sm:h-9 rounded-full border-2 border-outline-variant/30 hover:border-primary transition-colors overflow-hidden shadow-sm cursor-pointer"
                @click="showUserMenu = !showUserMenu"
              >
                <img
                  :src="`https://api.dicebear.com/7.x/avataaars/svg?seed=${userStore.userName}`"
                  alt="用户头像"
                  class="w-full h-full object-cover"
                />
              </button>
              <!-- Dropdown -->
              <div
                v-if="showUserMenu"
                class="absolute right-0 top-full mt-2 w-40 bg-surface-container-lowest rounded-xl border border-outline-variant/30 shadow-lg py-1 z-50"
              >
                <button
                  class="w-full flex items-center gap-2 px-4 py-2.5 text-sm text-on-surface-variant hover:text-danger hover:bg-surface-container transition-colors cursor-pointer"
                  @click="handleLogout"
                >
                  <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
                    <polyline points="16 17 21 12 16 7"/>
                    <line x1="21" y1="12" x2="9" y2="12"/>
                  </svg>
                  退出登录
                </button>
              </div>
            </div>
          </div>
        </div>
      </nav>

      <!-- Main Content -->
      <main class="main-content flex-1 min-w-0 px-8 pt-6 pb-12">
        <router-view v-slot="{ Component }">
          <Transition name="fade" mode="out-in">
            <component :is="Component" />
          </Transition>
        </router-view>
      </main>
    </div>

    <!-- Login Dialog -->
    <tiny-dialog-box
      v-model:visible="showLoginDialog"
      :close-on-click-modal="true"
      append-to-body
      title="开发模式登录"
      width="380px"
    >
      <div class="space-y-4 py-2">
        <div>
          <label class="text-[10px] font-bold tracking-widest uppercase text-on-surface-variant">用户名</label>
          <input
            v-model="loginUsername"
            class="mt-1 w-full px-3 py-2 text-sm bg-surface-container rounded-lg border border-outline-variant/30 focus:border-primary focus:outline-none transition-colors"
            placeholder="输入用户名"
            @keyup.enter="handleLogin"
          />
        </div>
        <p v-if="loginError" class="text-xs text-danger">{{ loginError }}</p>
      </div>
      <template #footer>
        <tiny-button @click="showLoginDialog = false">取消</tiny-button>
        <tiny-button type="primary" :loading="loginLoading" @click="handleLogin">登录</tiny-button>
      </template>
    </tiny-dialog-box>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { useUserStore } from './stores/user'
import { Button as TinyButton, DialogBox as TinyDialogBox } from '@opentiny/vue'
import { Database, LayoutDashboard, ScrollText, Server, Settings, Wrench } from 'lucide-vue-next'

const route = useRoute()
const userStore = useUserStore()
const isCollapsed = ref(false)
const mobileOpen = ref(false)

const showLoginDialog = ref(false)
const showUserMenu = ref(false)
const loginUsername = ref('')
const loginError = ref('')
const loginLoading = ref(false)

const toggleSidebar = () => {
  // On mobile, toggle overlay
  if (window.innerWidth < 768) {
    mobileOpen.value = !mobileOpen.value
    return
  }
  isCollapsed.value = !isCollapsed.value
}

// Whether sidebar text should be shown
const sidebarShowsText = computed(() => {
  if (!isCollapsed.value) return true
  if (mobileOpen.value) return true
  return false
})

// Content area padding-left
const contentPaddingClass = computed(() => {
  if (mobileOpen.value) return 'md:pl-64'
  if (isCollapsed.value) return 'pl-16'
  return 'pl-64'
})

const isActiveRoute = (path) => {
  if (path === '/') return route.path === '/'
  return route.path.startsWith(path)
}

const navLinks = [
  { name: '仪表盘', path: '/dashboard' },
  { name: '提供商', path: '/providers' },
  { name: 'MCP 服务', path: '/mcp' },
  { name: '智能体', path: '/agents' },
  { name: '工具库', path: '/tools' },
  { name: '分析', path: '/logs' },
]

const sidebarItems = [
  {
    name: '集群概览',
    path: '/dashboard',
    icon: LayoutDashboard,
  },
  {
    name: '工具库',
    path: '/tools',
    icon: Wrench,
  },
  {
    name: '记忆库',
    path: '/shell',
    icon: Database,
  },
  {
    name: 'LLM 提供商',
    path: '/providers',
    icon: Server,
  },
  {
    name: '系统日志',
    path: '/logs',
    icon: ScrollText,
  },
  {
    name: '设置',
    path: '/settings',
    icon: Settings,
  },
]

const footerItems = []

async function handleLogin() {
  if (!loginUsername.value.trim()) {
    loginError.value = '请输入用户名'
    return
  }
  loginLoading.value = true
  loginError.value = ''
  try {
    await userStore.login(loginUsername.value.trim())
    showLoginDialog.value = false
    loginUsername.value = ''
  } catch (e) {
    loginError.value = e.response?.data?.detail || '登录失败'
  } finally {
    loginLoading.value = false
  }
}

function handleLogout() {
  userStore.logout()
  showUserMenu.value = false
}

// Click-outside to close user menu
function onDocumentClick(e) {
  if (showUserMenu.value && !e.target.closest('.user-menu-container')) {
    showUserMenu.value = false
  }
}
onMounted(() => document.addEventListener('click', onDocumentClick))
onUnmounted(() => document.removeEventListener('click', onDocumentClick))

// Listen for 401 unauthorized from axios interceptor
function onAuthUnauthorized() {
  userStore.logout()
  showUserMenu.value = false
  loginError.value = '登录已失效，请重新登录'
  showLoginDialog.value = true
}
onMounted(() => window.addEventListener('auth:unauthorized', onAuthUnauthorized))
onUnmounted(() => window.removeEventListener('auth:unauthorized', onAuthUnauthorized))

function onAuthRequired() {
  loginError.value = '请先登录后再继续'
  showLoginDialog.value = true
}
onMounted(() => window.addEventListener('auth:required', onAuthRequired))
onUnmounted(() => window.removeEventListener('auth:required', onAuthRequired))
</script>

<style scoped>
.main-content {
  position: relative;
}

.sidebar-transition {
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1),
              padding-left 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
</style>
