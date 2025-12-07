/**
 * Leaderboard page
 */
import { useLeaderboard } from '../hooks/useLeaderboard';
import { LeaderboardTable } from '../components/LeaderboardTable';

export const Leaderboard = () => {
  const { data: leaderboard, isLoading } = useLeaderboard(50);

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-4xl font-bold mb-2">🏆 Leaderboard</h1>
        <p className="text-gray-400">Top users by XP</p>
      </div>

      {isLoading ? (
        <div className="flex items-center justify-center py-12">
          <div className="text-xl text-gray-400">Loading leaderboard...</div>
        </div>
      ) : (
        <LeaderboardTable entries={leaderboard || []} />
      )}
    </div>
  );
};

