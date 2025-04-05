import sys
import os
import asyncio
import aiohttp
import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord import Intents

from app.server import server_thread
from app.logging_config import setup_logger

sys.dont_write_bytecode = True

logger = setup_logger(__name__)

# 環境変数のロード
if os.getenv("ENV", "local") == "production":
    load_dotenv(".env.production")
else:
    load_dotenv(".env.local")

TOKEN = os.getenv("TOKEN")
PING_URL = os.getenv("PING_URL")

# Botの初期化
intents = Intents.default()
intents.message_content = True
intents.voice_states = True
bot = commands.Bot(command_prefix=")", intents=intents)

async def send_ping():
    await bot.wait_until_ready()
    while not bot.is_closed():
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(PING_URL) as response:
                    logger.info(f"[PING] Sent to {PING_URL} | Status: {response.status}")
        except Exception as e:
            logger.error(f"[PING] Failed: {e}")
        await asyncio.sleep(180)

@bot.event
async def on_ready():
    logger.info(f"✅ Logged in as {bot.user}")
    bot.loop.create_task(send_ping())

    try:
        dev_guild_id = os.getenv("DEV_GUILD_ID")
        if dev_guild_id:
            guild = discord.Object(id=int(dev_guild_id))
            synced = await bot.tree.sync(guild=guild)
            logger.info(f"✅ Synced {len(synced)} commands to guild {dev_guild_id}.")
        else:
            synced = await bot.tree.sync()
            logger.info(f"✅ Synced {len(synced)} global commands.")
    except Exception as e:
        logger.error(f"❌ Sync failed: {e}")

async def load_extensions():
    await bot.load_extension("app.commands.view_option")
    await bot.load_extension("app.commands.character_select")

# サーバー起動
server_thread()

# Bot起動
async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

try:
    loop.run_until_complete(main())
except Exception:
    logger.exception(f"❌ {bot.user} stopped with error")
    raise