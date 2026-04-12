from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase


class PlayerPathApiTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="pathuser",
            password="testpass123",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_player_me_includes_path(self):
        self.user.player.path = "fitness_warrior"
        self.user.player.save(update_fields=["path", "updated_at"])

        response = self.client.get(reverse("player-me"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["path"], "fitness_warrior")
        self.assertEqual(response.data["path_display"], "Fitness Warrior")

    def test_player_path_update_endpoint_persists_path(self):
        response = self.client.patch(
            reverse("player-path"),
            {"path": "grind_visionary"},
            format="json",
        )

        self.user.player.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["path"], "grind_visionary")
        self.assertEqual(self.user.player.path, "grind_visionary")

    def test_player_path_update_rejects_invalid_path(self):
        response = self.client.patch(
            reverse("player-path"),
            {"path": "unknown"},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
