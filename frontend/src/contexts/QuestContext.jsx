import { createContext, useContext } from 'react';

/**
 * Provides daily quest state and completion actions.
 *
 * Value shape:
 *   quests              — array of today's PlayerDailyQuestAssignment objects
 *   setQuests           — setter for optimistic updates
 *   completingQuestId   — id of quest currently being submitted, or null
 *   handleCompleteQuest — async fn(questId, note?) → completes quest, updates player EXP
 */
export const QuestContext = createContext(null);

export function useQuests() {
  return useContext(QuestContext);
}
