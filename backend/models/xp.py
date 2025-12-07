"""
XP and leveling event models.
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID


class XPEvent(BaseModel):
    """XP gain event model."""
    user_id: UUID
    event_type: str = Field(..., description="Type of event (message, voice, command, daily)")
    xp_amount: int = Field(..., description="Amount of XP gained")
    channel_id: Optional[str] = Field(None, description="Discord channel ID")
    metadata: Optional[dict] = Field(default_factory=dict, description="Additional event data")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        from_attributes = True


class LevelUpEvent(BaseModel):
    """Level up event model for real-time notifications."""
    user_id: UUID
    discord_id: str
    username: str
    old_level: int
    new_level: int
    new_tier: str
    unlocked_tools: list[str] = Field(default_factory=list, description="Newly unlocked tool names")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class XPGainResponse(BaseModel):
    """Response model for XP gain."""
    success: bool
    xp_gained: int
    total_xp: int
    current_level: int
    leveled_up: bool = False
    new_level: Optional[int] = None
    unlocked_tools: list[str] = Field(default_factory=list)

