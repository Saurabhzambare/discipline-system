import { createContext, useContext } from 'react';

export const QUIZ_SCREEN = {
  WELCOME: 'welcome',
  QUESTION: 'question',
  RESULTS: 'results',
  PATH_CARDS: 'path_cards',
  COMMITMENT: 'commitment',
};

export const PathContext = createContext(null);

export function usePath() {
  return useContext(PathContext);
}
