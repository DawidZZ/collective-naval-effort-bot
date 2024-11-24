import discord
import asyncio
from app.db import SessionLocal

from app.queries.create import add_deposit, find_or_add_player
from app.queries.read import find_resource_by_name, get_all_resources


class DepositModal(discord.ui.Modal):
    def __init__(self, selected_resource: str) -> None:
        super().__init__(title=f"Deposit {selected_resource}")

        self.add_item(discord.ui.InputText(
            placeholder="Nickname",
            label="Enter player nickname",
            style=discord.InputTextStyle.short
        ))

        self.add_item(discord.ui.InputText(
            placeholder="Amount",
            label="Enter amount to deposit",
            style=discord.InputTextStyle.short
        ))

        self.selected_resource = selected_resource

    async def callback(self, interaction: discord.Interaction):
        session = SessionLocal()
        player = find_or_add_player(session, self.children[0].value)
        resource = find_resource_by_name(session, self.selected_resource)
        deposit = add_deposit(session, player.id, resource.id,
                              int(self.children[1].value))
        embed = discord.Embed(title="Resource deposited")
        embed.add_field(name="Player", value=deposit.player.nickname)
        embed.add_field(name="Resource", value=deposit.resource.name)
        embed.add_field(name="Amount", value=deposit.amount)
        await interaction.response.send_message(embeds=[embed])


class DepositSelect(discord.ui.Select):
    def __init__(self, resources) -> None:
        super().__init__(
            select_type=discord.ComponentType.string_select,
            placeholder="Select resource to deposit",
            options=[discord.SelectOption(
                label=resource.name, value=resource.name) for resource in resources]
        )

    async def callback(self, interaction: discord.Interaction):
        selected_resource = self.values[0]
        modal = DepositModal(selected_resource)
        await interaction.response.send_modal(modal)


class DepositView(discord.ui.View):
    def __init__(self) -> None:
        super().__init__()
        resources = get_all_resources(SessionLocal())
        self.add_item(DepositSelect(resources))
