"""Management command to seed Phase 5B quest data."""

from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from paths.models import QuestChain
from quests.models import Quest
from social.models import WeeklyBossQuest


# ── Universal daily quests (all players) ──────────────────────────────────────
UNIVERSAL_QUESTS = [
    {
        "title": "Hydration Protocol — 8 Glasses",
        "description": "Drink at least 8 glasses of water across the day.",
        "exp_reward": 15,
        "rank": "D",
        "pillar": "body",
        "pack_id": "universal_daily_core",
        "cooldown_days": 0,
        "universal_daily": True,
        "is_rest_day_quest": False,
        "is_weekly_boss": False,
        "is_one_time_only": False,
        "equipment_required": "",
        "path_target": "",
    },
    {
        "title": "Sunlight Walk — 10 Minutes",
        "description": "Take a 10-minute outdoor walk for recovery and reset.",
        "exp_reward": 15,
        "rank": "D",
        "pillar": "body",
        "pack_id": "universal_daily_core",
        "cooldown_days": 0,
        "universal_daily": True,
        "is_rest_day_quest": False,
        "is_weekly_boss": False,
        "is_one_time_only": False,
        "equipment_required": "",
        "path_target": "",
    },
    {
        "title": "Gratitude Log — 3 Lines",
        "description": "Write three things you are grateful for today.",
        "exp_reward": 15,
        "rank": "D",
        "pillar": "mind",
        "pack_id": "universal_daily_core",
        "cooldown_days": 0,
        "universal_daily": True,
        "is_rest_day_quest": False,
        "is_weekly_boss": False,
        "is_one_time_only": False,
        "equipment_required": "",
        "path_target": "",
    },
    {
        "title": "Mobility Reset — 5 Minutes",
        "description": "Do 5 minutes of light mobility for joints and posture.",
        "exp_reward": 15,
        "rank": "D",
        "pillar": "body",
        "pack_id": "universal_daily_core",
        "cooldown_days": 0,
        "universal_daily": True,
        "is_rest_day_quest": False,
        "is_weekly_boss": False,
        "is_one_time_only": False,
        "equipment_required": "",
        "path_target": "",
    },
    {
        "title": "Digital Sunset — 30 Minutes",
        "description": "No social media or scrolling for 30 minutes before sleep.",
        "exp_reward": 20,
        "rank": "C",
        "pillar": "mind",
        "pack_id": "universal_daily_core",
        "cooldown_days": 0,
        "universal_daily": True,
        "is_rest_day_quest": False,
        "is_weekly_boss": False,
        "is_one_time_only": False,
        "equipment_required": "",
        "path_target": "",
    },
    {
        "title": "Evening Reset — Plan Tomorrow",
        "description": "Write your top 3 priorities for tomorrow before bed.",
        "exp_reward": 20,
        "rank": "C",
        "pillar": "output",
        "pack_id": "universal_daily_core",
        "cooldown_days": 0,
        "universal_daily": True,
        "is_rest_day_quest": False,
        "is_weekly_boss": False,
        "is_one_time_only": False,
        "equipment_required": "",
        "path_target": "",
    },
]


# ── Fitness Warrior quests ────────────────────────────────────────────────────
FITNESS_WARRIOR_QUESTS = [
    {"title": "Push Session — Compound Focus", "description": "Complete your push workout: chest, shoulders, triceps.", "exp_reward": 22, "rank": "D", "pillar": "body", "pack_id": "fw_push_pull_legs", "cooldown_days": 1, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "", "path_target": "fitness_warrior"},
    {"title": "Pull Session — Back Builder", "description": "Complete your pull workout: back, rear delts, biceps.", "exp_reward": 22, "rank": "D", "pillar": "body", "pack_id": "fw_push_pull_legs", "cooldown_days": 1, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "", "path_target": "fitness_warrior"},
    {"title": "Leg Day — Lower Body Forge", "description": "Complete your lower-body session with intent and control.", "exp_reward": 24, "rank": "D", "pillar": "body", "pack_id": "fw_push_pull_legs", "cooldown_days": 1, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "", "path_target": "fitness_warrior"},
    {"title": "Zone 2 Cardio — 20 Minutes", "description": "Steady-state cardio to build engine and recovery capacity.", "exp_reward": 20, "rank": "D", "pillar": "body", "pack_id": "fw_conditioning", "cooldown_days": 0, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "", "path_target": "fitness_warrior"},
    {"title": "Dynamic Warm-Up Protocol", "description": "Perform a full warm-up before training.", "exp_reward": 15, "rank": "D", "pillar": "body", "pack_id": "fw_fundamentals", "cooldown_days": 0, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "", "path_target": "fitness_warrior"},
    {"title": "Post-Workout Protein Hit", "description": "Hit your post-workout protein target within 2 hours.", "exp_reward": 20, "rank": "C", "pillar": "body", "pack_id": "fw_nutrition", "cooldown_days": 0, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "", "path_target": "fitness_warrior"},
    {"title": "Mobility Flow — Hips and T-Spine", "description": "Complete 12 minutes of mobility for hips and thoracic spine.", "exp_reward": 22, "rank": "C", "pillar": "body", "pack_id": "fw_recovery", "cooldown_days": 0, "universal_daily": False, "is_rest_day_quest": True, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "foam_roller", "path_target": "fitness_warrior"},
    {"title": "Rest Day Recovery Walk — 8k Steps", "description": "On rest day, recover with low-intensity movement.", "exp_reward": 22, "rank": "C", "pillar": "body", "pack_id": "fw_recovery", "cooldown_days": 0, "universal_daily": False, "is_rest_day_quest": True, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "", "path_target": "fitness_warrior"},
    {"title": "Breathwork Cooldown — 5 Minutes", "description": "Downshift nervous system after training with breathwork.", "exp_reward": 20, "rank": "C", "pillar": "mind", "pack_id": "fw_recovery", "cooldown_days": 0, "universal_daily": False, "is_rest_day_quest": True, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "", "path_target": "fitness_warrior"},
    {"title": "Split Log Update", "description": "Log your split day, top sets, and recovery status.", "exp_reward": 24, "rank": "C", "pillar": "output", "pack_id": "fw_tracking", "cooldown_days": 0, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "", "path_target": "fitness_warrior"},
    {"title": "HIIT Finisher — 12 Minutes", "description": "Complete a hard conditioning finisher after lifting.", "exp_reward": 36, "rank": "B", "pillar": "body", "pack_id": "fw_conditioning", "cooldown_days": 1, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "", "path_target": "fitness_warrior"},
    {"title": "Progressive Overload Win", "description": "Beat a previous lift by reps or load with good form.", "exp_reward": 38, "rank": "B", "pillar": "body", "pack_id": "fw_strength", "cooldown_days": 1, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "barbell", "path_target": "fitness_warrior"},
    {"title": "Athletic Skill Block — 20 Minutes", "description": "Practice sprint mechanics, jumps, or agility ladders.", "exp_reward": 36, "rank": "B", "pillar": "body", "pack_id": "fw_athleticism", "cooldown_days": 1, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "", "path_target": "fitness_warrior"},
    {"title": "Meal Prep for 2 Days", "description": "Prepare high-protein meals to protect consistency.", "exp_reward": 35, "rank": "B", "pillar": "soul", "pack_id": "fw_nutrition", "cooldown_days": 2, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "", "path_target": "fitness_warrior"},
    {"title": "Cold Shower Protocol", "description": "Complete a 2+ minute cold shower for discipline and recovery.", "exp_reward": 40, "rank": "B", "pillar": "mind", "pack_id": "cross_cold_shower", "cooldown_days": 1, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "", "path_target": "fitness_warrior"},
    {"title": "Hybrid Day — Lift + Cardio", "description": "Combine strength and conditioning in one structured session.", "exp_reward": 55, "rank": "A", "pillar": "body", "pack_id": "fw_hybrid", "cooldown_days": 1, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "", "path_target": "fitness_warrior"},
    {"title": "Recovery Mastery Day", "description": "Execute full recovery stack: walk, mobility, sleep target.", "exp_reward": 52, "rank": "A", "pillar": "soul", "pack_id": "fw_recovery", "cooldown_days": 2, "universal_daily": False, "is_rest_day_quest": True, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "massage_ball", "path_target": "fitness_warrior"},
    {"title": "Athlete Standard Check-in", "description": "Track bodyweight, waist, and training readiness score.", "exp_reward": 50, "rank": "A", "pillar": "output", "pack_id": "fw_tracking", "cooldown_days": 1, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "", "path_target": "fitness_warrior"},
    {"title": "Warrior Weekly Gauntlet", "description": "Complete 4 training sessions + 2 cardio sessions this week.", "exp_reward": 82, "rank": "S", "pillar": "body", "pack_id": "fw_weekly_boss", "cooldown_days": 6, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": True, "is_one_time_only": False, "equipment_required": "", "path_target": "fitness_warrior"},
    {"title": "Peak Performance Trial", "description": "Set a weekly PR in strength, pace, or endurance marker.", "exp_reward": 95, "rank": "S", "pillar": "output", "pack_id": "fw_weekly_boss", "cooldown_days": 6, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": True, "is_one_time_only": False, "equipment_required": "", "path_target": "fitness_warrior"},
]


# ── Mindset Sage quests ────────────────────────────────────────────────────────
MINDSET_SAGE_QUESTS = [
    {"title": "Stillness Sit — 5 Minutes", "description": "Sit in silence and observe your breath for 5 minutes.", "exp_reward": 15, "rank": "D", "pillar": "mind", "pack_id": "ms_meditation", "cooldown_days": 0, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "", "path_target": "mindset_sage"},
    {"title": "Wisdom Log — One Honest Paragraph", "description": "Write one paragraph on what you learned about yourself today.", "exp_reward": 18, "rank": "D", "pillar": "mind", "pack_id": "ms_wisdom_log", "cooldown_days": 0, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "journal", "path_target": "mindset_sage"},
    {"title": "Mental Cleanse — 15 Minutes No Input", "description": "No phone, no media, no music. Just awareness.", "exp_reward": 18, "rank": "D", "pillar": "mind", "pack_id": "ms_clarity", "cooldown_days": 0, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "", "path_target": "mindset_sage"},
    {"title": "Reframe One Negative Thought", "description": "Catch one limiting thought and rewrite it constructively.", "exp_reward": 16, "rank": "D", "pillar": "mind", "pack_id": "ms_reframes", "cooldown_days": 0, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "", "path_target": "mindset_sage"},
    {"title": "Evening Reflection — Win + Lesson", "description": "Document one win and one lesson from today.", "exp_reward": 20, "rank": "C", "pillar": "soul", "pack_id": "ms_reflection", "cooldown_days": 0, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "", "path_target": "mindset_sage"},
    {"title": "Breath Ladder — 4-4-6 x 10", "description": "Run 10 rounds of calm breathing to reduce stress load.", "exp_reward": 20, "rank": "C", "pillar": "mind", "pack_id": "ms_breathwork", "cooldown_days": 0, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "", "path_target": "mindset_sage"},
    {"title": "Freedom Day Token Earn Step", "description": "Complete all assigned Sage quests to progress toward token.", "exp_reward": 22, "rank": "C", "pillar": "output", "pack_id": "ms_freedom_tokens", "cooldown_days": 0, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "", "path_target": "mindset_sage"},
    {"title": "Reading Session — 20 Minutes", "description": "Read a growth-focused book with full concentration.", "exp_reward": 24, "rank": "C", "pillar": "mind", "pack_id": "cross_reading", "cooldown_days": 0, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "book", "path_target": "mindset_sage"},
    {"title": "Shadow Prompt — Face the Avoided", "description": "Answer one hard prompt about what you are avoiding.", "exp_reward": 35, "rank": "B", "pillar": "soul", "pack_id": "ms_shadow_work", "cooldown_days": 1, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "journal", "path_target": "mindset_sage"},
    {"title": "Distraction Fast — 2 Hours", "description": "Block all non-essential notifications and stay present.", "exp_reward": 36, "rank": "B", "pillar": "mind", "pack_id": "ms_focus", "cooldown_days": 0, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "", "path_target": "mindset_sage"},
    {"title": "Wisdom Log — Mentor Letter", "description": "Write advice to your future self as if you are a mentor.", "exp_reward": 38, "rank": "B", "pillar": "soul", "pack_id": "ms_wisdom_log", "cooldown_days": 1, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "journal", "path_target": "mindset_sage"},
    {"title": "Emotional Audit", "description": "Track triggers, response, and preferred response pattern.", "exp_reward": 35, "rank": "B", "pillar": "output", "pack_id": "ms_emotional_mastery", "cooldown_days": 1, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "", "path_target": "mindset_sage"},
    {"title": "Dark Night Quest — Hold the Line", "description": "When mood is low, complete one stabilizing action and log it.", "exp_reward": 50, "rank": "A", "pillar": "soul", "pack_id": "ms_dark_night", "cooldown_days": 0, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "", "path_target": "mindset_sage"},
    {"title": "Mind Fortress Session — 30 Minutes", "description": "Meditation + reflection + intention stack in one session.", "exp_reward": 55, "rank": "A", "pillar": "mind", "pack_id": "ms_fortress", "cooldown_days": 1, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "", "path_target": "mindset_sage"},
    {"title": "Breathwork Protocol — 12 Minutes", "description": "Complete an extended breathing protocol for nervous-system recovery.", "exp_reward": 52, "rank": "A", "pillar": "mind", "pack_id": "cross_breathwork", "cooldown_days": 1, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "", "path_target": "mindset_sage"},
    {"title": "5AM Wake-Up Oath", "description": "Wake at 5AM and complete your first 30-minute ritual.", "exp_reward": 58, "rank": "A", "pillar": "output", "pack_id": "cross_5am", "cooldown_days": 1, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "", "path_target": "mindset_sage"},
    {"title": "Sage Weekly Silence Trial", "description": "Complete 60 minutes cumulative meditation across the week.", "exp_reward": 85, "rank": "S", "pillar": "mind", "pack_id": "ms_weekly_boss", "cooldown_days": 6, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": True, "is_one_time_only": False, "equipment_required": "", "path_target": "mindset_sage"},
    {"title": "Dark Night Conqueror", "description": "Complete the Dark Night quest on 3 separate days in one week.", "exp_reward": 95, "rank": "S", "pillar": "soul", "pack_id": "ms_weekly_boss", "cooldown_days": 6, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": True, "is_one_time_only": False, "equipment_required": "", "path_target": "mindset_sage"},
    {"title": "Boundary Lock — No Doomscroll Morning", "description": "No social feed for first 90 minutes after waking.", "exp_reward": 22, "rank": "C", "pillar": "mind", "pack_id": "ms_focus", "cooldown_days": 0, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "", "path_target": "mindset_sage"},
    {"title": "Values Alignment Check", "description": "Choose one value and act on it intentionally today.", "exp_reward": 24, "rank": "C", "pillar": "soul", "pack_id": "ms_values", "cooldown_days": 0, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "", "path_target": "mindset_sage"},
]


# ── Health Alchemist quests ────────────────────────────────────────────────────
HEALTH_ALCHEMIST_QUESTS = [
    {"title": "Morning Hydration Stack", "description": "Drink water on waking and add electrolytes.", "exp_reward": 18, "rank": "D", "pillar": "body", "pack_id": "ha_morning_protocol", "cooldown_days": 0, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "electrolytes", "path_target": "health_alchemist"},
    {"title": "Sleep Log Entry", "description": "Log sleep duration and quality in your body journal.", "exp_reward": 18, "rank": "D", "pillar": "output", "pack_id": "ha_body_journal", "cooldown_days": 0, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "", "path_target": "health_alchemist"},
    {"title": "Digestive Calm Meal", "description": "Eat one low-irritant whole-food meal and track response.", "exp_reward": 20, "rank": "D", "pillar": "body", "pack_id": "ha_gut_reset", "cooldown_days": 0, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "", "path_target": "health_alchemist"},
    {"title": "Body Journal — Energy/Mood/Digestion", "description": "Record your daily energy, mood, and digestion ratings.", "exp_reward": 20, "rank": "D", "pillar": "output", "pack_id": "ha_body_journal", "cooldown_days": 0, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "journal", "path_target": "health_alchemist"},
    {"title": "Gut Reset Day 1", "description": "Remove one known trigger food and document symptoms.", "exp_reward": 24, "rank": "C", "pillar": "body", "pack_id": "ha_gut_reset_chain", "cooldown_days": 0, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": True, "equipment_required": "", "path_target": "health_alchemist"},
    {"title": "Gut Reset Day 2", "description": "Repeat clean meals and hydration protocol from day 1.", "exp_reward": 24, "rank": "C", "pillar": "body", "pack_id": "ha_gut_reset_chain", "cooldown_days": 0, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": True, "equipment_required": "", "path_target": "health_alchemist"},
    {"title": "Gut Reset Day 3", "description": "Reintroduce one food and log body response by evening.", "exp_reward": 30, "rank": "C", "pillar": "output", "pack_id": "ha_gut_reset_chain", "cooldown_days": 0, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": True, "equipment_required": "", "path_target": "health_alchemist"},
    {"title": "Supplement Stack — Core Three", "description": "Take your core stack and log tolerance. Consult your doctor before starting any supplement regimen.", "exp_reward": 24, "rank": "C", "pillar": "body", "pack_id": "ha_supplement_stack", "cooldown_days": 0, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "supplement_stack", "path_target": "health_alchemist"},
    {"title": "Breathwork Protocol — 12 Minutes", "description": "Complete an extended breathing protocol for nervous-system recovery.", "exp_reward": 24, "rank": "C", "pillar": "mind", "pack_id": "cross_breathwork", "cooldown_days": 1, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "", "path_target": "health_alchemist"},
    {"title": "Cold Shower Protocol", "description": "Complete a 2+ minute cold shower for resilience and inflammation control.", "exp_reward": 36, "rank": "B", "pillar": "mind", "pack_id": "cross_cold_shower", "cooldown_days": 1, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "", "path_target": "health_alchemist"},
    {"title": "Circadian Light Timing", "description": "Get early sunlight and avoid bright light late evening.", "exp_reward": 35, "rank": "B", "pillar": "body", "pack_id": "ha_circadian", "cooldown_days": 0, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "", "path_target": "health_alchemist"},
    {"title": "Elixir Brew — Day Fill", "description": "Complete your daily non-negotiables to fill one elixir segment.", "exp_reward": 38, "rank": "B", "pillar": "soul", "pack_id": "ha_elixir_system", "cooldown_days": 0, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "", "path_target": "health_alchemist"},
    {"title": "Protein + Fiber Target", "description": "Hit protein and fiber targets in a single day.", "exp_reward": 36, "rank": "B", "pillar": "body", "pack_id": "ha_nutrition", "cooldown_days": 0, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "", "path_target": "health_alchemist"},
    {"title": "Recovery Walk After Dinner", "description": "Walk 15 minutes after your final meal.", "exp_reward": 35, "rank": "B", "pillar": "body", "pack_id": "ha_recovery", "cooldown_days": 0, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "", "path_target": "health_alchemist"},
    {"title": "Blood Sugar Stability Day", "description": "Balanced meals all day with no sugar crash.", "exp_reward": 54, "rank": "A", "pillar": "body", "pack_id": "ha_metabolic", "cooldown_days": 1, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "glucometer", "path_target": "health_alchemist"},
    {"title": "Lab Notes Deep Entry", "description": "Write a detailed body journal entry with patterns and hypotheses.", "exp_reward": 52, "rank": "A", "pillar": "output", "pack_id": "ha_body_journal", "cooldown_days": 1, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "journal", "path_target": "health_alchemist"},
    {"title": "Elixir Transmutation", "description": "Reach 7/7 elixir progress and complete transmutation ritual.", "exp_reward": 60, "rank": "A", "pillar": "soul", "pack_id": "ha_elixir_system", "cooldown_days": 6, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "", "path_target": "health_alchemist"},
    {"title": "Alchemist Weekly Protocol", "description": "Complete 6 health protocol quests in one week.", "exp_reward": 86, "rank": "S", "pillar": "body", "pack_id": "ha_weekly_boss", "cooldown_days": 6, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": True, "is_one_time_only": False, "equipment_required": "", "path_target": "health_alchemist"},
    {"title": "Metabolic Mastery Trial", "description": "Maintain stable energy for 5 straight days.", "exp_reward": 96, "rank": "S", "pillar": "output", "pack_id": "ha_weekly_boss", "cooldown_days": 6, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": True, "is_one_time_only": False, "equipment_required": "", "path_target": "health_alchemist"},
    {"title": "Supplement Adherence Audit", "description": "Check quality, timing, and consistency of supplement use. Consult your doctor before starting any supplement regimen.", "exp_reward": 22, "rank": "C", "pillar": "output", "pack_id": "ha_supplement_stack", "cooldown_days": 0, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "supplement_stack", "path_target": "health_alchemist"},
]


# ── Discipline Knight quests ───────────────────────────────────────────────────
DISCIPLINE_KNIGHT_QUESTS = [
    {"title": "First Hour Protocol", "description": "No phone in the first hour after waking.", "exp_reward": 20, "rank": "D", "pillar": "mind", "pack_id": "dk_morning_code", "cooldown_days": 0, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "", "path_target": "discipline_knight"},
    {"title": "Discipline Code Review", "description": "Read your personal oath before the day begins.", "exp_reward": 18, "rank": "D", "pillar": "soul", "pack_id": "dk_discipline_code", "cooldown_days": 0, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "", "path_target": "discipline_knight"},
    {"title": "War Room — Morning Plan", "description": "Write top 3 priorities in the war room.", "exp_reward": 20, "rank": "D", "pillar": "output", "pack_id": "dk_war_room", "cooldown_days": 0, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "", "path_target": "discipline_knight"},
    {"title": "Temptation Log Entry", "description": "Log one temptation and how you responded.", "exp_reward": 20, "rank": "D", "pillar": "mind", "pack_id": "dk_temptation_log", "cooldown_days": 0, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "journal", "path_target": "discipline_knight"},
    {"title": "Evening Debrief — Win/Loss/Fix", "description": "Complete your evening review with clear adjustments.", "exp_reward": 22, "rank": "C", "pillar": "output", "pack_id": "dk_war_room", "cooldown_days": 0, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "", "path_target": "discipline_knight"},
    {"title": "Wake at 5AM", "description": "Wake up at 5AM and start your routine immediately.", "exp_reward": 24, "rank": "C", "pillar": "output", "pack_id": "cross_5am", "cooldown_days": 1, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "", "path_target": "discipline_knight"},
    {"title": "No-Snooze Victory", "description": "Get up on first alarm with no negotiation.", "exp_reward": 22, "rank": "C", "pillar": "mind", "pack_id": "dk_morning_code", "cooldown_days": 0, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "", "path_target": "discipline_knight"},
    {"title": "Armor Piece Progress Day", "description": "Complete all Knight core quests to forge armor progress.", "exp_reward": 24, "rank": "C", "pillar": "soul", "pack_id": "dk_armor_system", "cooldown_days": 0, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "", "path_target": "discipline_knight"},
    {"title": "Distraction Lock — 90 Minutes", "description": "Single-task your highest priority with zero context switching.", "exp_reward": 36, "rank": "B", "pillar": "output", "pack_id": "dk_focus", "cooldown_days": 1, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "", "path_target": "discipline_knight"},
    {"title": "Hard Choice First", "description": "Do the hardest meaningful task before noon.", "exp_reward": 36, "rank": "B", "pillar": "mind", "pack_id": "dk_execution", "cooldown_days": 0, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "", "path_target": "discipline_knight"},
    {"title": "Deep Work Block — 90 Minutes", "description": "Complete an uninterrupted deep work block.", "exp_reward": 40, "rank": "B", "pillar": "output", "pack_id": "cross_deep_work", "cooldown_days": 1, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "", "path_target": "discipline_knight"},
    {"title": "Routine Integrity Day", "description": "Execute morning, midday, and evening anchors with no misses.", "exp_reward": 38, "rank": "B", "pillar": "soul", "pack_id": "dk_routine", "cooldown_days": 1, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "", "path_target": "discipline_knight"},
    {"title": "Honor Review Prep", "description": "Prepare your weekly honor review notes.", "exp_reward": 35, "rank": "B", "pillar": "output", "pack_id": "dk_honor_review", "cooldown_days": 2, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "journal", "path_target": "discipline_knight"},
    {"title": "Temptation Resistance Streak", "description": "Resist 3 temptations in one day and log all of them.", "exp_reward": 50, "rank": "A", "pillar": "mind", "pack_id": "dk_temptation_log", "cooldown_days": 1, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "journal", "path_target": "discipline_knight"},
    {"title": "War Room Commander Day", "description": "Morning planning + evening review completed with full honesty.", "exp_reward": 54, "rank": "A", "pillar": "output", "pack_id": "dk_war_room", "cooldown_days": 1, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "", "path_target": "discipline_knight"},
    {"title": "Code of Honor in Action", "description": "Choose one code line and prove it with behavior all day.", "exp_reward": 55, "rank": "A", "pillar": "soul", "pack_id": "dk_discipline_code", "cooldown_days": 1, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "", "path_target": "discipline_knight"},
    {"title": "Knight Weekly Citadel", "description": "Execute 7 consecutive days of your core discipline stack.", "exp_reward": 88, "rank": "S", "pillar": "soul", "pack_id": "dk_weekly_boss", "cooldown_days": 6, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": True, "is_one_time_only": False, "equipment_required": "", "path_target": "discipline_knight"},
    {"title": "Honor Review", "description": "Complete your full weekly honor review and set next-week standards.", "exp_reward": 92, "rank": "S", "pillar": "output", "pack_id": "dk_weekly_boss", "cooldown_days": 6, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": True, "is_one_time_only": False, "equipment_required": "journal", "path_target": "discipline_knight"},
    {"title": "Inbox Zero Discipline", "description": "Clear or categorize all pending messages/tasks by end of day.", "exp_reward": 24, "rank": "C", "pillar": "output", "pack_id": "dk_execution", "cooldown_days": 1, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "", "path_target": "discipline_knight"},
    {"title": "Discipline Walk — No Audio", "description": "Walk in silence for 20 minutes to sharpen inner command.", "exp_reward": 22, "rank": "C", "pillar": "mind", "pack_id": "dk_clarity", "cooldown_days": 0, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "", "path_target": "discipline_knight"},
]


# ── Grind Visionary quests ─────────────────────────────────────────────────────
GRIND_VISIONARY_QUESTS = [
    {"title": "Deep Work Sprint — 45 Minutes", "description": "Focused sprint on your singular goal.", "exp_reward": 20, "rank": "D", "pillar": "output", "pack_id": "gv_deep_work", "cooldown_days": 0, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "", "path_target": "grind_visionary"},
    {"title": "Skill Practice — 30 Minutes", "description": "Practice your core skill with deliberate reps.", "exp_reward": 20, "rank": "D", "pillar": "output", "pack_id": "gv_skill_building", "cooldown_days": 0, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "", "path_target": "grind_visionary"},
    {"title": "Singular Goal Check-In", "description": "Update today’s progress on your one major goal.", "exp_reward": 18, "rank": "D", "pillar": "mind", "pack_id": "gv_singular_goal", "cooldown_days": 0, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "", "path_target": "grind_visionary"},
    {"title": "Output Log Entry", "description": "Log what you shipped or learned today.", "exp_reward": 18, "rank": "D", "pillar": "output", "pack_id": "gv_output_log", "cooldown_days": 0, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "journal", "path_target": "grind_visionary"},
    {"title": "Study Block — 45 Minutes", "description": "Focused study on a direct bottleneck skill.", "exp_reward": 24, "rank": "C", "pillar": "mind", "pack_id": "gv_study", "cooldown_days": 0, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "", "path_target": "grind_visionary"},
    {"title": "Reading Session — 20 Minutes", "description": "Read a growth-focused book with full concentration.", "exp_reward": 24, "rank": "C", "pillar": "mind", "pack_id": "cross_reading", "cooldown_days": 0, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "book", "path_target": "grind_visionary"},
    {"title": "Accountability Ping", "description": "Send your daily proof-of-work update to accountability partner.", "exp_reward": 24, "rank": "C", "pillar": "soul", "pack_id": "gv_accountability", "cooldown_days": 0, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "", "path_target": "grind_visionary"},
    {"title": "System Cleanup — Remove 1 Bottleneck", "description": "Identify and remove one friction point in your workflow.", "exp_reward": 22, "rank": "C", "pillar": "output", "pack_id": "gv_systems", "cooldown_days": 1, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "", "path_target": "grind_visionary"},
    {"title": "Deep Work Block — 90 Minutes", "description": "Complete an uninterrupted deep work block.", "exp_reward": 40, "rank": "B", "pillar": "output", "pack_id": "cross_deep_work", "cooldown_days": 1, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "", "path_target": "grind_visionary"},
    {"title": "Build and Ship — Small Artifact", "description": "Ship something tiny but real today.", "exp_reward": 38, "rank": "B", "pillar": "output", "pack_id": "gv_output_log", "cooldown_days": 1, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "", "path_target": "grind_visionary"},
    {"title": "Skill Tree Node Unlock Session", "description": "Complete work tied to your next skill tree node.", "exp_reward": 36, "rank": "B", "pillar": "output", "pack_id": "gv_skill_tree", "cooldown_days": 1, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "", "path_target": "grind_visionary"},
    {"title": "Revenue Action", "description": "Take one direct action that can generate income.", "exp_reward": 35, "rank": "B", "pillar": "output", "pack_id": "gv_first_dollar", "cooldown_days": 1, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "", "path_target": "grind_visionary"},
    {"title": "Multiplier Streak Day", "description": "Complete all key quests to preserve multiplier growth.", "exp_reward": 50, "rank": "A", "pillar": "soul", "pack_id": "gv_multiplier", "cooldown_days": 0, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "", "path_target": "grind_visionary"},
    {"title": "Portfolio Proof Day", "description": "Publish one piece of visible proof-of-work.", "exp_reward": 55, "rank": "A", "pillar": "output", "pack_id": "gv_output_log", "cooldown_days": 1, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "", "path_target": "grind_visionary"},
    {"title": "Teaching Pass", "description": "Explain a concept from your field in a public post/thread.", "exp_reward": 50, "rank": "A", "pillar": "mind", "pack_id": "gv_study", "cooldown_days": 1, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "", "path_target": "grind_visionary"},
    {"title": "Weekly Build Sprint", "description": "Ship 3 meaningful outputs inside one week.", "exp_reward": 88, "rank": "S", "pillar": "output", "pack_id": "gv_weekly_boss", "cooldown_days": 6, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": True, "is_one_time_only": False, "equipment_required": "", "path_target": "grind_visionary"},
    {"title": "First Dollar Chain", "description": "Complete step in first-dollar quest chain.", "exp_reward": 95, "rank": "S", "pillar": "output", "pack_id": "gv_first_dollar_chain", "cooldown_days": 6, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": True, "is_one_time_only": False, "equipment_required": "", "path_target": "grind_visionary"},
    {"title": "Deep Study + Practice Combo", "description": "60-minute study + 60-minute practice block.", "exp_reward": 54, "rank": "A", "pillar": "mind", "pack_id": "gv_skill_building", "cooldown_days": 1, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "", "path_target": "grind_visionary"},
    {"title": "Content Repurposing Mission", "description": "Turn one insight into two formats (text + short post/video).", "exp_reward": 36, "rank": "B", "pillar": "output", "pack_id": "gv_output_log", "cooldown_days": 1, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "", "path_target": "grind_visionary"},
    {"title": "Reading-to-Action Conversion", "description": "Read 20 minutes and execute one action from notes.", "exp_reward": 35, "rank": "B", "pillar": "mind", "pack_id": "cross_reading", "cooldown_days": 0, "universal_daily": False, "is_rest_day_quest": False, "is_weekly_boss": False, "is_one_time_only": False, "equipment_required": "book", "path_target": "grind_visionary"},
]


ALL_QUESTS = (
    UNIVERSAL_QUESTS
    + FITNESS_WARRIOR_QUESTS
    + MINDSET_SAGE_QUESTS
    + HEALTH_ALCHEMIST_QUESTS
    + DISCIPLINE_KNIGHT_QUESTS
    + GRIND_VISIONARY_QUESTS
)

REQUIRED_FIELDS = {
    "title",
    "description",
    "exp_reward",
    "rank",
    "pillar",
    "pack_id",
    "cooldown_days",
    "universal_daily",
    "is_rest_day_quest",
    "is_weekly_boss",
    "is_one_time_only",
    "equipment_required",
    "path_target",
}

VALID_PATHS = {
    "",
    "fitness_warrior",
    "mindset_sage",
    "health_alchemist",
    "discipline_knight",
    "grind_visionary",
}

VALID_RANKS = {"D", "C", "B", "A", "S"}
VALID_PILLARS = {"body", "mind", "soul", "output"}
SUPPLEMENT_DISCLAIMER = "Consult your doctor before starting any supplement regimen."


def _is_supplement_quest(quest_data: dict) -> bool:
    if quest_data.get("path_target") != "health_alchemist":
        return False
    title = quest_data.get("title", "").lower()
    pack = quest_data.get("pack_id", "").lower()
    equipment = quest_data.get("equipment_required", "").lower()
    return (
        "supplement" in title
        or "supplement" in pack
        or equipment == "supplement_stack"
    )


def _current_week_start() -> timezone.datetime.date:
    today = timezone.localdate()
    return today - timedelta(days=today.weekday())


class Command(BaseCommand):
    help = "Replace all quests and seed the Phase 5B quest catalog."

    def handle(self, *args, **options):
        # 1) Hard reset existing quest templates
        deleted_count, _ = Quest.objects.all().delete()

        # 2) Validate structure before writes
        errors = []
        seen_keys = set()
        for idx, quest in enumerate(ALL_QUESTS, start=1):
            keys = set(quest.keys())
            missing = REQUIRED_FIELDS - keys
            extra = keys - REQUIRED_FIELDS
            if missing:
                errors.append(f"Quest #{idx} missing fields: {sorted(missing)}")
            if extra:
                errors.append(f"Quest #{idx} has unknown fields: {sorted(extra)}")

            if quest.get("path_target") not in VALID_PATHS:
                errors.append(f"Quest #{idx} has invalid path_target={quest.get('path_target')}")
            if quest.get("rank") not in VALID_RANKS:
                errors.append(f"Quest #{idx} has invalid rank={quest.get('rank')}")
            if quest.get("pillar") not in VALID_PILLARS:
                errors.append(f"Quest #{idx} has invalid pillar={quest.get('pillar')}")
            dedupe_key = (quest.get("path_target"), quest.get("title"))
            if dedupe_key in seen_keys:
                errors.append(
                    f"Quest #{idx} duplicates title/path pair: {dedupe_key}"
                )
            seen_keys.add(dedupe_key)

            if _is_supplement_quest(quest) and SUPPLEMENT_DISCLAIMER not in quest.get("description", ""):
                errors.append(
                    f"Quest #{idx} missing exact supplement disclaimer text."
                )

        if errors:
            for err in errors:
                self.stdout.write(self.style.ERROR(err))
            raise ValueError("Quest seed validation failed.")

        # 3) Create quest records
        for quest_data in ALL_QUESTS:
            Quest.objects.create(**quest_data)

        # 4) Seed chain relationships (Health Alchemist gut reset chain).
        # Because quest templates are hard-reset each run, this remains idempotent.
        gut_chain = list(
            Quest.objects.filter(
                path_target="health_alchemist",
                pack_id="ha_gut_reset_chain",
            ).order_by("title")
        )
        for sequence_order, (parent, child) in enumerate(zip(gut_chain, gut_chain[1:]), start=1):
            QuestChain.objects.update_or_create(
                parent_quest=parent,
                child_quest=child,
                defaults={"sequence_order": sequence_order},
            )

        # 5) Seed WeeklyBossQuest records from boss templates.
        # Model is unique per (path_target, week_start), so multiple boss templates
        # for a path are scheduled into consecutive weeks.
        weekly_boss_upserts = 0
        week_start = _current_week_start()
        for path_target in sorted(VALID_PATHS - {""}):
            path_bosses = list(
                Quest.objects.filter(
                    path_target=path_target,
                    is_weekly_boss=True,
                ).order_by("title")
            )
            for offset, boss in enumerate(path_bosses):
                scheduled_week = week_start + timedelta(days=7 * offset)
                WeeklyBossQuest.objects.update_or_create(
                    path_target=path_target,
                    week_start=scheduled_week,
                    defaults={
                        "title": boss.title,
                        "description": boss.description,
                        "exp_reward": boss.exp_reward,
                        "badge": None,
                        "is_active": True,
                    },
                )
                weekly_boss_upserts += 1

        total = len(ALL_QUESTS)
        path_counts = {
            "universal": len(UNIVERSAL_QUESTS),
            "fitness_warrior": len(FITNESS_WARRIOR_QUESTS),
            "mindset_sage": len(MINDSET_SAGE_QUESTS),
            "health_alchemist": len(HEALTH_ALCHEMIST_QUESTS),
            "discipline_knight": len(DISCIPLINE_KNIGHT_QUESTS),
            "grind_visionary": len(GRIND_VISIONARY_QUESTS),
        }
        boss_count = sum(1 for q in ALL_QUESTS if q["is_weekly_boss"])

        self.stdout.write(self.style.WARNING(f"Deleted {deleted_count} existing quest-related records."))
        self.stdout.write(self.style.SUCCESS(f"Created {total} Phase 5B quests."))
        for key, count in path_counts.items():
            self.stdout.write(f" - {key}: {count}")
        self.stdout.write(f" - weekly_boss_quests: {boss_count}")
        self.stdout.write(f" - quest_chain_links_upserted: {max(0, len(gut_chain) - 1)}")
        self.stdout.write(f" - weekly_boss_records_upserted: {weekly_boss_upserts}")
