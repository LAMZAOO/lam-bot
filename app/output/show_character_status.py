import discord

async def calc_result(character_name: str, harmony_name: str) -> str:
    # 仮のロジック。ここに実際の計算やデータ取得処理を入れられます。
    result_message = (
        f"🎉 最終結果 🎉\n"
        f"キャラクター: **{character_name}**\n"
        f"ハーモニー: **{harmony_name}**\n"
        f"\nこれにより、あなたの戦闘力は爆増することでしょう...！🔥"
    )
    return result_message

async def show_character_status(interaction: discord.Interaction, character_name: str, harmony_name: str):
    result = await calc_result(character_name, harmony_name)
    await interaction.followup.send(result, ephemeral=True)