import time

import serial
from serial import SerialException
from serial.tools import list_ports
import threading
from queue import Queue


class Serial:
    def __init__(self):
        self._serial = None
        self._queue = None

    @staticmethod
    def get_usable_ports():
        return [p.__dict__.get("name") for p in list_ports.comports()]

    def open(self, port, baudrate, timeout=None):
        print(port, baudrate)
        self._serial = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
        self._queue = Queue()
        threading.Thread(target=self.listen, daemon=True).start()

    def close(self):
        s = self._serial
        s.flushInput()
        s.flushOutput()
        self._serial = None
        time.sleep(0.2)
        s.close()

    def listen(self):
        if not self._serial or not self._serial.is_open:
            self._queue.put("串口未打开！")
            return
        while self._serial and self._serial.is_open:
            try:
                data = self._serial.readline().decode()
                self._queue.put(data.strip())
                continue
            except UnicodeDecodeError:
                self._queue.put("串口数据解码异常，请检查波特率是否匹配/数据是否太长被截断")
            except SerialException as e:
                self._queue.put(f"串口异常，{str(e)}")
            except Exception as e:
                self._queue.put(str(e))

    def read(self):
        result = []
        while not self._queue.empty():
            result.append(self._queue.get())
        return result

    def write(self, data):
        try:
            if self._serial and self._serial.is_open:
                self._serial.write(data.encode())
                self._serial.flushOutput()
            else:
                raise Exception("请先打开串口！")
        except Exception as e:
            raise Exception(f"串口数据发送失败：{str(e)}")


if __name__ == "__main__":
    s = Serial()
    print(s.get_usable_ports())
    s.open("COM4", 9600)
    s.read()
    time.sleep(3)
