import discord
import dotenv
import os
from app.components import MyScoreView
from app.components.DepositSelect import DepositView
from app.components.Leaderboard import LeaderBoardView
from app.db import engine, Base, SessionLocal
from app.helpers.create_leaderboard_embed import create_griefers_leaderboard_embed
from app.queries.create import add_resource, find_or_add_resource
from app.queries.delete import delete_resource
from app.queries.read import find_player_by_nickname, get_griefers

dotenv.load_dotenv()

Base.metadata.create_all(bind=engine)

# session = SessionLocal()
# add_resource(session, "Rare Metals")
# add_resource(session, "Rare Alloys")


token = str(os.getenv("BOT_TOKEN"))
bot = discord.Bot()


def is_admin(ctx):
    return ctx.author.guild_permissions.administrator


@bot.slash_command(name="add_resource")
async def add_resource_command(ctx, name: str):
    if not is_admin(ctx):
        await ctx.respond("You do not have permission to use this command.", ephemeral=True)
        return
    session = SessionLocal()
    find_or_add_resource(session, name)
    await ctx.respond(f"Resource {name} added")


@bot.slash_command(name="deposit")
async def deposit_command(ctx):
    if not is_admin(ctx):
        await ctx.respond("You do not have permission to use this command.", ephemeral=True)
        return
    depositView = DepositView()
    await ctx.respond("Select resource to deposit", view=depositView)


@bot.slash_command(name="delete_resource")
async def delete_resource_command(ctx, name: str):
    if not is_admin(ctx):
        await ctx.respond("You do not have permission to use this command.", ephemeral=True)
        return
    session = SessionLocal()
    delete_resource(session, name)
    await ctx.respond(f"Resource {name} deleted")


@bot.slash_command(name="leaderboard")
async def leaderboard_command(ctx):
    leaderboard = LeaderBoardView()
    await ctx.respond("Select resource", view=leaderboard)


@bot.slash_command(name="my_score")
async def my_score_command(ctx, nickname: str):
    session = SessionLocal()
    player = find_player_by_nickname(session, nickname)
    my_score = MyScoreView(player)
    await ctx.respond("Select resource", view=my_score)


@bot.slash_command(name="griefers")
async def griefers_command(ctx):
    leaderboard = create_griefers_leaderboard_embed()
    await ctx.respond(embed=leaderboard)


@bot.event
async def on_ready():
    # await bot.sync_commands()
    print(f"Logged in as {bot.user}")

if __name__ == "__main__":
    bot.run(token)
