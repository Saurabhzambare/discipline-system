from rest_framework import serializers

from .models import Player


class PlayerSerializer(serializers.ModelSerializer):
    # Username is denormalized into payload for convenience in profile responses.
    username = serializers.CharField(source="user.username", read_only=True)
    path_display = serializers.SerializerMethodField(read_only=True)
    exp_in_level = serializers.SerializerMethodField(read_only=True)
    exp_for_level = serializers.SerializerMethodField(read_only=True)
    exp_to_next_level = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Player
        fields = [
            "id",
            "username",
            "level",
            "exp",
            "streak",
            "path",
            "path_display",
            "timezone",
            "exp_in_level",
            "exp_for_level",
            "exp_to_next_level",
            "last_active_date",
            "created_at",
            "updated_at",
        ]

    def get_path_display(self, obj):
        return obj.get_path_display() if obj.path else ""

    def _exp_window(self, obj):
        current_level_floor = (obj.level**2 * 50) - 50
        next_level_floor = ((obj.level + 1) ** 2 * 50) - 50
        return {
            "exp_in_level": max(0, obj.exp - current_level_floor),
            "exp_for_level": max(1, next_level_floor - current_level_floor),
            "exp_to_next_level": max(0, next_level_floor - obj.exp),
        }

    def get_exp_in_level(self, obj):
        return self._exp_window(obj)["exp_in_level"]

    def get_exp_for_level(self, obj):
        return self._exp_window(obj)["exp_for_level"]

    def get_exp_to_next_level(self, obj):
        return self._exp_window(obj)["exp_to_next_level"]


class PlayerPathUpdateSerializer(serializers.Serializer):
    path = serializers.ChoiceField(choices=Player.PATH_CHOICES)
