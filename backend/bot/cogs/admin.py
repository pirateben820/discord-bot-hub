"""
Admin Commands Cog
Administrative commands for managing XP, levels, and bot configuration.
"""
import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional


class AdminCog(commands.Cog):
    """Cog for admin commands."""
    
    def __init__(self, bot):
        """Initialize admin cog."""
        self.bot = bot
    
    @app_commands.command(name="addxp", description="[Admin] Add XP to a user")
    @app_commands.checks.has_permissions(administrator=True)
    async def add_xp(
        self,
        interaction: discord.Interaction,
        user: discord.Member,
        amount: int
    ):
        """Add XP to a user."""
        await interaction.response.defer(ephemeral=True)
        
        # TODO: Send to API
        embed = discord.Embed(
            title="✅ XP Added",
            description=f"Added {amount} XP to {user.mention}",
            color=discord.Color.green()
        )
        
        await interaction.followup.send(embed=embed, ephemeral=True)
    
    @app_commands.command(name="setlevel", description="[Admin] Set user level")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_level(
        self,
        interaction: discord.Interaction,
        user: discord.Member,
        level: int
    ):
        """Set a user's level."""
        await interaction.response.defer(ephemeral=True)
        
        # TODO: Send to API
        embed = discord.Embed(
            title="✅ Level Set",
            description=f"Set {user.mention}'s level to {level}",
            color=discord.Color.green()
        )
        
        await interaction.followup.send(embed=embed, ephemeral=True)
    
    @app_commands.command(name="resetxp", description="[Admin] Reset user XP")
    @app_commands.checks.has_permissions(administrator=True)
    async def reset_xp(
        self,
        interaction: discord.Interaction,
        user: discord.Member
    ):
        """Reset a user's XP."""
        await interaction.response.defer(ephemeral=True)
        
        # TODO: Send to API
        embed = discord.Embed(
            title="✅ XP Reset",
            description=f"Reset {user.mention}'s XP to 0",
            color=discord.Color.orange()
        )
        
        await interaction.followup.send(embed=embed, ephemeral=True)
    
    @app_commands.command(name="botstats", description="[Admin] View bot statistics")
    @app_commands.checks.has_permissions(administrator=True)
    async def bot_stats(self, interaction: discord.Interaction):
        """Show bot statistics."""
        embed = discord.Embed(
            title="🤖 Bot Statistics",
            color=discord.Color.blue()
        )
        
        embed.add_field(name="Servers", value=len(self.bot.guilds), inline=True)
        embed.add_field(name="Users", value=len(self.bot.users), inline=True)
        embed.add_field(name="Latency", value=f"{self.bot.latency*1000:.0f}ms", inline=True)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot):
    """Load the admin cog."""
    await bot.add_cog(AdminCog(bot))

