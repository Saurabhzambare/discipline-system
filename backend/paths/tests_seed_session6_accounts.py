from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase

from paths.models import (
    DisciplineCode,
    DisciplineKnightProfile,
    EquipmentProfile,
    GrindVisionaryProfile,
    HealthAlchemistProfile,
    MindsetSageProfile,
    PathOnboardingProgress,
    PostFirstDollarChain,
    SingularGoal,
    SkillTree,
    UserPathSelection,
)


class SeedSession6TestAccountsCommandTests(TestCase):
    def test_command_creates_reusable_accounts_with_completed_onboarding(self):
        call_command("seed_session6_test_accounts")

        expectations = {
            "s6_mindset_sage": ("mindset_sage", MindsetSageProfile),
            "s6_discipline_knight": ("discipline_knight", DisciplineKnightProfile),
            "s6_health_alchemist": ("health_alchemist", HealthAlchemistProfile),
            "s6_grind_visionary": ("grind_visionary", GrindVisionaryProfile),
        }

        User = get_user_model()
        for username, (path_code, profile_model) in expectations.items():
            user = User.objects.get(username=username)
            self.assertTrue(user.check_password("testpass123"))

            player = user.player
            self.assertEqual(player.path, path_code)
            self.assertGreater(player.streak, 0)

            selection = UserPathSelection.objects.get(player=player)
            self.assertEqual(selection.path, path_code)
            self.assertTrue(selection.onboarding_complete)
            self.assertEqual(selection.multi_paths_active, [path_code])

            progress = PathOnboardingProgress.objects.get(player=player, path=path_code)
            self.assertTrue(progress.is_completed)
            self.assertEqual(progress.current_step, "complete")

            self.assertTrue(profile_model.objects.filter(player=player).exists())

        knight = User.objects.get(username="s6_discipline_knight").player
        self.assertTrue(DisciplineCode.objects.filter(player=knight).exists())

        alchemist = User.objects.get(username="s6_health_alchemist").player
        self.assertTrue(EquipmentProfile.objects.filter(player=alchemist).exists())

        visionary = User.objects.get(username="s6_grind_visionary").player
        self.assertTrue(SingularGoal.objects.filter(player=visionary).exists())
        self.assertTrue(SkillTree.objects.filter(player=visionary, path="grind_visionary").exists())
        self.assertTrue(PostFirstDollarChain.objects.filter(player=visionary).exists())
