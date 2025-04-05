import discord
import os
from dotenv import load_dotenv

from server import server_thread

load_dotenv()

TOKEN = os.getenv("TOKEN")
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
client = discord.Client(intents=intents)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

# Koyeb用 サーバー立ち上げ
server_thread()
client.run(TOKEN)