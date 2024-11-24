import discord
from app.db import SessionLocal
from app.queries.read import get_griefers, get_leaderboard


def create_leaderboard_embed(resource, limit=10):
    session = SessionLocal()
    leaderboard = get_leaderboard(session, resource, limit)

    if not leaderboard:
        return discord.Embed(
            title="Leaderboard",
            description=f"No results found for resource: **{resource}**",
            color=discord.Color.red()
        )

    rows = []
    for rank, (nickname, total_deposit) in enumerate(leaderboard, start=1):
        rows.append(f"**{rank}.** {nickname} - **{total_deposit}**")

    embed = discord.Embed(
        title=f"Leaderboard for {resource}",
        description="\n".join(rows),
        color=discord.Color.blue()
    )
    embed.set_footer(text=f"Top {resource} players")
    return embed


def create_griefers_leaderboard_embed(limit=10):
    session = SessionLocal()
    griefers = get_griefers(session)

    if not griefers:
        return discord.Embed(
            title="Griefers Leaderboard",
            description="No griefers found.",
            color=discord.Color.red()
        )

    rows = []
    for rank, (nickname, resource, total_amount) in enumerate(griefers, start=1):
        rows.append(
            f"**{rank}.** {nickname} - **{total_amount}** griefs ({resource})")

    embed = discord.Embed(
        title="Griefers Leaderboard",
        description="\n".join(rows),
        color=discord.Color.dark_red()
    )
    embed.set_footer(text="Top griefers")
    return embed
