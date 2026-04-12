from rest_framework import serializers

from .models import DailyCompletionSummary, DailyQuestLineupItem, Quest


class QuestSerializer(serializers.Serializer):
    id = serializers.IntegerField(source="quest_id")
    title = serializers.CharField()
    description = serializers.CharField()
    category = serializers.CharField(required=False, allow_blank=True)
    difficulty = serializers.CharField(required=False, allow_blank=True)
    recurrence = serializers.CharField(required=False, allow_blank=True)
    category_display = serializers.CharField(required=False, allow_blank=True)
    difficulty_display = serializers.CharField(required=False, allow_blank=True)
    recurrence_display = serializers.CharField(required=False, allow_blank=True)
    path_target = serializers.CharField(required=False, allow_blank=True)
    rank = serializers.CharField(required=False, allow_blank=True)
    pillar = serializers.CharField(required=False, allow_blank=True)
    universal_daily = serializers.BooleanField(required=False, default=False)
    is_weekly_boss = serializers.BooleanField(required=False, default=False)
    cooldown_days = serializers.IntegerField(required=False, default=0)
    exp_reward = serializers.IntegerField()
    completed_today = serializers.BooleanField()
    assigned_completed_today = serializers.BooleanField()


class QuestCompleteSerializer(serializers.Serializer):
    quest_id = serializers.IntegerField()


class DailyLineupQuerySerializer(serializers.Serializer):
    date = serializers.DateField(required=False)


class CompleteLineupItemSerializer(serializers.Serializer):
    item_id = serializers.IntegerField()


class SwapQuestSerializer(serializers.Serializer):
    item_id = serializers.IntegerField()
    new_quest_id = serializers.IntegerField()


class SwapAlternativesQuerySerializer(serializers.Serializer):
    item_id = serializers.IntegerField()


class DailyIntentionSerializer(serializers.Serializer):
    date = serializers.DateField()
    intention = serializers.ChoiceField(choices=["full_send", "steady", "recovery"])


class QuestFeedbackSerializer(serializers.Serializer):
    item_id = serializers.IntegerField()
    feedback = serializers.ChoiceField(choices=["up", "down"])


class DailySummaryQuerySerializer(serializers.Serializer):
    date = serializers.DateField(required=False)


class LineupItemSerializer(serializers.ModelSerializer):
    quest_id = serializers.IntegerField(source="quest.id", allow_null=True)
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    path_target = serializers.SerializerMethodField()
    rank = serializers.SerializerMethodField()
    pillar = serializers.SerializerMethodField()
    exp_reward = serializers.SerializerMethodField()
    completed_today = serializers.BooleanField(source="completed")
    assigned_completed_today = serializers.BooleanField(source="completed")

    class Meta:
        model = DailyQuestLineupItem
        fields = [
            "id",
            "quest_id",
            "title",
            "description",
            "path_target",
            "rank",
            "pillar",
            "exp_reward",
            "slot_order",
            "slot_type",
            "is_locked",
            "is_carried_over",
            "selection_reason",
            "completed_today",
            "assigned_completed_today",
            "feedback",
        ]

    def get_title(self, obj):
        return obj.quest.title if obj.quest else "Choose your own quest"

    def get_description(self, obj):
        return obj.quest.description if obj.quest else ""

    def get_path_target(self, obj):
        return obj.quest.path_target if obj.quest else obj.lineup.path

    def get_rank(self, obj):
        return obj.quest.rank if obj.quest else ""

    def get_pillar(self, obj):
        return obj.quest.pillar if obj.quest else ""

    def get_exp_reward(self, obj):
        return obj.quest.exp_reward if obj.quest else 0


class SwapAlternativeQuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quest
        fields = ["id", "title", "description", "rank", "pillar", "exp_reward", "path_target"]


class DailySummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyCompletionSummary
        fields = [
            "summary_date",
            "path",
            "quests_completed",
            "quests_total",
            "total_exp_earned",
            "bonus_exp_earned",
            "streak_status",
            "streak_maintained",
            "cross_path_bonus_earned",
        ]


class AdaptiveDifficultyDecisionSerializer(serializers.Serializer):
    decision = serializers.ChoiceField(choices=["accept", "decline"])
