from time import sleep
from digitemp.master import UART_Adapter
from digitemp.device import DS18B20
import random


class TemperatureMonitor:
    def __init__(self, cbfunc):
        self.cbfunc = cbfunc
        # self.bus = UART_Adapter('/dev/ttyUSB0')
        # self.sensor = DS18B20(self.bus)

    def check_temp(self):
        cur_temp = self.sensor.get_temperature()
        if cur_temp > 50:
            self.cbfunc()

    async def monitor(self):
        while True:
            # self.check_temp()
            sleep(5)
            await self.cbfunc()
