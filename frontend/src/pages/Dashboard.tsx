/**
 * Dashboard page - Main user dashboard
 */
import { useCurrentUser } from '../hooks/useUser';
import { useUserTools } from '../hooks/useTools';
import { UserCard } from '../components/UserCard';
import { ToolsGrid } from '../components/ToolsGrid';
import { XPProgress } from '../components/XPProgress';

export const Dashboard = () => {
  const { data: user, isLoading: userLoading } = useCurrentUser();
  const discordId = localStorage.getItem('discord_id');
  const { data: tools, isLoading: toolsLoading } = useUserTools(discordId);

  if (userLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-xl">Loading...</div>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="card max-w-md">
          <h2 className="text-2xl font-bold mb-4">Welcome to Discord Bot Hub!</h2>
          <p className="text-gray-400 mb-4">
            Please connect your Discord account to get started.
          </p>
          <button className="btn-primary w-full">
            Connect Discord
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold mb-8">Dashboard</h1>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        <div className="lg:col-span-2">
          <UserCard user={user} />
        </div>
        <div>
          <XPProgress user={user} />
        </div>
      </div>

      <div className="mb-8">
        <h2 className="text-2xl font-bold mb-4">Your Tools</h2>
        {toolsLoading ? (
          <div className="text-gray-400">Loading tools...</div>
        ) : (
          <ToolsGrid tools={tools || []} discordId={discordId!} />
        )}
      </div>
    </div>
  );
};

