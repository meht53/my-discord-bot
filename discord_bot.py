import discord
from discord.ext import commands
import os
from datetime import timedelta

intents = discord.Intents.all()

class mybot(commands.Bot):
    def __init__(self,*args,**kwargs):
        super().__init__(command_prefix="!",intents=intents,*args,**kwargs)
        self.remove_command('help') # Varsayilan help komutunu kaldir

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

@bot.command(name="sustur")
@commands.has_role("Moderatör")
async def sustur(ctx, member: discord.Member, sure: int, *, reason="Sebep belirtilmedi"):
    time = timedelta(minutes=sure)
    await member.timeout(time, reason=reason)
    await ctx.send(f"{member.mention} {sure} dakika boyunca susturuldu. Sebep: {reason}")

@bot.command(name="sustur_ac")
@commands.has_role("Moderatör")
async def sustur_ac(ctx, member: discord.Member):
    await member.timeout(None) # Timeout'u kaldirir
    await ctx.send(f"{member.mention} kullanıcısının susturulması kaldırıldı.")

@bot.command(name="rol_ver")
@commands.has_role("Moderatör")
async def rol_ver(ctx, member: discord.Member, role: discord.Role):
    await member.add_roles(role)
    await ctx.send(f"{member.mention} kullanıcısına {role.name} rolü verildi.")

@bot.command(name="rol_al")
@commands.has_role("Moderatör")
async def rol_al(ctx, member: discord.Member, role: discord.Role):
    await member.remove_roles(role)
    await ctx.send(f"{member.mention} kullanıcısından {role.name} rolü alındı.")

@bot.command(name="temizle")
@commands.has_role("Moderatör")
async def temizle(ctx, miktar: int):
    # Komut mesajinin kendisini de silmek icin +1 ekleyebiliriz ama genelde direkt silinmesi istenir.
    await ctx.channel.purge(limit=miktar + 1)
    # Bilgi mesaji atip 5 saniye sonra silebiliriz
    await ctx.send(f"{miktar} mesaj silindi.", delete_after=5)

@bot.command(name="yardim")
async def yardim(ctx):
    embed = discord.Embed(title="Bot Komutları", description="Kullanabileceğiniz komutlar aşağıdadır:", color=discord.Color.blue())
    
    embed.add_field(name="!merhaba", value="Bot size selam verir.", inline=False)
    embed.add_field(name="!ping", value="Botun gecikme süresini gösterir.", inline=False)
    
    embed.add_field(name="--- Moderasyon ---", value="*Sadece 'Moderatör' rolü kullanabilir*", inline=False)
    embed.add_field(name="!kick @kullanıcı [sebep]", value="Kullanıcıyı sunucudan atar.", inline=False)
    embed.add_field(name="!ban @kullanıcı [sebep]", value="Kullanıcıyı yasaklar.", inline=False)
    embed.add_field(name="!sustur @kullanıcı [dakika] [sebep]", value="Kullanıcıyı belirli süre susturur.", inline=False)
    embed.add_field(name="!sustur_ac @kullanıcı", value="Susturmayı kaldırır.", inline=False)
    embed.add_field(name="!rol_ver @kullanıcı @rol", value="Kullanıcıya rol verir.", inline=False)
    embed.add_field(name="!rol_al @kullanıcı @rol", value="Kullanıcıdan rol alır.", inline=False)
    embed.add_field(name="!temizle [sayı]", value="Belirtilen sayıda mesajı siler.", inline=False)

    await ctx.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("Bu komutu kullanmak için 'Moderatör' rolüne sahip olmalısınız.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Eksik argüman girdiniz. Lütfen komutu doğru kullanın.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Hatalı bir argüman girdiniz (Örn: Sayı yerine yazı yazdınız veya rol bulunamadı).")
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send("Bunu yapmak için benim yetkim yok! (Lütfen botun rolünü yukarı taşıyın).")
    else:
        print(f"Bir hata oluştu: {error}")

if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if token:
        bot.run(token)
    else:
        print("Hata: DISCORD_TOKEN cevresel degiskeni bulunamadi.")
