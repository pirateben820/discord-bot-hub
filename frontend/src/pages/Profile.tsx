/**
 * Profile page - Detailed user profile
 */
import { useParams } from 'react-router-dom';
import { useUser } from '../hooks/useUser';
import { useUserTools } from '../hooks/useTools';
import { UserCard } from '../components/UserCard';
import { ToolsGrid } from '../components/ToolsGrid';
import { XPProgress } from '../components/XPProgress';

export const Profile = () => {
  const { discordId } = useParams<{ discordId: string }>();
  const { data: user, isLoading: userLoading } = useUser(discordId || null);
  const { data: tools, isLoading: toolsLoading } = useUserTools(discordId || null);

  if (userLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-xl">Loading profile...</div>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="card max-w-md">
          <h2 className="text-2xl font-bold mb-4">User Not Found</h2>
          <p className="text-gray-400">
            The user you're looking for doesn't exist.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold mb-8">{user.username}'s Profile</h1>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        <div className="lg:col-span-2">
          <UserCard user={user} />
        </div>
        <div>
          <XPProgress user={user} />
        </div>
      </div>

      <div className="mb-8">
        <h2 className="text-2xl font-bold mb-4">Unlocked Tools</h2>
        {toolsLoading ? (
          <div className="text-gray-400">Loading tools...</div>
        ) : (
          <ToolsGrid 
            tools={tools?.filter(t => t.is_unlocked) || []} 
            discordId={discordId!}
            showUnlockButton={false}
          />
        )}
      </div>
    </div>
  );
};

