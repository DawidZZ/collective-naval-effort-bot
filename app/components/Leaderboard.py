import discord

from app.helpers.create_leaderboard_embed import create_griefers_leaderboard_embed, create_leaderboard_embed
from app.queries.read import get_all_resources, get_leaderboard
from app.db import SessionLocal


class ResourceSelect(discord.ui.Select):
    def __init__(self, resources, limit) -> None:
        super().__init__(
            select_type=discord.ComponentType.string_select,
            placeholder="Select resource to show leaderboard",
            options=[discord.SelectOption(
                label=resource.name, value=resource.name) for resource in resources]
        )
        self.limit = limit

    async def callback(self, interaction: discord.Interaction):
        selected_resource = self.values[0]
        embed = create_leaderboard_embed(
            selected_resource, limit=self.limit)
        await interaction.response.send_message(embed=embed)


class LeaderBoardView(discord.ui.View):
    def __init__(self, limit: int = 10):
        super().__init__()
        all_resources = get_all_resources(SessionLocal())
        self.add_item(ResourceSelect(all_resources, limit))
