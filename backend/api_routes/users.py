"""
User API routes.
"""
from fastapi import APIRouter, HTTPException, status
from typing import List
from uuid import UUID

from models.user import User, UserCreate, UserUpdate, UserResponse
from services.database import db
from services.leveling_service import leveling_service

router = APIRouter()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate):
    """Create a new user or return existing user."""
    try:
        # Check if user already exists
        existing = db.client.table('users').select('*').eq('discord_id', user_data.discord_id).execute()
        
        if existing.data:
            # User exists, update their info
            user = existing.data[0]
            updated = db.client.table('users').update({
                'username': user_data.username,
                'avatar_url': user_data.avatar_url
            }).eq('discord_id', user_data.discord_id).execute()
            
            user_dict = updated.data[0]
        else:
            # Create new user
            new_user = {
                'discord_id': user_data.discord_id,
                'username': user_data.username,
                'avatar_url': user_data.avatar_url,
                'xp': 0,
                'level': 1,
                'rank_tier': 'Basic',
                'streak_days': 0
            }
            
            result = db.client.table('users').insert(new_user).execute()
            user_dict = result.data[0]
        
        # Calculate next level XP
        next_level_xp = leveling_service.get_xp_for_next_level(
            user_dict['xp'],
            user_dict['level']
        )
        
        return UserResponse(
            **user_dict,
            unlocked_tools_count=0,  # TODO: Query from user_tool_access
            next_level_xp=next_level_xp
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create user: {str(e)}"
        )


@router.get("/{discord_id}", response_model=UserResponse)
async def get_user(discord_id: str):
    """Get user by Discord ID."""
    try:
        result = db.client.table('users').select('*').eq('discord_id', discord_id).execute()
        
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with Discord ID {discord_id} not found"
            )
        
        user_dict = result.data[0]
        
        # Calculate next level XP
        next_level_xp = leveling_service.get_xp_for_next_level(
            user_dict['xp'],
            user_dict['level']
        )
        
        return UserResponse(
            **user_dict,
            unlocked_tools_count=0,  # TODO: Query from user_tool_access
            next_level_xp=next_level_xp
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get user: {str(e)}"
        )


@router.patch("/{discord_id}", response_model=UserResponse)
async def update_user(discord_id: str, user_update: UserUpdate):
    """Update user information."""
    try:
        # Build update dict (only include non-None values)
        update_data = {k: v for k, v in user_update.dict().items() if v is not None}
        
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields to update"
            )
        
        result = db.client.table('users').update(update_data).eq('discord_id', discord_id).execute()
        
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with Discord ID {discord_id} not found"
            )
        
        user_dict = result.data[0]
        
        next_level_xp = leveling_service.get_xp_for_next_level(
            user_dict['xp'],
            user_dict['level']
        )
        
        return UserResponse(
            **user_dict,
            unlocked_tools_count=0,
            next_level_xp=next_level_xp
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update user: {str(e)}"
        )


@router.get("/", response_model=List[UserResponse])
async def list_users(limit: int = 100, offset: int = 0):
    """List all users with pagination."""
    try:
        result = db.client.table('users').select('*').range(offset, offset + limit - 1).execute()
        
        users = []
        for user_dict in result.data:
            next_level_xp = leveling_service.get_xp_for_next_level(
                user_dict['xp'],
                user_dict['level']
            )
            users.append(UserResponse(
                **user_dict,
                unlocked_tools_count=0,
                next_level_xp=next_level_xp
            ))
        
        return users
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list users: {str(e)}"
        )

