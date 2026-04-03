import { createContext, useContext } from 'react';

/**
 * Provides daily quest state and completion actions.
 *
 * Value shape:
 *   quests              — array used by legacy dashboard cards
 *   dailyLineup         — normalized lineup payload from /api/quests/daily/
 *   lineupItems         — lineup item array with slot metadata
 *   intention           — full_send / steady / recovery
 *   swapsRemaining      — integer, daily swap budget for current path
 *   featuresUnlocked    — progressive reveal flags
 *   setQuests           — setter for optimistic updates
 *   completingQuestId   — id of quest currently being submitted, or null
 *   handleCompleteQuest — async fn(questId, note?) → completes quest, updates player EXP
 */
export const QuestContext = createContext(null);

export function useQuests() {
  return useContext(QuestContext);
}
