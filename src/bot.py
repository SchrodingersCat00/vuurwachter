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

async def send_alert():
    global is_ready
    if not is_ready:
        raise ValueError('Discord not ready')

    await channel.send('Hello world!')

is_ready = None
channel = None


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

def between_callback():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    temp_monitor = TemperatureMonitor(send_alert)
    loop.run_until_complete(temp_monitor.monitor())
    loop.close()

# t = threading.Thread(target=between_callback)
# t.start()
temp_monitor = TemperatureMonitor(send_alert)
temp_monitor.monitor()
client.run(TOKEN)