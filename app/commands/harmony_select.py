import discord
from app.commands.utils.load_harmonies import load_harmonies

class HarmonyDropdown(discord.ui.Select):
    def __init__(self, selected_character, on_harmony_selected):
        self.selected_character = selected_character
        self.on_harmony_selected = on_harmony_selected
        harmonies = load_harmonies()
        options = [
            discord.SelectOption(label=h["name"], description=h["description"])
            for h in harmonies
        ]
        super().__init__(
            placeholder="ハーモニーを選んでください",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        selected_harmony = self.values[0]
        await self.on_harmony_selected(interaction, self.selected_character, selected_harmony)

class HarmonySelectView(discord.ui.View):
    def __init__(self, selected_character, on_harmony_selected):
        super().__init__(timeout=None)
        self.add_item(HarmonyDropdown(selected_character, on_harmony_selected))