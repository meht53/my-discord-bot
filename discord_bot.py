import discord
from discord.ext import commands
import os

intents = discord.Intents.all()

class mybot(commands.Bot):
    def __init__(self,*args,**kwargs):
        super().__init__(command_prefix="!",intents=intents,*args,**kwargs)

bot = mybot()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command(name="merhaba")
async def hello(ctx):
    await ctx.send("Merhaba!")

if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if token:
        bot.run(token)
    else:
        print("Hata: DISCORD_TOKEN cevresel degiskeni bulunamadi.")
