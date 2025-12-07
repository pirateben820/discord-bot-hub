-- Discord Bot Hub Database Schema
-- PostgreSQL with pgvector extension for Supabase

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Enable pgvector for future AI features
CREATE EXTENSION IF NOT EXISTS vector;

-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    discord_id TEXT UNIQUE NOT NULL,
    username TEXT NOT NULL,
    avatar_url TEXT,
    xp INTEGER DEFAULT 0 CHECK (xp >= 0),
    level INTEGER DEFAULT 1 CHECK (level >= 1),
    rank_tier TEXT DEFAULT 'Basic' CHECK (rank_tier IN ('Basic', 'Member', 'Advanced', 'Elite', 'Master')),
    streak_days INTEGER DEFAULT 0 CHECK (streak_days >= 0),
    last_active TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tools table
CREATE TABLE tools (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    icon TEXT DEFAULT '🛠️',
    required_level INTEGER NOT NULL CHECK (required_level >= 1),
    tier TEXT NOT NULL CHECK (tier IN ('Basic', 'Member', 'Advanced', 'Elite', 'Master')),
    enabled BOOLEAN DEFAULT TRUE,
    config JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- User tool access table
CREATE TABLE user_tool_access (
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    tool_id UUID REFERENCES tools(id) ON DELETE CASCADE,
    unlocked_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    usage_count INTEGER DEFAULT 0 CHECK (usage_count >= 0),
    PRIMARY KEY (user_id, tool_id)
);

-- XP events table
CREATE TABLE xp_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    event_type TEXT NOT NULL,
    xp_amount INTEGER NOT NULL,
    channel_id TEXT,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Achievements table (future feature)
CREATE TABLE achievements (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    icon TEXT DEFAULT '🏆',
    requirement_type TEXT NOT NULL,
    requirement_value INTEGER NOT NULL,
    reward_xp INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- User achievements table (future feature)
CREATE TABLE user_achievements (
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    achievement_id UUID REFERENCES achievements(id) ON DELETE CASCADE,
    unlocked_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    PRIMARY KEY (user_id, achievement_id)
);

-- Indexes for performance
CREATE INDEX idx_users_discord_id ON users(discord_id);
CREATE INDEX idx_users_xp ON users(xp DESC);
CREATE INDEX idx_users_level ON users(level DESC);
CREATE INDEX idx_xp_events_user_id ON xp_events(user_id);
CREATE INDEX idx_xp_events_created_at ON xp_events(created_at DESC);
CREATE INDEX idx_tools_tier ON tools(tier);
CREATE INDEX idx_tools_required_level ON tools(required_level);
CREATE INDEX idx_user_tool_access_user_id ON user_tool_access(user_id);

-- Updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply updated_at trigger to tables
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_tools_updated_at BEFORE UPDATE ON tools
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Row Level Security (RLS) policies
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE tools ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_tool_access ENABLE ROW LEVEL SECURITY;
ALTER TABLE xp_events ENABLE ROW LEVEL SECURITY;

-- Allow service role full access (for backend API)
CREATE POLICY "Service role has full access to users" ON users
    FOR ALL USING (auth.role() = 'service_role');

CREATE POLICY "Service role has full access to tools" ON tools
    FOR ALL USING (auth.role() = 'service_role');

CREATE POLICY "Service role has full access to user_tool_access" ON user_tool_access
    FOR ALL USING (auth.role() = 'service_role');

CREATE POLICY "Service role has full access to xp_events" ON xp_events
    FOR ALL USING (auth.role() = 'service_role');

-- Public read access to tools
CREATE POLICY "Anyone can view enabled tools" ON tools
    FOR SELECT USING (enabled = TRUE);

-- Users can view their own data
CREATE POLICY "Users can view their own data" ON users
    FOR SELECT USING (auth.uid()::text = discord_id);

-- Insert default tools
INSERT INTO tools (name, description, icon, required_level, tier, config) VALUES
-- Basic Tier (Levels 1-10)
('Basic Chat', 'Access to basic chat commands and features', '💬', 1, 'Basic', '{"max_messages_per_day": 100}'),
('Profile Customization', 'Customize your profile with colors and status', '🎨', 1, 'Basic', '{}'),
('Leaderboard View', 'View server leaderboards and rankings', '📊', 1, 'Basic', '{}'),
('Daily Rewards', 'Claim daily XP bonuses', '🎁', 5, 'Basic', '{"daily_xp": 50}'),

-- Member Tier (Levels 11-25)
('Voice Channels', 'Create temporary voice channels', '🎤', 11, 'Member', '{"max_channels": 2}'),
('Custom Emojis', 'Upload and use custom emojis', '😀', 11, 'Member', '{"max_emojis": 5}'),
('Poll Creator', 'Create polls and surveys', '📋', 15, 'Member', '{}'),
('Music Bot', 'Play music in voice channels', '🎵', 20, 'Member', '{"max_queue": 10}'),

-- Advanced Tier (Levels 26-50)
('AI Chat Assistant', 'Chat with AI assistant', '🤖', 26, 'Advanced', '{"model": "gpt-3.5-turbo"}'),
('Code Helper', 'Get coding help and examples', '💻', 26, 'Advanced', '{}'),
('Image Generation', 'Generate images with AI', '🖼️', 30, 'Advanced', '{"daily_limit": 5}'),
('Advanced Analytics', 'View detailed server analytics', '📈', 40, 'Advanced', '{}'),

-- Elite Tier (Levels 51-75)
('Custom Commands', 'Create custom bot commands', '⚙️', 51, 'Elite', '{"max_commands": 10}'),
('Auto-Moderation', 'Configure auto-moderation rules', '🛡️', 51, 'Elite', '{}'),
('Web Scraper', 'Scrape and monitor websites', '🌐', 60, 'Elite', '{"max_urls": 5}'),
('Database Access', 'Query server database', '🗄️', 70, 'Elite', '{}'),

-- Master Tier (Levels 76-100)
('Admin Dashboard', 'Access full admin dashboard', '👑', 76, 'Master', '{}'),
('Bot Configuration', 'Configure bot settings', '🔧', 76, 'Master', '{}'),
('MCP Tools', 'Access Model Context Protocol tools', '🔌', 80, 'Master', '{}'),
('API Access', 'Full API access with custom endpoints', '🔑', 90, 'Master', '{"rate_limit": 1000}');

