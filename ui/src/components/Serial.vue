<script setup>
import { ref } from 'vue'
import bus from './eventBus'

const portList = ref([])
// 波特率
const baudrateList = ref([
  { value: 4800, text: "4800" },
  { value: 9600, text: "9600" },
  { value: 19200, text: "19200" },
  { value: 38400, text: "38400" },
  { value: 57600, text: "57600" },
  { value: 115200, text: "115200" },
])
const portValue = ref(null)
const baudrateValue = ref(null)
const serialButtonText = ref('打开')
const receiveData = ref('')
const sendData = ref('')
const lineChartState = ref(false)
const flyControlState = ref(false)
const serialDataList = ref([])


// 设置可用串口
function setUsablePorts() {
  pywebview.api.get_usable_ports().then(function (data) {
    portList.value = data
  })
}

// 点击串口按钮
function serialButtonToggleClick() {
  if (serialButtonText.value == '打开') {
    openSerial()
  } else {
    closeSerial()
  }
}

// 点击重置按钮
function serialButtonReset() {
  serialDataList.value = []
  receiveData.value = ''
}

// 点击发送按钮
function serialButtonSendClick() {
  if (sendData.value == '') {
    return
  }
  pywebview.api.send_serial_data(sendData.value).then(function (data) {
    if (data.code == 0) {
      updateDataPanel('<- ' + sendData.value)
      sendData.value = ''
    } else {
      updateDataPanel(data.msg)
    }
  })
}

// 打开串口
function openSerial() {
  pywebview.api.open_serial(portValue.value, baudrateValue.value).then(function (data) {
    updateDataPanel(data.msg)
    if (data.code == 0) {
      serialButtonText.value = '关闭'
      // 读取串口数据
      readSerialData()
    }
  })
}

// 关闭串口
function closeSerial() {
  pywebview.api.close_serial().then(function (data) {
    if (data.code == 0) {
      serialButtonText.value = '打开'
    }
    updateDataPanel(data.msg)
  })
}
// 更新数据面板
function updateDataPanel(...dataItems) {
  serialDataList.value.push(...dataItems)
  while (serialDataList.value.length > 200) {
    serialDataList.value.shift()
  }
  receiveData.value = serialDataList.value.join('\n')
  const textarea = document.getElementById('receiveData')
  setTimeout(function () { textarea.scrollTop = textarea.scrollHeight }, 10)
}

// 读取串口数据
function readSerialData() {
  pywebview.api.read_serial_data().then(function (dataItems) {
    handlerData(dataItems)
    // 轮询串口数据
    if (serialButtonText.value == '关闭') {
      setTimeout(readSerialData, 100)
    }
  })
}

function handlerData(dataItems) {
  if (dataItems.length == 0) {
    return
  }
  // 更新数据面板
  for (var i in dataItems) {
    serialDataList.value.push('-> ' + dataItems[i])
  }
  updateDataPanel()

  // 发送数据到数据曲线
  if (lineChartState.value) {
    for (var i in dataItems) {
      bus.emit("lineChartData", parseDataItem(dataItems[i]))
    }
  }
  // 发送数据到飞控模拟
  if (flyControlState.value) {
    for (var i in dataItems) {
      bus.emit("flyControlData", parseDataItem(dataItems[i]))
    }
  }
}

// 解析数据，格式："x=1, y=2, z=3"
function parseDataItem(data) {
  var rsp = {}
  var parts = data.split(',')
  for (var i = 0; i < parts.length; i++) {
    var kv = parts[i].split('=')
    if (kv.length == 2) {
      rsp[kv[0].trim()] = kv[1].trim()
    }
  }
  return rsp
}

</script>

<template>
  <Layout>
    <LayoutPanel region="north" title="" :split=false style="width: 100%; padding: 20px;" :border=false>
      <!-- <Panel title="" :bodyStyle="{ padding: '20px' }"> -->
      串口:&nbsp;<ComboBox inputId="port" v-model="portValue" :data="portList" style="width: 120px;"
        @click="setUsablePorts"></ComboBox>
      <!-- <Label for="baudrate" align="right" style="width: auto;">&nbsp;&nbsp;&nbsp;&nbsp;波特率：</Label> -->
      &nbsp;&nbsp;&nbsp;波特率:&nbsp;<ComboBox inputId="baudrate" v-model="baudrateValue" :data="baudrateList"
        style="width: 120px;"></ComboBox>
      &nbsp;&nbsp;<LinkButton iconCls="icon-ok" @click="serialButtonToggleClick">{{ serialButtonText }}</LinkButton>
      &nbsp;&nbsp;<LinkButton iconCls="icon-reload" @click="serialButtonReset">清空数据</LinkButton>
      <!-- </Panel> -->
    </LayoutPanel>
    <LayoutPanel region="center" title="接收数据" :split=false style="height: 100%;" :border=false>
      <!-- <Panel title="接收数据" :bodyStyle="{ padding: '0px' }" style="height: 500px;"> -->
      <!-- <Label for="receiveData" align="top">接收数据：</Label> -->
      <TextBox inputId="receiveData" :multiline="true" :editable="false" v-model="receiveData"
        style="border-width: 0px;width: 100%;height: 100%;">
      </TextBox>
      <!-- </Panel> -->

    </LayoutPanel>
    <LayoutPanel region="south" title="" :split=false :border=false>
      <Panel title="发送数据" :bodyStyle="{ padding: '0px' }" :border=false>
        <!-- <Label for="sendData" align="top">发送数据：</Label> -->
        <TextBox inputId="sendData" :multiline="true" v-model="sendData"
          style="width: calc(100% - 90px); height: 70px; border-width: 0px" placeholder="输入数据"></TextBox>
        <LinkButton btnCls="c1" iconCls="icon-large-smartart" style="width: 70px;height: 70px;margin: 5px 10px;" size="large" iconAlign="top"
          @click="serialButtonSendClick">
          发送</LinkButton>
      </Panel>
      <Panel title="辅助工具" :bodyStyle="{ padding: '20px' }" :border=false>
        <div style="color: greenyellow;">
        数据曲线：<SwitchButton class="rounded" v-model="lineChartState" onText="开启" offText="关闭"></SwitchButton>
        &nbsp&nbsp
        <span style="font-size: 20;color: #ada;border: 1px dotted greenyellow;padding: 3px;">数据格式："x=1,y=2,z=3"</span>
        <br><br>
        飞控调试：<SwitchButton class="rounded" v-model="flyControlState" onText="开启" offText="关闭"></SwitchButton>
        &nbsp&nbsp
        <span style="font-size: 20;color: #ada;border: 1px dotted greenyellow;padding: 3px;">数据格式："x=1,y=2,z=3"，x/y/z为各轴向旋转角度</span>
        <br><br>
        <!-- 关于作者：<SwitchButton class="rounded" v-model="flyControlState" onText="开启" offText="关闭"></SwitchButton>
        &nbsp&nbsp
        <span style="font-size: 20;color: #ada;border: 1px dotted greenyellow;padding: 3px;">数据格式："x=1,y=2,z=3"，x/y/z为各轴向旋转角度</span> -->
      </div>
      </Panel>
    </LayoutPanel>
  </Layout>
</template>
<style>
#receiveData,
#sendData {
  background-color: rgb(54, 56, 54);
  color: #fbfcfb;
  border-radius: 0px;
}

.rounded.switchbutton {
  border-radius: 30px;
}

.switchbutton-on {
  background-color: rgb(137, 206, 27);
}

.switchbutton-off {
  background-color: rgba(192, 184, 181, 0.457);
}

.rounded.switchbutton .switchbutton-handle {
  border-radius: 30px;
}
</style>