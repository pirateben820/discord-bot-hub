/**
 * Frontend configuration
 */

export const config = {
  apiUrl: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  socketUrl: import.meta.env.VITE_SOCKET_URL || 'http://localhost:8000',
  discordClientId: import.meta.env.VITE_DISCORD_CLIENT_ID || '',
  discordRedirectUri: import.meta.env.VITE_DISCORD_REDIRECT_URI || 'http://localhost:5173/auth/callback',
} as const;

export const API_ENDPOINTS = {
  users: '/api/users',
  leveling: '/api/leveling',
  tools: '/api/tools',
  leaderboard: '/api/leveling/leaderboard',
} as const;

