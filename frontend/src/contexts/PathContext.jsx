import { createContext, useContext } from 'react';

/**
 * Provides the player's chosen RPG path and path-selection actions.
 *
 * Value shape:
 *   selectedPath        — raw path key e.g. "fitness_warrior" or ''
 *   selectedPathDisplay — human label e.g. "Fitness Warrior" or ''
 *   savingPath          — true while PATCH /player/path/ is in-flight
 *   handleSelectPath    — async fn(pathKey) → updates player.path via API
 */
export const PathContext = createContext(null);

export function usePath() {
  return useContext(PathContext);
}
