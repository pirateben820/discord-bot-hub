"""
Leveling service - XP calculations and level progression.
Based on patterns from pem/archon service architecture.
"""
from typing import Tuple, List
from uuid import UUID
import math


class LevelingService:
    """Service for XP and leveling calculations."""
    
    # XP formula constants
    BASE_XP = 100
    COEFFICIENT = 50
    CONSTANT = 0
    
    # XP sources and amounts
    XP_AMOUNTS = {
        "message": 15,
        "voice_minute": 10,
        "command": 5,
        "daily_bonus": 50,
        "streak_bonus": 10
    }
    
    # Cooldowns in seconds
    COOLDOWNS = {
        "message": 60,
        "command": 30
    }
    
    # Tier thresholds
    TIERS = {
        "Basic": (1, 10),
        "Member": (11, 25),
        "Advanced": (26, 50),
        "Elite": (51, 75),
        "Master": (76, 100)
    }
    
    @staticmethod
    def calculate_xp_for_level(level: int) -> int:
        """
        Calculate total XP required to reach a specific level.
        Formula: XP = base * (level^2) + coefficient * level + constant
        
        Args:
            level: Target level
            
        Returns:
            Total XP required
        """
        return (
            LevelingService.BASE_XP * (level ** 2) +
            LevelingService.COEFFICIENT * level +
            LevelingService.CONSTANT
        )
    
    @staticmethod
    def calculate_level_from_xp(xp: int) -> int:
        """
        Calculate level from total XP using quadratic formula.
        
        Args:
            xp: Total experience points
            
        Returns:
            Current level
        """
        # Solve quadratic equation: BASE*level^2 + COEF*level + (CONST - xp) = 0
        a = LevelingService.BASE_XP
        b = LevelingService.COEFFICIENT
        c = LevelingService.CONSTANT - xp
        
        discriminant = b**2 - 4*a*c
        if discriminant < 0:
            return 1
        
        level = (-b + math.sqrt(discriminant)) / (2 * a)
        return max(1, int(level))
    
    @staticmethod
    def get_tier_from_level(level: int) -> str:
        """
        Get rank tier based on level.
        
        Args:
            level: User level
            
        Returns:
            Tier name
        """
        for tier_name, (min_level, max_level) in LevelingService.TIERS.items():
            if min_level <= level <= max_level:
                return tier_name
        return "Master"  # Default for levels > 100
    
    @staticmethod
    def get_xp_for_next_level(current_xp: int, current_level: int) -> int:
        """
        Calculate XP needed for next level.
        
        Args:
            current_xp: Current total XP
            current_level: Current level
            
        Returns:
            XP needed for next level
        """
        next_level_xp = LevelingService.calculate_xp_for_level(current_level + 1)
        return next_level_xp - current_xp
    
    @staticmethod
    def apply_multiplier(base_xp: int, multipliers: List[float]) -> int:
        """
        Apply multipliers to base XP.
        
        Args:
            base_xp: Base XP amount
            multipliers: List of multiplier values (e.g., [1.5, 2.0])
            
        Returns:
            XP after multipliers
        """
        total_multiplier = 1.0
        for mult in multipliers:
            total_multiplier *= mult
        return int(base_xp * total_multiplier)
    
    @staticmethod
    def check_level_up(old_xp: int, new_xp: int) -> Tuple[bool, int, int]:
        """
        Check if user leveled up.
        
        Args:
            old_xp: XP before gain
            new_xp: XP after gain
            
        Returns:
            Tuple of (leveled_up, old_level, new_level)
        """
        old_level = LevelingService.calculate_level_from_xp(old_xp)
        new_level = LevelingService.calculate_level_from_xp(new_xp)
        return (new_level > old_level, old_level, new_level)


# Global leveling service instance
leveling_service = LevelingService()

