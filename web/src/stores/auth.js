import { defineStore } from 'pinia'
import { ref } from 'vue'
import { authAPI, userAPI } from '@/api'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('access_token') || '')
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))

  // 登录
  async function login(credentials) {
    const data = await authAPI.login(credentials)
    token.value = data.access_token
    user.value = data.user
    
    localStorage.setItem('access_token', data.access_token)
    localStorage.setItem('user', JSON.stringify(data.user))
    
    return data
  }

  // 登出
  function logout() {
    token.value = ''
    user.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('user')
  }

  // 刷新用户信息
  async function refreshUser() {
    const data = await userAPI.getMe()
    user.value = data
    localStorage.setItem('user', JSON.stringify(data))
  }

  // 是否是管理员
  const isAdmin = () => user.value?.role === 'ADMIN'

  return { token, user, login, logout, refreshUser, isAdmin }
})