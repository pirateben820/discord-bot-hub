/**
 * Tool card component - Display individual tool
 */
import { ToolResponse } from '../lib/api';
import { useUnlockTool } from '../hooks/useTools';

interface ToolCardProps {
  toolResponse: ToolResponse;
  discordId: string;
  showUnlockButton?: boolean;
}

export const ToolCard = ({ toolResponse, discordId, showUnlockButton = true }: ToolCardProps) => {
  const { tool, is_unlocked, can_unlock, usage_count } = toolResponse;
  const unlockMutation = useUnlockTool();

  const handleUnlock = () => {
    if (can_unlock) {
      unlockMutation.mutate({ discordId, toolId: tool.id });
    }
  };

  return (
    <div
      className={`card ${
        is_unlocked
          ? 'border-green-500'
          : can_unlock
          ? 'border-primary'
          : 'border-gray-700 opacity-60'
      }`}
    >
      <div className="flex items-start justify-between mb-3">
        <div className="text-4xl">{tool.icon}</div>
        {is_unlocked && (
          <div className="bg-green-500 text-white text-xs px-2 py-1 rounded-full">
            Unlocked
          </div>
        )}
        {!is_unlocked && can_unlock && (
          <div className="bg-primary text-white text-xs px-2 py-1 rounded-full">
            Available
          </div>
        )}
        {!is_unlocked && !can_unlock && (
          <div className="bg-gray-600 text-white text-xs px-2 py-1 rounded-full">
            Locked
          </div>
        )}
      </div>

      <h4 className="text-lg font-bold mb-2">{tool.name}</h4>
      <p className="text-gray-400 text-sm mb-4">{tool.description}</p>

      <div className="flex items-center justify-between text-sm">
        <div className="text-gray-400">
          Level {tool.required_level} required
        </div>
        {is_unlocked && (
          <div className="text-secondary">
            Used {usage_count} times
          </div>
        )}
      </div>

      {showUnlockButton && can_unlock && !is_unlocked && (
        <button
          onClick={handleUnlock}
          disabled={unlockMutation.isPending}
          className="btn-primary w-full mt-4"
        >
          {unlockMutation.isPending ? 'Unlocking...' : 'Unlock Tool'}
        </button>
      )}
    </div>
  );
};

