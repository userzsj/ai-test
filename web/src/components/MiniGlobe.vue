<template>
    <div ref="chartRef" class="mini-globe"></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import 'echarts-gl'

const chartRef = ref(null)
let chart = null

onMounted(() => {
    chart = echarts.init(chartRef.value)

    chart.setOption({
        backgroundColor: 'transparent',
        globe: {
            baseTexture: '/earth.jpg',
            heightTexture: '/earth.jpg',
            displacementScale: 0.05,
            shading: 'realistic',
            displacementQuality: 'high',
            realisticMaterial: { roughness: 0.5, metalness: 0.1 },
            postEffect: {
                enable: true,
                bloom: { enable: true, bloomIntensity: 0.2 },
                SSAO: { enable: true, radius: 3, intensity: 1.2 }
            },
            light: {
                main: { intensity: 1.5, shadow: true, alpha: 10, beta: 70 },
                ambient: { intensity: 0.6 }
            },
            viewControl: {
                autoRotate: true,
                autoRotateSpeed: 10,
                minDistance: 180,
                maxDistance: 180,       // 固定距离，不能缩放
                rotateSensitivity: 0,   // 禁止手动旋转
                zoomSensitivity: 0      // 禁止缩放
            },
            atmosphere: { show: true, offset: 3, color: '#409EFF', glowPower: 3 }
        }
    })

    window.addEventListener('resize', () => chart?.resize())
})

onUnmounted(() => {
    chart?.dispose()
})
</script>

<style scoped>
.mini-globe {
    width: 100%;
    height: 100%;
}
</style>