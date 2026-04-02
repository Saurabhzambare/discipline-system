from rest_framework import serializers

from .models import PlayerDailyQuestAssignment


class QuestSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="quest.id", read_only=True)
    title = serializers.CharField(source="quest.title", read_only=True)
    description = serializers.CharField(source="quest.description", read_only=True)
    category = serializers.CharField(source="quest.category", read_only=True)
    difficulty = serializers.CharField(source="quest.difficulty", read_only=True)
    recurrence = serializers.CharField(source="quest.recurrence", read_only=True)
    category_display = serializers.CharField(source="quest.get_category_display", read_only=True)
    difficulty_display = serializers.CharField(source="quest.get_difficulty_display", read_only=True)
    recurrence_display = serializers.CharField(source="quest.get_recurrence_display", read_only=True)
    path_target = serializers.CharField(source="quest.path_target", read_only=True)
    rank = serializers.CharField(source="quest.rank", read_only=True)
    pillar = serializers.CharField(source="quest.pillar", read_only=True)
    universal_daily = serializers.BooleanField(source="quest.universal_daily", read_only=True)
    is_weekly_boss = serializers.BooleanField(source="quest.is_weekly_boss", read_only=True)
    cooldown_days = serializers.IntegerField(source="quest.cooldown_days", read_only=True)
    exp_reward = serializers.IntegerField(source="assigned_exp_reward", read_only=True)
    completed_today = serializers.BooleanField(source="completed", read_only=True)
    # Kept for API compatibility with existing frontend payload contract.
    assigned_completed_today = serializers.BooleanField(source="completed", read_only=True)

    class Meta:
        model = PlayerDailyQuestAssignment
        fields = [
            "id",
            "title",
            "description",
            "category",
            "difficulty",
            "recurrence",
            "category_display",
            "difficulty_display",
            "recurrence_display",
            "path_target",
            "rank",
            "pillar",
            "universal_daily",
            "is_weekly_boss",
            "cooldown_days",
            "exp_reward",
            "completed_today",
            "assigned_completed_today",
        ]


class QuestCompleteSerializer(serializers.Serializer):
    quest_id = serializers.IntegerField()
