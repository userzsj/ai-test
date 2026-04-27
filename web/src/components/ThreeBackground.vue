<template>
    <div ref="canvasContainer" :class="['three-container', mode === 'inline' ? 'three-inline' : 'three-full']"></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import * as THREE from 'three'
const props = defineProps({
    // 'full' = 全屏固定定位，'inline' = 宽高 100% 跟随父容器
    mode: { type: String, default: 'full' },
})
const canvasContainer = ref(null)
let scene, camera, renderer, particles
let mouseX = 0, mouseY = 0
let animationId

const initThree = () => {
    const container = canvasContainer.value
    const width = window.innerWidth
    const height = window.innerHeight

    // 场景
    scene = new THREE.Scene()
    scene.background = new THREE.Color(0x0a0a1a)

    // 相机
    camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000)
    camera.position.z = 30

    // 渲染器
    renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true })
    renderer.setSize(width, height)
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
    container.appendChild(renderer.domElement)

    // 创建粒子
    const particlesGeometry = new THREE.BufferGeometry()
    const particlesCount = 2000
    const posArray = new Float32Array(particlesCount * 3)
    const colorArray = new Float32Array(particlesCount * 3)

    for (let i = 0; i < particlesCount * 3; i += 3) {
        // 位置 - 分布在球形空间内
        const radius = 50
        const theta = Math.random() * Math.PI * 2
        const phi = Math.acos((Math.random() * 2) - 1)

        posArray[i] = Math.sin(phi) * Math.cos(theta) * radius
        posArray[i + 1] = Math.sin(phi) * Math.sin(theta) * radius
        posArray[i + 2] = Math.cos(phi) * radius

        // 颜色 - 蓝紫色系
        const color = new THREE.Color()
        const hue = 0.6 + Math.random() * 0.3 // 蓝到紫
        const saturation = 0.5 + Math.random() * 0.5
        const lightness = 0.5 + Math.random() * 0.5
        color.setHSL(hue, saturation, lightness)

        colorArray[i] = color.r
        colorArray[i + 1] = color.g
        colorArray[i + 2] = color.b
    }

    particlesGeometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3))
    particlesGeometry.setAttribute('color', new THREE.BufferAttribute(colorArray, 3))

    const particlesMaterial = new THREE.PointsMaterial({
        size: 0.15,
        vertexColors: true,
        transparent: true,
        blending: THREE.AdditiveBlending,
        depthWrite: false
    })

    particles = new THREE.Points(particlesGeometry, particlesMaterial)
    scene.add(particles)

    // 添加一些更大的星星
    const starGeometry = new THREE.BufferGeometry()
    const starCount = 100
    const starPosArray = new Float32Array(starCount * 3)

    for (let i = 0; i < starCount * 3; i += 3) {
        const radius = 55
        const theta = Math.random() * Math.PI * 2
        const phi = Math.acos((Math.random() * 2) - 1)

        starPosArray[i] = Math.sin(phi) * Math.cos(theta) * radius
        starPosArray[i + 1] = Math.sin(phi) * Math.sin(theta) * radius
        starPosArray[i + 2] = Math.cos(phi) * radius
    }

    starGeometry.setAttribute('position', new THREE.BufferAttribute(starPosArray, 3))
    const starMaterial = new THREE.PointsMaterial({
        size: 0.35,
        color: 0xffffff,
        transparent: true,
        blending: THREE.AdditiveBlending,
        depthWrite: false
    })

    const stars = new THREE.Points(starGeometry, starMaterial)
    scene.add(stars)

    // 鼠标移动监听
    window.addEventListener('mousemove', onMouseMove)
    window.addEventListener('resize', onWindowResize)
}

const onMouseMove = (event) => {
    mouseX = (event.clientX / window.innerWidth) * 2 - 1
    mouseY = -(event.clientY / window.innerHeight) * 2 + 1
}

const onWindowResize = () => {
    camera.aspect = window.innerWidth / window.innerHeight
    camera.updateProjectionMatrix()
    renderer.setSize(window.innerWidth, window.innerHeight)
}

const animate = () => {
    animationId = requestAnimationFrame(animate)

    // 自动旋转
    particles.rotation.y += 0.0002
    particles.rotation.x += 0.0001

    // 鼠标跟随效果
    camera.position.x += (mouseX * 5 - camera.position.x) * 0.01
    camera.position.y += (mouseY * 5 - camera.position.y) * 0.01
    camera.lookAt(scene.position)

    renderer.render(scene, camera)
}

onMounted(() => {
    initThree()
    animate()
})

onUnmounted(() => {
    window.removeEventListener('mousemove', onMouseMove)
    window.removeEventListener('resize', onWindowResize)
    if (animationId) cancelAnimationFrame(animationId)
    if (renderer) renderer.dispose()
})
</script>

<style scoped>
.three-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 0;
}

.three-inline {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
  pointer-events: none;      /* 不挡住鼠标交互 */
}
</style>