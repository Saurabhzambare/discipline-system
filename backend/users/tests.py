from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from django.test import TestCase

from players.models import Player


class SignupApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.signup_url = reverse("auth-signup")

    def test_signup_endpoint_creates_user_and_player(self):
        payload = {
            "username": "newuser",
            "password": "StrongPass123!",
        }

        response = self.client.post(self.signup_url, payload, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["username"], "newuser")
        self.assertEqual(response.data["message"], "Signup successful.")

        user = get_user_model().objects.get(username="newuser")
        self.assertTrue(Player.objects.filter(user=user).exists())

    def test_signup_endpoint_rejects_duplicate_username(self):
        get_user_model().objects.create_user(
            username="newuser",
            password="StrongPass123!",
        )

        payload = {
            "username": "newuser",
            "password": "StrongPass123!",
        }

        response = self.client.post(self.signup_url, payload, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertIn("username", response.data)
