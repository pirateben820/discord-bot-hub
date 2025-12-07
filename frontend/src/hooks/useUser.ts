/**
 * React Query hooks for user data
 */
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api, User } from '../lib/api';

export const useUser = (discordId: string | null) => {
  return useQuery({
    queryKey: ['user', discordId],
    queryFn: () => api.getUser(discordId!),
    enabled: !!discordId,
    staleTime: 1000 * 60 * 5, // 5 minutes
  });
};

export const useCurrentUser = () => {
  const discordId = localStorage.getItem('discord_id');
  return useUser(discordId);
};

