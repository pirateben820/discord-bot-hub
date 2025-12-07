"""
Database service using Supabase client.
"""
from supabase import create_client, Client
from config import settings
from typing import Optional


class DatabaseService:
    """Supabase database service."""
    
    _instance: Optional['DatabaseService'] = None
    _client: Optional[Client] = None
    
    def __new__(cls):
        """Singleton pattern for database service."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize Supabase client."""
        if self._client is None:
            self._client = create_client(
                settings.supabase_url,
                settings.supabase_key
            )
    
    @property
    def client(self) -> Client:
        """Get Supabase client instance."""
        if self._client is None:
            raise RuntimeError("Database client not initialized")
        return self._client
    
    async def health_check(self) -> bool:
        """Check database connection health."""
        try:
            # Simple query to test connection
            result = self.client.table('users').select('id').limit(1).execute()
            return True
        except Exception as e:
            print(f"Database health check failed: {e}")
            return False


# Global database service instance
db = DatabaseService()

