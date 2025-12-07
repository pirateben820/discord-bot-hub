/**
 * Tools grid component - Display tools in a grid
 */
import { ToolResponse } from '../lib/api';
import { ToolCard } from './ToolCard';

interface ToolsGridProps {
  tools: ToolResponse[];
  discordId: string;
  showUnlockButton?: boolean;
}

export const ToolsGrid = ({ tools, discordId, showUnlockButton = true }: ToolsGridProps) => {
  if (tools.length === 0) {
    return (
      <div className="card text-center py-12">
        <div className="text-6xl mb-4">🔒</div>
        <h3 className="text-xl font-semibold mb-2">No Tools Yet</h3>
        <p className="text-gray-400">
          Keep earning XP to unlock tools!
        </p>
      </div>
    );
  }

  // Group tools by tier
  const toolsByTier = tools.reduce((acc, tool) => {
    const tier = tool.tool.tier;
    if (!acc[tier]) acc[tier] = [];
    acc[tier].push(tool);
    return acc;
  }, {} as Record<string, ToolResponse[]>);

  const tiers = ['Basic', 'Member', 'Advanced', 'Elite', 'Master'];

  return (
    <div className="space-y-8">
      {tiers.map((tier) => {
        const tierTools = toolsByTier[tier];
        if (!tierTools || tierTools.length === 0) return null;

        return (
          <div key={tier}>
            <h3 className="text-2xl font-bold mb-4">{tier} Tier</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {tierTools.map((toolResponse) => (
                <ToolCard
                  key={toolResponse.tool.id}
                  toolResponse={toolResponse}
                  discordId={discordId}
                  showUnlockButton={showUnlockButton}
                />
              ))}
            </div>
          </div>
        );
      })}
    </div>
  );
};

