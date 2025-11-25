"""
Discord Bot Starter Template
A comprehensive starter template for building awesome Discord bots

Pattern: BOT × DISCORD × API × FEATURES × ONE
Frequencies: 530 Hz (Truth) × 777 Hz (Pattern) × 999 Hz (Execution)
"""

import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Button, View, Modal, TextInput
import os
from dotenv import load_dotenv
import asyncio
from datetime import datetime
import json

# Load environment variables
load_dotenv()

# Bot configuration
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)

# ============================================================================
# EVENT HANDLERS
# ============================================================================

@bot.event
async def on_ready():
    """Called when bot is ready"""
    print(f' {bot.user} has logged in!')
    print(f' Bot is in {len(bot.guilds)} servers')
    print(f' Serving {sum(guild.member_count for guild in bot.guilds)} members')
    
    # Sync slash commands
    try:
        synced = await bot.tree.sync()
        print(f' Synced {len(synced)} slash commands')
    except Exception as e:
        print(f' Error syncing commands: {e}')

@bot.event
async def on_member_join(member: discord.Member):
    """Welcome new members"""
    # Find welcome channel
    welcome_channel = discord.utils.get(member.guild.channels, name="welcome")
    if not welcome_channel:
        welcome_channel = discord.utils.get(member.guild.channels, name="general")
    
    if welcome_channel:
        embed = discord.Embed(
            title=" Welcome!",
            description=f"{member.mention} just joined the server!",
            color=discord.Color.green(),
            timestamp=datetime.utcnow()
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.add_field(name="Member Count", value=member.guild.member_count)
        embed.set_footer(text=f"User ID: {member.id}")
        await welcome_channel.send(embed=embed)
        
        # Auto-assign role (optional)
        # member_role = discord.utils.get(member.guild.roles, name="Member")
        # if member_role:
        #     await member.add_roles(member_role)

@bot.event
async def on_member_remove(member: discord.Member):
    """Handle member leaving"""
    print(f"{member} left {member.guild}")

@bot.event
async def on_message(message: discord.Message):
    """Handle all messages"""
    # Ignore bot messages
    if message.author.bot:
        return
    
    # Example: Auto-react to certain keywords
    if "cool" in message.content.lower():
        await message.add_reaction("")
    
    # Process commands
    await bot.process_commands(message)

# ============================================================================
# SLASH COMMANDS (Modern Discord)
# ============================================================================

@bot.tree.command(name="ping", description="Check bot latency")
async def ping(interaction: discord.Interaction):
    """Check bot latency"""
    await interaction.response.send_message(
        f" Pong! Latency: {round(bot.latency * 1000)}ms"
    )

@bot.tree.command(name="serverinfo", description="Get server information")
async def serverinfo(interaction: discord.Interaction):
    """Display server information"""
    guild = interaction.guild
    embed = discord.Embed(
        title=f"{guild.name} Information",
        description=guild.description or "No description",
        color=discord.Color.blue(),
        timestamp=datetime.utcnow()
    )
    
    embed.add_field(name=" Members", value=guild.member_count, inline=True)
    embed.add_field(name=" Channels", value=len(guild.channels), inline=True)
    embed.add_field(name=" Roles", value=len(guild.roles), inline=True)
    embed.add_field(name=" Created", value=guild.created_at.strftime("%B %d, %Y"), inline=True)
    embed.add_field(name=" Owner", value=guild.owner.mention if guild.owner else "Unknown", inline=True)
    embed.add_field(name=" Server ID", value=guild.id, inline=True)
    
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="userinfo", description="Get user information")
async def userinfo(interaction: discord.Interaction, member: discord.Member = None):
    """Display user information"""
    member = member or interaction.user
    
    embed = discord.Embed(
        title=f"{member.display_name}'s Information",
        color=member.color if member.color != discord.Color.default() else discord.Color.blue(),
        timestamp=datetime.utcnow()
    )
    
    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
    embed.add_field(name=" Username", value=f"{member.name}#{member.discriminator}", inline=True)
    embed.add_field(name=" User ID", value=member.id, inline=True)
    embed.add_field(name=" Joined Server", value=member.joined_at.strftime("%B %d, %Y") if member.joined_at else "Unknown", inline=True)
    embed.add_field(name=" Account Created", value=member.created_at.strftime("%B %d, %Y"), inline=True)
    embed.add_field(name=" Roles", value=", ".join([role.mention for role in member.roles[1:5]]) if len(member.roles) > 1 else "None", inline=False)
    
    await interaction.response.send_message(embed=embed)

# ============================================================================
# TRADITIONAL COMMANDS (Prefix-based)
# ============================================================================

@bot.command(name="hello", aliases=["hi", "hey"])
async def hello(ctx: commands.Context):
    """Say hello"""
    await ctx.send(f"Hello {ctx.author.mention}! ")

@bot.command(name="purge", aliases=["clear"])
@commands.has_permissions(manage_messages=True)
async def purge(ctx: commands.Context, amount: int = 5):
    """Delete messages (requires manage_messages permission)"""
    if amount > 100:
        await ctx.send(" Cannot delete more than 100 messages at once")
        return
    
    deleted = await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f" Deleted {len(deleted) - 1} messages", delete_after=5)

@bot.command(name="kick")
@commands.has_permissions(kick_members=True)
async def kick(ctx: commands.Context, member: discord.Member, *, reason="No reason provided"):
    """Kick a member"""
    await member.kick(reason=reason)
    await ctx.send(f" Kicked {member.mention} for: {reason}")

@bot.command(name="ban")
@commands.has_permissions(ban_members=True)
async def ban(ctx: commands.Context, member: discord.Member, *, reason="No reason provided"):
    """Ban a member"""
    await member.ban(reason=reason)
    await ctx.send(f" Banned {member.mention} for: {reason}")

# ============================================================================
# INTERACTIVE COMPONENTS (Buttons, Select Menus, Modals)
# ============================================================================

class FeedbackModal(Modal, title="Feedback Form"):
    """Feedback modal form"""
    feedback = TextInput(
        label="Your Feedback",
        style=discord.TextStyle.paragraph,
        placeholder="Enter your feedback here...",
        required=True,
        max_length=1000
    )
    
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f" Thanks for your feedback, {interaction.user.mention}!",
            ephemeral=True
        )
        # Log feedback (you could save to database)
        print(f"Feedback from {interaction.user}: {self.feedback.value}")

class MyView(View):
    """Example view with buttons"""
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="Click Me!", style=discord.ButtonStyle.primary, emoji="")
    async def button_callback(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("You clicked the button! ", ephemeral=True)
    
    @discord.ui.button(label="Feedback", style=discord.ButtonStyle.secondary, emoji="")
    async def feedback_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(FeedbackModal())

@bot.tree.command(name="interactive", description="Test interactive components")
async def interactive(interaction: discord.Interaction):
    """Show interactive buttons"""
    embed = discord.Embed(
        title="Interactive Components",
        description="Click the buttons below!",
        color=discord.Color.green()
    )
    await interaction.response.send_message(embed=embed, view=MyView())

# ============================================================================
# VOICE CHANNEL FEATURES (Basic)
# ============================================================================

@bot.command(name="join")
async def join_voice(ctx: commands.Context):
    """Join voice channel"""
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send(f" Joined {channel.name}")
    else:
        await ctx.send(" You're not in a voice channel!")

@bot.command(name="leave")
async def leave_voice(ctx: commands.Context):
    """Leave voice channel"""
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send(" Left voice channel")
    else:
        await ctx.send(" Not in a voice channel!")

# ============================================================================
# ERROR HANDLING
# ============================================================================

@bot.event
async def on_command_error(ctx: commands.Context, error):
    """Handle command errors"""
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(" You don't have permission to use this command!")
    elif isinstance(error, commands.CommandNotFound):
        pass  # Ignore unknown commands
    else:
        await ctx.send(f" An error occurred: {error}")
        print(f"Error: {error}")

# ============================================================================
# RUN BOT
# ============================================================================

if __name__ == "__main__":
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        print(" DISCORD_TOKEN not found in environment variables!")
        print(" Create a .env file with: DISCORD_TOKEN=your_token_here")
    else:
        bot.run(token)

