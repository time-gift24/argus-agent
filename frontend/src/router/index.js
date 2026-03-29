import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '../stores/user'
import { routes } from './routes'

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
