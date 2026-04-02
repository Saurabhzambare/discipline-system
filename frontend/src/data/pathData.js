/**
 * Static display data for all 5 RPG paths + locked 6th placeholder.
 * Source of truth: docs/game-design/systems/path-discovery.md
 *
 * This file is frontend-only — no API calls, no backend dependency.
 * Update only when game design copy changes.
 */

export const PATH_DATA = [
  {
    code: "fitness_warrior",
    name: "Fitness Warrior",
    tagline: "Forge your body. Break your limits.",
    icon: "⚔️",
    color: { primary: "#dc2626", bg: "#7f1d1d", accent: "#ef4444" },
    whoYouAreNow:
      "You train but inconsistency, plateau, or lack of structure is keeping you from the body and performance you know you are capable of.",
    whoYouBecome:
      "In 90 days you will have built a structured training system around your split, developed hybrid strength and endurance, established nutrition habits that fuel performance, and built a streak that proves to yourself you are someone who shows up no matter what.",
    whatYouGain: [
      "A gamified training system built around your actual split",
      "Daily quests that reward what you are already doing",
      "Strength, endurance, and conditioning working together",
      "A public social profile showing your athletic progress",
      "Badges and achievements that make your discipline visible",
    ],
    thisPathIsForYouIf:
      "You already train or want to — but you need a system that keeps you accountable, tracks your progress like a game, and makes consistency feel rewarding instead of exhausting.",
    commitmentMessage:
      "You have chosen the path of the Fitness Warrior.\nThis is not just a choice — it is a declaration.\nEvery quest you complete from this day forward is proof of who you are becoming.\nThe forge begins now Hunter.",
    resultsOpener:
      "You are a warrior who has not yet found your battlefield. Your body is your weapon — and it is time to forge it.",
    keyMechanics: [
      "Split Day Training System",
      "Streak Tracking",
      "Hybrid Athletic Quests",
      "Athletic Achievement Badges",
    ],
  },
  {
    code: "mindset_sage",
    name: "Mindset Sage",
    tagline: "Sharpen your mind. Master your thoughts.",
    icon: "🧘",
    color: { primary: "#7c3aed", bg: "#3b0764", accent: "#a855f7" },
    whoYouAreNow:
      "Your mind is your biggest obstacle. Overthinking, self-doubt, lack of mental clarity, or the inability to stay present is costing you more than you realize.",
    whoYouBecome:
      "In 90 days you will have built a daily meditation and journaling practice, developed emotional resilience through consistent Shadow Training, filled your Wisdom Log with 90 personal insights, and built the mental stillness to think clearly under pressure.",
    whatYouGain: [
      "A daily mental training system across four pillars",
      "Freedom Day tokens earned through consistency",
      "A personal Wisdom Log that becomes your life philosophy",
      "The Dark Night Quest for your hardest days",
      "An identity shift from reactive thinker to deliberate Sage",
    ],
    thisPathIsForYouIf:
      "You want to stop being controlled by your emotions, your phone, and your overthinking — and start moving through life with the calm clarity of someone who has done the inner work.",
    commitmentMessage:
      "You have chosen the path of the Mindset Sage.\nThis is not just a choice — it is a declaration.\nEvery moment of stillness you create is a weapon being sharpened.\nThe inner journey begins now Hunter.",
    resultsOpener:
      "Your greatest battles happen inside your own mind. It is time to become the master of your thoughts.",
    keyMechanics: [
      "Freedom Day Token System",
      "Wisdom Log",
      "Shadow Training Quests",
      "Dark Night Emergency Quest",
    ],
  },
  {
    code: "health_alchemist",
    name: "Health Alchemist",
    tagline: "Transform your body from within.",
    icon: "⚗️",
    color: { primary: "#059669", bg: "#064e3b", accent: "#10b981" },
    whoYouAreNow:
      "You feel drained, stressed, or burnt out. Your body is running on empty. You know your health habits need work but you do not know where to start or what actually matters.",
    whoYouBecome:
      "In 90 days you will have built a morning protocol that optimizes your body from the moment you wake up, established nutrition and hydration habits that fuel your energy, completed multiple Elixirs through consistent daily practice, and developed a Body Journal with 90 days of personal health data showing your transformation.",
    whatYouGain: [
      "A personalized supplement and nutrition guide built for your goals",
      "The Elixir System — a brewing streak with a mercy mechanic",
      "A Body Journal tracking energy, sleep, mood, and digestion daily",
      "Budget-friendly biohacking tools and cold therapy guidance",
      "An Alchemist Setup Guide showing exactly how to start",
    ],
    thisPathIsForYouIf:
      "You want to feel as good on the inside as you want to look on the outside. You are ready to treat your body like a laboratory and experiment with the habits that actually transform your energy, health, and vitality.",
    commitmentMessage:
      "You have chosen the path of the Health Alchemist.\nThis is not just a choice — it is a declaration.\nEvery habit you build is an ingredient in your transformation.\nThe laboratory opens now Hunter.",
    resultsOpener:
      "Your body is trying to tell you something. It is time to listen — and transform from within.",
    keyMechanics: [
      "Elixir Brewing System",
      "Body Journal (daily metrics)",
      "Morning Protocol Quests",
      "Alchemist Setup Guide",
    ],
  },
  {
    code: "discipline_knight",
    name: "Discipline Knight",
    tagline: "Forge your armor. Honor your code.",
    icon: "🛡️",
    color: { primary: "#1d4ed8", bg: "#1e3a8a", accent: "#3b82f6" },
    whoYouAreNow:
      "You know exactly what you need to do. The gap is not knowledge — it is execution. You start strong and fade. You make promises to yourself and break them. The routine never sticks.",
    whoYouBecome:
      "In 90 days you will have built an unbreakable daily routine, forged four pieces of your armor through consistent weekly execution, sworn and honored your personal Discipline Code, and become someone whose word to themselves actually means something.",
    whatYouGain: [
      "The Armor System — visible public proof of your consistency",
      "A personal Discipline Code you write and live by",
      "The War Room daily planning tool built into the app",
      "A Temptation Log that tracks your growing Iron Will",
      "Weekly automated reports showing your discipline data",
    ],
    thisPathIsForYouIf:
      "You are tired of knowing what to do and not doing it. You want a system with real consequences for breaking it and real rewards for honoring it — and you want the world to see your armor growing.",
    commitmentMessage:
      "You have chosen the path of the Discipline Knight.\nThis is not just a choice — it is a declaration.\nEvery day you show up adds armor that the world can see.\nThe forge begins now Hunter.",
    resultsOpener:
      "You know exactly what you need to do. The only thing standing between you and your goals is the system to execute it.",
    keyMechanics: [
      "Armor System (earned weekly)",
      "Discipline Code Oath",
      "War Room Planning Tool",
      "Temptation Log",
    ],
  },
  {
    code: "grind_visionary",
    name: "Grind Visionary",
    tagline: "Build the proof. Ship the work.",
    icon: "🔥",
    color: { primary: "#d97706", bg: "#78350f", accent: "#f59e0b" },
    whoYouAreNow:
      "You have a vision — something you want to build, learn, or become. But the gap between where you are and where you want to be feels overwhelming. You consume more than you create. You think more than you ship.",
    whoYouBecome:
      "In 90 days you will have built a daily skill practice around your chosen field, logged real output in your portfolio, progressed through your Skill Tree, potentially generated your first income from your skill, and built a multiplier streak that compounds every action you take.",
    whatYouGain: [
      "An XP multiplier that rewards compound consistency",
      "A Skill Tree that maps your progression in your chosen field",
      "An Output Log that becomes your proof of work portfolio",
      "The Vision Board showing your singular goal and countdown daily",
      "The First Dollar legendary moment when your skill pays off",
    ],
    thisPathIsForYouIf:
      "You have something you want to build — a skill, a career, a side hustle, a body of work. You need a system that turns daily effort into visible progress and makes showing up feel like leveling up.",
    commitmentMessage:
      "You have chosen the path of the Grind Visionary.\nThis is not just a choice — it is a declaration.\nEvery day you show up compounds into the empire you are building.\nThe grind begins now Hunter.",
    resultsOpener:
      "You have a vision that most people cannot see yet. It is time to build the proof.",
    keyMechanics: [
      "XP Multiplier (compounds with streak)",
      "Skill Tree progression",
      "Output Log portfolio",
      "First Dollar legendary milestone",
    ],
  },
];

// Sixth path — locked placeholder (frontend only, no backend)
export const LOCKED_PATH = {
  code: "locked",
  name: "???",
  tagline: "A new path is coming...",
  icon: "🔒",
  color: { primary: "#6b7280", bg: "#1f2937", accent: "#9ca3af" },
  description:
    "This path has not yet been revealed. Continue your journey and it will reveal itself in time.",
  lockedMessage:
    "A new path is being forged. Stay disciplined Hunter — it is coming.",
  locked: true,
};

// Lookup by path code
export const PATH_MAP = Object.fromEntries(PATH_DATA.map((p) => [p.code, p]));

export function getPathData(code) {
  return PATH_MAP[code] || null;
}
