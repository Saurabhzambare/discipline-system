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
        self.user.player.path = "gym"
        self.user.player.save(update_fields=["path", "updated_at"])

        response = self.client.get(reverse("player-me"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["path"], "gym")
        self.assertEqual(response.data["path_display"], "Gym")

    def test_player_path_update_endpoint_persists_path(self):
        response = self.client.patch(
            reverse("player-path"),
            {"path": "runner"},
            format="json",
        )

        self.user.player.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["path"], "runner")
        self.assertEqual(self.user.player.path, "runner")

    def test_player_path_update_rejects_invalid_path(self):
        response = self.client.patch(
            reverse("player-path"),
            {"path": "unknown"},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
