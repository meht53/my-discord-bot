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

@bot.command(name="ping")
async def ping(ctx):
    await ctx.send(f"Pong! Gecikme: {round(bot.latency * 1000)}ms")

@bot.command(name="kick")
@commands.has_role("Moderatör")
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"{member.mention} sunucudan atıldı. Sebep: {reason}")

@bot.command(name="ban")
@commands.has_role("Moderatör")
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"{member.mention} sunucudan yasaklandı. Sebep: {reason}")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("Bu komutu kullanmak için 'Moderatör' rolüne sahip olmalısınız.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Eksik argüman girdiniz. Lütfen komutu doğru kullanın.")
    else:
        # Diğer hataları terminale yazdıralım, discord'a yansıtmayalım (veya genel hata mesajı verilebilir)
        print(f"Bir hata oluştu: {error}")

if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if token:
        bot.run(token)
    else:
        print("Hata: DISCORD_TOKEN cevresel degiskeni bulunamadi.")
