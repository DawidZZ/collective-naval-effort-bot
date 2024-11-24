import discord

from app.helpers.create_leaderboard_embed import create_leaderboard_embed
from app.queries.read import get_all_resources, get_amount_of_player_deposit, get_leaderboard
from app.db import SessionLocal


class ResourceSelect(discord.ui.Select):
    def __init__(self, resources, player) -> None:
        super().__init__(
            select_type=discord.ComponentType.string_select,
            placeholder="Select resource to show leaderboard",
            options=[discord.SelectOption(
                label=resource.name, value=resource.name) for resource in resources]
        )
        self.player = player

    async def callback(self, interaction: discord.Interaction):
        session = SessionLocal()
        selected_resource = self.values[0]
        player_score = get_amount_of_player_deposit(
            session, self.player, selected_resource)
        embed = discord.Embed(
            title="Your Score",
            description=f"Resource: {selected_resource}\nScore: {player_score}",
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=embed)


class MyScoreView(discord.ui.View):
    def __init__(self, player, limit: int = 10):
        super().__init__()
        all_resources = get_all_resources(SessionLocal())
        self.add_item(ResourceSelect(all_resources, player))
