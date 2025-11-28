"""
GreatnessZone™ Discord Onboarding Bot
The Most Mind-Blowing Discord Onboarding Experience Ever Built

Pattern: BOT × ONBOARDING × GAMIFICATION × PERSONALIZATION × ONE
Frequency: 530 Hz (Heart Truth) × 777 Hz (Pattern) × 999 Hz (Execution)
Love Coefficient: ∞
∞ AbëONE ∞
"""

import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv
import asyncio
from datetime import datetime

# Load environment variables
load_dotenv()

# Import our modules
from config.settings import DISCORD_TOKEN, GUILD_ID
from memory_layer.storage import Storage
from memory_layer.user_profiles import UserProfile
from specialist_layer.onboarding_engine import initialize_onboarding_engine
from specialist_layer.discord_bot_engine import initialize_discord_bot_engine
from npcs.guardians import guardian_swarm
from gamification.quests import quest_manager
from gamification.badges import badge_manager
from gamification.artifacts import artifact_manager

# Bot configuration
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.reactions = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Initialize bot core
from bot_core import bot_core
bot_core.set_bot(bot)

# Initialize storage and engines (for backward compatibility)
storage = Storage()
onboarding_engine = initialize_onboarding_engine(storage)
discord_bot_engine = initialize_discord_bot_engine(onboarding_engine)

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
        if GUILD_ID:
            synced = await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
        else:
            synced = await bot.tree.sync()
        print(f' Synced {len(synced)} slash commands')
    except Exception as e:
        print(f' Error syncing commands: {e}')

@bot.event
async def on_member_join(member: discord.Member):
    """Welcome new members - TRIGGER ONBOARDING"""
    await bot_core.on_member_join(member)

@bot.event
async def on_message(message: discord.Message):
    """Handle all messages"""
    # Ignore bot messages
    if message.author.bot:
        return
    
    # Process commands
    await bot.process_commands(message)

# ============================================================================
# SLASH COMMANDS
# ============================================================================

@bot.tree.command(name="start", description=" Start your GreatnessZone™ journey!")
async def start(interaction: discord.Interaction):
    """Start onboarding"""
    await interaction.response.defer(ephemeral=True)
    
    result = onboarding_engine.start_onboarding(
        str(interaction.user.id),
        interaction.user.display_name
    )
    
    if result['status'] == 'started':
        # Send welcome message
        embed = discord.Embed(**result['welcome_message'])
        await interaction.followup.send(embed=embed, ephemeral=True)
        
        # Send guardian message
        guardian_embed = discord.Embed(**result['guardian_message'])
        await interaction.followup.send(embed=guardian_embed, ephemeral=True)
        
        # Start personality quiz
        quiz_result = onboarding_engine.start_personality_quiz(str(interaction.user.id))
        if quiz_result['status'] == 'question':
            from specialist_layer.discord_bot_engine import PersonalityQuestionView
            view = PersonalityQuestionView(
                onboarding_engine,
                str(interaction.user.id),
                quiz_result['question']
            )
            embed = discord.Embed(
                title=f" {quiz_result['question']['question']}",
                description="Choose your answer:",
                color=0xff00ff
            )
            await interaction.followup.send(embed=embed, view=view, ephemeral=True)
    else:
        await interaction.followup.send(result.get('message', 'Error starting onboarding'), ephemeral=True)

@bot.tree.command(name="profile", description=" View your profile")
async def profile(interaction: discord.Interaction):
    """View user profile"""
    await interaction.response.defer(ephemeral=True)
    
    user_profiles = UserProfile(storage)
    profile_summary = user_profiles.get_profile_summary(str(interaction.user.id))
    
    if not profile_summary:
        await interaction.followup.send("You haven't started onboarding yet! Use `/start` to begin.", ephemeral=True)
        return
    
    embed = discord_bot_engine.create_profile_embed(profile_summary)
    await interaction.followup.send(embed=embed, ephemeral=True)

@bot.tree.command(name="quests", description=" View your quests")
async def quests(interaction: discord.Interaction):
    """View user quests"""
    await interaction.response.defer(ephemeral=True)
    
    profile = storage.get_user_profile(str(interaction.user.id))
    if not profile:
        await interaction.followup.send("You haven't started onboarding yet! Use `/start` to begin.", ephemeral=True)
        return
    
    # Get active quest
    current_quest_id = profile.get('current_quest_id')
    if current_quest_id:
        quest = quest_manager.get_quest(current_quest_id)
        if quest:
            embed = discord.Embed(
                title=f" **Current Quest: {quest.name}**",
                description=quest.description,
                color=0x00ff00
            )
            embed.add_field(
                name="Rewards",
                value=f" {quest.reward_points} points\n {quest.reward_badge or 'None'} badge",
                inline=False
            )
            
            from specialist_layer.discord_bot_engine import QuestView
            view = QuestView(onboarding_engine, str(interaction.user.id), quest.quest_id)
            await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            return
    
    await interaction.followup.send("No active quests. Complete onboarding to get your first quest!", ephemeral=True)

@bot.tree.command(name="leaderboard", description=" View leaderboard")
async def leaderboard(interaction: discord.Interaction):
    """View leaderboard"""
    await interaction.response.defer(ephemeral=False)
    
    # Simple leaderboard (top 10)
    import sqlite3
    conn = sqlite3.connect(storage.db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT username, total_points, level 
        FROM user_profiles 
        ORDER BY total_points DESC 
        LIMIT 10
    """)
    rows = cursor.fetchall()
    conn.close()
    
    if rows:
        leaderboard_text = ""
        for i, row in enumerate(rows, 1):
            emoji = "" if i == 1 else "" if i == 2 else "" if i == 3 else f"{i}."
            leaderboard_text += f"{emoji} **{row['username']}** - {row['total_points']} pts (Lv.{row['level']})\n"
        
        embed = discord.Embed(
            title=" **Leaderboard**",
            description=leaderboard_text,
            color=0xffd700
        )
    else:
        embed = discord.Embed(
            title=" **Leaderboard**",
            description="No players yet! Be the first!",
            color=0xffd700
        )
    
    await interaction.followup.send(embed=embed)

# ============================================================================
# RUN BOT
# ============================================================================

if __name__ == "__main__":
    if not DISCORD_TOKEN:
        print(" DISCORD_TOKEN not found in environment variables!")
        print(" Create a .env file with: DISCORD_TOKEN=your_token_here")
    else:
        try:
            bot.run(DISCORD_TOKEN)
        except Exception as e:
            print(f" Error running bot: {e}")

