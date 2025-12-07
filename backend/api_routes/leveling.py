"""
Leveling and XP API routes.
"""
from fastapi import APIRouter, HTTPException, status
from typing import List
from datetime import datetime

from models.xp import XPEvent, XPGainResponse, LevelUpEvent
from models.user import LeaderboardEntry, UserResponse
from services.database import db
from services.leveling_service import leveling_service

router = APIRouter()


@router.post("/xp", response_model=XPGainResponse)
async def add_xp(discord_id: str, event_type: str, xp_amount: int = None, channel_id: str = None):
    """Add XP to a user and check for level up."""
    try:
        # Get user
        user_result = db.client.table('users').select('*').eq('discord_id', discord_id).execute()
        
        if not user_result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with Discord ID {discord_id} not found"
            )
        
        user = user_result.data[0]
        old_xp = user['xp']
        old_level = user['level']
        
        # Calculate XP amount if not provided
        if xp_amount is None:
            xp_amount = leveling_service.XP_AMOUNTS.get(event_type, 0)
        
        # Add XP
        new_xp = old_xp + xp_amount
        
        # Check for level up
        leveled_up, _, new_level = leveling_service.check_level_up(old_xp, new_xp)
        
        # Update tier if leveled up
        new_tier = leveling_service.get_tier_from_level(new_level) if leveled_up else user['rank_tier']
        
        # Update user in database
        update_data = {
            'xp': new_xp,
            'level': new_level,
            'rank_tier': new_tier,
            'last_active': datetime.utcnow().isoformat()
        }
        
        db.client.table('users').update(update_data).eq('discord_id', discord_id).execute()
        
        # Log XP event
        xp_event = {
            'user_id': user['id'],
            'event_type': event_type,
            'xp_amount': xp_amount,
            'channel_id': channel_id,
            'created_at': datetime.utcnow().isoformat()
        }
        db.client.table('xp_events').insert(xp_event).execute()
        
        # TODO: Check for newly unlocked tools
        unlocked_tools = []
        
        # TODO: Emit Socket.IO event if leveled up
        
        return XPGainResponse(
            success=True,
            xp_gained=xp_amount,
            total_xp=new_xp,
            current_level=new_level,
            leveled_up=leveled_up,
            new_level=new_level if leveled_up else None,
            unlocked_tools=unlocked_tools
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to add XP: {str(e)}"
        )


@router.get("/leaderboard", response_model=List[LeaderboardEntry])
async def get_leaderboard(limit: int = 10):
    """Get server leaderboard by XP."""
    try:
        result = db.client.table('users').select('*').order('xp', desc=True).limit(limit).execute()
        
        leaderboard = []
        for rank, user_dict in enumerate(result.data, start=1):
            next_level_xp = leveling_service.get_xp_for_next_level(
                user_dict['xp'],
                user_dict['level']
            )
            
            user_response = UserResponse(
                **user_dict,
                unlocked_tools_count=0,
                next_level_xp=next_level_xp
            )
            
            leaderboard.append(LeaderboardEntry(
                rank=rank,
                user=user_response,
                xp=user_dict['xp'],
                level=user_dict['level']
            ))
        
        return leaderboard
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get leaderboard: {str(e)}"
        )


@router.get("/xp-history/{discord_id}", response_model=List[XPEvent])
async def get_xp_history(discord_id: str, limit: int = 50):
    """Get XP history for a user."""
    try:
        # Get user ID
        user_result = db.client.table('users').select('id').eq('discord_id', discord_id).execute()
        
        if not user_result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with Discord ID {discord_id} not found"
            )
        
        user_id = user_result.data[0]['id']
        
        # Get XP events
        events_result = db.client.table('xp_events').select('*').eq('user_id', user_id).order('created_at', desc=True).limit(limit).execute()
        
        return [XPEvent(**event) for event in events_result.data]
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get XP history: {str(e)}"
        )

