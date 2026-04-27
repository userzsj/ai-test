<template>
    <div class="layout-root">
        <div class="layout-inner">
            <!-- 左侧菜单 -->
            <SideMenu :menu-tree="menuTree" :active-path="route.path" :collapsed="collapsed" />

            <div class="layout-right">
                <!-- 顶部栏 -->
                <header class="top-bar">
                    <div class="top-left">
                        <span class="collapse-btn" @click="collapsed = !collapsed">
                            <el-icon :size="18">
                                <Fold v-if="!collapsed" />
                                <Expand v-else />
                            </el-icon>
                        </span>
                        <span class="logo-text">用户管理系统</span>
                    </div>
                    <div class="top-right">
                        <!-- 通知按钮 -->
                        <el-popover placement="bottom" :width="320" trigger="click" :show-arrow="false">
                            <template #reference>
                                <el-badge :value="unreadCount" :hidden="unreadCount === 0" class="header-btn">
                                    <el-icon :size="20">
                                        <Bell />
                                    </el-icon>
                                </el-badge>
                            </template>

                            <div class="notice-panel">
                                <div class="notice-header">
                                    <span class="notice-title">消息通知</span>
                                    <span class="notice-more" @click="ElMessage.info('查看全部消息功能开发中')">查看全部</span>
                                </div>

                                <div class="notice-list">
                                    <div v-for="item in notices" :key="item.id" class="notice-item"
                                        :class="{ unread: !item.read }">
                                        <div class="notice-left">
                                            <span class="notice-dot" v-if="!item.read"></span>
                                            <div class="notice-icon" :style="{ background: item.color }">
                                                <el-icon :size="14">
                                                    <component :is="item.icon" />
                                                </el-icon>
                                            </div>
                                        </div>
                                        <div class="notice-body">
                                            <div class="notice-text">{{ item.text }}</div>
                                            <div class="notice-time">{{ item.time }}</div>
                                        </div>
                                    </div>
                                </div>

                                <div class="notice-footer" @click="ElMessage.info('全部标为已读功能开发中')">
                                    全部标为已读
                                </div>
                            </div>
                        </el-popover>

                        <!-- 全屏按钮 -->
                        <el-tooltip :content="isFullscreen ? '退出全屏' : '全屏'" placement="bottom">
                            <span class="header-btn" @click="toggleFullscreen">
                                <el-icon :size="20">
                                    <FullScreen v-if="!isFullscreen" />
                                    <Aim v-else />
                                </el-icon>
                            </span>
                        </el-tooltip>
                        <!-- 分隔线 -->
                        <span class="header-divider"></span>

                        <!-- 用户下拉 -->
                        <el-dropdown trigger="click" @command="handleUserCmd">
                            <span class="user-info">
                                <el-avatar :size="32" class="user-avatar">
                                    {{ authStore.user?.name?.charAt(0) || 'U' }}
                                </el-avatar>
                                <span class="user-name">{{ authStore.user?.name || '用户' }}</span>
                                <el-icon :size="14">
                                    <ArrowDown />
                                </el-icon>
                            </span>
                            <template #dropdown>
                                <el-dropdown-menu>
                                    <div class="dropdown-header">
                                        <el-avatar :size="40">{{ authStore.user?.name?.charAt(0) || 'U' }}</el-avatar>
                                        <div>
                                            <div class="dropdown-name">{{ authStore.user?.name }}</div>
                                            <div class="dropdown-role">{{ authStore.user?.role === 'ADMIN' ? '管理员' :
                                                '普通用户' }}</div>
                                        </div>
                                    </div>
                                    <el-dropdown-item command="profile" divided>
                                        <el-icon>
                                            <User />
                                        </el-icon>
                                        个人中心
                                    </el-dropdown-item>
                                    <el-dropdown-item command="settings">
                                        <el-icon>
                                            <Setting />
                                        </el-icon>
                                        系统设置
                                    </el-dropdown-item>
                                    <el-dropdown-item command="logout" divided>
                                        <el-icon>
                                            <SwitchButton />
                                        </el-icon>
                                        退出登录
                                    </el-dropdown-item>
                                </el-dropdown-menu>
                            </template>
                        </el-dropdown>
                    </div>
                </header>

                <!-- Tab 栏 -->
                <div class="tabs-bar">
                    <div class="tabs-list">
                        <div v-for="tab in tabsStore.openedTabs" :key="tab.path" class="tab-item"
                            :class="{ active: tabsStore.activeTab === tab.path }" @click="router.push(tab.path)"
                            @contextmenu.prevent="onTabContext($event, tab)">
                            <span>{{ tab.name }}</span>
                            <el-icon v-if="tab.closable" class="tab-close" @click.stop="tabsStore.closeTab(tab.path)">
                                <Close />
                            </el-icon>
                        </div>
                    </div>
                </div>

                <!-- 内容区 -->
                <div class="content-area">
                    <el-main id="main-content">
                        <router-view v-slot="{ Component }">
                            <transition name="fade" mode="out-in">
                                <component :is="Component" />
                            </transition>
                        </router-view>
                    </el-main>

                    <!-- 回到顶部 -->
                    <transition name="fade">
                        <div v-show="showBackTop" class="back-top-btn" @click="scrollToTop">
                            <el-icon :size="20">
                                <ArrowUpBold />
                            </el-icon>
                        </div>
                    </transition>
                </div>
            </div>
        </div>

        <!-- Tab 右键菜单 -->
        <div v-if="ctx.visible" class="ctx-menu" :style="{ left: ctx.x + 'px', top: ctx.y + 'px' }">
            <div @click="tabsStore.refreshPage(); ctx.visible = false">刷新</div>
            <div v-if="ctx.tab?.closable" @click="tabsStore.closeTab(ctx.tab.path); ctx.visible = false">关闭</div>
            <div v-if="ctx.tab?.closable" @click="tabsStore.closeOtherTabs(ctx.tab.path); ctx.visible = false">关闭其他
            </div>
            <div @click="tabsStore.closeAllTabs(); ctx.visible = false">关闭全部</div>
        </div>
    </div>
</template>

<script setup>
import { ref, reactive, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Close, Fold, Expand, UserFilled, ArrowDown } from '@element-plus/icons-vue'
import SideMenu from '@/components/SideMenu.vue'
import { useTabsStore } from '@/stores/tabs'
import { useAuthStore } from '@/stores/auth'
import { House, User } from '@element-plus/icons-vue'
import { ArrowUpBold, Setting, Bell } from '@element-plus/icons-vue'
import { onMounted, onUnmounted } from 'vue'

const unreadCount = ref(3)

const notices = ref([
  { id: 1, text: '新用户 "张三" 已注册', time: '5 分钟前', color: '#409EFF', icon: User, read: false },
  { id: 2, text: '系统已更新至 v2.1.0', time: '1 小时前', color: '#67C23A', icon: Setting, read: false },
  { id: 3, text: '备份任务已完成', time: '3 小时前', color: '#E6A23C', icon: Bell, read: true },
])
const route = useRoute()
const router = useRouter()
const tabsStore = useTabsStore()
const authStore = useAuthStore()
const collapsed = ref(false)

const menuTree = [
    { id: 'dashboard', name: '首页', path: '/dashboard', icon: House },
    {
        id: 'user-manage', name: '用户管理', icon: User, children: [
            { id: 'users', name: '用户列表', path: '/users' }
        ]
    }
]

const ctx = reactive({ visible: false, x: 0, y: 0, tab: null })
function onTabContext(e, tab) {
    ctx.visible = true; ctx.x = e.clientX; ctx.y = e.clientY; ctx.tab = tab
    const off = () => { ctx.visible = false; document.removeEventListener('click', off) }
    setTimeout(() => document.addEventListener('click', off), 0)
}


watch(() => route.path, path => {
    if (path === '/_refresh') return router.replace(route.query.redirect || '/dashboard')
    if (path !== '/login' && path !== '/register') {
        const name = menuTree.flatMap(m => [m, ...(m.children || [])]).find(m => m.path === path)?.name || path
        tabsStore.addTab({ path, meta: { title: name } })
    }
}, { immediate: true })
const showBackTop = ref(false)
let mainEl = null

function handleScroll() {
    showBackTop.value = mainEl?.scrollTop > 200
}

function scrollToTop() {
    mainEl?.scrollTo({ top: 0, behavior: 'smooth' })
}
const isFullscreen = ref(false)

function toggleFullscreen() {
    if (document.fullscreenElement) {
        document.exitFullscreen()
        isFullscreen.value = false
    } else {
        document.documentElement.requestFullscreen()
        isFullscreen.value = true
    }
}



function handleUserCmd(cmd) {
    if (cmd === 'logout') {
        authStore.logout()
        router.push('/login')
    } else if (cmd === 'profile') {
        ElMessage.info('个人中心开发中')
    } else if (cmd === 'settings') {
        ElMessage.info('系统设置开发中')
    }
}
onMounted(() => {
    mainEl = document.getElementById('main-content')
    if (mainEl) {
        mainEl.addEventListener('scroll', handleScroll)
    }
    document.addEventListener('fullscreenchange', () => {
        isFullscreen.value = !!document.fullscreenElement
    })
})

onUnmounted(() => {
    mainEl?.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped>
.layout-root {
    width: 100vw;
    height: 100vh;
    overflow: hidden;
    background: #f0f2f5;
}

.layout-inner {
    display: flex;
    height: 100%;
}

.layout-right {
    flex: 1;
    display: flex;
    flex-direction: column;
    min-width: 0;
}

/* 顶部栏 */
.top-bar {
    height: 48px;
    background: #fff;
    border-bottom: 1px solid #e8e8e8;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 16px;
    flex-shrink: 0;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}

/* 调整角标位置 */
.header-btn :deep(.el-badge__content) {
    top: 2px;
    width: 16px;
    height: 16px;
    font-size: 10px;
    line-height: 16px;
    padding: 0;
}

.top-left {
    display: flex;
    align-items: center;
    gap: 12px;
}

.collapse-btn {
    cursor: pointer;
    color: #666;
    display: flex;
    align-items: center;
    transition: color 0.2s;
}

.collapse-btn:hover {
    color: #409EFF;
}

.logo-text {
    font-size: 16px;
    font-weight: 600;
    color: #333;
}

.top-right {
    display: flex;
    align-items: center;
    gap: 4px;
}

.header-btn {
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 8px;
    color: #888;
    cursor: pointer;
    transition: all 0.15s;
}

.header-btn:hover {
    background: #f0f2f5;
    color: #409EFF;
}

.header-divider {
    width: 1px;
    height: 20px;
    background: #e8e8e8;
    margin: 0 8px;
}

.user-info {
    display: flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    padding: 2px 8px;
    border-radius: 8px;
    transition: all 0.15s;
}

.user-info:hover {
    background: #f0f2f5;
}

.user-avatar {
    background: linear-gradient(135deg, #409EFF, #67C23A) !important;
    color: #fff !important;
    font-weight: 600;
    font-size: 14px;
}

.user-name {
    font-size: 14px;
    color: #555;
    max-width: 100px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

/* 下拉菜单头部 */
.dropdown-header {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 16px 14px;
    border-bottom: 1px solid #f0f0f0;
}

.dropdown-name {
    font-size: 14px;
    font-weight: 600;
    color: #333;
}

.dropdown-role {
    font-size: 12px;
    color: #999;
    margin-top: 2px;
}

/* Tab 栏 */
.tabs-bar {
    height: 36px;
    background: #fff;
    /* border-bottom: 1px solid #e8e8e8; */
    flex-shrink: 0;
}

.tabs-list {
    display: flex;
    gap: 0;
    padding: 2px 8px 0;
    overflow-x: auto;
    height: 100%;
    align-items: flex-end;
}

.tab-item {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 6px 14px;
    border-radius: 6px 6px 0 0;
    font-size: 13px;
    color: #999;
    cursor: pointer;
    white-space: nowrap;
    transition: all 0.15s;
    border: 1px solid transparent;
    border-bottom: none;
}

.tab-item:hover {
    color: #409EFF;
    background: rgba(64, 158, 255, 0.04);
}

.tab-item.active {
    color: #409EFF;
    background: #f0f2f5;
    border-color: #e8e8e8;
}

.tab-close {
    font-size: 12px;
    opacity: 0.5;
    transition: opacity 0.15s;
}

.tab-close:hover {
    opacity: 1;
    color: #f56c6c;
}

/* 内容区 */
.content-area {
    flex: 1;
    position: relative;
    overflow: hidden;
}

/* el-main 已经自带滚动，不需要再设置 overflow: auto */
.content-area .el-main {
    height: 100%;
    padding: 20px;
}

/* 回到顶部按钮 */
.back-top-btn {
    position: absolute;
    bottom: 28px;
    right: 28px;
    width: 44px;
    height: 44px;
    border-radius: 50%;
    background: rgba(64, 158, 255, 0.85);
    backdrop-filter: blur(8px);
    color: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    box-shadow: 0 4px 16px rgba(64, 158, 255, 0.35), 0 0 0 4px rgba(64, 158, 255, 0.12);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    z-index: 10;
    overflow: hidden;
    /* 隐藏超出部分 */
}

.back-top-btn:hover {
    background: #409EFF;
    transform: translateY(-4px) scale(1.05);
    box-shadow: 0 6px 24px rgba(64, 158, 255, 0.5), 0 0 0 8px rgba(64, 158, 255, 0.08);
}

.back-top-btn:active {
    transform: translateY(-2px) scale(0.95);
}

/* 图标滚动动画 - 仅在悬停时播放 */
.back-top-btn .el-icon {
    animation: none;
}

.back-top-btn:hover .el-icon {
    animation: scroll-top 2.5s ease-in-out infinite;
}

@keyframes scroll-top {
    0% {
        transform: translateY(0);
        opacity: 1;
    }

    20% {
        transform: translateY(-28px);
        opacity: 0;
    }

    21% {
        transform: translateY(28px);
        opacity: 0;
    }

    50% {
        transform: translateY(0);
        opacity: 1;
    }

    100% {
        transform: translateY(0);
        opacity: 1;
    }
}

/* 右键菜单 */
.ctx-menu {
    position: fixed;
    z-index: 999;
    background: #fff;
    border: 1px solid #e8e8e8;
    border-radius: 8px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
    padding: 4px;
    min-width: 120px;
}

.ctx-menu div {
    padding: 6px 12px;
    font-size: 13px;
    color: #555;
    cursor: pointer;
    border-radius: 4px;
}

.ctx-menu div:hover {
    background: #f5f5f5;
    color: #409EFF;
}

.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.15s;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}

.notice-panel {
    margin: -12px;
}

.notice-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 14px 16px 10px;
    border-bottom: 1px solid #f0f0f0;
}

.notice-title {
    font-size: 15px;
    font-weight: 600;
    color: #333;
}

.notice-more {
    font-size: 13px;
    color: #409EFF;
    cursor: pointer;
}

.notice-more:hover {
    text-decoration: underline;
}

.notice-list {
    padding: 4px 0;
}

.notice-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 12px 16px;
  transition: background 0.15s;
  cursor: pointer;
}
.notice-item.unread {
  background: rgba(64, 158, 255, 0.03);
}
.notice-item:hover {
  background: #f8f9fa;
}
.notice-item.unread:hover {
  background: rgba(64, 158, 255, 0.06);
}

.notice-left {
  position: relative;
  flex-shrink: 0;
}
.notice-dot {
  position: absolute;
  top: -2px;
  left: -2px;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--el-color-danger);
  z-index: 1;
  box-shadow: 0 0 0 2px #fff;
}

.notice-icon {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  flex-shrink: 0;
}

.notice-body {
  flex: 1;
  min-width: 0;
}
.notice-text {
  font-size: 13px;
  color: #444;
  line-height: 1.5;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.notice-item.unread .notice-text {
  font-weight: 500;
  color: #333;
}
.notice-time {
  font-size: 12px;
  color: #bbb;
  margin-top: 4px;
}

.notice-footer {
    padding: 12px 16px;
    text-align: center;
    font-size: 13px;
    color: #666;
    border-top: 1px solid #f0f0f0;
    cursor: pointer;
    transition: all 0.15s;
    border-radius: 0 0 4px 4px;
}

.notice-footer:hover {
    background: #f8f9fa;
    color: #409EFF;
}
</style>