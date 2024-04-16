<template>
  <Layout style="height:100vh;">
    <LayoutPanel region="west" title="串口设置" :split=true style="min-width: 600px;max-width: 800px;">
      <Serial></Serial>
    </LayoutPanel>
    <LayoutPanel region="center" :border=false style="height:100%;">
      <Layout>
        <LayoutPanel region="center" id="lineChart" title="数据曲线" style="height:100%">
          <LineChart></LineChart>
        </LayoutPanel>
        <LayoutPanel region="south" id="flyControl" title="飞控调试" :split=true :collapsible=true :expander=true
          style="min-height:360px;max-height:600px;">
          <FlyControl></FlyControl>
        </LayoutPanel>
      </Layout>
    </LayoutPanel>
  </Layout>
</template>


<script setup>
import { onMounted } from 'vue'
import LineChart from './components/LineChart.vue'
import FlyControl from './components/FlyControl.vue'
import Serial from './components/Serial.vue'
import bus from './components/eventBus'
onMounted(() => {
  document.body.style = "margin:0;padding:0;background-image: url('/static/bg.png');background-repeat: no-repeat; background-size: cover;"
})
window.onresize = function(e){
  console.log('window resize')
}
</script>