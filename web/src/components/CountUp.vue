<template>
  <span ref="countRef">{{ displayValue }}</span>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'

const props = defineProps({
  endVal: { type: Number, default: 0 },
  duration: { type: Number, default: 1.5 }
})

const countRef = ref(null)
const displayValue = ref(0)

function animate() {
  const startTime = Date.now()
  const startVal = displayValue.value
  const diff = props.endVal - startVal

  function tick() {
    const elapsed = (Date.now() - startTime) / 1000
    const progress = Math.min(elapsed / props.duration, 1)
    // easeOutCubic
    const eased = 1 - Math.pow(1 - progress, 3)
    displayValue.value = Math.round(startVal + diff * eased)
    if (progress < 1) requestAnimationFrame(tick)
  }
  requestAnimationFrame(tick)
}

onMounted(() => animate())
watch(() => props.endVal, () => animate())
</script>