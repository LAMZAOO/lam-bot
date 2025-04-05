import discord
from discord import app_commands
from discord.ext import commands

class SelectDropdown(discord.ui.Select):
    def __init__(self, option: str):
        if option == "fruits":
            options = [
                discord.SelectOption(label="Apple", description="A sweet red fruit"),
                discord.SelectOption(label="Banana", description="A long yellow fruit"),
                discord.SelectOption(label="Cherry", description="A small red fruit"),
            ]
        elif option == "colors":
            options = [
                discord.SelectOption(label="Red", description="Color of fire"),
                discord.SelectOption(label="Blue", description="Color of sky"),
                discord.SelectOption(label="Green", description="Color of nature"),
            ]
        else:
            options = []

        super().__init__(placeholder="Choose an option...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"You selected: {self.values[0]}", ephemeral=True)

class SelectView(discord.ui.View):
    def __init__(self, option: str):
        super().__init__()
        self.add_item(SelectDropdown(option))

class ViewOption(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="select", description="カテゴリを選んで選択肢を表示します（fruits または colors）")
    @app_commands.describe(option="カテゴリを選択（fruits または colors）")
    async def select(self, interaction: discord.Interaction, option: str):
        if option not in ["fruits", "colors"]:
            await interaction.response.send_message(
                "⚠️ `fruits` または `colors` を選んでください。", ephemeral=True
            )
            return

        await interaction.response.send_message(
            f"🔽 選択肢（{option}）を選んでください：", 
            view=SelectView(option)
        )

async def setup(bot: commands.Bot):
    await bot.add_cog(ViewOption(bot))