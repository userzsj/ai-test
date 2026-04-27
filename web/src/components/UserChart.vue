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
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      backgroundColor: 'rgba(255,255,255,0.95)',
      borderColor: '#e8e8e8',
      textStyle: { color: '#333', fontSize: 13 }
    },
    grid: { top: 50, right: 20, bottom: 30, left: 50 },
    xAxis: {
      type: 'category',
      data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日'],
      axisLine: { lineStyle: { color: '#e8e8e8' } },
      axisLabel: { color: '#999', fontSize: 12 }
    },
    yAxis: {
      type: 'value',
      splitLine: { lineStyle: { color: '#f5f5f5' } },
      axisLabel: { color: '#999', fontSize: 12 }
    },
    series: [
      {
        name: '新增用户',
        type: 'bar',
        data: [5, 8, 12, 7, 15, 20, 18],
        itemStyle: {
          borderRadius: [6, 6, 0, 0],
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#409EFF' },
            { offset: 1, color: '#a0cfff' }
          ])
        },
        emphasis: {
          itemStyle: { color: '#337ecc' }
        },
        barWidth: '40%'
      },
      {
        name: '活跃用户',
        type: 'line',
        smooth: true,
        data: [30, 45, 38, 55, 48, 62, 70],
        lineStyle: { color: '#67C23A', width: 2 },
        itemStyle: { color: '#67C23A' },
        symbol: 'circle',
        symbolSize: 6
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