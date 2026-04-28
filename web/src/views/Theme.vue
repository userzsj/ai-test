<template>
    <div class="theme-page">
        <!-- 页面标题 -->
        <div class="page-header">
            <h2 class="page-title">
                <el-icon :size="22">
                    <Brush />
                </el-icon>
                主题设置
            </h2>
            <p class="page-desc">自定义你的界面风格，打造专属视觉体验</p>
        </div>

        <!-- 内容区域 -->
        <div class="theme-content">
            <!-- 布局模式 -->
            <div class="section-card">
                <div class="section-header">
                    <el-icon :size="18">
                        <Grid />
                    </el-icon>
                    <span class="section-title">布局模式</span>
                </div>
                <div class="layout-options">
                    <!-- 经典侧栏 -->
                    <div class="layout-card" :class="{ active: currentLayout === 'sidebar-dark' }"
                        @click="switchLayout('sidebar-dark')">
                        <div class="layout-thumb layout-sidebar-dark">
                            <div class="thumb-sidebar"></div>
                            <div class="thumb-body">
                                <div class="thumb-topbar"></div>
                                <div class="thumb-content"></div>
                            </div>
                        </div>
                        <span class="layout-name">经典侧栏</span>
                        <el-icon v-if="currentLayout === 'sidebar-dark'" class="layout-check">
                            <CircleCheckFilled />
                        </el-icon>
                    </div>

                    <!-- 顶部导航 -->
                    <div class="layout-card" :class="{ active: currentLayout === 'top-nav' }"
                        @click="switchLayout('top-nav')">
                        <div class="layout-thumb layout-top-nav">
                            <div class="thumb-top-nav-bar"></div>
                            <div class="thumb-content-full"></div>
                        </div>
                        <span class="layout-name">顶部导航</span>
                        <el-icon v-if="currentLayout === 'top-nav'" class="layout-check">
                            <CircleCheckFilled />
                        </el-icon>
                    </div>

                    <!-- 沉浸布局 -->
                    <div class="layout-card" :class="{ active: currentLayout === 'immersive' }"
                        @click="switchLayout('immersive')">
                        <div class="layout-thumb layout-immersive">
                            <div class="thumb-immersive-content"></div>
                            <div class="thumb-immersive-tabs"></div>
                            <div class="thumb-immersive-hamburger">
                                <span></span><span></span><span></span>
                            </div>
                        </div>
                        <span class="layout-name">沉浸布局</span>
                        <el-icon v-if="currentLayout === 'immersive'" class="layout-check">
                            <CircleCheckFilled />
                        </el-icon>
                    </div>
                </div>
            </div>

            <!-- 主题色 -->
            <div class="section-card">
                <div class="section-header">
                    <el-icon :size="18">
                        <PictureFilled />
                    </el-icon>
                    <span class="section-title">主题配色</span>
                </div>
                <div class="color-options">
                    <div v-for="color in themeColors" :key="color.value" class="color-card"
                        :class="{ active: currentColor === color.value }" @click="switchColor(color.value)">
                        <div class="color-circle" :style="{ background: color.gradient }">
                            <el-icon v-if="currentColor === color.value" class="color-check">
                                <Check />
                            </el-icon>
                        </div>
                        <span class="color-name">{{ color.name }}</span>
                    </div>
                </div>
            </div>

            <!-- 外观模式 -->
            <div class="section-card">
                <div class="section-header">
                    <el-icon :size="18">
                        <Moon />
                    </el-icon>
                    <span class="section-title">外观模式</span>
                </div>
                <div class="appearance-options">
                    <div v-for="mode in appearanceModes" :key="mode.value" class="appearance-card"
                        :class="{ active: currentAppearance === mode.value }" @click="switchAppearance(mode.value)">
                        <div class="appearance-icon" :style="{ background: mode.bg }">
                            <el-icon :size="24">
                                <component :is="mode.icon" />
                            </el-icon>
                        </div>
                        <div class="appearance-info">
                            <span class="appearance-name">{{ mode.name }}</span>
                            <span class="appearance-desc">{{ mode.desc }}</span>
                        </div>
                        <el-icon v-if="currentAppearance === mode.value" class="appearance-check">
                            <Check />
                        </el-icon>
                    </div>
                </div>
            </div>
        </div>
        <RightPanel :saving="loading" :buttons="[
            { key: 'reset', icon: RefreshRight, label: '重置', tip: '重置表单', expandable: false }
        ]" @save="handleSave" @btn-click="handleBtnClick">
        </RightPanel>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import {
    Brush, Grid, PictureFilled, Moon, Sunny, MagicStick, RefreshLeft, Check, CircleCheckFilled, RefreshRight
} from '@element-plus/icons-vue'
import RightPanel from '@/components/RightPanel.vue'
const loading = ref(false)

function handleSave() {
    loading.value = true
    setTimeout(() => { loading.value = false; ElMessage.success('设置已保存') }, 1000)
}
function handleBtnClick(btn) {
    if (btn.key === 'reset') {
        // 直接执行，不展开
        console.log('重置表单')
    }
}
// 布局模式
const currentLayout = ref('sidebar-dark')
const layoutModes = [
    { name: '经典侧栏', value: 'sidebar-dark' },
    { name: '顶部导航', value: 'top-nav' },
    { name: '沉浸布局', value: 'immersive' }
]

// 主题颜色
const currentColor = ref('blue')
const themeColors = [
    { name: '天空蓝', value: 'blue', gradient: 'linear-gradient(135deg, #409EFF, #36cfc9)' },
    { name: '活力绿', value: 'green', gradient: 'linear-gradient(135deg, #52c41a, #a0d911)' },
    { name: '夕阳橙', value: 'orange', gradient: 'linear-gradient(135deg, #fa8c16, #ffc53d)' },
    { name: '魅惑紫', value: 'purple', gradient: 'linear-gradient(135deg, #722ed1, #b37feb)' },
    { name: '玫瑰红', value: 'red', gradient: 'linear-gradient(135deg, #f5222d, #ff4d4f)' },
    { name: '极简黑', value: 'black', gradient: 'linear-gradient(135deg, #262626, #595959)' }
]

// 外观模式
const currentAppearance = ref('light')
const appearanceModes = [
    { name: '浅色模式', value: 'light', desc: '明亮清爽', icon: Sunny, bg: 'linear-gradient(135deg, #ffd43b, #fab005)' },
    { name: '深色模式', value: 'dark', desc: '护眼舒适', icon: Moon, bg: 'linear-gradient(135deg, #5c7cfa, #845ef7)' },
    { name: '自动切换', value: 'auto', desc: '跟随系统', icon: Check, bg: 'linear-gradient(135deg, #20c997, #12b886)' }
]

// 圆角大小
const borderRadius = ref(8)
const radiusMarks = {
    0: '直角',
    8: '默认',
    16: '大圆角'
}

function switchLayout(mode) {
    currentLayout.value = mode
    ElMessage.success(`已切换至${layoutModes.find(m => m.value === mode)?.name}布局`)
}

function switchColor(color) {
    currentColor.value = color
    ElMessage.success(`主题色已更新`)
}

function switchAppearance(mode) {
    currentAppearance.value = mode
    ElMessage.success(`已切换至${appearanceModes.find(m => m.value === mode)?.name}`)
}

function resetTheme() {
    currentLayout.value = 'sidebar-dark'
    currentColor.value = 'blue'
    currentAppearance.value = 'light'
    borderRadius.value = 8
    ElMessage.success('已恢复默认设置')
}
</script>

<style scoped>
.theme-page {
    padding: 0;
}

.page-header {
    margin-bottom: 32px;
}

.page-title {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 22px;
    color: #1a1a2e;
    margin-bottom: 6px;
}

.page-desc {
    color: #999;
    font-size: 14px;
    margin-left: 32px;
}

/* 内容区 */
.theme-content {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

/* 卡片 */
.section-card {
    background: #fff;
    border-radius: 14px;
    padding: 24px;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04);
}

.section-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 20px;
    color: #1a1a2e;
}

.section-title {
    font-size: 15px;
    font-weight: 600;
}

/* 布局选项 */
.layout-options {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
}

.layout-card {
    cursor: pointer;
    text-align: center;
    padding: 16px 12px 12px;
    border: 2px solid #f0f0f0;
    border-radius: 14px;
    transition: all 0.25s;
    position: relative;
}

.layout-card:hover {
    border-color: #d0d5ff;
    background: #fafaff;
}

.layout-card.active {
    border-color: #409EFF;
    background: rgba(64, 158, 255, 0.03);
}

.layout-check {
    position: absolute;
    top: -8px;
    right: -8px;
    color: #409EFF;
    font-size: 22px;
    background: #fff;
    border-radius: 50%;
}

.layout-name {
    display: block;
    margin-top: 12px;
    font-size: 13px;
    font-weight: 500;
    color: #444;
}

/* 缩略图 */
.layout-thumb {
    width: 100%;
    height: 90px;
    border-radius: 8px;
    overflow: hidden;
    position: relative;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

/* 经典侧栏缩略图 */
.layout-sidebar-dark {
    display: flex;
    background: #f0f2f5;
}

.layout-sidebar-dark .thumb-sidebar {
    width: 28%;
    background: #304156;
}

.layout-sidebar-dark .thumb-body {
    flex: 1;
    display: flex;
    flex-direction: column;
}

.layout-sidebar-dark .thumb-topbar {
    height: 25%;
    background: #fff;
    border-bottom: 1px solid #eee;
}

.layout-sidebar-dark .thumb-content {
    flex: 1;
    background: #f8f9fa;
}

/* 顶部导航缩略图 */
.layout-top-nav {
    display: flex;
    flex-direction: column;
    background: #f0f2f5;
}

.layout-top-nav .thumb-top-nav-bar {
    height: 28%;
    background: #304156;
}

.layout-top-nav .thumb-content-full {
    flex: 1;
    background: #fff;
}

/* 沉浸布局缩略图 */
.layout-immersive {
    background: linear-gradient(180deg, #1a1a2e 0%, #0d0d1a 100%);
    position: relative;
    border: 1px solid rgba(255, 255, 255, 0.06);
}

.layout-immersive .thumb-immersive-content {
    width: 100%;
    height: 100%;
    background: radial-gradient(ellipse at center, rgba(64, 158, 255, 0.06) 0%, transparent 70%);
}

.layout-immersive .thumb-immersive-tabs {
    position: absolute;
    top: 10%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 50%;
    height: 10px;
    background: rgba(255, 255, 255, 0.08);
    border-radius: 5px;
}

.layout-immersive .thumb-immersive-hamburger {
    position: absolute;
    bottom: 10px;
    left: 12px;
    display: flex;
    flex-direction: column;
    gap: 3px;
}

.layout-immersive .thumb-immersive-hamburger span {
    display: block;
    width: 14px;
    height: 2px;
    background: rgba(255, 255, 255, 0.35);
    border-radius: 1px;
}

/* 颜色选项 */
.color-options {
    display: flex;
    gap: 16px;
    flex-wrap: wrap;
}

.color-card {
    cursor: pointer;
    text-align: center;
    transition: transform 0.2s;
}

.color-card:hover {
    transform: translateY(-2px);
}

.color-circle {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    margin: 0 auto 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    transition: box-shadow 0.2s;
}

.color-card.active .color-circle {
    box-shadow: 0 0 0 3px #fff, 0 0 0 5px #409EFF;
}

.color-check {
    color: #fff;
    font-size: 18px;
    font-weight: bold;
}

.color-name {
    font-size: 12px;
    color: #777;
}

/* 外观模式 */
.appearance-options {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.appearance-card {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 14px;
    border: 2px solid transparent;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.2s;
}

.appearance-card:hover {
    background: #f8f9fa;
}

.appearance-card.active {
    border-color: #409EFF;
    background: rgba(64, 158, 255, 0.04);
}

.appearance-icon {
    width: 44px;
    height: 44px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #fff;
    flex-shrink: 0;
}

.appearance-info {
    flex: 1;
}

.appearance-name {
    font-size: 14px;
    color: #333;
    font-weight: 500;
}

.appearance-desc {
    font-size: 12px;
    color: #999;
    margin-top: 2px;
    margin-left: 5px;
}

.appearance-check {
    color: #409EFF;
    font-size: 18px;
}

/* 圆角 */
.radius-slider {
    padding: 10px 0;
}

/* 重置 */
.reset-area {
    text-align: center;
    padding: 10px 0;
}
</style>