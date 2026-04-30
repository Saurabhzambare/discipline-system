"""
Shared constants for the paths app.

Kept separate from models/services so they can be imported anywhere
without circular dependencies.
"""

# Pack IDs that count toward Mastery Lab quest completion totals
# (used by Grind Visionary skill tree progression).
MASTERY_LAB_PACK_IDS = {
    "gv_skill_building",
    "gv_study",
    "gv_skill_tree",
}

# Grind Visionary skill tree node order (must match GV_SKILL_TREE_NODES in services.py).
# Index 0 ("foundation") is unlocked at onboarding for free; the remaining six are
# threshold-gated by cumulative Mastery Lab quest completions.
SKILL_TREE_NODE_ORDER = [
    "foundation",
    "consistency",
    "execution",
    "shipping",
    "audience",
    "monetization",
    "scaling",
]

# Cumulative Mastery Lab completion thresholds per node_key.
# Spec called for 7 thresholds (5/15/30/50/80/120/175) but the existing
# onboarding flow unlocks "foundation" for free, leaving 6 threshold tiers
# for the remaining nodes. Top tier 175 was dropped to fit; document if changed.
SKILL_TREE_THRESHOLDS = {
    "foundation":   0,    # unlocked at onboarding
    "consistency":  5,
    "execution":    15,
    "shipping":     30,
    "audience":     50,
    "monetization": 80,
    "scaling":      120,
}
