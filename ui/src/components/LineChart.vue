<script setup>
import { onMounted } from 'vue'
import * as echarts from 'echarts'
import bus from './eventBus'


var inited = false
var chartContainer
var chart
var chartWidth = 0
var chartHeight = 0

var option = {
  animation: false,
  silent: true,
  tooltip: {
    trigger: 'axis',
    animation: false,
    axisPointer: {
      animation: false
    }
  },
  legend: {
    data: []
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true
  },
  toolbox: {
    feature: {
      // saveAsImage: {}
    }
  },
  xAxis: {
    type: 'category',
    boundaryGap: false
  },
  yAxis: {
    type: 'value'
  },
  series: []
};

onMounted(() => {
  bus.on("lineChartData", function (dataItem) {
    // console.log("lineChartData:", dataItem)
    // 初始化
    if (!inited) {
      init()
    }

    // 当前已存在的曲线名称
    var curLineNames = option.series.map(item => item.name)
    // 提取数据曲线名称
    var newLineNames = Object.keys(dataItem)
    // 移除已经不存在的曲线
    option.series = option.series.filter(item => newLineNames.includes(item.name))
    // 设置legend
    option.legend.data = newLineNames
    // 添加还不存在的曲线
    for (var lineName in dataItem) {
      if (!curLineNames.includes(lineName)) {
        option.series.push({
          name: lineName,
          type: 'line',
          smooth: false,
          showSymbol: false,
          data: new Array(200).fill(0)
        })
      }
    }

    // 添加数据
    for (var i in option.series) {
      var serial = option.series[i]
      serial.data.shift()
      serial.data.push(dataItem[serial.name] || 0)
    }
  })
})

// 初始化
function init() {
  inited = true
  console.log('init line chart')
  // 创建图表实例
  chartContainer = document.getElementById("lineChart")
  chartContainer.parentElement.style.overflow = 'hidden'
  // var width = chartContainer.parentElement.clientWidth
  // var height = chartContainer.parentElement.clientHeight
  chart = echarts.init(chartContainer, 'dark')
  // 定时刷新
  refreshChart()

}

function refreshChart() {
  var width = chartContainer.parentElement.clientWidth
  var height = chartContainer.parentElement.clientHeight
  if (chartWidth != width || chartHeight != height) {
    console.log("width", width, "height: ", height)
    chartWidth = width
    chartHeight = height
    chart.resize({ width: chartWidth, height: chartHeight })
  }
  // Draw the chart
  chart.setOption(option)
  setTimeout(refreshChart, 200)
}
</script> 

<template>
  <!-- <div>{{ props.chartData }}</div> -->
  <div id="lineChart"></div>
</template>
