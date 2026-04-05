from rest_framework import serializers

from .quiz_data import PATH_CODES


class SubmitAnswerSerializer(serializers.Serializer):
    quiz_id = serializers.IntegerField()
    question_number = serializers.IntegerField(min_value=1, max_value=9)
    answer = serializers.ChoiceField(choices=["A", "B", "C", "D", "E"])


class CompleteQuizSerializer(serializers.Serializer):
    quiz_id = serializers.IntegerField()


class SelectPathSerializer(serializers.Serializer):
    path_code = serializers.ChoiceField(choices=PATH_CODES)


class FitnessWarriorOnboardingSerializer(serializers.Serializer):
    training_split = serializers.ChoiceField(
        choices=["ppl", "full_body", "bro_split", "calisthenics", "cardio_focused", "custom"]
    )
    primary_goal = serializers.ChoiceField(
        choices=["muscle_gain", "fat_loss", "recomp", "general_performance"]
    )
    training_days_per_week = serializers.ChoiceField(choices=[3, 4, 5, 6, 7])
    experience_level = serializers.ChoiceField(
        choices=["beginner", "intermediate", "advanced"]
    )
    split_day_start = serializers.ChoiceField(
        choices=["push", "pull", "legs", "rest", "fresh_start"],
        required=False,
        allow_null=True,
    )


class MindsetSageOnboardingSerializer(serializers.Serializer):
    motivation = serializers.ChoiceField(
        choices=["mental_clarity", "stress_relief", "personal_growth", "discipline_building"]
    )
    daily_time_commitment = serializers.ChoiceField(
        choices=["15_minutes", "30_minutes", "1_hour", "as_much_as_needed"]
    )
    experience_level = serializers.ChoiceField(
        choices=["complete_beginner", "some_experience", "daily_practitioner"]
    )
    archetype = serializers.ChoiceField(
        choices=["stoic", "scholar", "monk", "warrior_sage"]
    )


class HealthAlchemistOnboardingSerializer(serializers.Serializer):
    primary_health_goal = serializers.ChoiceField(
        choices=[
            "optimize_energy",
            "reduce_stress_and_burnout",
            "improve_gut_health",
            "build_better_sleep",
            "full_body_transformation",
        ]
    )
    health_relationship = serializers.ChoiceField(
        choices=[
            "starting_from_scratch",
            "some_good_habits",
            "already_health_conscious",
            "biohack_and_optimize",
        ]
    )
    focus_area = serializers.ChoiceField(
        choices=["nutrition", "sleep", "mental_health", "hydration", "all_of_them"]
    )
    equipment_list = serializers.ListField(
        child=serializers.ChoiceField(
            choices=[
                "cold_shower",
                "cold_plunge",
                "sauna",
                "fitness_tracker",
                "supplements",
                "none_yet",
            ]
        ),
        allow_empty=True,
    )


class DisciplineKnightOnboardingSerializer(serializers.Serializer):
    routine_level = serializers.ChoiceField(
        choices=[
            "no_routine",
            "partial_routine",
            "routine_but_break_often",
            "solid_routine_level_up",
        ]
    )
    biggest_challenge = serializers.ChoiceField(
        choices=["wake_consistently", "staying_focused", "resisting_distractions", "managing_money", "all_of_them"]
    )
    structure_preference = serializers.ChoiceField(
        choices=["fully_structured", "semi_structured", "flexible"]
    )
    time_commitment = serializers.ChoiceField(
        choices=["30_minutes", "1_hour", "2_hours", "as_much_as_it_takes"]
    )


class DisciplineCodeSerializer(serializers.Serializer):
    rules = serializers.ListField(
        child=serializers.CharField(max_length=200),
        min_length=3,
        max_length=5,
    )


class GrindVisionaryOnboardingSerializer(serializers.Serializer):
    grind_focus = serializers.ChoiceField(
        choices=[
            "coding_and_tech",
            "design_and_creative",
            "writing_and_content",
            "business_and_entrepreneurship",
            "marketing_and_growth",
            "finance_and_investing",
            "other",
        ]
    )
    grind_focus_other = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=80,
    )
    experience_state = serializers.ChoiceField(
        choices=[
            "complete_beginner",
            "some_skills_go_deeper",
            "intermediate_ready_to_ship",
            "advanced_scaling",
        ]
    )
    singular_goal_text = serializers.CharField(max_length=255)
    goal_timeline = serializers.ChoiceField(choices=["3_months", "6_months", "1_year", "2_years"])
    daily_hours = serializers.ChoiceField(choices=["30_minutes", "1_hour", "2_hours", "3_plus_hours"])
    current_output_state = serializers.ChoiceField(
        choices=[
            "consume_more_than_create",
            "create_occasionally",
            "ship_regularly",
            "audience_or_income_already",
        ]
    )


class OnboardingCompleteSerializer(serializers.Serializer):
    path_code = serializers.ChoiceField(choices=PATH_CODES)


class FreedomDayRedeemSerializer(serializers.Serializer):
    date = serializers.DateField(required=False)


class WisdomLogSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    log_date = serializers.DateField(required=False)
    entry = serializers.CharField()
    is_public = serializers.BooleanField(required=False, default=False)
    created_at = serializers.DateTimeField(read_only=True)


class DarkNightSerializer(serializers.Serializer):
    date = serializers.DateField(required=False)
    entry = serializers.CharField()


class BodyJournalSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    log_date = serializers.DateField(required=False)
    weight_kg = serializers.DecimalField(max_digits=5, decimal_places=2, required=False, allow_null=True)
    sleep_hours = serializers.DecimalField(max_digits=4, decimal_places=2, required=False, allow_null=True)
    energy_level = serializers.IntegerField(required=False, allow_null=True, min_value=1, max_value=10)
    notes = serializers.CharField(required=False, allow_blank=True, default="")
    created_at = serializers.DateTimeField(read_only=True)


class OutputLogSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    log_date = serializers.DateField(required=False)
    deep_work_hours = serializers.DecimalField(max_digits=4, decimal_places=2, required=False, allow_null=True)
    tasks_shipped = serializers.IntegerField(required=False, min_value=0)
    revenue_usd = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, allow_null=True)
    notes = serializers.CharField(required=False, allow_blank=True, default="")
    is_public = serializers.BooleanField(required=False, default=False)
    created_at = serializers.DateTimeField(read_only=True)


class WarRoomEntrySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    week_start = serializers.DateField(required=False)
    phase = serializers.ChoiceField(choices=["morning", "evening"])
    objectives = serializers.ListField(child=serializers.CharField(max_length=180), required=False, allow_empty=True)
    reflection = serializers.CharField(required=False, allow_blank=True, default="")
    morning_exp_awarded = serializers.IntegerField(read_only=True)
    evening_exp_awarded = serializers.IntegerField(read_only=True)
    bonus_exp_awarded = serializers.IntegerField(read_only=True)
    same_day_bonus_awarded = serializers.BooleanField(read_only=True)
    weekly_report_input = serializers.DictField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)


class KnightWeeklyReportQuerySerializer(serializers.Serializer):
    week_start = serializers.DateField(required=False)
