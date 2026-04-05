from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from paths.models import (
    ArmorPiece,
    ArmorSystem,
    BodyJournal,
    DarkNightEntry,
    ElixirProgress,
    FreedomDayToken,
    GraceToken,
    MultiplierProtection,
    OutputLog,
    PostFirstDollarChain,
    StreakShield,
    TemptationLog,
    TransmutationMilestone,
    WarRoomEntry,
    WisdomLog,
    XPMultiplier,
)
from social.services import has_active_accountability_partner


@dataclass
class CompletionMechanicResult:
    bonus_exp: int = 0
    notes: list[str] | None = None


FIRST_DOLLAR_PACK = "gv_first_dollar"
FIRST_DOLLAR_CHAIN_10_PACK = "gv_first_dollar_10"
FIRST_DOLLAR_CHAIN_100_PACK = "gv_first_dollar_100"
FIRST_DOLLAR_CHAIN_MONTHLY_PACK = "gv_first_dollar_monthly"


@transaction.atomic
def apply_post_completion_mechanics(*, player, lineup_path: str, completion_date, quest=None) -> CompletionMechanicResult:
    notes: list[str] = []
    bonus_exp = 0

    # Mindset Sage: Freedom token every 7-day streak, cap 3, overflow bonus exp.
    if lineup_path == "mindset_sage" and player.streak > 0 and player.streak % 7 == 0:
        available = FreedomDayToken.objects.filter(player=player, is_used=False).count()
        if available >= 3:
            bonus_exp += 200
            notes.append("freedom_token_overflow_exp")
        else:
            FreedomDayToken.objects.create(player=player, earned_on=completion_date)
            notes.append("freedom_token_earned")

    # Health Alchemist: fill elixir progress and award milestones.
    if lineup_path == "health_alchemist":
        progress, _ = ElixirProgress.objects.get_or_create(player=player)
        if progress.last_fill_date != completion_date:
            progress.fill_days = min(7, progress.fill_days + 1)
            progress.last_fill_date = completion_date
            if progress.fill_days >= 7:
                progress.brews_completed += 1
                progress.last_brew_date = completion_date
                progress.fill_days = 0
                notes.append("elixir_brew_completed")
            progress.save(update_fields=["fill_days", "last_fill_date", "brews_completed", "last_brew_date"])

        milestone_edges = [(1, "first_brew"), (3, "triple_brew"), (7, "master_formula")]
        for threshold, key in milestone_edges:
            if progress.brews_completed >= threshold:
                TransmutationMilestone.objects.get_or_create(
                    player=player,
                    milestone_key=key,
                    defaults={"achieved_on": completion_date},
                )

    # Discipline Knight: armor progression and streak shield earn threshold.
    if lineup_path == "discipline_knight":
        armor, _ = ArmorSystem.objects.get_or_create(player=player)
        if player.streak in {7, 14, 21, 28, 35, 42}:
            slot_map = {
                7: "helmet",
                14: "chest",
                21: "gauntlets",
                28: "legs",
                35: "boots",
                42: "shield",
            }
            slot = slot_map.get(player.streak)
            if slot:
                ArmorPiece.objects.get_or_create(
                    player=player,
                    slot=slot,
                    defaults={"name": f"Forged {slot.title()}"},
                )

        if player.streak > 0 and player.streak % 14 == 0:
            shield, _ = StreakShield.objects.get_or_create(player=player)
            if shield.shields_available < 1:
                shield.shields_available = 1
                shield.last_earned_date = completion_date
                shield.save(update_fields=["shields_available", "last_earned_date"])
                notes.append("streak_shield_earned")

        armor.save(update_fields=["total_cracks", "repaired_at", "last_cracked_on"])

    # Grind Visionary: multipliers and first-dollar progression.
    if lineup_path == "grind_visionary":
        multiplier, _ = XPMultiplier.objects.get_or_create(player=player)
        days_active = max(player.streak, 1)
        # 1.0x -> 2.0x over 30 days.
        next_multiplier = min(2.0, 1.0 + ((days_active - 1) / 30.0))
        multiplier.multiplier = round(next_multiplier, 2)
        multiplier.source = "streak_growth"
        multiplier.save(update_fields=["multiplier", "source"])

        if quest and quest.pack_id == FIRST_DOLLAR_PACK:
            chain, _ = PostFirstDollarChain.objects.get_or_create(player=player)
            if not chain.first_dollar_completed:
                multiplier_value = float(multiplier.multiplier or 1.0)
                first_dollar_reward = int(round(200 * multiplier_value))
                bonus_exp += first_dollar_reward
                chain.first_dollar_completed = True
                chain.first_dollar_completed_on = completion_date
                chain.chain_unlocked = True
                chain.chain_stage = max(chain.chain_stage, 1)
                chain.current_chain = max(chain.current_chain, 1)
                chain.longest_chain = max(chain.longest_chain, 1)
                chain.last_revenue_date = completion_date
                chain.save(
                    update_fields=[
                        "first_dollar_completed",
                        "first_dollar_completed_on",
                        "chain_unlocked",
                        "chain_stage",
                        "current_chain",
                        "longest_chain",
                        "last_revenue_date",
                    ]
                )
                notes.append("first_dollar_triggered")

        if quest and quest.pack_id == FIRST_DOLLAR_CHAIN_10_PACK:
            chain, _ = PostFirstDollarChain.objects.get_or_create(player=player)
            if chain.chain_unlocked and not chain.first_ten_completed:
                chain.first_ten_completed = True
                chain.chain_stage = max(chain.chain_stage, 2)
                chain.save(update_fields=["first_ten_completed", "chain_stage"])
                notes.append("first_dollar_chain_10_completed")

        if quest and quest.pack_id == FIRST_DOLLAR_CHAIN_100_PACK:
            chain, _ = PostFirstDollarChain.objects.get_or_create(player=player)
            if chain.first_ten_completed and not chain.first_hundred_completed:
                chain.first_hundred_completed = True
                chain.chain_stage = max(chain.chain_stage, 3)
                chain.save(update_fields=["first_hundred_completed", "chain_stage"])
                notes.append("first_dollar_chain_100_completed")

        if quest and quest.pack_id == FIRST_DOLLAR_CHAIN_MONTHLY_PACK:
            chain, _ = PostFirstDollarChain.objects.get_or_create(player=player)
            if chain.first_hundred_completed and not chain.first_monthly_completed:
                chain.first_monthly_completed = True
                chain.chain_stage = max(chain.chain_stage, 4)
                chain.save(update_fields=["first_monthly_completed", "chain_stage"])
                notes.append("first_dollar_chain_monthly_completed")

        output_today = OutputLog.objects.filter(player=player, log_date=completion_date).first()
        if output_today and output_today.revenue_usd > 0:
            chain, _ = PostFirstDollarChain.objects.get_or_create(player=player)
            if chain.last_revenue_date == completion_date - timedelta(days=1):
                chain.current_chain += 1
            elif chain.last_revenue_date != completion_date:
                chain.current_chain = max(chain.current_chain, 1)
            chain.longest_chain = max(chain.longest_chain, chain.current_chain)
            chain.last_revenue_date = completion_date
            chain.save(update_fields=["current_chain", "longest_chain", "last_revenue_date"])
            notes.append("revenue_chain_progressed")

        if has_active_accountability_partner(player=player):
            notes.append("accountability_partner_active")

    return CompletionMechanicResult(bonus_exp=bonus_exp, notes=notes)


@transaction.atomic
def process_dark_night_entry(*, player, entry: str, entry_date):
    word_count = len([w for w in entry.split() if w.strip()])
    if word_count < 100:
        raise ValueError("Dark Night entry must be at least 100 words.")

    dark_night, created = DarkNightEntry.objects.get_or_create(
        player=player,
        activated_on=entry_date,
        defaults={"entry": entry, "exp_awarded": 200},
    )
    if not created:
        raise ValueError("Dark Night can only be activated once per day.")

    player.exp += dark_night.exp_awarded
    player.save(update_fields=["exp", "updated_at"])
    return dark_night


@transaction.atomic
def redeem_freedom_day_token(*, player, redeem_date):
    token = (
        FreedomDayToken.objects.select_for_update()
        .filter(player=player, is_used=False)
        .order_by("earned_on")
        .first()
    )
    if not token:
        raise ValueError("No Freedom Day Token available.")

    token.is_used = True
    token.used_on = redeem_date
    token.save(update_fields=["is_used", "used_on"])
    return token


@transaction.atomic
def apply_missed_day_protections(*, player, today):
    """Order: Grace Token -> Streak Shield -> Multiplier Protection -> Elixir Mercy -> streak break."""
    if not player.last_active_date:
        return {"protected_by": None, "streak_broken": False}

    gap = (today - player.last_active_date).days
    if gap <= 1:
        return {"protected_by": None, "streak_broken": False}

    grace = GraceToken.objects.filter(player=player, is_used=False).order_by("earned_on").first()
    if grace:
        grace.is_used = True
        grace.used_on = today
        grace.save(update_fields=["is_used", "used_on"])
        player.last_active_date = today - timedelta(days=1)
        player.save(update_fields=["last_active_date", "updated_at"])
        return {"protected_by": "grace_token", "streak_broken": False}

    shield = StreakShield.objects.filter(player=player).first()
    if shield and shield.shields_available > 0:
        shield.shields_available -= 1
        shield.save(update_fields=["shields_available"])
        player.last_active_date = today - timedelta(days=1)
        player.save(update_fields=["last_active_date", "updated_at"])
        return {"protected_by": "streak_shield", "streak_broken": False}

    protection = MultiplierProtection.objects.filter(player=player, is_used=False).order_by("earned_on").first()
    if protection:
        protection.is_used = True
        protection.used_on = today
        protection.save(update_fields=["is_used", "used_on"])
        player.last_active_date = today - timedelta(days=1)
        player.save(update_fields=["last_active_date", "updated_at"])
        return {"protected_by": "multiplier_protection", "streak_broken": False}

    progress = ElixirProgress.objects.filter(player=player).first()
    if progress and progress.fill_days > 0:
        progress.mercy_retained_fill_days = progress.fill_days // 2
        progress.fill_days = progress.mercy_retained_fill_days
        progress.save(update_fields=["mercy_retained_fill_days", "fill_days"])
        player.streak = 1
        player.save(update_fields=["streak", "updated_at"])
        return {"protected_by": "elixir_mercy", "streak_broken": True}

    # Final fallback: streak break
    player.streak = 0
    player.save(update_fields=["streak", "updated_at"])
    if player.path == "discipline_knight":
        armor, _ = ArmorSystem.objects.get_or_create(player=player)
        armor.total_cracks += 1
        armor.last_cracked_on = today
        armor.save(update_fields=["total_cracks", "last_cracked_on"])
    return {"protected_by": None, "streak_broken": True}


def get_vision_board_summary(*, player, today):
    goal = getattr(player, "singular_goal", None)
    if not goal:
        return {"goal": None}
    countdown_days = None
    if goal.target_date:
        countdown_days = max(0, (goal.target_date - today).days)
    return {
        "goal": {
            "title": goal.title,
            "description": goal.description,
            "target_date": goal.target_date.isoformat() if goal.target_date else None,
            "countdown_days": countdown_days,
            "is_achieved": goal.is_achieved,
        }
    }


def can_view_wisdom_log_entry(*, requesting_player, entry: WisdomLog):
    return entry.player_id == requesting_player.id or entry.is_public


def can_view_output_log_entry(*, requesting_player, entry: OutputLog):
    return entry.player_id == requesting_player.id or entry.is_public


def can_view_body_journal_entry(*, requesting_player, entry: BodyJournal):
    return entry.player_id == requesting_player.id
