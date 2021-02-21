# bot.py
import os
import time
import discord
import threading
from dotenv import load_dotenv
from temp_monitor import TemperatureMonitor
import asyncio

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

async def send_alert(temp):
    global is_ready
    if not is_ready:
        raise ValueError('Discord not ready')

    await channel.send(f'Temperature too high!\nTemperature is: {temp}')

@client.event
async def on_ready():
    global is_ready
    global channel
    is_ready = True
    print(f'{client.user} has connected to Discord!')
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    for channel in guild.channels:
        if channel.name == 'develop':
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

async def main():
    monitor = TemperatureMonitor(send_alert)
    discord_task = loop.create_task(client.start(TOKEN))
    print_task = loop.create_task(monitor.monitor())
    await asyncio.wait([print_task, discord_task])

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()