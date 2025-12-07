/**
 * User card component - Display user info
 */
import { User } from '../lib/api';

interface UserCardProps {
  user: User;
}

export const UserCard = ({ user }: UserCardProps) => {
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

  const getTierBadge = (tier: string) => {
    const badges: Record<string, string> = {
      Basic: '🔰',
      Member: '⭐',
      Advanced: '💎',
      Elite: '👑',
      Master: '🏆',
    };
    return badges[tier] || '🔰';
  };

  return (
    <div className="card">
      <div className="flex items-start gap-6">
        {/* Avatar */}
        <div className="flex-shrink-0">
          {user.avatar_url ? (
            <img
              src={user.avatar_url}
              alt={user.username}
              className="w-24 h-24 rounded-full border-4 border-primary"
            />
          ) : (
            <div className="w-24 h-24 rounded-full bg-primary flex items-center justify-center text-4xl">
              {user.username[0].toUpperCase()}
            </div>
          )}
        </div>

        {/* User Info */}
        <div className="flex-1">
          <h2 className="text-3xl font-bold mb-2">{user.username}</h2>
          
          <div className="flex items-center gap-4 mb-4">
            <div className={`text-xl font-semibold ${getTierColor(user.rank_tier)}`}>
              {getTierBadge(user.rank_tier)} {user.rank_tier} Tier
            </div>
            <div className="text-gray-400">
              Level {user.level}
            </div>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div>
              <div className="text-gray-400 text-sm">Total XP</div>
              <div className="text-2xl font-bold text-primary">{user.xp.toLocaleString()}</div>
            </div>
            <div>
              <div className="text-gray-400 text-sm">Level</div>
              <div className="text-2xl font-bold">{user.level}</div>
            </div>
            <div>
              <div className="text-gray-400 text-sm">Streak</div>
              <div className="text-2xl font-bold text-secondary">{user.streak_days} days</div>
            </div>
            <div>
              <div className="text-gray-400 text-sm">Tools Unlocked</div>
              <div className="text-2xl font-bold text-purple-400">{user.unlocked_tools_count}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

