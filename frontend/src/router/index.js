import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '../stores/user'
import DashboardView from '../views/DashboardView.vue'
import AgentListView from '../views/AgentListView.vue'
import AgentDetailsView from '../views/AgentDetailsView.vue'
import ToolsView from '../views/ToolsView.vue'
import ShellView from '../views/ShellView.vue'
import LogsView from '../views/LogsView.vue'
import SettingsView from '../views/SettingsView.vue'

const routes = [
  { path: '/', redirect: '/dashboard' },
  { path: '/dashboard', component: DashboardView },
  { path: '/agents', component: AgentListView },
  { path: '/agents/:id', component: AgentDetailsView },
  { path: '/tools', component: ToolsView },
  { path: '/shell', component: ShellView },
  { path: '/logs', component: LogsView },
  { path: '/mcp', component: () => import('../views/McpConfigsView.vue') },
  { path: '/providers', component: () => import('../views/ProvidersView.vue') },
  { path: '/providers/new', component: () => import('../views/ProviderEditView.vue'), meta: { requiresAuth: true } },
  { path: '/providers/:id/edit', component: () => import('../views/ProviderEditView.vue'), meta: { requiresAuth: true } },
  { path: '/settings', component: SettingsView },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// DevMode: no forced redirect, just ensure user store is initialized
router.beforeEach(async (to) => {
  const userStore = useUserStore()
  if (userStore.isLoggedIn && !userStore.profile) {
    await userStore.fetchProfile()
  }

  if (to.meta.requiresAuth && !userStore.isLoggedIn) {
    window.dispatchEvent(new CustomEvent('auth:required'))
    return '/providers'
  }
})

export default router
