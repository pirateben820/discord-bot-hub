/**
 * API client using axios
 */
import axios from 'axios';
import { config } from '../config';

export const apiClient = axios.create({
  baseURL: config.apiUrl,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for auth tokens
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized
      localStorage.removeItem('auth_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// API types
export interface User {
  id: string;
  discord_id: string;
  username: string;
  avatar_url?: string;
  xp: number;
  level: number;
  rank_tier: string;
  streak_days: number;
  unlocked_tools_count: number;
  next_level_xp: number;
}

export interface Tool {
  id: string;
  name: string;
  description: string;
  icon: string;
  required_level: number;
  tier: string;
  enabled: boolean;
  config: Record<string, any>;
}

export interface ToolResponse {
  tool: Tool;
  is_unlocked: boolean;
  unlocked_at?: string;
  usage_count: number;
  can_unlock: boolean;
}

export interface LeaderboardEntry {
  rank: number;
  user: User;
  xp: number;
  level: number;
}

// API functions
export const api = {
  // Users
  getUser: async (discordId: string): Promise<User> => {
    const { data } = await apiClient.get(`/api/users/${discordId}`);
    return data;
  },

  // Leveling
  getLeaderboard: async (limit: number = 10): Promise<LeaderboardEntry[]> => {
    const { data } = await apiClient.get('/api/leveling/leaderboard', {
      params: { limit },
    });
    return data;
  },

  // Tools
  getUserTools: async (discordId: string): Promise<ToolResponse[]> => {
    const { data } = await apiClient.get(`/api/tools/user/${discordId}`);
    return data;
  },

  unlockTool: async (discordId: string, toolId: string): Promise<{ message: string }> => {
    const { data } = await apiClient.post(`/api/tools/unlock/${discordId}/${toolId}`);
    return data;
  },
};

