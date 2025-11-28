"""
Discord Bot Engine - 8-Step Cinematic Flow UI
Pattern: DISCORD × INTERACTIONS × ONE
"""

import discord
from discord.ui import Button, View, Modal, TextInput, Select
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
import asyncio

class OnboardingView(View):
    """Onboarding view with buttons"""
    
    def __init__(self, onboarding_engine, discord_id: str):
        super().__init__(timeout=600)  # 10 minute timeout
        self.onboarding_engine = onboarding_engine
        self.discord_id = discord_id
    
    @discord.ui.button(label=" Start Journey", style=discord.ButtonStyle.primary, emoji="")
    async def start_button(self, interaction: discord.Interaction, button: Button):
        """Step 0: Entry Trigger → Welcome Screen"""
        await interaction.response.defer(ephemeral=True)
        
        result = self.onboarding_engine.start_onboarding(
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
            
            # Start energy scan
            await self._start_energy_scan(interaction)
        else:
            await interaction.followup.send(result['message'], ephemeral=True)
    
    async def _start_energy_scan(self, interaction: discord.Interaction):
        """Step 1: Energy Scan → Animated Loading"""
        result = self.onboarding_engine.start_energy_scan(str(interaction.user.id))
        
        if result['status'] == 'energy_scan':
            embed = discord.Embed(**result['energy_message'])
            
            # Send initial message
            loading_msg = await interaction.followup.send(embed=embed, ephemeral=True)
            
            # Animated sequence: Initializing scan…
            await asyncio.sleep(1)
            embed.description = "Initializing scan…"
            await loading_msg.edit(embed=embed)
            
            # Calibrating greatness…
            await asyncio.sleep(1)
            embed.description = "Initializing scan…\n\nCalibrating greatness…"
            await loading_msg.edit(embed=embed)
            
            # Hold tight… this might tingle 
            await asyncio.sleep(1)
            embed.description = "Initializing scan…\n\nCalibrating greatness…\n\nHold tight… this might tingle "
            await loading_msg.edit(embed=embed)
            
            # Start Greatness Sprint
            await asyncio.sleep(1)
            await self._start_greatness_sprint(interaction)
    
    async def _start_greatness_sprint(self, interaction: discord.Interaction):
        """Step 2: 5-Question Greatness Sprint"""
        result = self.onboarding_engine.start_greatness_sprint(str(interaction.user.id))
        
        if result['status'] == 'question':
            await self._send_question(interaction, result['question'], result.get('progress', 0))
    
    async def _send_question(self, interaction: discord.Interaction, question: Dict, progress: float = 0):
        """Send question with buttons"""
        view = GreatnessSprintView(
            self.onboarding_engine,
            str(interaction.user.id),
            question
        )
        
        embed = discord.Embed(
            title=f" **Greatness Sprint** - Question {int(progress * 5) + 1}/5",
            description=f"**{question['question']}**\n\nChoose your answer:",
            color=0xff00ff
        )
        embed.set_footer(text=f"Progress: {int(progress * 100)}%")
        
        await interaction.followup.send(embed=embed, view=view, ephemeral=True)

class GreatnessSprintView(View):
    """5-Question Greatness Sprint view"""
    
    def __init__(self, onboarding_engine, discord_id: str, question: Dict):
        super().__init__(timeout=300)
        self.onboarding_engine = onboarding_engine
        self.discord_id = discord_id
        self.question = question
        
        # Add buttons for each option
        for i, option in enumerate(question['options']):
            button = Button(
                label=option['text'][:80],  # Discord limit
                style=discord.ButtonStyle.secondary,
                custom_id=f"answer_{question['id']}_{i}"
            )
            button.callback = self.create_callback(i)
            self.add_item(button)
    
    def create_callback(self, option_index: int):
        """Create callback for option button"""
        async def callback(interaction: discord.Interaction):
            await interaction.response.defer(ephemeral=True)
            
            # Get AURORA reaction to choice
            from npcs.guardians import guardian_swarm
            aurora = guardian_swarm.get_guardian('AURORA')
            selected_option = self.question['options'][option_index]
            if aurora:
                reaction = aurora.react_to_choice(
                    interaction.user.display_name,
                    selected_option['text'],
                    "Great choice! This reveals something powerful about you!"
                )
                reaction_embed = discord.Embed(**reaction)
                await interaction.followup.send(embed=reaction_embed, ephemeral=True)
            
            result = self.onboarding_engine.answer_question(
                self.discord_id,
                self.question['id'],
                option_index
            )
            
            if result['status'] == 'question':
                # Next question
                await asyncio.sleep(1)  # Brief pause for cinematic effect
                view = GreatnessSprintView(
                    self.onboarding_engine,
                    self.discord_id,
                    result['question']
                )
                embed = discord.Embed(
                    title=f" **Greatness Sprint** - Question {int(result.get('progress', 0) * 5) + 1}/5",
                    description=f"**{result['question']['question']}**\n\nChoose your answer:",
                    color=0xff00ff
                )
                embed.set_footer(text=f"Progress: {int(result.get('progress', 0) * 100)}%")
                await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            elif result['status'] == 'role_stack_assigned':
                # Step 3: Traits → Role Stack Assignment
                await self._show_role_stack(interaction, result)
        
        return callback
    
    async def _show_role_stack(self, interaction: discord.Interaction, result: Dict):
        """Show role stack assignment"""
        reveal_embed = discord.Embed(**result['reveal_message'])
        await interaction.followup.send(embed=reveal_embed, ephemeral=True)
        
        guardian_embed = discord.Embed(**result['guardian_message'])
        await interaction.followup.send(embed=guardian_embed, ephemeral=True)
        
        # Show role stack
        role_stack = result.get('role_stack', [])
        from specialist_layer.personalization_engine import personalization_engine
        role_names = [result['personality']['personality_type']]
        for r in role_stack[1:]:
            if r in personalization_engine.trait_mappings:
                role_names.append(personalization_engine.trait_mappings[r]['personality'])
        
        stack_embed = discord.Embed(
            title=" **Your Role Stack**",
            description="You've unlocked multiple roles:\n\n" + "\n".join([
                f" **{role}**" for role in role_names[:3]
            ]),
            color=result['personality']['personality_color']
        )
        await interaction.followup.send(embed=stack_embed, ephemeral=True)
        
        # Step 4: Access Pathway
        await self._unlock_channels(interaction)
    
    async def _unlock_channels(self, interaction: discord.Interaction):
        """Step 4: Access Pathway → Channels Unlock"""
        result = self.onboarding_engine.unlock_access_pathway(
            self.discord_id,
            interaction.guild
        )
        
        if result['status'] == 'channels_unlocked':
            map_data = result.get('map_data', {})
            channels_embed = discord.Embed(
                title=" **Access Pathway Unlocked!**",
                description="You now have access to these areas:",
                color=0x00ff00
            )
            
            # Show unlocked areas
            for area in map_data.get('map_areas', [])[:5]:
                channels_text = ", ".join([f"#{c}" for c in area['channels'][:3]])
                channels_embed.add_field(
                    name=f"{area['icon']} {area['name']}",
                    value=channels_text,
                    inline=True
                )
            
            await interaction.followup.send(embed=channels_embed, ephemeral=True)
            
            # Step 5: Artifact Quest
            await self._start_artifact_quest(interaction)
    
    async def _start_artifact_quest(self, interaction: discord.Interaction):
        """Step 5: Artifact Quest → Choose Your Item"""
        result = self.onboarding_engine.start_artifact_quest(self.discord_id)
        
        if result['status'] == 'artifact_selection':
            view = ArtifactSelectionView(
                self.onboarding_engine,
                self.discord_id,
                result['artifacts']
            )
            
            artifacts_text = ""
            for a in result['artifacts'][:4]:
                role_info = ""
                if a.get('role'):
                    role_emoji = a.get('role_emoji', '')
                    role_info = f"\n{role_emoji} **{a['role']}**"
                
                perk_info = ""
                if a.get('perk'):
                    perk_info = f" | {a['perk']}"
                
                artifacts_text += f"{a['emoji']} **{a['name']}**{role_info}{perk_info}\n"
            
            embed = discord.Embed(
                title=" **ARTIFACT QUEST**",
                description="Choose your first Artifact.\n\nThis defines your starting destiny.\n\n" + artifacts_text,
                color=0xff00ff
            )
            await interaction.followup.send(embed=embed, view=view, ephemeral=True)

class ArtifactSelectionView(View):
    """Artifact selection view"""
    
    def __init__(self, onboarding_engine, discord_id: str, artifacts: List[Dict]):
        super().__init__(timeout=300)
        self.onboarding_engine = onboarding_engine
        self.discord_id = discord_id
        self.artifacts = artifacts
        
        # Add buttons for artifacts (max 5 buttons per view)
        for artifact in artifacts[:5]:
            # Create button label with emoji and name
            role_emoji = artifact.get('role_emoji', '')
            button_label = f"{artifact['emoji']} {artifact['name']}"
            if role_emoji:
                button_label = f"{artifact['emoji']} {role_emoji} {artifact['name']}"
            
            button = Button(
                label=button_label[:80],  # Discord limit
                style=discord.ButtonStyle.primary,
                custom_id=f"artifact_{artifact['artifact_id']}"
            )
            button.callback = self.create_callback(artifact['artifact_id'])
            self.add_item(button)
    
    def create_callback(self, artifact_id: str):
        """Create callback for artifact button"""
        async def callback(interaction: discord.Interaction):
            await interaction.response.defer(ephemeral=True)
            
            result = self.onboarding_engine.select_artifact(self.discord_id, artifact_id)
            
            if result['status'] == 'artifact_selected':
                artifact = result['artifact']
                
                role_info = ""
                if artifact.get('role'):
                    role_emoji = artifact.get('role_emoji', '')
                    role_info = f"\n\n{role_emoji} **Role Unlocked: {artifact['role']}**"
                
                perk_info = ""
                if artifact.get('perk'):
                    perk_info = f"\n **Perk:** {artifact['perk']}"
                
                embed = discord.Embed(
                    title=f" **{artifact['emoji']} {artifact['name']} Selected!**",
                    description=f"{artifact['description']}{role_info}{perk_info}\n\n"
                              f"**Bonus:** +{artifact['bonus_points']} points\n\n"
                              f"This artifact is now yours!",
                    color=0xff00ff
                )
                await interaction.followup.send(embed=embed, ephemeral=True)
                
                # Step 6: Personal Profile
                await self._generate_profile(interaction)
        
        return callback
    
    async def _generate_profile(self, interaction: discord.Interaction):
        """Step 6: Personal Profile → Generated by AI"""
        result = self.onboarding_engine.generate_personal_profile(self.discord_id)
        
        if result['status'] == 'profile_generated':
            profile_embed = discord.Embed(**result['ai_profile'])
            await interaction.followup.send(embed=profile_embed, ephemeral=True)
            
            # Step 7: Map Drop
            await self._show_map(interaction)
    
    async def _show_map(self, interaction: discord.Interaction):
        """Step 7: Map Drop → Teleport Buttons"""
        result = self.onboarding_engine.create_map_drop(self.discord_id)
        
        if result['status'] == 'map_ready':
            map_data = result['map_data']
            view = MapTeleportView(self.onboarding_engine, self.discord_id, map_data)
            
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
            
            # Add teleport points summary
            teleport_text = "\n".join([
                f"{point['name']} → #{point['channel']}"
                for point in map_data['teleport_points'][:8]
                if point.get('type') == 'channel'
            ])
            if teleport_text:
                embed.add_field(name=" Quick Teleport", value=teleport_text, inline=False)
            
            await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            
            # Step 8: First Quest
            await asyncio.sleep(2)
            await self._assign_first_quest(interaction)
    
    async def _assign_first_quest(self, interaction: discord.Interaction):
        """Step 8: First Quest → Immediate engagement"""
        result = self.onboarding_engine.assign_first_quest(self.discord_id)
        
        if result['status'] == 'quest_assigned':
            quest = result['quest']
            quest_embed = discord.Embed(**result['quest_message'])
            quest_embed.add_field(
                name="Quest Details",
                value=f"**{quest['name']}**\n{quest['description']}",
                inline=False
            )
            quest_embed.add_field(
                name="Rewards",
                value=f" {quest['reward_points']} points\n {quest.get('reward_badge', 'None')} badge",
                inline=False
            )
            
            view = QuestView(self.onboarding_engine, self.discord_id, quest['quest_id'])
            await interaction.followup.send(embed=quest_embed, view=view, ephemeral=True)

class MapTeleportView(View):
    """Map teleport view"""
    
    def __init__(self, onboarding_engine, discord_id: str, map_data: Dict):
        super().__init__(timeout=600)
        self.onboarding_engine = onboarding_engine
        self.discord_id = discord_id
        self.map_data = map_data
        
        # Add teleport buttons for channels only (max 5)
        channel_points = [p for p in map_data.get('teleport_points', []) if p.get('type') == 'channel']
        for point in channel_points[:5]:
            button = Button(
                label=point['name'][:80],
                style=discord.ButtonStyle.secondary,
                custom_id=f"teleport_{point['channel']}"
            )
            button.callback = self.create_callback(point['channel'], point.get('name', f"#{point['channel']}"))
            self.add_item(button)
    
    def create_callback(self, channel_name: str, display_name: str):
        """Create callback for teleport button"""
        async def callback(interaction: discord.Interaction):
            await interaction.response.send_message(
                f" **Teleporting to {display_name}...**\n\n"
                f"*Jump to #{channel_name} to continue your journey!*",
                ephemeral=True
            )
        return callback

class QuestView(View):
    """Quest view"""
    
    def __init__(self, onboarding_engine, discord_id: str, quest_id: str):
        super().__init__(timeout=600)
        self.onboarding_engine = onboarding_engine
        self.discord_id = discord_id
        self.quest_id = quest_id
    
    @discord.ui.button(label=" Complete Quest", style=discord.ButtonStyle.success, emoji="")
    async def complete_quest(self, interaction: discord.Interaction, button: Button):
        """Complete quest"""
        await interaction.response.defer(ephemeral=True)
        
        result = self.onboarding_engine.complete_quest(self.discord_id, self.quest_id)
        
        if result['status'] == 'quest_completed':
            # Success message
            embed = discord.Embed(**result['encouragement'])
            embed.add_field(
                name="Rewards Earned",
                value=f" +{result['points_awarded']} points\n"
                      f" Total: {result['total_points']} points",
                inline=False
            )
            
            if result.get('badge_unlocked'):
                badge = result['badge_unlocked']
                embed.add_field(
                    name="Badge Unlocked!",
                    value=f"{badge['emoji']} **{badge['name']}**\n{badge['description']}",
                    inline=False
                )
            
            await interaction.followup.send(embed=embed, ephemeral=True)
            
            # Complete onboarding if welcome quest
            if self.quest_id == 'welcome_001':
                complete_result = self.onboarding_engine.complete_onboarding(self.discord_id)
                if complete_result['status'] == 'completed':
                    complete_embed = discord.Embed(
                        title=" **Onboarding Complete!**",
                        description=complete_result['message'],
                        color=0x00ff00
                    )
                    await interaction.followup.send(embed=complete_embed, ephemeral=True)

class DiscordBotEngine:
    """Discord bot engine - handles all Discord interactions"""
    
    def __init__(self, onboarding_engine):
        self.onboarding_engine = onboarding_engine
    
    def create_welcome_embed(self, username: str) -> discord.Embed:
        """Create welcome embed"""
        return discord.Embed(
            title=" **Welcome to GreatnessZone™!**",
            description=f"Hey {username}! Ready to discover your greatness?\n\n"
                       f"Click the button below to start your 8-step journey!",
            color=0xff00ff,
            timestamp=datetime.utcnow()
        )
    
    def create_onboarding_view(self, discord_id: str) -> OnboardingView:
        """Create onboarding view"""
        return OnboardingView(self.onboarding_engine, discord_id)
    
    def create_profile_embed(self, profile_summary: Dict) -> discord.Embed:
        """Create profile embed"""
        profile = profile_summary['profile']
        embed = discord.Embed(
            title=f" **{profile['username']}'s Profile**",
            color=0x00ff00,
            timestamp=datetime.utcnow()
        )
        
        embed.add_field(name="Level", value=f" {profile_summary['level']}", inline=True)
        embed.add_field(name="Points", value=f" {profile_summary['points']}", inline=True)
        
        if profile_summary['roles']:
            embed.add_field(
                name="Roles",
                value=", ".join(profile_summary['roles']),
                inline=False
            )
        
        if profile_summary['traits']:
            traits_str = "\n".join([
                f"{t['trait_name']}: {int(t['trait_value'] * 100)}%"
                for t in profile_summary['traits'][:5]
            ])
            embed.add_field(name="Traits", value=traits_str, inline=False)
        
        return embed

# Global instance (will be initialized)
discord_bot_engine = None

def initialize_discord_bot_engine(onboarding_engine):
    """Initialize Discord bot engine"""
    global discord_bot_engine
    discord_bot_engine = DiscordBotEngine(onboarding_engine)
    return discord_bot_engine
