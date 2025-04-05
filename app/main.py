import discord
import os
import asyncio
import aiohttp
from dotenv import load_dotenv
import time

from app.server import server_thread
from app.logging_config import setup_logger

# ロガー初期化
logger = setup_logger(__name__)

# 環境に応じた.envファイルを選択
if os.getenv("ENV", "local") == "production":
    load_dotenv(".env.production")
else:
    load_dotenv(".env.local")

TOKEN = os.getenv("TOKEN")
PING_URL = os.getenv("PING_URL")

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
client = discord.Client(intents=intents)

async def send_ping():
    await client.wait_until_ready()
    while not client.is_closed():
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(PING_URL) as response:
                    logger.info(f"[PING] Sent to {PING_URL} | Status: {response.status}")
        except Exception as e:
            logger.error(f"[PING] Failed: {e}")
        await asyncio.sleep(180)

@client.event
async def on_ready():
    logger.info(f"✅ Logged in as {client.user}")
    client.loop.create_task(send_ping())

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

# サーバー起動
server_thread()

# Bot起動（例外をキャッチして原因をログ出力）
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

try:
    loop.run_until_complete(client.start(TOKEN))
except Exception:
    logger.exception("❌ Discord client stopped with error")
    while True:
        time.sleep(60)