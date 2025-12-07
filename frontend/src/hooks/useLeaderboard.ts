/**
 * React Query hooks for leaderboard
 */
import { useQuery } from '@tanstack/react-query';
import { api } from '../lib/api';

export const useLeaderboard = (limit: number = 10) => {
  return useQuery({
    queryKey: ['leaderboard', limit],
    queryFn: () => api.getLeaderboard(limit),
    staleTime: 1000 * 60, // 1 minute
    refetchInterval: 1000 * 60, // Refetch every minute
  });
};

