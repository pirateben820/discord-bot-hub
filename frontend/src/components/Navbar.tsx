/**
 * Navigation bar component
 */
import { Link } from 'react-router-dom';
import { useCurrentUser } from '../hooks/useUser';

export const Navbar = () => {
  const { data: user } = useCurrentUser();

  return (
    <nav className="bg-gray-800 border-b border-gray-700">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-2">
            <div className="text-2xl">🎮</div>
            <span className="text-xl font-bold">Discord Bot Hub</span>
          </Link>

          {/* Navigation Links */}
          <div className="flex items-center gap-6">
            <Link
              to="/"
              className="text-gray-300 hover:text-white transition-colors"
            >
              Dashboard
            </Link>
            <Link
              to="/leaderboard"
              className="text-gray-300 hover:text-white transition-colors"
            >
              Leaderboard
            </Link>

            {/* User Menu */}
            {user && (
              <Link
                to={`/profile/${user.discord_id}`}
                className="flex items-center gap-2 text-gray-300 hover:text-white transition-colors"
              >
                {user.avatar_url ? (
                  <img
                    src={user.avatar_url}
                    alt={user.username}
                    className="w-8 h-8 rounded-full"
                  />
                ) : (
                  <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center text-sm">
                    {user.username[0].toUpperCase()}
                  </div>
                )}
                <span>{user.username}</span>
              </Link>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

