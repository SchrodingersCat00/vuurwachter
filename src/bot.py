# bot.py
import asyncio
import logging
import os
import threading
import time

import discord
from dotenv import load_dotenv

from discord_notifier import DiscordNotifier
from file_logger import FileLogger
from temp_monitor import TemperatureMonitor

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

async def send_alert(msg):
    global is_ready
    if not is_ready:
        raise ValueError('Discord not ready')

    await channel.send(msg)

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

def main():
    monitor = TemperatureMonitor()
    flogger = FileLogger()
    disc_notifier = DiscordNotifier(send_alert)
    monitor.register_listener(flogger)
    monitor.register_listener(disc_notifier)
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(
                client.start(TOKEN),
                monitor.monitor()
            ),
        )
    except KeyboardInterrupt:
        loop.run_until_complete(client.close())
        # cancel all tasks lingering
    finally:
        loop.close()


if __name__ == '__main__':
    main()
