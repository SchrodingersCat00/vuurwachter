# bot.py
import os
import time
import discord
import threading
from dotenv import load_dotenv
from temp_monitor import TemperatureMonitor
import asyncio
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s,%(msecs)d %(levelname)s: %(message)s",
    datefmt="%H:%M:%S",
)


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()
is_ready = None

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

def handle_exception(loop, context):
    # context["message"] will always be there; but context["exception"] may not
    msg = context.get("exception", context["message"])
    logging.error(f"Caught exception: {msg}")
    logging.info("Shutting down...")
    asyncio.create_task(shutdown(loop))

async def shutdown(loop, signal=None):
    """Cleanup tasks tied to the service's shutdown."""
    if signal:
        logging.info(f"Received exit signal {signal.name}...")
    logging.info("Closing database connections")

async def main():
    monitor = TemperatureMonitor(send_alert)
    discord_task = loop.create_task(client.start(TOKEN))
    print_task = loop.create_task(monitor.monitor())
    await asyncio.wait([print_task, discord_task])

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.set_exception_handler(handle_exception)
    loop.run_until_complete(main())
    loop.close()