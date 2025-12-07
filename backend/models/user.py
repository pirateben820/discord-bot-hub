"""
User models for Discord Bot Hub.
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID


class UserBase(BaseModel):
    """Base user model with common fields."""
    discord_id: str = Field(..., description="Discord user ID")
    username: str = Field(..., description="Discord username")
    avatar_url: Optional[str] = Field(None, description="Discord avatar URL")


class UserCreate(UserBase):
    """Model for creating a new user."""
    pass


class UserUpdate(BaseModel):
    """Model for updating user information."""
    username: Optional[str] = None
    avatar_url: Optional[str] = None
    xp: Optional[int] = None
    level: Optional[int] = None


class User(UserBase):
    """Complete user model from database."""
    id: UUID
    xp: int = Field(default=0, description="Total experience points")
    level: int = Field(default=1, description="Current level")
    rank_tier: str = Field(default="Basic", description="Current rank tier")
    streak_days: int = Field(default=0, description="Consecutive active days")
    last_active: Optional[datetime] = Field(None, description="Last activity timestamp")
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    """User response model for API endpoints."""
    id: UUID
    discord_id: str
    username: str
    avatar_url: Optional[str]
    xp: int
    level: int
    rank_tier: str
    streak_days: int
    unlocked_tools_count: int = 0
    next_level_xp: int = 0
    
    class Config:
        from_attributes = True


class LeaderboardEntry(BaseModel):
    """Leaderboard entry model."""
    rank: int
    user: UserResponse
    xp: int
    level: int

