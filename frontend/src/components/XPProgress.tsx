/**
 * XP Progress component - Show progress to next level
 */
import { User } from '../lib/api';

interface XPProgressProps {
  user: User;
}

export const XPProgress = ({ user }: XPProgressProps) => {
  // Calculate XP for current level
  const calculateXPForLevel = (level: number) => {
    return 100 * (level ** 2) + 50 * level;
  };

  const currentLevelXP = calculateXPForLevel(user.level);
  const nextLevelXP = calculateXPForLevel(user.level + 1);
  const xpInCurrentLevel = user.xp - currentLevelXP;
  const xpNeededForLevel = nextLevelXP - currentLevelXP;
  const progress = (xpInCurrentLevel / xpNeededForLevel) * 100;

  return (
    <div className="card">
      <h3 className="text-xl font-bold mb-4">Level Progress</h3>
      
      <div className="mb-4">
        <div className="flex justify-between text-sm mb-2">
          <span className="text-gray-400">Level {user.level}</span>
          <span className="text-gray-400">Level {user.level + 1}</span>
        </div>
        
        <div className="w-full bg-gray-700 rounded-full h-4 overflow-hidden">
          <div
            className="bg-gradient-to-r from-primary to-secondary h-full transition-all duration-500"
            style={{ width: `${Math.min(progress, 100)}%` }}
          />
        </div>
        
        <div className="flex justify-between text-sm mt-2">
          <span className="text-primary font-semibold">
            {xpInCurrentLevel.toLocaleString()} XP
          </span>
          <span className="text-gray-400">
            {xpNeededForLevel.toLocaleString()} XP needed
          </span>
        </div>
      </div>

      <div className="space-y-2">
        <div className="flex justify-between">
          <span className="text-gray-400">Next Level</span>
          <span className="font-semibold">{user.level + 1}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-gray-400">XP to Next Level</span>
          <span className="font-semibold text-primary">
            {user.next_level_xp.toLocaleString()}
          </span>
        </div>
        <div className="flex justify-between">
          <span className="text-gray-400">Progress</span>
          <span className="font-semibold">{progress.toFixed(1)}%</span>
        </div>
      </div>
    </div>
  );
};

