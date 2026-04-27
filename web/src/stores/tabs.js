import { defineStore } from 'pinia'
import { ref } from 'vue'
import router from '@/router'

export const useTabsStore = defineStore('tabs', () => {
  const savedTabs = localStorage.getItem('openedTabs')
  const savedActive = localStorage.getItem('activeTab')

  const openedTabs = ref(
    savedTabs ? JSON.parse(savedTabs) : [{ path: '/dashboard', name: '首页', closable: false }]
  )
  const activeTab = ref(savedActive || '/dashboard')

  function saveToStorage() {
    localStorage.setItem('openedTabs', JSON.stringify(openedTabs.value))
    localStorage.setItem('activeTab', activeTab.value)
  }

  function addTab(route) {
    const path = route.path
    if (path === '/login' || path === '/register') return
    activeTab.value = path
    const exists = openedTabs.value.find(tab => tab.path === path)
    if (!exists) {
      openedTabs.value.push({ path, name: route.meta?.title || path, closable: true })
    }
    saveToStorage()
  }

  function closeTab(path) {
    const index = openedTabs.value.findIndex(tab => tab.path === path)
    if (index === -1) return
    openedTabs.value.splice(index, 1)
    if (activeTab.value === path) {
      const next = openedTabs.value[index] || openedTabs.value[index - 1]
      if (next) {
        activeTab.value = next.path
        router.push(next.path)
      }
    }
    saveToStorage()
  }

  function closeOtherTabs(path) {
    openedTabs.value = openedTabs.value.filter(tab => !tab.closable || tab.path === path)
    activeTab.value = path
    router.push(path)
    saveToStorage()
  }

  function closeAllTabs() {
    openedTabs.value = openedTabs.value.filter(tab => !tab.closable)
    activeTab.value = '/dashboard'
    router.push('/dashboard')
    saveToStorage()
  }

  function refreshPage() {
    router.replace({ path: '/_refresh', query: { redirect: activeTab.value } })
  }

  return { openedTabs, activeTab, addTab, closeTab, closeOtherTabs, closeAllTabs, refreshPage }
})