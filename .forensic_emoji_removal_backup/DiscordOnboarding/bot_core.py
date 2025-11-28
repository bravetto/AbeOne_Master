"""
Bot Core - Central Event & Function Hub
Pattern: BOT × CORE × EVENTS × FUNCTIONS × ONE
"""

import discord
from discord.ext import commands
from discord.ui import Button, View, Modal, TextInput
from typing import Dict, List, Optional, Any
from datetime import datetime
import asyncio

from config.settings import DISCORD_TOKEN
from memory_layer.storage import Storage
from memory_layer.user_profiles import UserProfile
from specialist_layer.onboarding_engine import initialize_onboarding_engine
from specialist_layer.discord_bot_engine import initialize_discord_bot_engine
from specialist_layer.personalization_engine import personalization_engine
from npcs.guardians import guardian_swarm
from gamification.artifacts import artifact_manager
from config.gz_map import get_map_data_for_role_stack

class BotCore:
    """Core bot functionality - Events & Functions"""
    
    def __init__(self):
        self.storage = Storage()
        self.user_profiles = UserProfile(self.storage)
        self.onboarding_engine = initialize_onboarding_engine(self.storage)
        self.discord_bot_engine = initialize_discord_bot_engine(self.onboarding_engine)
        self.bot = None  # Will be set when bot is initialized
    
    def set_bot(self, bot: commands.Bot):
        """Set bot instance"""
        self.bot = bot
    
    # ============================================================================
    # EVENTS
    # ============================================================================
    
    async def on_member_join(self, member: discord.Member):
        """Event: Member joins server"""
        # Find welcome channel
        welcome_channel = discord.utils.get(member.guild.channels, name="start-here")
        if not welcome_channel:
            welcome_channel = discord.utils.get(member.guild.channels, name="general")
        
        if welcome_channel:
            # Create private onboarding channel
            private_channel = await self.create_private_channel(member, member.guild)
            
            # Send welcome screen
            await self.send_welcome_screen(member, private_channel)
    
    async def handle_button_click(self, interaction: discord.Interaction, button_id: str, data: Dict = None):
        """Handle button click (called from View callbacks)"""
        # Route button clicks to appropriate handlers
        if button_id.startswith('start_journey'):
            await self._handle_start_journey(interaction)
        elif button_id.startswith('answer_'):
            await self._handle_answer(interaction, button_id, data or {})
        elif button_id.startswith('artifact_'):
            await self._handle_artifact_selection(interaction, button_id, data or {})
        elif button_id.startswith('teleport_'):
            await self._handle_teleport(interaction, button_id, data or {})
        elif button_id.startswith('complete_quest'):
            await self._handle_complete_quest(interaction, data or {})
    
    async def handle_modal_submit(self, interaction: discord.Interaction, modal_id: str, data: Dict):
        """Handle modal submission (called from Modal callbacks)"""
        # Route modal submissions to appropriate handlers
        if modal_id.startswith('profile_'):
            await self._handle_profile_modal(interaction, modal_id, data)
        elif modal_id.startswith('feedback_'):
            await self._handle_feedback_modal(interaction, modal_id, data)
    
    # ============================================================================
    # FUNCTIONS
    # ============================================================================
    
    async def create_private_channel(self, member: discord.Member, guild: discord.Guild) -> Optional[discord.TextChannel]:
        """Create private channel for user onboarding"""
        try:
            # Create private channel
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(view_channel=False),
                member: discord.PermissionOverwrite(view_channel=True, send_messages=True),
                guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            }
            
            channel = await guild.create_text_channel(
                f"onboarding-{member.display_name.lower().replace(' ', '-')}",
                overwrites=overwrites,
                category=None
            )
            
            return channel
        except Exception as e:
            print(f"Error creating private channel: {e}")
            return None
    
    async def send_welcome_screen(self, member: discord.Member, channel: discord.TextChannel):
        """Send welcome screen to user"""
        embed = self.discord_bot_engine.create_welcome_embed(member.display_name)
        view = self.discord_bot_engine.create_onboarding_view(str(member.id))
        
        await channel.send(
            f"🎉 {member.mention} Welcome to GreatnessZone™!",
            embed=embed,
            view=view
        )
    
    async def run_energy_scan(self, discord_id: str, channel: discord.TextChannel) -> Dict[str, Any]:
        """Run energy scan animation"""
        result = self.onboarding_engine.start_energy_scan(discord_id)
        
        if result['status'] == 'energy_scan':
            embed = discord.Embed(**result['energy_message'])
            message = await channel.send(embed=embed)
            
            # Animated loading sequence
            await asyncio.sleep(1)
            embed.description = embed.description.replace("Scanning", "🔍 Scanning")
            await message.edit(embed=embed)
            
            await asyncio.sleep(1)
            embed.description = embed.description.replace("Scanning", "✅ Scanned")
            embed.description += "\n\n**Energy signature detected!** Ready for Greatness Sprint!"
            await message.edit(embed=embed)
            
            return result
        return result
    
    async def ask_question(self, step: int, discord_id: str, channel: discord.TextChannel) -> Dict[str, Any]:
        """Ask question for current step"""
        if step == 1:  # Start Greatness Sprint
            result = self.onboarding_engine.start_greatness_sprint(discord_id)
        else:
            # Get current question from session
            session = self.onboarding_engine.get_onboarding_status(discord_id)
            if session:
                result = self.onboarding_engine.start_greatness_sprint(discord_id)
            else:
                return {'status': 'error', 'message': 'No active session'}
        
        if result['status'] == 'question':
            from specialist_layer.discord_bot_engine import GreatnessSprintView
            view = GreatnessSprintView(
                self.onboarding_engine,
                discord_id,
                result['question']
            )
            
            embed = discord.Embed(
                title=f"⚡ **Greatness Sprint** - Question {int(result.get('progress', 0) * 5) + 1}/5",
                description=f"**{result['question']['question']}**\n\nChoose your answer:",
                color=0xff00ff
            )
            embed.set_footer(text=f"Progress: {int(result.get('progress', 0) * 100)}%")
            
            await channel.send(embed=embed, view=view)
        
        return result
    
    async def assign_roles(self, discord_id: str, guild: discord.Guild, role_stack: List[str]) -> List[discord.Role]:
        """Assign roles based on role stack"""
        assigned_roles = []
        
        for role_name in role_stack:
            # Find or create role
            role = discord.utils.get(guild.roles, name=role_name.replace('_', ' ').title())
            
            if not role:
                # Create role with color from settings
                from config.settings import ROLE_COLORS
                color = ROLE_COLORS.get(role_name, 0x808080)
                
                role = await guild.create_role(
                    name=role_name.replace('_', ' ').title(),
                    color=discord.Color(color),
                    mentionable=True
                )
            
            # Assign to member
            member = guild.get_member(int(discord_id))
            if member and role not in member.roles:
                await member.add_roles(role)
                assigned_roles.append(role)
        
        return assigned_roles
    
    async def unlock_channels(self, discord_id: str, guild: discord.Guild, role_stack: List[str]) -> List[discord.TextChannel]:
        """Unlock channels based on role stack"""
        from config.gz_map import get_all_channels_for_role_stack
        
        channels_to_unlock = get_all_channels_for_role_stack(role_stack)
        unlocked_channels = []
        
        for channel_name in channels_to_unlock:
            channel = discord.utils.get(guild.channels, name=channel_name)
            if channel:
                # In production, would set permissions here
                # For now, just track them
                unlocked_channels.append(channel)
        
        return unlocked_channels
    
    async def drop_map(self, discord_id: str, channel: discord.TextChannel) -> Dict[str, Any]:
        """Drop map with teleport buttons"""
        result = self.onboarding_engine.create_map_drop(discord_id)
        
        if result['status'] == 'map_ready':
            map_data = result['map_data']
            from specialist_layer.discord_bot_engine import MapTeleportView
            view = MapTeleportView(self.onboarding_engine, discord_id, map_data)
            
            embed = discord.Embed(
                title=map_data['title'],
                description=map_data['description'],
                color=0x00ffff
            )
            
            # Add map areas
            for area in map_data.get('map_areas', [])[:5]:
                channels_text = ", ".join([f"#{c}" for c in area['channels'][:3]])
                embed.add_field(
                    name=f"{area['icon']} {area['name']}",
                    value=f"{area['description']}\n{channels_text}",
                    inline=False
                )
            
            await channel.send(embed=embed, view=view)
        
        return result
    
    async def give_artifact(self, discord_id: str, artifact_id: str, channel: discord.TextChannel) -> Dict[str, Any]:
        """Give artifact to user"""
        result = self.onboarding_engine.select_artifact(discord_id, artifact_id)
        
        if result['status'] == 'artifact_selected':
            artifact = result['artifact']
            
            role_info = ""
            if artifact.get('role'):
                role_emoji = artifact.get('role_emoji', '')
                role_info = f"\n\n{role_emoji} **Role Unlocked: {artifact['role']}**"
            
            perk_info = ""
            if artifact.get('perk'):
                perk_info = f"\n✨ **Perk:** {artifact['perk']}"
            
            embed = discord.Embed(
                title=f"💎 **{artifact['emoji']} {artifact['name']} Selected!**",
                description=f"{artifact['description']}{role_info}{perk_info}\n\n"
                          f"**Bonus:** +{artifact['bonus_points']} points\n\n"
                          f"This artifact is now yours!",
                color=0xff00ff
            )
            
            await channel.send(embed=embed)
        
        return result
    
    async def generate_profile(self, discord_id: str, channel: discord.TextChannel) -> Dict[str, Any]:
        """Generate and display AI profile"""
        result = self.onboarding_engine.generate_personal_profile(discord_id)
        
        if result['status'] == 'profile_generated':
            profile_embed = discord.Embed(**result['ai_profile'])
            await channel.send(embed=profile_embed)
        
        return result
    
    # ============================================================================
    # EVENT HANDLERS (Private)
    # ============================================================================
    
    async def _handle_start_journey(self, interaction: discord.Interaction):
        """Handle start journey button"""
        await interaction.response.defer(ephemeral=True)
        
        result = self.onboarding_engine.start_onboarding(
            str(interaction.user.id),
            interaction.user.display_name
        )
        
        if result['status'] == 'started':
            embed = discord.Embed(**result['welcome_message'])
            await interaction.followup.send(embed=embed, ephemeral=True)
            
            guardian_embed = discord.Embed(**result['guardian_message'])
            await interaction.followup.send(embed=guardian_embed, ephemeral=True)
            
            # Start energy scan
            await self.run_energy_scan(str(interaction.user.id), interaction.channel)
    
    async def _handle_answer(self, interaction: discord.Interaction, button_id: str, data: Dict):
        """Handle answer button"""
        # Handled by GreatnessSprintView
        pass
    
    async def _handle_artifact_selection(self, interaction: discord.Interaction, button_id: str, data: Dict):
        """Handle artifact selection"""
        artifact_id = button_id.replace('artifact_', '')
        await self.give_artifact(str(interaction.user.id), artifact_id, interaction.channel)
    
    async def _handle_teleport(self, interaction: discord.Interaction, button_id: str, data: Dict):
        """Handle teleport button"""
        channel_name = button_id.replace('teleport_', '')
        await interaction.response.send_message(
            f"🗺️ **Teleporting to #{channel_name}...**\n\n"
            f"*Jump to #{channel_name} to continue your journey!*",
            ephemeral=True
        )
    
    async def _handle_complete_quest(self, interaction: discord.Interaction, data: Dict):
        """Handle complete quest button"""
        quest_id = data.get('quest_id', 'welcome_001')
        result = self.onboarding_engine.complete_quest(str(interaction.user.id), quest_id)
        
        if result['status'] == 'quest_completed':
            embed = discord.Embed(**result['encouragement'])
            embed.add_field(
                name="Rewards Earned",
                value=f"💰 +{result['points_awarded']} points\n💎 Total: {result['total_points']} points",
                inline=False
            )
            
            if result.get('badge_unlocked'):
                badge = result['badge_unlocked']
                embed.add_field(
                    name="Badge Unlocked!",
                    value=f"{badge['emoji']} **{badge['name']}**\n{badge['description']}",
                    inline=False
                )
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    async def _handle_profile_modal(self, interaction: discord.Interaction, modal_id: str, data: Dict):
        """Handle profile modal submission"""
        # Future: Handle profile customization
        await interaction.response.send_message("Profile updated!", ephemeral=True)
    
    async def _handle_feedback_modal(self, interaction: discord.Interaction, modal_id: str, data: Dict):
        """Handle feedback modal submission"""
        # Future: Handle feedback collection
        await interaction.response.send_message("Thanks for your feedback!", ephemeral=True)

# Global instance
bot_core = BotCore()

