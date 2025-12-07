"""
Tool models for Discord Bot Hub.
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID


class ToolBase(BaseModel):
    """Base tool model."""
    name: str = Field(..., description="Tool name")
    description: str = Field(..., description="Tool description")
    icon: str = Field(default="🛠️", description="Tool icon emoji")
    required_level: int = Field(..., description="Minimum level to unlock")
    tier: str = Field(..., description="Tool tier (Basic, Member, Advanced, Elite, Master)")


class ToolCreate(ToolBase):
    """Model for creating a new tool."""
    config: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Tool configuration")
    enabled: bool = Field(default=True, description="Whether tool is enabled")


class Tool(ToolBase):
    """Complete tool model from database."""
    id: UUID
    enabled: bool
    config: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ToolAccess(BaseModel):
    """User tool access model."""
    user_id: UUID
    tool_id: UUID
    unlocked_at: datetime
    usage_count: int = 0
    
    class Config:
        from_attributes = True


class ToolResponse(BaseModel):
    """Tool response with user access info."""
    tool: Tool
    is_unlocked: bool
    unlocked_at: Optional[datetime] = None
    usage_count: int = 0
    can_unlock: bool = False

