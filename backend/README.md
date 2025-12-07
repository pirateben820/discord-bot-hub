# Discord Bot Hub - Backend

Backend services for Discord Bot Hub including FastAPI server, Discord bot, and database integration.

## 🏗️ Architecture

```
backend/
├── main.py                 # FastAPI + Socket.IO server
├── config.py               # Configuration management
├── requirements.txt        # Python dependencies
├── database_schema.sql     # PostgreSQL schema
├── .env.example            # Environment variables template
├── models/                 # Pydantic models
│   ├── user.py
│   ├── tool.py
│   └── xp.py
├── services/               # Business logic
│   ├── database.py
│   └── leveling_service.py
├── api_routes/             # API endpoints
│   ├── users.py
│   ├── leveling.py
│   └── tools.py
└── bot/                    # Discord bot
    ├── main.py
    └── cogs/
        ├── xp.py           # XP tracking
        ├── rank.py         # Rank commands
        ├── admin.py        # Admin commands
        └── sync.py         # API sync
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Set Up Environment

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

Required environment variables:
- `DATABASE_URL` - PostgreSQL connection string
- `SUPABASE_URL` - Your Supabase project URL
- `SUPABASE_KEY` - Supabase anon/service key
- `DISCORD_TOKEN` - Discord bot token
- `API_SECRET_KEY` - Secret key for API authentication

### 3. Set Up Database

Run the schema in your Supabase SQL editor:

```bash
# Copy contents of database_schema.sql to Supabase SQL Editor
# Or use psql:
psql $DATABASE_URL < database_schema.sql
```

### 4. Run the API Server

```bash
python main.py
```

Server will start on `http://localhost:8000`

### 5. Run the Discord Bot

```bash
python bot/main.py
```

## 📡 API Endpoints

### Users
- `POST /api/users` - Create or update user
- `GET /api/users/{discord_id}` - Get user by Discord ID
- `PATCH /api/users/{discord_id}` - Update user
- `GET /api/users` - List all users

### Leveling
- `POST /api/leveling/xp` - Add XP to user
- `GET /api/leveling/leaderboard` - Get leaderboard
- `GET /api/leveling/xp-history/{discord_id}` - Get XP history

### Tools
- `POST /api/tools` - Create tool (admin)
- `GET /api/tools` - List all tools
- `GET /api/tools/user/{discord_id}` - Get user's tools with access status
- `POST /api/tools/unlock/{discord_id}/{tool_id}` - Unlock tool for user

## 🎮 Discord Bot Commands

### User Commands
- `/rank` - Check your rank and level
- `/leaderboard` - View server leaderboard
- `/levels` - View level requirements
- `!xp` - Check your XP

### Admin Commands
- `/addxp <user> <amount>` - Add XP to user
- `/setlevel <user> <level>` - Set user level
- `/resetxp <user>` - Reset user XP
- `/botstats` - View bot statistics

## 🔢 Leveling System

### XP Formula
```
XP Required = 100 * (level^2) + 50 * level
```

### XP Sources
- **Message**: 15 XP (60s cooldown)
- **Voice (per minute)**: 10 XP
- **Command**: 5 XP (30s cooldown)
- **Daily Bonus**: 50 XP
- **Streak Bonus**: 10 XP per day

### Tiers
- **Basic** (Levels 1-10): 4 tools
- **Member** (Levels 11-25): 4 tools
- **Advanced** (Levels 26-50): 4 tools
- **Elite** (Levels 51-75): 4 tools
- **Master** (Levels 76-100): 4 tools

## 🔌 Socket.IO Events

### Client → Server
- `connect` - Client connection
- `ping` - Latency check

### Server → Client
- `connection_established` - Connection confirmed
- `pong` - Ping response
- `level_up` - User leveled up (planned)
- `tool_unlocked` - Tool unlocked (planned)

## 🧪 Testing

```bash
pytest
```

## 📝 Development

### Code Style
```bash
black .
ruff check .
```

### Type Checking
```bash
mypy .
```

## 🐳 Docker (Coming Soon)

```bash
docker-compose up
```

## 📚 Documentation

API documentation available at: `http://localhost:8000/docs`

## 🤝 Contributing

1. Follow the existing code structure
2. Use Pydantic models for validation
3. Add type hints to all functions
4. Write tests for new features
5. Update documentation

## 📄 License

MIT License - See LICENSE file for details

