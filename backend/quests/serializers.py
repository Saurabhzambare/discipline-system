from rest_framework import serializers
from .models import Quest


class QuestSerializer(serializers.ModelSerializer):
    """
    Used when sending quest data from the backend to the frontend.
    Example use case:
    GET /api/quests/
    """

    completed_today = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Quest

        # These are the fields we want to expose in the API response
        fields = [
            "id",
            "title",
            "description",
            "exp_reward",
            "is_active",
            "completed_today",
        ]

    def get_completed_today(self, obj):
        completed_today_quest_ids = self.context.get("completed_today_quest_ids", set())
        return obj.id in completed_today_quest_ids


class QuestCompleteSerializer(serializers.Serializer):
    """
    Used when the frontend sends a request to complete a quest.
    Example request body:
    {
        "quest_id": 1
    }
    """

    # We only need the quest ID from the frontend for now
    quest_id = serializers.IntegerField()