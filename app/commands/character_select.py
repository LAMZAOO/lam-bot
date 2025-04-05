import discord
import os
import asyncio
from discord import app_commands
from discord.ext import commands

from app.commands.utils.load_characters import load_characters

ENV = os.getenv("ENV", "local")
DEV_GUILD_ID = os.getenv("DEV_GUILD_ID")

class CharacterDropdown(discord.ui.Select):
    def __init__(self):
        characters = load_characters()
        options = [
            discord.SelectOption(label=char["name"], description=char["description"])
            for char in characters
        ]
        super().__init__(
            placeholder="キャラクターを選んでください",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"✅ あなたは `{self.values[0]}` を選びました！", ephemeral=True
        )

class CharacterSelectView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)  # Optional: 無限に表示したいなら
        self.add_item(CharacterDropdown())

class CharacterSelect(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="character_select", description="キャラクターを選びます")
    async def character_select(self, interaction: discord.Interaction):
        # 即時返答が必要なら defer() する
        await interaction.response.defer(ephemeral=True)
        await asyncio.sleep(0.2)  # 軽く待ってもOK（データ処理の余裕）
        await interaction.followup.send(
            "🔽 キャラクターを選んでください：", view=CharacterSelectView(), ephemeral=True
        )

    async def cog_load(self):
        # コマンドを手動で登録（ギルド or グローバル）
        if ENV != "production" and DEV_GUILD_ID:
            guild = discord.Object(id=int(DEV_GUILD_ID))
            self.bot.tree.add_command(self.character_select, guild=guild)
        else:
            self.bot.tree.add_command(self.character_select)

async def setup(bot: commands.Bot):
    await bot.add_cog(CharacterSelect(bot))