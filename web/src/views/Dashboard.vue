<template>
    <div class="dashboard">
        <!-- 顶部欢迎区 -->
        <div class="hero-section">
            <ThreeBackground mode="inline" />
            <div class="hero-content">
                <div class="hero-text">
                    <h1>👋 欢迎回来，{{ authStore.user?.name }}</h1>
                    <p>{{ greetingText }}</p>
                    <div class="hero-tags">
                        <el-tag type="info" effect="dark" round>{{ authStore.user?.role === 'ADMIN' ? '管理员' : '普通用户'
                        }}</el-tag>
                        <el-tag effect="dark" round>{{ currentDate }}</el-tag>
                    </div>
                </div>
                <div class="hero-illustration" @click="goGlobe">
                    <MiniGlobe></MiniGlobe>
                </div>
            </div>
        </div>

        <!-- 统计卡片 -->
        <div class="stats-row">
            <div v-for="stat in stats" :key="stat.label" class="stat-card" :style="{ '--accent': stat.color }">
                <div class="stat-icon">
                    <el-icon :size="28">
                        <component :is="stat.icon" />
                    </el-icon>
                </div>
                <div class="stat-info">
                    <div class="stat-value">
                        <span v-if="stat.loading" class="stat-skeleton"></span>
                        <template v-else>
                            <CountUp :end-val="stat.value" :duration="1.5" />
                        </template>
                    </div>
                    <div class="stat-label">{{ stat.label }}</div>
                </div>
                <div class="stat-spark">
                    <div class="spark-bar" v-for="i in 5" :key="i" :style="{ height: randomHeight() }"></div>
                </div>
            </div>
        </div>

        <div class="content-grid">
            <div class="card chart-card">
                <h3 class="card-title">用户增长趋势</h3>
                <UserChart />
            </div>
            <div class="card chart-card">
                <h3 class="card-title">角色分布</h3>
                <RoleChart />
            </div>
            <div class="card quick-actions">
                <h3 class="card-title">快捷操作</h3>
                <div class="actions-grid">
                    <div v-for="action in quickActions" :key="action.label" class="action-item" @click="action.click">
                        <div class="action-icon" :style="{ background: action.color }">
                            <el-icon :size="20">
                                <component :is="action.icon" />
                            </el-icon>
                        </div>
                        <span class="action-label">{{ action.label }}</span>
                    </div>
                </div>
            </div>
        </div>
        <!-- 3D 地球 -->
        <FullScreenModal title="全球用户分布" :isShowSmall="false" ref="GlobeChartModalRef">
            <GlobeChart />
        </FullScreenModal>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import CountUp from '@/components/CountUp.vue'
import { User, List, Plus, DataBoard, Setting, Brush, Camera, AlarmClock } from '@element-plus/icons-vue'
import UserChart from '@/components/UserChart.vue'
import RoleChart from '@/components/RoleChart.vue'
import GlobeChart from '@/components/GlobeChart.vue'
import FullScreenModal from '@/components/FullScreenModal.vue'
import ThreeBackground from '@/components/ThreeBackground.vue'
import MiniGlobe from '@/components/MiniGlobe.vue'
import { fa } from 'element-plus/es/locale/index.mjs'

const router = useRouter()
const authStore = useAuthStore()

const currentDate = computed(() => {
    const d = new Date()
    return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
})
const GlobeChartModalRef = ref(null)
function goGlobe() {
    // 滚动到地球区域
    GlobeChartModalRef.value.visible = true
}
const greetingText = computed(() => {
    const hour = new Date().getHours()
    if (hour < 6) return '夜深了，注意休息 🌙'
    if (hour < 9) return '早上好，新的一天开始了 ☀️'
    if (hour < 12) return '上午好，今天效率很高 💪'
    if (hour < 14) return '中午好，别忘了吃饭 🍜'
    if (hour < 18) return '下午好，继续加油 🚀'
    return '晚上好，回顾一下今天的收获 📝'
})

const stats = ref([
    { label: '总用户数', value: 128, color: '#409EFF', icon: User, loading: false },
    { label: '今日新增', value: 12, color: '#67C23A', icon: DataBoard, loading: false },
    { label: '活跃用户', value: 86, color: '#E6A23C', icon: AlarmClock, loading: false },
    { label: '系统模块', value: 8, color: '#f56c6c', icon: Setting, loading: false },
])

const quickActions = [
    { label: '用户列表', icon: List, color: '#409EFF', click: () => router.push('/users') },
    { label: '创建用户', icon: Plus, color: '#67C23A', click: () => router.push('/users') },
    { label: '数据报表', icon: DataBoard, color: '#E6A23C', click: () => { } },
    { label: '系统设置', icon: Setting, color: '#f56c6c', click: () => { } },
]

const activities = ref([
    { text: '管理员创建了新用户 "李四"', time: '2 分钟前', color: '#409EFF' },
    { text: '系统备份任务已完成', time: '15 分钟前', color: '#67C23A' },
    { text: '用户 "张三" 更新了个人资料', time: '1 小时前', color: '#E6A23C' },
    { text: '系统自动更新至 v2.1.0', time: '3 小时前', color: '#f56c6c' },
    { text: '新用户 "王五" 完成邮箱验证', time: '5 小时前', color: '#909399' },
])

function randomHeight() {
    return Math.floor(Math.random() * 24 + 4) + 'px'
}
</script>

<style scoped>
.dashboard {
    padding: 0;
}

/* ========== 顶部欢迎区 ========== */
.hero-section {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    border-radius: 16px;
    margin-bottom: 24px;
    overflow: hidden;
    position: relative;
}

.hero-section::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -20%;
    width: 60%;
    height: 200%;
    background: radial-gradient(circle, rgba(64, 158, 255, 0.1) 0%, transparent 70%);
    pointer-events: none;
}

.hero-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px;
    position: relative;
    z-index: 1;
}
.hero-text{
   padding: 20px;
}

.hero-text h1 {
    font-size: 26px;
    color: #fff;
    margin-bottom: 8px;
    font-weight: 600;
}

.hero-text p {
    color: rgba(255, 255, 255, 0.65);
    font-size: 15px;
    margin-bottom: 16px;
}

.hero-tags {
    display: flex;
    gap: 8px;
}

/* 装饰动画 */
.hero-illustration {
    position: relative;
    width: 160px;
    height: 140px;
    flex-shrink: 0;
    padding-right: 20px;
}

.orbit-ring {
    position: absolute;
    inset: 0;
    border: 2px solid rgba(64, 158, 255, 0.2);
    border-radius: 50%;
    animation: orbit-spin 6s linear infinite;
}

.orbit-ring.delay {
    animation-delay: -3s;
    width: 80%;
    height: 80%;
    top: 10%;
    left: 10%;
    border-color: rgba(103, 194, 58, 0.2);
}

.center-dot {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 16px;
    height: 16px;
    background: linear-gradient(135deg, #409EFF, #67C23A);
    border-radius: 50%;
    box-shadow: 0 0 24px rgba(64, 158, 255, 0.5);
}

@keyframes orbit-spin {
    from {
        transform: rotate(0deg);
    }

    to {
        transform: rotate(360deg);
    }
}

/* ========== 统计卡片 ========== */
.stats-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 24px;
}

.stat-card {
    background: #fff;
    border-radius: 14px;
    padding: 20px 24px;
    display: flex;
    align-items: center;
    gap: 16px;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
    position: relative;
    overflow: hidden;
    transition: all 0.3s;
}

.stat-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.stat-card::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 4px;
    height: 100%;
    background: var(--accent);
}

.stat-icon {
    width: 52px;
    height: 52px;
    border-radius: 14px;
    background: color-mix(in srgb, var(--accent) 10%, transparent);
    color: var(--accent);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

.stat-value {
    font-size: 28px;
    font-weight: 700;
    color: #1a1a2e;
    line-height: 1.2;
}

.stat-label {
    font-size: 13px;
    color: #999;
    margin-top: 2px;
}

.stat-spark {
    display: flex;
    align-items: flex-end;
    gap: 3px;
    position: absolute;
    right: 20px;
    bottom: 20px;
}

.spark-bar {
    width: 4px;
    background: var(--accent);
    border-radius: 2px;
    opacity: 0.3;
    border-radius: 2px 2px 0 0;
}

/* ========== 内容网格 ========== */
.content-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
}

.chart-card {
    min-height: 340px;
}

.card {
    background: #fff;
    border-radius: 14px;
    padding: 24px;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
}

.card-title {
    font-size: 16px;
    font-weight: 600;
    color: #1a1a2e;
    margin-bottom: 20px;
}

/* 快捷操作 */
.actions-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
}

.action-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 14px;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.2s;
    border: 1px solid #f0f0f0;
}

.action-item:hover {
    background: #f8f9fa;
    border-color: #e0e0e0;
}

.action-icon {
    width: 40px;
    height: 40px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #fff;
    flex-shrink: 0;
}

.action-label {
    font-size: 14px;
    color: #555;
    font-weight: 500;
}

/* 最近活动 */
.activity-list {
    display: flex;
    flex-direction: column;
}

.activity-item {
    display: flex;
    gap: 14px;
    padding: 10px 0;
    position: relative;
}

.activity-item+.activity-item::before {
    content: '';
    position: absolute;
    top: 0;
    left: 5px;
    width: 1px;
    height: 100%;
    background: #e8e8e8;
}

.timeline-dot {
    width: 11px;
    height: 11px;
    border-radius: 50%;
    flex-shrink: 0;
    margin-top: 4px;
    position: relative;
    z-index: 1;
    box-shadow: 0 0 0 3px #fff, 0 0 0 4px var(--color, #e8e8e8);
}

.activity-text {
    font-size: 14px;
    color: #444;
}

.activity-time {
    font-size: 12px;
    color: #bbb;
    margin-top: 2px;
}

/* 骨架屏 */
.stat-skeleton {
    display: inline-block;
    width: 60px;
    height: 28px;
    background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
    background-size: 200% 100%;
    animation: shimmer 1.5s infinite;
    border-radius: 4px;
}

@keyframes shimmer {
    0% {
        background-position: 200% 0;
    }

    100% {
        background-position: -200% 0;
    }
}

.globe-row {
    margin-top: 24px;
}
</style>