from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from paths.models import PathOnboardingProgress, UserPathSelection


class OnboardingCompletionAuthTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="onboard_auth",
            password="testpass123",
        )
        self.player = self.user.player
        self.player.path = "fitness_warrior"
        self.player.save(update_fields=["path", "updated_at"])

        UserPathSelection.objects.create(
            player=self.player,
            path="fitness_warrior",
            onboarding_complete=False,
            multi_paths_active=["fitness_warrior"],
        )

        self.url = reverse("onboarding-complete")

    def test_authenticated_user_can_complete_onboarding(self):
        client = APIClient()
        token = str(RefreshToken.for_user(self.user).access_token)
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = client.post(
            self.url,
            {"path_code": "fitness_warrior"},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["completed"])
        self.assertEqual(response.data["path_code"], "fitness_warrior")
        self.assertIn("player", response.data)

        selection = UserPathSelection.objects.get(player=self.player)
        self.assertTrue(selection.onboarding_complete)

        progress = PathOnboardingProgress.objects.get(
            player=self.player,
            path="fitness_warrior",
        )
        self.assertTrue(progress.is_completed)
        self.assertEqual(progress.current_step, "complete")

    def test_onboarding_complete_requires_authentication(self):
        client = APIClient()

        response = client.post(
            self.url,
            {"path_code": "fitness_warrior"},
            format="json",
        )

        self.assertEqual(response.status_code, 401)
