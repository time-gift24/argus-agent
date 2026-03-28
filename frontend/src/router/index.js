import { createRouter, createWebHistory } from 'vue-router'
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
  { path: '/settings', component: SettingsView },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
