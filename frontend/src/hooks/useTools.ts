/**
 * React Query hooks for tools
 */
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '../lib/api';

export const useUserTools = (discordId: string | null) => {
  return useQuery({
    queryKey: ['tools', discordId],
    queryFn: () => api.getUserTools(discordId!),
    enabled: !!discordId,
    staleTime: 1000 * 60 * 5, // 5 minutes
  });
};

export const useUnlockTool = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ discordId, toolId }: { discordId: string; toolId: string }) =>
      api.unlockTool(discordId, toolId),
    onSuccess: (_, variables) => {
      // Invalidate tools query to refetch
      queryClient.invalidateQueries({ queryKey: ['tools', variables.discordId] });
      queryClient.invalidateQueries({ queryKey: ['user', variables.discordId] });
    },
  });
};

