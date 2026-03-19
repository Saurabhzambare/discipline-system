from rest_framework import serializers

from .models import Player


class PlayerSerializer(serializers.ModelSerializer):
    # Username is denormalized into payload for convenience in profile responses.
    username = serializers.CharField(source="user.username", read_only=True)
    path_display = serializers.SerializerMethodField(read_only=True)

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
            "created_at",
            "updated_at",
        ]

    def get_path_display(self, obj):
        return obj.get_path_display() if obj.path else ""


class PlayerPathUpdateSerializer(serializers.Serializer):
    path = serializers.ChoiceField(choices=Player.PATH_CHOICES)
