import discord
import dotenv
import os
from app.db import engine, Base, SessionLocal

dotenv.load_dotenv()

Base.metadata.create_all(bind=engine)

token = str(os.getenv("BOT_TOKEN"))
bot = discord.Bot()


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

bot.run(token)
