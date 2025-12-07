"""
XP Tracking Cog
Tracks user activity and awards XP based on messages, voice, and commands.
"""
import discord
from discord.ext import commands
from datetime import datetime, timedelta
from collections import defaultdict
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from services.leveling_service import leveling_service


class XPCog(commands.Cog):
    """Cog for tracking XP from user activity."""
    
    def __init__(self, bot):
        """Initialize XP cog."""
        self.bot = bot
        self.message_cooldowns = defaultdict(lambda: datetime.min)
        self.voice_tracking = {}  # user_id: join_time
    
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Award XP for messages."""
        # Ignore bots and DMs
        if message.author.bot or not message.guild:
            return
        
        user_id = str(message.author.id)
        now = datetime.utcnow()
        
        # Check cooldown
        last_message = self.message_cooldowns[user_id]
        cooldown = timedelta(seconds=leveling_service.COOLDOWNS["message"])
        
        if now - last_message < cooldown:
            return
        
        # Update cooldown
        self.message_cooldowns[user_id] = now
        
        # Award XP
        xp_amount = leveling_service.XP_AMOUNTS["message"]
        
        # TODO: Send XP to API
        # For now, just log it
        print(f"[XP] {message.author.name} earned {xp_amount} XP from message")
    
    @commands.Cog.listener()
    async def on_voice_state_update(
        self,
        member: discord.Member,
        before: discord.VoiceState,
        after: discord.VoiceState
    ):
        """Track voice chat time and award XP."""
        user_id = str(member.id)
        
        # User joined voice
        if before.channel is None and after.channel is not None:
            self.voice_tracking[user_id] = datetime.utcnow()
            print(f"[Voice] {member.name} joined voice channel")
        
        # User left voice
        elif before.channel is not None and after.channel is None:
            if user_id in self.voice_tracking:
                join_time = self.voice_tracking.pop(user_id)
                duration = (datetime.utcnow() - join_time).total_seconds()
                minutes = int(duration / 60)
                
                if minutes > 0:
                    xp_amount = minutes * leveling_service.XP_AMOUNTS["voice_minute"]
                    print(f"[XP] {member.name} earned {xp_amount} XP from {minutes} minutes in voice")
                    # TODO: Send XP to API
    
    @commands.command(name="xp")
    async def check_xp(self, ctx):
        """Check your current XP and level."""
        # TODO: Fetch from API
        embed = discord.Embed(
            title=f"{ctx.author.name}'s XP",
            description="XP tracking coming soon!",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)


async def setup(bot):
    """Load the XP cog."""
    await bot.add_cog(XPCog(bot))

