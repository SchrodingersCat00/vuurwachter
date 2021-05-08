from time import sleep
from digitemp.master import UART_Adapter
from digitemp.device import DS18B20
import random
import asyncio
import logging


class TemperatureMonitor:
    def __init__(self):
        self.bus = UART_Adapter('/dev/ttyUSB0')
        self.sensor = DS18B20(self.bus)
        self.listeners = []

    def register_listener(self, listener):
        # A listener has a on_notify(new_temp) async function
        self.listeners.append(listener)

    def unregister_listener(self, listener):
        self.listeners.remove(listener)

    async def notify_listeners(self):
        cur_temp = self.sensor.get_temperature()
        # f = open('afile', 'r')
        # cur_temp = int(f.readline().strip())
        # f.close()
        self.cur_temp = cur_temp
        logging.info(f'Temperature is: {cur_temp}')
        await asyncio.gather(
            *(l.on_notify(cur_temp) for l in self.listeners)
        )

    async def monitor(self):
        while True:
            await asyncio.gather(
                self.notify_listeners(),
                asyncio.sleep(10)
            )
