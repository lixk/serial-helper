# -*- coding: utf-8 -*-
"""使用JS API调用Python函数"""

import webview
from serialutils import Serial
import time
from queue import Queue
from dataclasses import dataclass, asdict

@dataclass
class Response:
    code: int = 0
    msg: str = ""
    data: object = None

    def todict(self):
        return asdict(self)


class Api:
    def __init__(self):
        self.cancel_heavy_stuff_flag = False
        self._serial = None
        self.received_queue = Queue()

    def get_usable_ports(self):
        ports = [{"value": p, "text": p} for p in Serial.get_usable_ports()]
        if not ports:
            ports = [{"value": "", "text": "没有可用串口"}]
        return ports

    def open_serial(self, port, baudrate):
        if not port:
            return Response(1, "请检查串口设备连接是否正常！").todict()
        try:
            self._serial = Serial()
            self._serial.open(port=port, baudrate=baudrate)
        except Exception as e:
            print(e)
            return Response(1, str(e)).todict()
        return Response(msg="串口打开成功！").todict()

    def read_serial_data(self):
        data = self._serial.read()
        if not data:
            time.sleep(0.1)
        print(data)
        return data

    def send_serial_data(self, data):
        if not self._serial:
            return Response(1, '请先打开串口！').todict()
        try:
            self._serial.write(data)
        except Exception as e:
            return Response(1, str(e)).todict()
        return Response(msg="发送成功！").todict()

    def close_serial(self):
        try:
            self._serial.close()
        except Exception as e:
            return Response(1, f"串口关闭异常：{str(e)}").todict()
        return Response(msg="串口已关闭！").todict()


if __name__ == "__main__":
    api = Api()
    webview.create_window(
        "串口小助手   作者：浅醉樱花雨 1749498702@qq.com",
        url="ui/dist/index.html",
        js_api=api,
        width=1200,
        height=800,
        min_size=(1000, 600),
    )
    webview.start(debug=False)
