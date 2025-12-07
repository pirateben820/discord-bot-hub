/**
 * Leaderboard table component
 */
import { LeaderboardEntry } from '../lib/api';
import { Link } from 'react-router-dom';

interface LeaderboardTableProps {
  entries: LeaderboardEntry[];
}

export const LeaderboardTable = ({ entries }: LeaderboardTableProps) => {
  const getRankEmoji = (rank: number) => {
    if (rank === 1) return '🥇';
    if (rank === 2) return '🥈';
    if (rank === 3) return '🥉';
    return `#${rank}`;
  };

  const getTierColor = (tier: string) => {
    const colors: Record<string, string> = {
      Basic: 'text-gray-400',
      Member: 'text-green-400',
      Advanced: 'text-blue-400',
      Elite: 'text-purple-400',
      Master: 'text-yellow-400',
    };
    return colors[tier] || 'text-gray-400';
  };

  return (
    <div className="card overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-gray-700">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">
                Rank
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">
                User
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">
                Level
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">
                Tier
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">
                XP
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-700">
            {entries.map((entry) => (
              <tr
                key={entry.user.id}
                className="hover:bg-gray-700/50 transition-colors"
              >
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-2xl">{getRankEmoji(entry.rank)}</div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <Link
                    to={`/profile/${entry.user.discord_id}`}
                    className="flex items-center gap-3 hover:text-primary transition-colors"
                  >
                    {entry.user.avatar_url ? (
                      <img
                        src={entry.user.avatar_url}
                        alt={entry.user.username}
                        className="w-10 h-10 rounded-full"
                      />
                    ) : (
                      <div className="w-10 h-10 rounded-full bg-primary flex items-center justify-center">
                        {entry.user.username[0].toUpperCase()}
                      </div>
                    )}
                    <span className="font-semibold">{entry.user.username}</span>
                  </Link>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-lg font-bold">{entry.level}</div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className={`font-semibold ${getTierColor(entry.user.rank_tier)}`}>
                    {entry.user.rank_tier}
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-primary font-bold">
                    {entry.xp.toLocaleString()}
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

