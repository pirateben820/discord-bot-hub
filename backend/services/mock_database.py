"""
Mock database service for testing without Supabase.
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid


class MockDatabase:
    """Mock database for testing."""
    
    def __init__(self):
        self.users: Dict[str, Dict] = {}
        self.tools: Dict[str, Dict] = {}
        self.user_tool_access: List[Dict] = []
        self.xp_events: List[Dict] = []
        
        # Initialize with sample data
        self._init_sample_data()
    
    def _init_sample_data(self):
        """Initialize with sample users and tools."""
        # Sample user
        user_id = str(uuid.uuid4())
        self.users['123456789'] = {
            'id': user_id,
            'discord_id': '123456789',
            'username': 'TestUser',
            'avatar_url': 'https://cdn.discordapp.com/embed/avatars/0.png',
            'xp': 250,
            'level': 3,
            'rank_tier': 'Basic',
            'streak_days': 5,
            'last_active': datetime.utcnow().isoformat(),
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat()
        }
        
        # Sample tools
        tools_data = [
            {'name': 'Basic Chat', 'tier': 'Basic', 'required_level': 1, 'icon': '💬'},
            {'name': 'Profile Customization', 'tier': 'Basic', 'required_level': 1, 'icon': '🎨'},
            {'name': 'Daily Rewards', 'tier': 'Basic', 'required_level': 5, 'icon': '🎁'},
            {'name': 'Voice Channels', 'tier': 'Member', 'required_level': 11, 'icon': '🎤'},
            {'name': 'AI Chat Assistant', 'tier': 'Advanced', 'required_level': 26, 'icon': '🤖'},
        ]
        
        for tool_data in tools_data:
            tool_id = str(uuid.uuid4())
            self.tools[tool_id] = {
                'id': tool_id,
                'name': tool_data['name'],
                'description': f"Access to {tool_data['name']}",
                'icon': tool_data['icon'],
                'required_level': tool_data['required_level'],
                'tier': tool_data['tier'],
                'enabled': True,
                'config': {},
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat()
            }
        
        # Unlock first 2 tools for test user
        unlocked_tools = list(self.tools.values())[:2]
        for tool in unlocked_tools:
            self.user_tool_access.append({
                'user_id': user_id,
                'tool_id': tool['id'],
                'unlocked_at': datetime.utcnow().isoformat(),
                'usage_count': 0
            })
    
    def table(self, table_name: str):
        """Mock table method."""
        return MockTable(self, table_name)


class MockTable:
    """Mock table for query building."""
    
    def __init__(self, db: MockDatabase, table_name: str):
        self.db = db
        self.table_name = table_name
        self._filters = {}
        self._select_fields = '*'
        self._limit_val = None
        self._order_by = None
    
    def select(self, fields: str = '*'):
        self._select_fields = fields
        return self
    
    def eq(self, field: str, value: Any):
        self._filters[field] = value
        return self
    
    def limit(self, n: int):
        self._limit_val = n
        return self
    
    def order(self, field: str, desc: bool = False):
        self._order_by = (field, desc)
        return self
    
    def execute(self):
        """Execute the query."""
        if self.table_name == 'users':
            data = list(self.db.users.values())
        elif self.table_name == 'tools':
            data = list(self.db.tools.values())
        elif self.table_name == 'user_tool_access':
            data = self.db.user_tool_access
        elif self.table_name == 'xp_events':
            data = self.db.xp_events
        else:
            data = []
        
        # Apply filters
        for field, value in self._filters.items():
            data = [item for item in data if item.get(field) == value]
        
        # Apply ordering
        if self._order_by:
            field, desc = self._order_by
            data = sorted(data, key=lambda x: x.get(field, 0), reverse=desc)
        
        # Apply limit
        if self._limit_val:
            data = data[:self._limit_val]
        
        return MockResponse(data)
    
    def insert(self, data: Dict):
        """Insert data."""
        if self.table_name == 'users':
            self.db.users[data['discord_id']] = data
        elif self.table_name == 'tools':
            self.db.tools[data['id']] = data
        elif self.table_name == 'user_tool_access':
            self.db.user_tool_access.append(data)
        elif self.table_name == 'xp_events':
            self.db.xp_events.append(data)
        
        return MockResponse([data])
    
    def update(self, data: Dict):
        """Update data."""
        return self


class MockResponse:
    """Mock response object."""
    
    def __init__(self, data: List[Dict]):
        self.data = data


# Global mock database instance
mock_db = MockDatabase()

