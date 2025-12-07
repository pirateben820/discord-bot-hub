"""
Rank Commands Cog
Display user rank, level, and leaderboard.
"""
import discord
from discord import app_commands
from discord.ext import commands
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from services.leveling_service import leveling_service


class RankCog(commands.Cog):
    """Cog for rank and leaderboard commands."""
    
    def __init__(self, bot):
        """Initialize rank cog."""
        self.bot = bot
    
    @app_commands.command(name="rank", description="Check your rank and level")
    async def rank_slash(self, interaction: discord.Interaction):
        """Slash command to check rank."""
        await interaction.response.defer()
        
        # TODO: Fetch user data from API
        # For now, show placeholder
        embed = discord.Embed(
            title=f"📊 {interaction.user.name}'s Rank",
            color=discord.Color.blue()
        )
        embed.add_field(name="Level", value="1", inline=True)
        embed.add_field(name="XP", value="0 / 100", inline=True)
        embed.add_field(name="Rank", value="#???", inline=True)
        embed.add_field(name="Tier", value="Basic", inline=True)
        embed.add_field(name="Streak", value="0 days", inline=True)
        embed.add_field(name="Tools Unlocked", value="4 / 20", inline=True)
        
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        embed.set_footer(text="Keep chatting to earn more XP!")
        
        await interaction.followup.send(embed=embed)
    
    @commands.command(name="rank")
    async def rank_prefix(self, ctx):
        """Prefix command to check rank."""
        # TODO: Fetch user data from API
        embed = discord.Embed(
            title=f"📊 {ctx.author.name}'s Rank",
            color=discord.Color.blue()
        )
        embed.add_field(name="Level", value="1", inline=True)
        embed.add_field(name="XP", value="0 / 100", inline=True)
        embed.add_field(name="Rank", value="#???", inline=True)
        
        embed.set_thumbnail(url=ctx.author.display_avatar.url)
        await ctx.send(embed=embed)
    
    @app_commands.command(name="leaderboard", description="View server leaderboard")
    async def leaderboard(self, interaction: discord.Interaction):
        """Show server leaderboard."""
        await interaction.response.defer()
        
        # TODO: Fetch leaderboard from API
        embed = discord.Embed(
            title="🏆 Server Leaderboard",
            description="Top users by XP",
            color=discord.Color.gold()
        )
        
        # Placeholder data
        embed.add_field(
            name="Top 10",
            value="Leaderboard coming soon!\nKeep earning XP to climb the ranks!",
            inline=False
        )
        
        await interaction.followup.send(embed=embed)
    
    @app_commands.command(name="levels", description="View level requirements")
    async def levels(self, interaction: discord.Interaction):
        """Show level requirements and tiers."""
        embed = discord.Embed(
            title="📈 Level Tiers & Requirements",
            description="Unlock new tools as you level up!",
            color=discord.Color.purple()
        )
        
        for tier_name, (min_level, max_level) in leveling_service.TIERS.items():
            xp_required = leveling_service.calculate_xp_for_level(min_level)
            embed.add_field(
                name=f"{tier_name} Tier",
                value=f"Levels {min_level}-{max_level}\n{xp_required:,} XP to unlock",
                inline=True
            )
        
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    """Load the rank cog."""
    await bot.add_cog(RankCog(bot))

