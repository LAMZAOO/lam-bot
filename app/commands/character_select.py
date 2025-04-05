import discord
from app.commands.utils.load_characters import load_characters

class CharacterDropdown(discord.ui.Select):
    def __init__(self, on_character_selected):
        self.on_character_selected = on_character_selected
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
        selected_character = self.values[0]
        await self.on_character_selected(interaction, selected_character)

class CharacterSelectView(discord.ui.View):
    def __init__(self, on_character_selected):
        super().__init__(timeout=None)
        self.add_item(CharacterDropdown(on_character_selected))