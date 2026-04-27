<template>
    <div class="globe-wrapper">
        <!-- 局部 Three.js 星空 -->
        <ThreeBackground mode="inline"/>
        
        <!-- ECharts 地球 -->
        <div ref="chartRef" class="globe-box"></div>
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import ThreeBackground from '@/components/ThreeBackground.vue'

import * as echarts from 'echarts'
import 'echarts-gl'
import * as THREE from 'three'

const chartRef = ref(null)
const threeContainer = ref(null)
let chart = null
let scene, camera, renderer, particles, animationId

// ========== 局部 Three.js 星空 ==========
function initThree() {
    console.log('initThree');

    const container = threeContainer.value
    if (!container) return

    // 弹窗打开瞬间容器尺寸可能为 0，需要延迟初始化
    const w = container.clientWidth
    const h = container.clientHeight
    if (w === 0 || h === 0) {
        setTimeout(initThree, 100)
        return
    }


    scene = new THREE.Scene()
    camera = new THREE.PerspectiveCamera(60, w / h, 0.1, 100)
    camera.position.z = 30

    renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true })
    renderer.setSize(w, h)
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
    container.appendChild(renderer.domElement)

    const count = 600
    const geo = new THREE.BufferGeometry()
    const pos = new Float32Array(count * 3)
    for (let i = 0; i < count * 3; i += 3) {
        pos[i] = (Math.random() - 0.5) * 60
        pos[i + 1] = (Math.random() - 0.5) * 40
        pos[i + 2] = (Math.random() - 0.5) * 30
    }
    geo.setAttribute('position', new THREE.BufferAttribute(pos, 3))
    function createGlowTexture() {
        const canvas = document.createElement('canvas')
        canvas.width = 64
        canvas.height = 64
        const ctx = canvas.getContext('2d')

        // 径向渐变：中心亮白 → 边缘完全透明
        const gradient = ctx.createRadialGradient(32, 32, 0, 32, 32, 32)
        gradient.addColorStop(0, 'rgba(255, 255, 255, 1)')
        gradient.addColorStop(0.05, 'rgba(255, 255, 255, 0.95)')  // 更近中心更亮
        gradient.addColorStop(0.2, 'rgba(180, 210, 255, 0.7)')
        gradient.addColorStop(0.5, 'rgba(100, 160, 255, 0.3)')
        gradient.addColorStop(1, 'rgba(0, 0, 0, 0)')

        ctx.fillStyle = gradient
        ctx.fillRect(0, 0, 64, 64)

        return new THREE.CanvasTexture(canvas)
    }
    const mat = new THREE.PointsMaterial({
        size: 0.6,                    // 稍微大一点，让光晕可见
        map: createGlowTexture(),
        color: 0xaaccff,              // 浅蓝紫色
        transparent: true,
        blending: THREE.AdditiveBlending,
        depthWrite: false,
        opacity: 1
    })
    particles = new THREE.Points(geo, mat)
    scene.add(particles)

    function animate() {
        animationId = requestAnimationFrame(animate)
        particles.rotation.y += 0.0005
        particles.rotation.x += 0.0002
        renderer.render(scene, camera)
    }
    animate()

    window.addEventListener('resize', () => {
        camera.aspect = container.clientWidth / container.clientHeight
        camera.updateProjectionMatrix()
        renderer.setSize(container.clientWidth, container.clientHeight)
    })
}

function destroyThree() {
    cancelAnimationFrame(animationId)
    renderer?.dispose()
}

// ========== ECharts 地球 ==========
onMounted(() => {
    initThree()

    chart = echarts.init(chartRef.value)
    chart.setOption({
        backgroundColor: 'transparent',
        tooltip: {
            trigger: 'item',
            backgroundColor: 'rgba(0, 0, 0, 0.75)',
            borderColor: '#409EFF',
            borderWidth: 1,
            textStyle: { color: '#fff', fontSize: 13 },
            formatter: (p) => `${p.name}<br/>用户: ${p.data.count} 人`
        },
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
                main: { intensity: 1.5, shadow: true, alpha: 40, beta: 30 },
                ambient: { intensity: 0.4 }
            },
            viewControl: {
                autoRotate: true,
                autoRotateSpeed: 1.2,
                targetCoord: [116, 35],
                minDistance: 110,
                maxDistance: 300,
                zoomSensitivity: 3,  
            },
            atmosphere: { show: true, offset: 3, color: '#409EFF', glowPower: 3 }
        },
        series: [
            // 保留原来的散点
            //   {
            //     type: 'scatter3D',
            //     coordinateSystem: 'globe',
            //     symbolSize: 4,
            //     itemStyle: { color: '#67C23A', borderColor: '#fff', borderWidth: 1 },
            //     data: [
            //       [116.4, 39.9, 0], [121.5, 31.2, 0], [114.1, 22.5, 0],
            //       [-74.0, 40.7, 0], [139.7, 35.7, 0], [-0.1, 51.5, 0], [151.2, -33.9, 0]
            //     ]
            //   },
            // 新的城市散点 - 全部贴地
            {
                type: 'scatter3D',
                coordinateSystem: 'globe',
                symbolSize: 8,
                symbol: 'circle',
                itemStyle: {
                    color: '#ffcc00',
                    borderColor: '#fff',
                    borderWidth: 1,
                    shadowBlur: 10,
                    shadowColor: '#ffcc00'
                },
                label: {
                    show: false
                },
                emphasis: {
                    label: {
                        show: false,
                    },
                    itemStyle: {
                        color: '#ffffff',      // 鼠标移入变白
                        shadowBlur: 20,
                        shadowColor: '#ffcc00'
                    },
                    scale: 2                 // 放大效果
                },
                data: [
                    { name: '北京', value: [116.4, 39.9, 0], count: 128 },
                    { name: '上海', value: [121.5, 31.2, 0], count: 96 },
                    { name: '深圳', value: [114.1, 22.5, 0], count: 74 },
                    { name: '成都', value: [104.1, 30.6, 0], count: 55 },
                    { name: '纽约', value: [-74.0, 40.7, 0], count: 32 },
                    { name: '伦敦', value: [-0.1, 51.5, 0], count: 28 },
                    { name: '东京', value: [139.7, 35.7, 0], count: 41 },
                    { name: '悉尼', value: [151.2, -33.9, 0], count: 15 },
                ]
            }
        ]
    })
    // 监听容器尺寸变化（弹窗打开时触发）
    const observer = new ResizeObserver(() => {
        chart?.resize()
    })
    observer.observe(chartRef.value)
    window.addEventListener('resize', () => chart?.resize())
})

function generateFlightData() {
    const cities = [[116.4, 39.9], [121.5, 31.2], [-74.0, 40.7], [139.7, 35.7], [-0.1, 51.5]]
    const lines = []
    for (let i = 0; i < cities.length; i++) {
        for (let j = i + 1; j < cities.length; j++) {
            if (Math.random() > 0.5) {
                lines.push({ coords: [[cities[i][0], cities[i][1], 2], [cities[j][0], cities[j][1], 2]] })
            }
        }
    }
    return lines
}

onUnmounted(() => {
    chart?.dispose()
    destroyThree()
})
</script>

<style scoped>
.globe-wrapper {
    position: relative;
    width: 100%;
    aspect-ratio: 16 / 10;
    overflow: hidden;
    border-radius: 14px;
}

.three-local {
    position: absolute;
    inset: 0;
    z-index: 0;
    background: radial-gradient(ellipse at center, #0a0f1e 0%, #020408 100%);
}

.globe-box {
    position: absolute;
    inset: 0;
    z-index: 1;
}
</style>