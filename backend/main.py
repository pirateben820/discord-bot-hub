"""
Discord Bot Hub - FastAPI Backend
Main application entry point with FastAPI server and Socket.IO integration.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import socketio
import uvicorn

from config import settings

# Create Socket.IO server
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins=settings.cors_origins,
    logger=settings.debug,
    engineio_logger=settings.debug
)

# Create FastAPI app
app = FastAPI(
    title="Discord Bot Hub API",
    description="Backend API for Discord bot with leveling and tool unlock system",
    version="1.0.0",
    debug=settings.debug
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Combine FastAPI with Socket.IO
socket_app = socketio.ASGIApp(
    sio,
    other_asgi_app=app,
    socketio_path='/socket.io'
)


@app.get("/")
async def root():
    """Root endpoint - API health check."""
    return {
        "status": "online",
        "service": "Discord Bot Hub API",
        "version": "1.0.0",
        "environment": settings.environment
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "database": "connected",  # TODO: Add actual DB check
        "socketio": "running"
    }


# Socket.IO event handlers
@sio.event
async def connect(sid, environ):
    """Handle client connection."""
    print(f"Client connected: {sid}")
    await sio.emit('connection_established', {'sid': sid}, room=sid)


@sio.event
async def disconnect(sid):
    """Handle client disconnection."""
    print(f"Client disconnected: {sid}")


@sio.event
async def ping(sid, data):
    """Handle ping from client."""
    await sio.emit('pong', {'timestamp': data.get('timestamp')}, room=sid)


# Import and include routers
from api_routes import users, leveling, tools

app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(leveling.router, prefix="/api/leveling", tags=["leveling"])
app.include_router(tools.router, prefix="/api/tools", tags=["tools"])


if __name__ == "__main__":
    uvicorn.run(
        "main:socket_app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
        log_level="debug" if settings.debug else "info"
    )


