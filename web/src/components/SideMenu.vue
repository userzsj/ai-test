<template>
    <div :style="{ width: collapsed ? '64px' : '220px' }" class="side-menu">
        <!-- 系统 Logo 区域 -->
        <div class="side-logo">
            <!-- 顶部装饰线 -->
            <!-- <div class="logo-decor-line"></div> -->
            
            <!-- 图片容器 + 两侧特效 -->
            <div class="logo-img-wrapper">
                <div class="logo-effect logo-effect-left"></div>
                <img :src="defaultAvatar" class="logo-img" alt="Logo" />
                <div class="logo-effect logo-effect-right"></div>
            </div>
            
            <span v-show="!collapsed" class="logo-text">Control Hub</span>
            
            <!-- 底部装饰点 -->
            <!-- <div class="logo-decor-dots" v-show="!collapsed">
                <span class="dot" v-for="i in 5" :key="i"></span>
            </div> -->
        </div>

        <!-- 菜单 -->
        <el-menu :default-active="activePath" :collapse="collapsed" :router="true" class="custom-menu">
            <SideMenuItem :menu-list="menuTree" />
        </el-menu>
    </div>
</template>

<script setup>
import SideMenuItem from './SideMenuItem.vue'

const defaultAvatar = '/default-avatar.png'

defineProps({
    menuTree: { type: Array, default: () => [] },
    activePath: { type: String, default: '' },
    collapsed: { type: Boolean, default: false }
})
</script>

<style scoped>
.side-menu {
    height: 100%;
    transition: width 0.25s;
    flex-shrink: 0;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    background: #304156 !important;
}

/* Logo 区域 */
.side-logo {
    padding: 24px 0 18px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 14px;
    flex-shrink: 0;
    position: relative;
}

/* 顶部装饰线 */
.logo-decor-line {
    width: 40px;
    height: 2px;
    background: linear-gradient(90deg, transparent, #409EFF, #67C23A, #409EFF, transparent);
    border-radius: 2px;
    margin-bottom: 4px;
    animation: line-shimmer 2s ease-in-out infinite;
}

@keyframes line-shimmer {
    0%, 100% { opacity: 0.4; }
    50% { opacity: 1; }
}

/* 图片容器 */
.logo-img-wrapper {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
}

.logo-img {
    width: 60px;
    height: 60px;
    object-fit: contain;
    border-radius: 16px;
    display: block;
    position: relative;
    z-index: 2;
    box-shadow: 0 4px 20px rgba(64, 158, 255, 0.3);
    border: 2px solid rgba(64, 158, 255, 0.25);
}

/* 左右两侧特效 */
.logo-effect {
    position: absolute;
    width: 14px;
    height: 40px;
    border-radius: 7px;
    z-index: 1;
    animation: effect-pulse 2s ease-in-out infinite;
}

.logo-effect-left {
    right: calc(100% + 6px);
    background: linear-gradient(180deg, #409EFF, #67C23A);
    opacity: 0.6;
    box-shadow: 0 0 12px rgba(64, 158, 255, 0.4);
}

.logo-effect-right {
    left: calc(100% + 6px);
    background: linear-gradient(180deg, #67C23A, #409EFF);
    opacity: 0.6;
    box-shadow: 0 0 12px rgba(103, 194, 58, 0.4);
    animation-delay: 1s;
}

@keyframes effect-pulse {
    0%, 100% { 
        opacity: 0.3; 
        transform: scaleY(0.8); 
    }
    50% { 
        opacity: 0.8; 
        transform: scaleY(1.2); 
    }
}

/* 文字 */
.logo-text {
    font-size: 14px;
    font-weight: 700;
    color: #fff;
    letter-spacing: 3px;
    text-align: center;
    text-shadow: 0 0 10px rgba(64, 158, 255, 0.4);
}

/* 底部装饰点 */
.logo-decor-dots {
    display: flex;
    gap: 6px;
    margin-top: 2px;
}

.dot {
    width: 4px;
    height: 4px;
    border-radius: 50%;
    background: #409EFF;
    animation: dot-blink 1.5s ease-in-out infinite;
}

.dot:nth-child(1) { animation-delay: 0s; }
.dot:nth-child(2) { animation-delay: 0.2s; }
.dot:nth-child(3) { animation-delay: 0.4s; }
.dot:nth-child(4) { animation-delay: 0.6s; }
.dot:nth-child(5) { animation-delay: 0.8s; }

@keyframes dot-blink {
    0%, 100% { opacity: 0.3; }
    50% { opacity: 1; }
}
</style>

<style>
/* 菜单样式保持不变 */
.custom-menu {
    height: 100%;
    background: #304156 !important;
    border-right: none !important;
}

.custom-menu .el-menu-item,
.custom-menu .el-sub-menu__title {
    color: #bfcbd9;
    transition: all 0.2s;
}

.custom-menu .el-menu-item:hover,
.custom-menu .el-sub-menu__title:hover {
    background-color: rgba(255, 255, 255, 0.06) !important;
    color: #fff !important;
}

.custom-menu .el-menu-item.is-active {
    background: rgba(64, 158, 255, 0.15) !important;
    color: #409EFF !important;
}

.custom-menu .el-sub-menu .el-menu {
    background: rgba(0, 0, 0, 0.2) !important;
}
</style>