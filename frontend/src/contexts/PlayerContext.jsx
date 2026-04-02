import { createContext, useContext } from 'react';

/**
 * Provides player profile state and dashboard loading state.
 *
 * Value shape:
 *   player              — Player object from API (null when not loaded)
 *   setPlayer           — setter for optimistic updates
 *   loadingDashboard    — true while fetching player + quests
 *   dashboardError      — string error message or ''
 *   levelUpInfo         — { newLevel } when player just levelled up, else null
 *   setLevelUpInfo      — setter to trigger or dismiss level-up modal
 *   loadDashboard       — async fn to refresh player + quests
 *   handleAuthExpired   — fn to clear session and redirect to /login
 */
export const PlayerContext = createContext(null);

export function usePlayer() {
  return useContext(PlayerContext);
}
