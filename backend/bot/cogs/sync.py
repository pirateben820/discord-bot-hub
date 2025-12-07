"""
Sync Cog
Syncs Discord bot data with the FastAPI backend.
"""
import discord
from discord.ext import commands, tasks
import aiohttp
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from config import settings


class SyncCog(commands.Cog):
    """Cog for syncing data with backend API."""
    
    def __init__(self, bot):
        """Initialize sync cog."""
        self.bot = bot
        self.api_url = f"http://{settings.api_host}:{settings.api_port}/api"
        self.session: aiohttp.ClientSession = None
    
    async def cog_load(self):
        """Called when cog is loaded."""
        self.session = aiohttp.ClientSession()
        # Start background sync task
        # self.sync_users.start()
    
    async def cog_unload(self):
        """Called when cog is unloaded."""
        # self.sync_users.cancel()
        if self.session:
            await self.session.close()
    
    async def ensure_user_exists(self, discord_user: discord.User):
        """Ensure user exists in database."""
        try:
            user_data = {
                "discord_id": str(discord_user.id),
                "username": discord_user.name,
                "avatar_url": str(discord_user.display_avatar.url)
            }
            
            # TODO: Implement API call
            # async with self.session.post(f"{self.api_url}/users", json=user_data) as resp:
            #     return await resp.json()
            
            print(f"[Sync] Would create/update user: {discord_user.name}")
        except Exception as e:
            print(f"[Sync] Error ensuring user exists: {e}")
    
    async def send_xp_event(self, user_id: str, event_type: str, xp_amount: int, channel_id: str = None):
        """Send XP event to API."""
        try:
            event_data = {
                "user_id": user_id,
                "event_type": event_type,
                "xp_amount": xp_amount,
                "channel_id": channel_id
            }
            
            # TODO: Implement API call
            # async with self.session.post(f"{self.api_url}/xp/events", json=event_data) as resp:
            #     return await resp.json()
            
            print(f"[Sync] Would send XP event: {event_type} +{xp_amount} XP")
        except Exception as e:
            print(f"[Sync] Error sending XP event: {e}")
    
    @tasks.loop(minutes=5)
    async def sync_users(self):
        """Periodically sync all guild members."""
        print("[Sync] Starting user sync...")
        for guild in self.bot.guilds:
            for member in guild.members:
                if not member.bot:
                    await self.ensure_user_exists(member)
        print("[Sync] User sync complete")


async def setup(bot):
    """Load the sync cog."""
    await bot.add_cog(SyncCog(bot))

