import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { devLogin } from '../api/auth'
import { getProfile } from '../api/users'

export const useUserStore = defineStore('user', () => {
  const token = ref(localStorage.getItem('token') || '')
  const profile = ref(JSON.parse(localStorage.getItem('user_profile') || 'null'))

  const isLoggedIn = computed(() => !!token.value)
  const userName = computed(() => profile.value?.name || '')
  const userId = computed(() => profile.value?.id || '')

  async function login(username) {
    const { data } = await devLogin(username)
    token.value = data.token
    localStorage.setItem('token', data.token)
    await fetchProfile()
  }

  async function fetchProfile() {
    if (!token.value) return
    try {
      const { data } = await getProfile()
      profile.value = data
      localStorage.setItem('user_profile', JSON.stringify(data))
    } catch {
      // Token invalid — clear state
      logout()
    }
  }

  function logout() {
    token.value = ''
    profile.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user_profile')
  }

  return { token, profile, isLoggedIn, userName, userId, login, fetchProfile, logout }
})
