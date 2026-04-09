from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from players.models import Player
from paths.models import (
    ArmorPiece,
    ArmorSystem,
    BodyJournal,
    DisciplineCode,
    DisciplineKnightProfile,
    ElixirProgress,
    EquipmentProfile,
    GrindVisionaryProfile,
    HealthAlchemistProfile,
    MindsetSageProfile,
    OutputLog,
    PathOnboardingProgress,
    PostFirstDollarChain,
    SingularGoal,
    SkillTree,
    SkillTreeNode,
    StreakShield,
    UserPathSelection,
    XPMultiplier,
)

User = get_user_model()

TEST_PASSWORD = "testpass123"
GV_SKILL_TREE_NODES = [
    "foundation",
    "consistency",
    "execution",
    "shipping",
    "audience",
    "monetization",
    "scaling",
]

ACCOUNT_BLUEPRINTS = {
    "mindset_sage": {
        "username": "s6_mindset_sage",
        "player": {"level": 6, "exp": 1900, "streak": 12},
        "onboarding_answers": {
            "motivation": "personal_growth",
            "daily_time_commitment": "30_minutes",
            "experience_level": "some_experience",
            "archetype": "warrior_sage",
        },
    },
    "discipline_knight": {
        "username": "s6_discipline_knight",
        "player": {"level": 8, "exp": 3150, "streak": 21},
        "onboarding_answers": {
            "routine_level": "partial_routine",
            "biggest_challenge": "staying_focused",
            "structure_preference": "semi_structured",
            "time_commitment": "1_hour",
        },
    },
    "health_alchemist": {
        "username": "s6_health_alchemist",
        "player": {"level": 7, "exp": 2400, "streak": 16},
        "onboarding_answers": {
            "primary_health_goal": "optimize_energy",
            "health_relationship": "some_good_habits",
            "focus_area": "nutrition",
            "equipment_list": ["fitness_tracker", "supplements"],
        },
    },
    "grind_visionary": {
        "username": "s6_grind_visionary",
        "player": {"level": 9, "exp": 4100, "streak": 27},
        "onboarding_answers": {
            "grind_focus": "coding_and_tech",
            "grind_focus_other": "",
            "experience_state": "intermediate_ready_to_ship",
            "singular_goal_text": "Launch a usable MVP with weekly shipping cadence",
            "goal_timeline": "6_months",
            "daily_hours": "2_hours",
            "current_output_state": "ship_regularly",
        },
    },
}


class Command(BaseCommand):
    help = (
        "Create or repair Session 6 test accounts that bypass onboarding and open dashboard directly."
    )

    def handle(self, *args, **options):
        today = timezone.localdate()
        now = timezone.now()

        for path_code, blueprint in ACCOUNT_BLUEPRINTS.items():
            username = blueprint["username"]
            player_state = blueprint["player"]
            onboarding_answers = blueprint["onboarding_answers"]

            user, created = User.objects.get_or_create(username=username)
            user.set_password(TEST_PASSWORD)
            user.is_active = True
            user.save(update_fields=["password", "is_active"])

            player, _ = Player.objects.get_or_create(user=user)
            player.path = path_code
            player.level = player_state["level"]
            player.exp = player_state["exp"]
            player.streak = player_state["streak"]
            player.last_active_date = today
            player.timezone = "UTC"
            player.save(
                update_fields=[
                    "path",
                    "level",
                    "exp",
                    "streak",
                    "last_active_date",
                    "timezone",
                    "updated_at",
                ]
            )

            UserPathSelection.objects.update_or_create(
                player=player,
                defaults={
                    "path": path_code,
                    "onboarding_complete": True,
                    "multi_paths_active": [path_code],
                    "multi_path_unlock_day": 30,
                },
            )

            PathOnboardingProgress.objects.update_or_create(
                player=player,
                path=path_code,
                defaults={
                    "current_step": "complete",
                    "answers_snapshot": onboarding_answers,
                    "is_completed": True,
                    "completed_at": now,
                },
            )

            if path_code == "mindset_sage":
                MindsetSageProfile.objects.update_or_create(
                    player=player,
                    defaults=onboarding_answers,
                )

            if path_code == "discipline_knight":
                DisciplineKnightProfile.objects.update_or_create(
                    player=player,
                    defaults=onboarding_answers,
                )
                DisciplineCode.objects.update_or_create(
                    player=player,
                    defaults={
                        "code_items": [
                            "No snooze, no negotiation.",
                            "Deep work before dopamine.",
                            "Finish what I start each day.",
                        ]
                    },
                )
                ArmorSystem.objects.update_or_create(
                    player=player,
                    defaults={"total_cracks": 0, "last_cracked_on": None, "repaired_at": today},
                )
                StreakShield.objects.update_or_create(
                    player=player,
                    defaults={"shields_available": 1, "last_earned_date": today},
                )
                ArmorPiece.objects.update_or_create(
                    player=player,
                    slot="boots",
                    defaults={"name": "Forged Boots", "is_equipped": True},
                )

            if path_code == "health_alchemist":
                HealthAlchemistProfile.objects.update_or_create(
                    player=player,
                    defaults={
                        "primary_health_goal": onboarding_answers["primary_health_goal"],
                        "health_relationship": onboarding_answers["health_relationship"],
                        "focus_area": onboarding_answers["focus_area"],
                    },
                )
                EquipmentProfile.objects.update_or_create(
                    player=player,
                    defaults={"equipment_list": onboarding_answers["equipment_list"]},
                )
                ElixirProgress.objects.update_or_create(
                    player=player,
                    defaults={
                        "elixir_level": 2,
                        "current_formula": "AM hydration + PM sleep stack",
                        "brews_completed": 2,
                        "fill_days": 4,
                        "mercy_retained_fill_days": 2,
                        "last_brew_date": today - timedelta(days=3),
                        "last_fill_date": today,
                    },
                )
                BodyJournal.objects.update_or_create(
                    player=player,
                    log_date=today,
                    defaults={
                        "weight_kg": "78.30",
                        "sleep_hours": "7.40",
                        "energy_level": 8,
                        "notes": "Steady energy with cleaner meals.",
                        "is_public": False,
                    },
                )

            if path_code == "grind_visionary":
                GrindVisionaryProfile.objects.update_or_create(
                    player=player,
                    defaults={
                        "grind_focus": onboarding_answers["grind_focus"],
                        "grind_focus_other": onboarding_answers["grind_focus_other"],
                        "experience_state": onboarding_answers["experience_state"],
                        "daily_hours": onboarding_answers["daily_hours"],
                        "current_output_state": onboarding_answers["current_output_state"],
                    },
                )
                SingularGoal.objects.update_or_create(
                    player=player,
                    defaults={
                        "title": onboarding_answers["singular_goal_text"],
                        "description": "Timeline: 6_months",
                        "target_date": today + timedelta(days=180),
                        "is_achieved": False,
                        "achieved_at": None,
                    },
                )
                skill_tree, _ = SkillTree.objects.get_or_create(player=player, path="grind_visionary")
                for index, node_key in enumerate(GV_SKILL_TREE_NODES):
                    SkillTreeNode.objects.update_or_create(
                        tree=skill_tree,
                        node_key=node_key,
                        defaults={
                            "is_unlocked": index < 3,
                            "unlocked_at": now if index < 3 else None,
                        },
                    )
                XPMultiplier.objects.update_or_create(
                    player=player,
                    defaults={"multiplier": 1.45, "source": "seed_session6_test_accounts", "expires_at": None},
                )
                PostFirstDollarChain.objects.update_or_create(
                    player=player,
                    defaults={
                        "current_chain": 5,
                        "longest_chain": 7,
                        "last_revenue_date": today,
                        "first_dollar_completed": True,
                        "first_dollar_completed_on": today - timedelta(days=14),
                        "chain_unlocked": True,
                        "chain_stage": 1,
                        "first_ten_completed": False,
                        "first_hundred_completed": False,
                        "first_monthly_completed": False,
                    },
                )
                OutputLog.objects.update_or_create(
                    player=player,
                    log_date=today,
                    defaults={
                        "deep_work_hours": "2.50",
                        "tasks_shipped": 2,
                        "revenue_usd": "120.00",
                        "notes": "Shipped MVP bugfixes and posted changelog.",
                        "is_public": False,
                    },
                )

            state_word = "Created" if created else "Repaired"
            self.stdout.write(
                self.style.SUCCESS(
                    f"{state_word}: {username} ({path_code}) | password={TEST_PASSWORD}"
                )
            )

        self.stdout.write(self.style.SUCCESS("Session 6 test accounts are ready."))
