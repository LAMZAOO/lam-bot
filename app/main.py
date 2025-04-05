import discord
import os
import asyncio
import aiohttp
from dotenv import load_dotenv

from app.server import server_thread

# 環境に応じた.envファイルを選択
env_type = os.getenv("ENV", "local")
load_dotenv(f".env.{env_type}")

TOKEN = os.getenv("TOKEN")
PING_URL = os.getenv("PING_URL")

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
client = discord.Client(intents=intents)

async def ping_self():
    await client.wait_until_ready()
    async with aiohttp.ClientSession() as session:
        while not client.is_closed():
            if PING_URL:
                try:
                    async with session.get(PING_URL) as res:
                        print(f"[PING] Sent to {PING_URL} | Status: {res.status}")
                except Exception as e:
                    print(f"[PING ERROR] {e}")
            else:
                print("[PING] No PING_URL set")
            await asyncio.sleep(180)  # 3分おき

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")
    client.loop.create_task(ping_self())

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

# Web サーバー起動 (Koyeb維持用)
server_thread()

# Bot 実行
try:
    client.run(TOKEN)
except Exception as e:
    print(f"[BOT ERROR] {e}")
    import time
    while True:
        time.sleep(60)