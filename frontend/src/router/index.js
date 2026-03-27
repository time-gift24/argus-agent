import { createRouter, createWebHistory } from 'vue-router'
import AgentDashboardLayout from '../layouts/AgentDashboardLayout.vue'
import DashboardView from '../views/DashboardView.vue'
import AgentListView from '../views/AgentListView.vue'
import AgentDetailsView from '../views/AgentDetailsView.vue'
import ShellView from '../views/ShellView.vue'
import LogsView from '../views/LogsView.vue'
import SettingsView from '../views/SettingsView.vue'

const routes = [
  {
    path: '/',
    component: AgentDashboardLayout,
    children: [
      { path: '', component: DashboardView },
      { path: 'agents', component: AgentListView },
      { path: 'agents/:id', component: AgentDetailsView },
      { path: 'shell', component: ShellView },
      { path: 'logs', component: LogsView },
      { path: 'settings', component: SettingsView },
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
