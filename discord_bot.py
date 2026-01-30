import discord
from discord.ext import commands
import os
from datetime import timedelta
import asyncio

intents = discord.Intents.all()

class mybot(commands.Bot):
    def __init__(self,*args,**kwargs):
        super().__init__(command_prefix="!",intents=intents,*args,**kwargs)
        self.remove_command('help')

bot = mybot()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command(name="hello")
async def hello(ctx):
    await ctx.send("Hello!")

@bot.command(name="ping")
async def ping(ctx):
    await ctx.send(f"Pong! Latency: {round(bot.latency * 1000)}ms")

@bot.command(name="kick")
@commands.has_role("Moderatör")
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"{member.mention} has been kicked. Reason: {reason}")

@bot.command(name="ban")
@commands.has_role("Moderatör")
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"{member.mention} has been banned. Reason: {reason}")

@bot.command(name="mute")
@commands.has_role("Moderatör")
async def mute(ctx, member: discord.Member, minutes: int, *, reason="No reason provided"):
    time = timedelta(minutes=minutes)
    await member.timeout(time, reason=reason)
    await ctx.send(f"{member.mention} has been muted for {minutes} minutes. Reason: {reason}")

@bot.command(name="unmute")
@commands.has_role("Moderatör")
async def unmute(ctx, member: discord.Member):
    await member.timeout(None)
    await ctx.send(f"{member.mention} has been unmuted.")

@bot.command(name="add_role")
@commands.has_role("Moderatör")
async def add_role(ctx, member: discord.Member, role: discord.Role):
    await member.add_roles(role)
    await ctx.send(f"Added {role.name} role to {member.mention}.")

@bot.command(name="remove_role")
@commands.has_role("Moderatör")
async def remove_role(ctx, member: discord.Member, role: discord.Role):
    await member.remove_roles(role)
    await ctx.send(f"Removed {role.name} role from {member.mention}.")

@bot.command(name="clear")
@commands.has_role("Moderatör")
async def clear(ctx, amount: int):
    # Delete the command message + amount
    await ctx.channel.purge(limit=amount + 1)
    # Send info message and delete after 5 seconds
    await ctx.send(f"{amount} messages cleared.", delete_after=5)

@bot.command(name="help")
async def help(ctx):
    embed = discord.Embed(title="Bot Commands", description="Here are the available commands:", color=discord.Color.blue())
    
    embed.add_field(name="!hello", value="Says hello.", inline=False)
    embed.add_field(name="!ping", value="Shows bot latency.", inline=False)
    
    embed.add_field(name="--- Moderation ---", value="*Requires 'Moderatör' role*", inline=False)
    embed.add_field(name="!kick @user [reason]", value="Kicks a user.", inline=False)
    embed.add_field(name="!ban @user [reason]", value="Bans a user.", inline=False)
    embed.add_field(name="!mute @user [minutes] [reason]", value="Mutes a user for a duration.", inline=False)
    embed.add_field(name="!unmute @user", value="Unmutes a user.", inline=False)
    embed.add_field(name="!add_role @user @role", value="Gives a role to a user.", inline=False)
    embed.add_field(name="!remove_role @user @role", value="Removes a role from a user.", inline=False)
    embed.add_field(name="!clear [amount]", value="Deletes X amount of messages.", inline=False)

    await ctx.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You need the 'Moderatör' role to use this command.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing arguments. Please check command usage.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Invalid argument provided.")
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send("I don't have permission to do that! (Check my role hierarchy).")
    else:
        print(f"An error occurred: {error}")

if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if token:
        bot.run(token)
    else:
        print("Error: DISCORD_TOKEN environment variable not found.")
