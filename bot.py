import discord
from discord.ext import commands
import asyncio
import os
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='.', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name='general')
    if channel:
        await channel.send(f"Welcome to the server, {member.mention}! Read the rules and enjoy your stay.")

@bot.command()
@commands.has_role('owne')
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"Kicked {member.mention} for: {reason}")

@bot.command()
@commands.has_role('owne')
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"Banned {member.mention} for: {reason}")

@bot.command()
@commands.has_role('owne')
async def mute(ctx, member: discord.Member, minutes: int):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not role:
        role = await ctx.guild.create_role(name="Muted")
        for channel in ctx.guild.channels:
            await channel.set_permissions(role, send_messages=False)
    await member.add_roles(role)
    await ctx.send(f"{member.mention} has been muted for {minutes} minutes.")
    await asyncio.sleep(minutes * 60)
    await member.remove_roles(role)
    await ctx.send(f"{member.mention} has been unmuted.")

@bot.command()
@commands.has_role('owne')
async def warn(ctx, member: discord.Member, *, reason=None):
    await ctx.send(f"{member.mention} has been warned for: {reason}")

@bot.command()
@commands.has_role('owne')
async def purge(ctx, amount: int):
    await ctx.channel.purge(limit=amount)
    await ctx.send(f"Deleted {amount} messages.", delete_after=5)

@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title="User Info", color=discord.Color.blue())
    embed.add_field(name="Username", value=str(member))
    embed.add_field(name="ID", value=member.id)
    embed.add_field(name="Account Created", value=member.created_at.strftime("%Y-%m-%d"))
    embed.add_field(name="Joined Server", value=member.joined_at.strftime("%Y-%m-%d"))
    await ctx.send(embed=embed)

@bot.command()
async def serverinfo(ctx):
    guild = ctx.guild
    embed = discord.Embed(title="Server Info", color=discord.Color.green())
    embed.add_field(name="Server Name", value=guild.name)
    embed.add_field(name="Member Count", value=guild.member_count)
    await ctx.send(embed=embed)

@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")

@bot.command()
async def help(ctx):
    help_text = """
**Trader Bot Commands:**
`.kick @user reason` - Kick a user
`.ban @user reason` - Ban a user
`.mute @user minutes` - Mute a user
`.warn @user reason` - Warn a user
`.purge amount` - Delete messages
`.userinfo @user` - Info on user
`.serverinfo` - Info on server
`.ping` - Bot ping
"""
    await ctx.send(help_text)

keep_alive()
bot.run(os.environ['BOT_TOKEN'])
