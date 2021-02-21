from time import sleep
from digitemp.master import UART_Adapter
from digitemp.device import DS18B20
import random
import asyncio


class TemperatureMonitor:
    def __init__(self, cbfunc):
        self.cbfunc = cbfunc # asyncio task
        self.bus = UART_Adapter('/dev/ttyUSB0')
        self.sensor = DS18B20(self.bus)

    async def check_temp(self):
        cur_temp = self.sensor.get_temperature()
        if cur_temp > 23:
            await self.cbfunc(cur_temp)
        print(cur_temp)

    async def monitor(self):
        while True:
            await asyncio.sleep(3)
            await self.check_temp()
