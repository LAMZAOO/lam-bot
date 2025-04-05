import discord
from discord.ext import commands
from discord import app_commands

from app.commands.character_select import CharacterSelectView
from app.commands.harmony_select import HarmonySelectView
from app.output.show_character_status import show_character_status

class CalcStatus(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="calc_status", description="キャラとハーモニーからステータスを算出します")
    async def calc_status(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        # キャラ選択後の処理
        async def on_character_selected(interaction, selected_character):
            await interaction.response.send_message(
                f"✅ `{selected_character}` を選びました！次にハーモニーを選んでください：",
                view=HarmonySelectView(selected_character, on_harmony_selected),
                ephemeral=True
            )

        # ハーモニー選択後の処理
        async def on_harmony_selected(interaction, selected_character, selected_harmony):
            await interaction.response.send_message(
                f"🎉 `{selected_harmony}` を選びました！ ステータスを計算中...",
                ephemeral=True
            )
            await show_character_status(interaction, selected_character, selected_harmony)

        # 最初にキャラ選択を表示
        await interaction.followup.send(
            "🔽 キャラクターを選んでください：",
            view=CharacterSelectView(on_character_selected),
            ephemeral=True
        )

    async def cog_load(self):
        from os import getenv
        DEV_GUILD_ID = getenv("DEV_GUILD_ID")
        if DEV_GUILD_ID:
            guild = discord.Object(id=int(DEV_GUILD_ID))
            self.bot.tree.add_command(self.calc_status, guild=guild)
        else:
            self.bot.tree.add_command(self.calc_status)

async def setup(bot: commands.Bot):
    await bot.add_cog(CalcStatus(bot))