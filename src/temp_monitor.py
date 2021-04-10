from time import sleep
from digitemp.master import UART_Adapter
from digitemp.device import DS18B20
import random
import asyncio
import logging


class TemperatureMonitor:
    def __init__(self, cbfunc):
        self.cbfunc = cbfunc # asyncio task
        self.bus = UART_Adapter('/dev/ttyUSB0')
        self.sensor = DS18B20(self.bus)

    async def check_temp(self):
        cur_temp = self.sensor.get_temperature()
        logging.info(f'Temperature is: {cur_temp}')
        if cur_temp > 75:
            try:
                await self.cbfunc(cur_temp)
            except ValueError:
                logging.warning(f'Temperature is too high but discord is not initialized yet!')

    async def monitor(self):
        while True:
            await asyncio.gather(
                self.check_temp(),
                asyncio.sleep(3)
            )