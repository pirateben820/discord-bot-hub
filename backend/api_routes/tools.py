"""
Tools API routes.
"""
from fastapi import APIRouter, HTTPException, status
from typing import List
from uuid import UUID

from models.tool import Tool, ToolCreate, ToolResponse
from services.database import db
from services.leveling_service import leveling_service

router = APIRouter()


@router.post("/", response_model=Tool, status_code=status.HTTP_201_CREATED)
async def create_tool(tool_data: ToolCreate):
    """Create a new tool."""
    try:
        tool_dict = tool_data.dict()
        result = db.client.table('tools').insert(tool_dict).execute()
        
        return Tool(**result.data[0])
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create tool: {str(e)}"
        )


@router.get("/", response_model=List[Tool])
async def list_tools(tier: str = None, enabled_only: bool = True):
    """List all tools, optionally filtered by tier."""
    try:
        query = db.client.table('tools').select('*')
        
        if tier:
            query = query.eq('tier', tier)
        
        if enabled_only:
            query = query.eq('enabled', True)
        
        result = query.order('required_level').execute()
        
        return [Tool(**tool) for tool in result.data]
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list tools: {str(e)}"
        )


@router.get("/user/{discord_id}", response_model=List[ToolResponse])
async def get_user_tools(discord_id: str):
    """Get all tools with user's access status."""
    try:
        # Get user
        user_result = db.client.table('users').select('*').eq('discord_id', discord_id).execute()
        
        if not user_result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with Discord ID {discord_id} not found"
            )
        
        user = user_result.data[0]
        user_level = user['level']
        
        # Get all tools
        tools_result = db.client.table('tools').select('*').eq('enabled', True).order('required_level').execute()
        
        # Get user's unlocked tools
        access_result = db.client.table('user_tool_access').select('*').eq('user_id', user['id']).execute()
        unlocked_tool_ids = {access['tool_id'] for access in access_result.data}
        access_map = {access['tool_id']: access for access in access_result.data}
        
        tool_responses = []
        for tool_dict in tools_result.data:
            tool = Tool(**tool_dict)
            tool_id = str(tool.id)
            is_unlocked = tool_id in unlocked_tool_ids
            can_unlock = user_level >= tool.required_level and not is_unlocked
            
            access_info = access_map.get(tool_id, {})
            
            tool_responses.append(ToolResponse(
                tool=tool,
                is_unlocked=is_unlocked,
                unlocked_at=access_info.get('unlocked_at'),
                usage_count=access_info.get('usage_count', 0),
                can_unlock=can_unlock
            ))
        
        return tool_responses
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get user tools: {str(e)}"
        )


@router.post("/unlock/{discord_id}/{tool_id}", response_model=dict)
async def unlock_tool(discord_id: str, tool_id: UUID):
    """Unlock a tool for a user."""
    try:
        # Get user
        user_result = db.client.table('users').select('*').eq('discord_id', discord_id).execute()
        
        if not user_result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with Discord ID {discord_id} not found"
            )
        
        user = user_result.data[0]
        
        # Get tool
        tool_result = db.client.table('tools').select('*').eq('id', str(tool_id)).execute()
        
        if not tool_result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tool with ID {tool_id} not found"
            )
        
        tool = tool_result.data[0]
        
        # Check if user has required level
        if user['level'] < tool['required_level']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User level {user['level']} is below required level {tool['required_level']}"
            )
        
        # Check if already unlocked
        existing = db.client.table('user_tool_access').select('*').eq('user_id', user['id']).eq('tool_id', str(tool_id)).execute()
        
        if existing.data:
            return {"message": "Tool already unlocked", "already_unlocked": True}
        
        # Unlock tool
        access_data = {
            'user_id': user['id'],
            'tool_id': str(tool_id),
            'usage_count': 0
        }
        
        db.client.table('user_tool_access').insert(access_data).execute()
        
        return {"message": "Tool unlocked successfully", "tool_name": tool['name']}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to unlock tool: {str(e)}"
        )

