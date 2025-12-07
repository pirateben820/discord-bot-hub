# 🎮 Discord Bot Hub - Leveling & Tool Unlock System

A modern Discord bot with companion website featuring a progressive leveling system where users unlock AI-powered tools as they rank up through Discord activity.

Built with best practices from **pem/archon** architecture patterns.

## ✨ Features

- 🎯 **Progressive Leveling System** - Earn XP from Discord activity (messages, voice, commands)
- 🔓 **Tool Unlock System** - 20 tools across 5 tiers (Basic → Master)
- 🏆 **Leaderboard** - Compete with other users
- 📊 **Real-time Updates** - Socket.IO for instant level-ups and notifications
- 🎨 **Modern UI** - React + TailwindCSS with Discord-themed design
- 🤖 **AI Integration** - PydanticAI agents for advanced features
- 🔌 **MCP Support** - Model Context Protocol for AI IDE integration

## 🏗️ Architecture

```
discord-bot-hub/
├── backend/                # Python FastAPI + Discord bot
│   ├── main.py            # FastAPI server with Socket.IO
│   ├── bot/               # Discord bot with cogs
│   ├── models/            # Pydantic models
│   ├── services/          # Business logic
│   ├── api_routes/        # API endpoints
│   └── database_schema.sql
├── frontend/              # React + TypeScript + Vite
│   ├── src/
│   │   ├── pages/        # Dashboard, Leaderboard, Profile
│   │   ├── components/   # Reusable UI components
│   │   ├── hooks/        # TanStack Query hooks
│   │   └── lib/          # API client, Socket.IO
│   └── tailwind.config.js
└── docs/                  # Documentation
```

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- Node.js 18+
- PostgreSQL (via Supabase)
- Discord Bot Token

### 1. Clone Repository

```bash
git clone https://github.com/pirateben820/discord-bot-hub.git
cd discord-bot-hub
```

### 2. Set Up Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your credentials

# Run API server
python main.py

# In another terminal, run Discord bot
python bot/main.py
```

### 3. Set Up Frontend

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env
# Edit .env with API URL

# Run development server
npm run dev
```

### 4. Set Up Database

1. Create a Supabase project at https://supabase.com
2. Run `backend/database_schema.sql` in SQL Editor
3. Copy project URL and anon key to `.env`

## 📊 Leveling System

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

### Tiers & Tools

| Tier | Levels | Tools | Examples |
|------|--------|-------|----------|
| 🔰 Basic | 1-10 | 4 | Basic Chat, Profile, Leaderboard, Daily Rewards |
| ⭐ Member | 11-25 | 4 | Voice Channels, Custom Emojis, Polls, Music Bot |
| 💎 Advanced | 26-50 | 4 | AI Chat, Code Helper, Image Gen, Analytics |
| 👑 Elite | 51-75 | 4 | Custom Commands, Auto-Mod, Web Scraper, Database |
| 🏆 Master | 76-100 | 4 | Admin Dashboard, Bot Config, MCP Tools, API Access |

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

## 📡 API Endpoints

- `POST /api/users` - Create/update user
- `GET /api/users/{discord_id}` - Get user
- `POST /api/leveling/xp` - Add XP
- `GET /api/leveling/leaderboard` - Get leaderboard
- `GET /api/tools/user/{discord_id}` - Get user tools
- `POST /api/tools/unlock/{discord_id}/{tool_id}` - Unlock tool

Full API docs: `http://localhost:8000/docs`

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **discord.py** - Discord bot library
- **Supabase** - PostgreSQL + pgvector
- **PydanticAI** - AI agent framework
- **Socket.IO** - Real-time communication

### Frontend
- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool
- **TailwindCSS** - Styling
- **TanStack Query** - Data fetching
- **React Router** - Navigation

## 📝 Development

```bash
# Backend
cd backend
black .                    # Format code
ruff check .              # Lint code
pytest                    # Run tests

# Frontend
cd frontend
npm run dev               # Development server
npm run build             # Production build
npm run preview           # Preview build
```

## 🚢 Deployment

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for deployment instructions.

## 📄 License

MIT License - See [LICENSE](LICENSE) for details

## 🤝 Contributing

Contributions welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) first.

## 📧 Support

- GitHub Issues: https://github.com/pirateben820/discord-bot-hub/issues
- Discord Server: [Coming Soon]

---

Built with ❤️ using patterns from [pem/archon](https://github.com/pirateben820/archon)

