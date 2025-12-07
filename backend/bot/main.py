"""
Discord Bot - Main entry point
Cog-based architecture inspired by old/discord-bot patterns.
"""
import discord
from discord.ext import commands
import asyncio
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import settings


class DiscordBotHub(commands.Bot):
    """Custom bot class with initialization logic."""
    
    def __init__(self):
        """Initialize bot with intents and configuration."""
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.presences = True
        intents.voice_states = True
        
        super().__init__(
            command_prefix='!',
            intents=intents,
            help_command=None  # We'll create custom help
        )
    
    async def setup_hook(self):
        """Load cogs and sync commands."""
        print("Loading cogs...")
        
        # List of cogs to load
        cogs = [
            'bot.cogs.xp',
            'bot.cogs.rank',
            'bot.cogs.admin',
            'bot.cogs.sync'
        ]
        
        for cog in cogs:
            try:
                await self.load_extension(cog)
                print(f"✓ Loaded {cog}")
            except Exception as e:
                print(f"✗ Failed to load {cog}: {e}")
        
        # Sync slash commands
        try:
            synced = await self.tree.sync()
            print(f"✓ Synced {len(synced)} slash commands")
        except Exception as e:
            print(f"✗ Failed to sync commands: {e}")
    
    async def on_ready(self):
        """Called when bot is ready."""
        print(f"\n{'='*50}")
        print(f"Bot is ready!")
        print(f"Logged in as: {self.user.name} ({self.user.id})")
        print(f"Servers: {len(self.guilds)}")
        print(f"{'='*50}\n")
        
        # Set bot status
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="you level up! | !help"
            )
        )
    
    async def on_command_error(self, ctx, error):
        """Global error handler."""
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You don't have permission to use this command.")
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"⏰ Command on cooldown. Try again in {error.retry_after:.1f}s")
        else:
            print(f"Error in command {ctx.command}: {error}")
            await ctx.send("❌ An error occurred while executing the command.")


async def main():
    """Main bot entry point."""
    bot = DiscordBotHub()
    
    try:
        await bot.start(settings.discord_token)
    except KeyboardInterrupt:
        print("\nShutting down bot...")
        await bot.close()
    except Exception as e:
        print(f"Fatal error: {e}")
        await bot.close()


if __name__ == "__main__":
    asyncio.run(main())

