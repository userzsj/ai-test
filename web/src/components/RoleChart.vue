<template>
  <div ref="chartRef" class="chart-box"></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'

const chartRef = ref(null)
let chart = null

onMounted(() => {
  chart = echarts.init(chartRef.value)

  const option = {
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(255,255,255,0.95)',
      borderColor: '#e8e8e8',
      textStyle: { color: '#333', fontSize: 13 }
    },
    legend: {
      bottom: 10,
      textStyle: { color: '#666', fontSize: 12 }
    },
    series: [
      {
        name: '角色分布',
        type: 'pie',
        radius: ['55%', '78%'],
        center: ['50%', '47%'],
        avoidLabelOverlap: false,
        itemStyle: { borderRadius: 4, borderColor: '#fff', borderWidth: 3 },
        label: { show: false },
        emphasis: {
          label: { show: true, fontSize: 16, fontWeight: 'bold' },
          scaleSize: 8
        },
        data: [
          { value: 95, name: '普通用户', itemStyle: { color: '#409EFF' } },
          { value: 18, name: '管理员', itemStyle: { color: '#67C23A' } },
          { value: 8, name: 'VIP 用户', itemStyle: { color: '#E6A23C' } }
        ]
      }
    ]
  }

  chart.setOption(option)
  window.addEventListener('resize', () => chart?.resize())
})

onUnmounted(() => {
  chart?.dispose()
})
</script>

<style scoped>
.chart-box {
  width: 100%;
  height: 280px;
}
</style>