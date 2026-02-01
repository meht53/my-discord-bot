import discord
from discord.ext import commands
import os
from datetime import timedelta
import asyncio
import json
import typing

intents = discord.Intents.all()

class mybot(commands.Bot):
    def __init__(self,*args,**kwargs):
        super().__init__(command_prefix="!",intents=intents,*args,**kwargs)
        self.remove_command('help')

bot = mybot()

# Warnings file path
WARNINGS_FILE = "warnings.json"

def load_warnings():
    try:
        with open(WARNINGS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_warnings(warnings):
    with open(WARNINGS_FILE, "w") as f:
        json.dump(warnings, f, indent=4)

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
@commands.has_role("meht53")
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"{member.mention} has been kicked. Reason: {reason}")

@bot.command(name="ban")
@commands.has_role("meht53")
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"{member.mention} has been banned. Reason: {reason}")

@bot.command(name="unban")
@commands.has_role("meht53")
async def unban(ctx, user_id: int):
    user = await bot.fetch_user(user_id)
    await ctx.guild.unban(user)
    await ctx.send(f"{user.name} has been unbanned.")

@bot.command(name="tempban")
@commands.has_role("meht53")
async def tempban(ctx, member: discord.Member, minutes: int, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"{member.mention} has been banned for {minutes} minutes. Reason: {reason}")
    await asyncio.sleep(minutes * 60)
    await ctx.guild.unban(member)
    await ctx.send(f"{member.mention} has been unbanned (tempban expired).")

@bot.command(name="mute")
@commands.has_role("meht53")
async def mute(ctx, member: discord.Member, minutes: int, *, reason="No reason provided"):
    time = timedelta(minutes=minutes)
    await member.timeout(time, reason=reason)
    await ctx.send(f"{member.mention} has been muted for {minutes} minutes. Reason: {reason}")

@bot.command(name="unmute")
@commands.has_role("meht53")
async def unmute(ctx, member: discord.Member):
    await member.timeout(None)
    await ctx.send(f"{member.mention} has been unmuted.")

@bot.command(name="slowmode")
@commands.has_role("meht53")
async def slowmode(ctx, seconds: int):
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"Slowmode set to {seconds} seconds.")

@bot.command(name="add_role")
@commands.has_role("meht53")
async def add_role(ctx, member: discord.Member, role: discord.Role):
    await member.add_roles(role)
    await ctx.send(f"Added {role.name} role to {member.mention}.")

@bot.command(name="remove_role")
@commands.has_role("meht53")
async def remove_role(ctx, member: discord.Member, role: discord.Role):
    await member.remove_roles(role)
    await ctx.send(f"Removed {role.name} role from {member.mention}.")

@bot.command(name="warn")
@commands.has_role("meht53")
async def warn(ctx, member: discord.Member, *, reason):
    warnings = load_warnings()
    user_id = str(member.id)
    
    if user_id not in warnings:
        warnings[user_id] = []
        
    warnings[user_id].append({"reason": reason, "author": ctx.author.name})
    save_warnings(warnings)
    
    await ctx.send(f"{member.mention} has been warned. Reason: {reason}")

@bot.command(name="infractions")
@commands.has_role("meht53")
async def infractions(ctx, member: discord.Member):
    warnings = load_warnings()
    user_id = str(member.id)
    
    if user_id not in warnings or not warnings[user_id]:
        await ctx.send(f"{member.mention} has no warnings.")
        return
        
    embed = discord.Embed(title=f"Infractions for {member.name}", color=discord.Color.red())
    for i, warn in enumerate(warnings[user_id], 1):
        embed.add_field(name=f"Warning {i}", value=f"Reason: {warn['reason']}\nBy: {warn['author']}", inline=False)
        
    await ctx.send(embed=embed)

@bot.command(name="clear")
@commands.has_role("meht53")
async def clear(ctx, amount: int):
    # Delete the command message + amount
    await ctx.channel.purge(limit=amount + 1)
    # Send info message and delete after 5 seconds
    await ctx.send(f"{amount} messages cleared.", delete_after=5)

@bot.command(name="server_info")
async def server_info(ctx):
    embed = discord.Embed(title=f"{ctx.guild.name} Info", color=discord.Color.blue())
    embed.add_field(name="Server ID", value=ctx.guild.id, inline=True)
    embed.add_field(name="Owner", value=ctx.guild.owner, inline=True)
    embed.add_field(name="Members", value=ctx.guild.member_count, inline=True)
    embed.add_field(name="Roles", value=len(ctx.guild.roles), inline=True)
    embed.set_thumbnail(url=ctx.guild.icon.url if ctx.guild.icon else None)
    await ctx.send(embed=embed)

@bot.command(name="user_info")
async def user_info(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"{member.name} Info", color=member.color)
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="Joined At", value=member.joined_at.strftime("%Y-%m-%d"), inline=True)
    embed.add_field(name="Created At", value=member.created_at.strftime("%Y-%m-%d"), inline=True)
    embed.add_field(name="Top Role", value=member.top_role.mention, inline=True)
    embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
    await ctx.send(embed=embed)

@bot.command(name="role_info")
async def role_info(ctx, role: discord.Role):
    embed = discord.Embed(title=f"{role.name} Info", color=role.color)
    embed.add_field(name="ID", value=role.id, inline=True)
    embed.add_field(name="Members", value=len(role.members), inline=True)
    embed.add_field(name="Mentionable", value=role.mentionable, inline=True)
    embed.add_field(name="Position", value=role.position, inline=True)
    await ctx.send(embed=embed)

@bot.command(name="help")
async def help(ctx):
    embed = discord.Embed(title="Bot Commands", description="Here are the available commands:", color=discord.Color.blue())
    
    embed.add_field(name="!hello", value="Says hello.", inline=False)
    embed.add_field(name="!ping", value="Shows bot latency.", inline=False)
    
    embed.add_field(name="--- Moderation ---", value="*Requires 'meht53' role*", inline=False)
    embed.add_field(name="!kick @user [reason]", value="Kicks a user.", inline=False)
    embed.add_field(name="!ban @user [reason]", value="Bans a user.", inline=False)
    embed.add_field(name="!tempban @user [minutes] [reason]", value="Temporarily bans a user.", inline=False)
    embed.add_field(name="!unban [user_id]", value="Unbans a user by ID.", inline=False)
    embed.add_field(name="!mute @user [minutes] [reason]", value="Mutes a user for a duration.", inline=False)
    embed.add_field(name="!unmute @user", value="Unmutes a user.", inline=False)
    embed.add_field(name="!slowmode [seconds]", value="Sets channel slowmode.", inline=False)
    embed.add_field(name="!warn @user [reason]", value="Warns a user.", inline=False)
    embed.add_field(name="!infractions @user", value="Views user warnings.", inline=False)
    embed.add_field(name="!add_role @user @role", value="Gives a role to a user.", inline=False)
    embed.add_field(name="!remove_role @user @role", value="Removes a role from a user.", inline=False)
    embed.add_field(name="!clear [amount]", value="Deletes X amount of messages.", inline=False)
    
    embed.add_field(name="--- Info ---", value="*Information commands*", inline=False)
    embed.add_field(name="!server_info", value="Server details.", inline=False)
    embed.add_field(name="!user_info [@user]", value="User details.", inline=False)
    embed.add_field(name="!role_info @role", value="Role details.", inline=False)

    await ctx.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You need the 'meht53' role to use this command.")
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
