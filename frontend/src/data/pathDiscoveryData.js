import { LOCKED_PATH, PATH_MAP } from './pathData';

export const PATH_COLORS = {
  fitness_warrior: '#DC2626',
  mindset_sage: '#8B5CF6',
  health_alchemist: '#10B981',
  discipline_knight: '#3B82F6',
  grind_visionary: '#F59E0B',
};

export const WELCOME_LINES = [
  'Before you begin your journey, Hunter — let us understand who you are right now.',
  'There are no wrong answers. Only honest ones.',
];

export const LOCKED_PATH_TOAST = 'A new path is being forged. Stay disciplined, Hunter — it is coming.';

export function getPathMeta(pathCode) {
  return PATH_MAP[pathCode] || null;
}

export { LOCKED_PATH };
