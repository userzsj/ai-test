import { defineStore } from 'pinia'
import { ref } from 'vue'
import { authAPI } from '@/api'
import { useRouter } from 'vue-router'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(uni.getStorageSync('access_token') || '')
  const user = ref(JSON.parse(uni.getStorageSync('user') || 'null'))

  async function login(credentials) {
    const data = await authAPI.login(credentials)
    token.value = data.access_token
    user.value = data.user
    uni.setStorageSync('access_token', data.access_token)
    uni.setStorageSync('user', JSON.stringify(data.user))
    return data
  }

  function logout() {
    token.value = ''
    user.value = null
    uni.removeStorageSync('access_token')
    uni.removeStorageSync('user')
    uni.reLaunch({ url: '/pages/login/login' })
  }

  const isAdmin = () => user.value?.role === 'ADMIN'

  return { token, user, login, logout, isAdmin }
})